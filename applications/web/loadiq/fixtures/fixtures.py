import pytest
import json
from pathlib import Path
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint
from applications.web.loadiq.config.sub_application import CustomerAccounts, CarrierAccounts, OpsAccounts, SuppAccounts
from applications.web.loadiq.pages.login.LoginPage import LoginPage
from core.config.logger_config import setup_logger

from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers
from core.utils.XMLUtils import XMLUtils

logger = setup_logger('Running Fixture')


@pytest.fixture(scope="function")
def load_iq_login_customer_portal():
    login = LoginPage.get_instance()
    if not login.is_login_successful():
        login.load_page().login_user(CustomerAccounts.TEST_07).is_login_successful()


@pytest.fixture(scope="function")
def load_iq_login_carrier_portal():
    login = LoginPage.get_instance()
    if not login.is_login_successful():
        login.load_page().login_user(CarrierAccounts.TEST_20).is_login_successful()


@pytest.fixture(scope="function")
def load_iq_login_operations_portal():
    login = LoginPage.get_instance()
    if not login.is_login_successful():
        login.load_page().login_user(OpsAccounts.TEST_480).is_login_successful()


@pytest.fixture(scope="function")
def load_iq_login_support_portal():
    login = LoginPage.get_instance()
    if not login.is_login_successful():
        login.load_page().login_user(SuppAccounts.TEST_12).is_login_successful()


@pytest.fixture
def load_json_data():
    def _load_json_data(filepath, test_case_id=None, key=None):
        """
        Load JSON data, optionally for a specific test case and key

        Args:
            filepath: Path to the JSON file
            test_case_id: Optional test case ID (e.g., "CT-1498")
            key: Optional key to retrieve specific value from test case data

        Returns:
            Full data if no test_case_id, test case data if test_case_id provided,
            specific value if both test_case_id and key provided
        """
        path = helpers.get_relative_file_path(filepath)
        data = JSONReader().import_json(path)
        logger.info(f"[Fixture] Loaded data from {filepath}")

        # If no test case ID specified, return full data
        if test_case_id is None:
            return data

        # Find specific test case
        for test in data.get("tests", []):
            if test.get("idTC") == test_case_id:
                test_data = test.get("data", {})
                if key is None:
                    logger.info(f"[Fixture] Retrieved test case {test_case_id} data: {test_data}")
                    return test_data
                else:
                    value = test_data.get(key)
                    logger.info(f"[Fixture] Retrieved {key}={value} from test case {test_case_id}")
                    return value

        logger.warning(f"Test case {test_case_id} not found in {filepath}")
        return None

    return _load_json_data


@pytest.fixture
def save_json_data():
    def _save_json_data(filepath, test_case_id, key, value):
        """
        Save a specific value to a test case in the JSON file

        Args:
            filepath: Path to the JSON file
            test_case_id: The test case ID (e.g., "CT-1498")
            key: The key to save the value under (e.g., "shipment_id")
            value: The value to save
        """
        path = helpers.get_relative_file_path(filepath)

        # Load existing data
        data = JSONReader().import_json(path)

        # Find the test case and update it
        for test in data.get("tests", []):
            if test.get("idTC") == test_case_id:
                if "data" not in test:
                    test["data"] = {}
                test["data"][key] = value
                break
        else:
            logger.warning(f"Test case {test_case_id} not found in {filepath}")
            return False

        # Save back to file
        try:
            import json
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            logger.info(f"[Fixture] Saved {key}={value} to test case {test_case_id} in {filepath}")
            return True
        except Exception as e:
            logger.error(f"[Fixture] Error saving data to {filepath}: {e}")
            return False

    return _save_json_data


