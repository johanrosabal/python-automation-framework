# core/utils/xml_utils.py

import xml.etree.ElementTree as ET
import re
from typing import Optional, Union, List
from core.config.logger_config import setup_logger

logger = setup_logger('XMLUtils')


class XMLUtils:
    """
    Utility class for XML extraction and parsing using Fluent Interface pattern.

    Usage:
        xml = XMLUtils() \\
            .load_from_multipart_body(body) \\
            .assert_root('CISDocument') \\
            .log_value('.//SystemLoadID')

        load_id = xml.get_value('.//SystemLoadID')
    """

    def __init__(self):
        """Initialize XMLUtils instance."""
        self._root: Optional[ET.Element] = None
        self._raw_body: Optional[str] = None
        self._extraction_success: bool = False

    # ====================================================================
    # LOAD METHODS - Entry points
    # ====================================================================

    def load_from_multipart_body(self, body: Union[str, bytes]) -> 'XMLUtils':
        """
        Extracts and parses XML from multipart/form-data request body.

        Args:
            body: Request body (str or bytes)

        Returns:
            self: For method chaining
        """
        self._raw_body = body.decode('utf-8', errors='ignore') if isinstance(body, bytes) else body

        if not self._raw_body:
            logger.error("Request body is empty")
            return self

        # Find XML start position
        start_pos = -1
        for marker in ['<?xml', '<CISDocument', '<LoadTender', '<']:
            start_pos = self._raw_body.find(marker)
            if start_pos != -1:
                break

        if start_pos == -1:
            logger.error("XML content not found in request body")
            return self

        # Extract XML content
        xml_content = self._raw_body[start_pos:]

        # Clean: remove everything after last closing tag
        last_close = xml_content.rfind('</')
        if last_close != -1:
            end_pos = xml_content.find('>', last_close)
            if end_pos != -1:
                xml_content = xml_content[:end_pos + 1]

        # Parse XML
        try:
            self._root = ET.fromstring(xml_content.strip())
            self._extraction_success = True
            logger.info(f"✓ XML extracted successfully. Root: {self._root.tag}")
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            self._extraction_success = False

        return self

    def load_from_file(self, file_path: str) -> 'XMLUtils':
        """
        Loads and parses XML from a file.

        Args:
            file_path: Path to XML file

        Returns:
            self: For method chaining
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            self._root = ET.fromstring(xml_content.strip())
            self._extraction_success = True
            logger.info(f"✓ XML loaded from file. Root: {self._root.tag}")
        except Exception as e:
            logger.error(f"Error loading XML from file: {e}")
            self._extraction_success = False

        return self

    def load_from_string(self, xml_string: str) -> 'XMLUtils':
        """
        Parses XML from a string.

        Args:
            xml_string: XML content as string

        Returns:
            self: For method chaining
        """
        try:
            self._root = ET.fromstring(xml_string.strip())
            self._extraction_success = True
            logger.info(f"✓ XML parsed from string. Root: {self._root.tag}")
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            self._extraction_success = False

        return self

    # ====================================================================
    # VALIDATION METHODS
    # ====================================================================

    def assert_root(self, expected_tag: str, message: str = None) -> 'XMLUtils':
        """
        Asserts that the root element tag matches expected value.

        Args:
            expected_tag: Expected root tag name
            message: Custom error message

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If root tag doesn't match
        """
        if not self._extraction_success or self._root is None:
            raise AssertionError(message or f"XML extraction failed. Expected root: {expected_tag}")

        actual_tag = self._root.tag.split('}')[-1]  # Remove namespace if present
        if actual_tag != expected_tag:
            raise AssertionError(message or f"Root tag mismatch. Expected: {expected_tag}, Got: {actual_tag}")

        logger.info(f"✓ Root tag validated: {expected_tag}")
        return self

    def assert_value(self, xpath: str, expected: str, message: str = None) -> 'XMLUtils':
        """
        Asserts that an XML element value matches expected value.

        Args:
            xpath: XPath expression
            expected: Expected text value
            message: Custom error message

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If value doesn't match
        """
        actual = self.get_value(xpath)
        if actual != expected:
            raise AssertionError(message or f"Value mismatch at {xpath}. Expected: {expected}, Got: {actual}")

        logger.info(f"✓ Value validated at {xpath}: {expected}")
        return self

    def assert_exists(self, xpath: str, message: str = None) -> 'XMLUtils':
        """
        Asserts that an XML element exists.

        Args:
            xpath: XPath expression
            message: Custom error message

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If element doesn't exist
        """
        element = self._root.find(xpath) if self._root is not None else None
        if element is None:
            raise AssertionError(message or f"Element not found: {xpath}")

        logger.info(f"✓ Element exists: {xpath}")
        return self

    # ====================================================================
    # GETTER METHODS
    # ====================================================================

    def get_value(self, xpath: str, default: str = '') -> str:
        """
        Gets text value from XML element.

        Args:
            xpath: XPath expression
            default: Default value if not found

        Returns:
            str: Element text or default value
        """
        if self._root is None:
            return default

        element = self._root.find(xpath)
        return element.text if element is not None and element.text else default

    def get_values(self, xpath: str) -> List[str]:
        """
        Gets all matching element texts from XML.

        Args:
            xpath: XPath expression

        Returns:
            list: List of element texts
        """
        if self._root is None:
            return []

        elements = self._root.findall(xpath)
        return [elem.text for elem in elements if elem.text]

    def get_attribute(self, xpath: str, attribute: str, default: str = '') -> str:
        """
        Gets attribute value from XML element.

        Args:
            xpath: XPath expression
            attribute: Attribute name
            default: Default value if not found

        Returns:
            str: Attribute value or default
        """
        if self._root is None:
            return default

        element = self._root.find(xpath)
        return element.get(attribute, default) if element is not None else default

    def get_root(self) -> Optional[ET.Element]:
        """Gets the parsed XML root element."""
        return self._root

    def is_valid(self) -> bool:
        """Checks if XML was successfully parsed."""
        return self._extraction_success and self._root is not None

    # ====================================================================
    # LOGGING & DEBUG METHODS
    # ====================================================================

    def log_value(self, xpath: str, label: str = None) -> 'XMLUtils':
        """
        Logs an XML element value.

        Args:
            xpath: XPath expression
            label: Custom label for logging

        Returns:
            self: For method chaining
        """
        value = self.get_value(xpath)
        label = label or xpath
        logger.info(f"{label}: {value}")
        return self

    def log_structure(self, max_depth: int = 3) -> 'XMLUtils':
        """
        Logs XML structure for debugging.

        Args:
            max_depth: Maximum depth to log

        Returns:
            self: For method chaining
        """
        if self._root is None:
            logger.warning("No XML loaded to log structure")
            return self

        def print_tree(element, depth=0):
            if depth > max_depth:
                return
            indent = "  " * depth
            tag = element.tag.split('}')[-1]
            text = (element.text or '').strip()[:50]
            attrs = ' '.join(f"{k}='{v}'" for k, v in element.attrib.items())
            logger.info(f"{indent}<{tag}{' ' + attrs if attrs else ''}>{text}")
            for child in element:
                print_tree(child, depth + 1)

        logger.info("=== XML Structure ===")
        print_tree(self._root)
        logger.info("=== End XML Structure ===")
        return self

    def reset(self) -> 'XMLUtils':
        """
        Resets the instance for reuse.

        Returns:
            self: For method chaining
        """
        self._root = None
        self._raw_body = None
        self._extraction_success = False
        return self


# from core.utils.xml_utils import XMLUtils
#
#
# @test(test_case_id="CT-2301", test_description="Verify milestone details", feature="Status Update", skip=False)
# def test_verify_milestone_details_display_in_tracking_section1(self, load_iq_login_carrier_portal,
#                                                                load_iq_upload_blueyonder_load, record_property):
#     record_property("test_key", "CT-2301")
#
#     xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml"
#
#     # 1. Create the load via API
#     result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
#
#     # 2. Extract and validate XML with fluent interface (VERY CLEAN ✅)
#     xml = XMLUtils() \
#         .load_from_multipart_body(result.request.body) \
#         .assert_root('CISDocument') \
#         .log_value('.//EventName', 'Event Name') \
#         .log_value('.//SystemLoadID', 'Load ID') \
#         .log_value('.//CarrierName', 'Carrier Name')
#
#     # 3. Assert extraction was successful
#     assert xml.is_valid(), "XML extraction failed"
#
#     # 4. Get values for further validations
#     load_id = xml.get_value('.//SystemLoadID')
#     carrier_name = xml.get_value('.//CarrierName')
#     event_name = xml.get_value('.//EventName')
#
#     # 5. Your test assertions
#     assert load_id == "10000048625", f"Load ID mismatch: {load_id}"
#     assert carrier_name == "REMOLQUES DE PUERTO RICO INC", f"Carrier name mismatch: {carrier_name}"
#     assert event_name == "LoadTenderAccepted", f"Event name mismatch: {event_name}"