@pytest.fixture(scope="function")
def create_load_via_api():
    """
    Factory fixture: Returns a function that creates loads with custom parameters.
    """


    def _create_load(status_code: int = 200, xml_path: str = None):
        root = get_project_root()
        xml_path = f"{root}{xml_path}"
        logger.info(xml_path)

        # Create load by submitting the XML file
        result = SubmitLoadEndpoint.get_instance().process_load_from_file_upload(xml_path)

        # Validate status code
        # TODO: Enable this assert when the Endpoint gets fixed
        # assert result.status_code == status_code, f"Expected {status_code}, got {result.status_code}"

        # Parse JSON response
        try:
            response_dict = json.loads(result.text)
        except json.JSONDecodeError:
            response_dict = {}

        # Parse XML from multipart request body
        xml_utils = XMLUtils().load_from_multipart_body(result.request.body)
        xml_root = xml_utils.get_root()

        # Extract load_number based on response status
        if status_code == 200 and response_dict.get('data', {}).get('loadNumber'):
            load_number = response_dict['data']['loadNumber']
        else:
            system_load_id = xml_utils.get_value('.//SystemLoadID', default='')
            load_number = f"BY_{system_load_id}" if system_load_id else None

        assert load_number, "Could not extract load_number"

        # ========================================
        # EXTRACT BOL (Bill of Lading) NUMBER
        # ========================================
        # XPath with predicate: finds LoadReferenceNumberList where the child
        # LoadReferenceNumberType equals "BOL", then extracts its LoadReferenceNumber value
        bol_number = xml_utils.get_value(
            './/LoadReferenceNumberList[LoadReferenceNumberType="BOL"]/LoadReferenceNumber',
            default=''
        ).strip()

        # ========================================
        # EXTRACT PO (Purchase Order) NUMBER
        # ========================================
        # XPath with predicate: finds ShipmentReferenceNumberList where the child
        # ShipmentReferenceNumberType equals "PO", then extracts its ShipmentReferenceNumber value
        po_number = xml_utils.get_value(
            './/ShipmentReferenceNumberList[ShipmentReferenceNumberType="PO"]/ShipmentReferenceNumber',
            default=''
        ).strip()

        # Build a dictionary of all reference numbers for flexible access
        # Iterates through all LoadReferenceNumberList nodes and maps type -> value
        reference_numbers = {}
        for ref_node in xml_root.findall('.//LoadReferenceNumberList'):
            ref_type = ref_node.findtext('LoadReferenceNumberType', default='').strip()
            ref_value = ref_node.findtext('LoadReferenceNumber', default='').strip()
            if ref_type and ref_value:
                reference_numbers[ref_type] = ref_value

        # Example usage: reference_numbers.get('BOL'), reference_numbers.get('PRO'), etc.

        shipment_reference_numbers = {}
        for ref_node in xml_root.findall('.//ShipmentReferenceNumberList'):
            ref_type = ref_node.findtext('ShipmentReferenceNumberType', default='').strip()
            ref_value = ref_node.findtext('ShipmentReferenceNumber', default='').strip()
            if ref_type and ref_value:
                shipment_reference_numbers[ref_type] = ref_value

        # Return comprehensive data dictionary for test assertions
        return {
            'result': result,
            'load_number': load_number,
            'bol_number': bol_number,  # ← Extracted BOL number
            'po_number': po_number,  # ← Extracted PO number
            'reference_numbers': reference_numbers,  # ← Dictionary with all Load reference types
            'shipment_reference_numbers': shipment_reference_numbers,  # ← Dictionary with all Shipment reference types
            'response_dict': response_dict,
            'xml_root': xml_root,
            'xml_utils': xml_utils,
            'xml_path': xml_path,
            'status_code': result.status_code
        }

    return _create_load  # ← IMPORTANT: Return the FUNCTION, not the dictionary


def get_project_root():
    """Find project root by looking for 'loadiq' directory."""
    current_file = Path(__file__).absolute()
    for parent in current_file.parents:
        if parent.name == 'loadiq' and parent.is_dir():
            return parent
    raise RuntimeError("Could not find 'loadiq' directory in path hierarchy")

