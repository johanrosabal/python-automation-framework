from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from pathlib import Path
from typing import Union
import xml.etree.ElementTree as ET
from core.utils.helpers import print_json

logger = setup_logger('LoadTenderXMLUploadEndpoint')


# Class to handle the request of a Load Tender via XML
class SubmitLoadEndpoint(BaseApi):

    # Receives base URL and authentication details
    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._url = "https://logibapi-tmsexchange-dev.solutions.logxplus.com"
        self._endpoint = "TMSExchangeAPI/TestProcessLoadFromFileUpload"
        self._authorization = "Bearer U2FsdGVkX18cla6Udi4vWC3O6PXEB57uhiihm+y7MlOm0vRMuADpcDt2ohbvz72zYOSz1OCWqyZkOfoThghxUjFFKVfB3Oq+zXDjqq82HnbOXLe2ttKpslPlz9qHliDPxg8jGiEztl5WjQiXb7vX7yb4VIyJFkWleCHH3T7r9WkULuLUJcLiHR40Uj8SYG9LpudjiMHLCXueQCgSQH1epYb2TSHaRB57iQsQnxuM558ZCQJW9pn4MjIyxh2eiLG1FJftMttGwqXNejrPvqrZ3zkmu3xvQx1nb/ME49bdwzOCqZddWdlWLUTY+RnxM5Z4GqP44PubQkDfZa0YIJGxHlyHUnwxmrrPxiTrvSiQf8Ysj3tQT2+Yw3efbnPZx/3tgD3s32CbsxUpOPxjkmEB98N3zWQP9wzO8MxRE8nPliqG3hyXjgSrJY8/VvjUxfBpkMz1dQ7Bs96JpJp+AcpKryaXMLIVDC/4sfEMiyGqCA1UUHahZV5jB6hGulagvSLBOi/NU4RSQvVv2mCkoHcp1G6pdjGska6ChvmMJ8/pyZShR2cyo+4bsXjIveoDiOejikXZ6lmtptMSkZDrL5ZkuqA+tMWkGWfRLAlWMXIT/ivT8NMoMiE3K04sT08PhWU6a7efUNOCs63BrY+BsRIXR+MQR35Dg6j8Knnc9SrU2OKplNpx0kxM81Uwcr2Y2c3HQKLgt1fHq1N1obYOa3Icn/KqruwibKPFQlOyRG4IJvmWv8gf6T1kCn1B7qpuu/Er5xkMSc8BofI7sJvwF0ZLq6VQFcT+bP6m3jTkzubu1WWml167Ew2nhA6fosR/is5C/Tb7SwqNoV07cHj1GBIMjCilkaVs83YoTXaXDpSofZwLnBXEro7zWrGrO1yNCWdgb9rtmEg66fjfPxgzXMQN8xh3FwRymSBkCFQW7J5PIokx0Is51PtZXSBi/09UjAak7mDeyfh4wGZeZrHiUzvRnvPRqdl1acRn1Y21V+tRlUEEWTaAavKyDCrgby+lTlnwxko/CImEzBU3oqeAMEdQNHwGhRiwEyItb6O338wDlSZ/OrpNqZiXzj3wKb0LG066l6ceCb1x8lIf8yqFvd5pMLhzDXOvznvLhbFW6sbBXFHguf6f2Z9Go09rd3AaoOIQdqUSDIU2oOU5Xs6wwPyisRJJW6uO+Oaw85NeICMLFwI0zwA4+C8E84lZ80nF/Pqe"
        self._custom_autorization = "U2FsdGVkX18wnJtNR0B+1WQtieiZZLIaCULEk2gWGvaDoj9k0xHCxBP70rCraY5kC3bLsSrngw7QUc3KkoTvOAwlSQPUCjR/a7e8kbYZx80bWckPzSzThE+HerMXDzQGQRyls7qwTcRA5KEk6Z2BNaxFns//Qz07hkgk7NTsWNzReWURod489JmqVAlE9eIJ7VfqMeMPe2uT8vmau5h4DV9scQDBpiSxX8uQOeZvYDSakUjuvZ7XAQS3AUQwEKriqFMrahary4q1pwEuz+n3rLFz6qtmqSoaxUeT42W/8+5fw+rMRoU1m5Zq+d1BSTqC1MpQrKpLNVFmWyfKXzY8gw5eFZ1b4QgVzEsCWTqNTkpkk/M3tmElmK/asbPEdhOYFImjxw4E5Ejh8SzoqKIV6PI/bHoOtwclC0ipWoHRW/q21Rxjx8vzfCYQk5P/XdsbhzthPXRe8yhXzhL26n+BukzludUCLIwcBIhN+iN3d5fI2rHGLko5nGzOtvhMfw9Sx2K/uX60zGrF9x8WLBFkolqcBWdo7coNsP0cn6XmLm/1erqKg4d6mfLNtz3MEjzOnMU6+bCgvu6XGzMTKM6mTMQJCeqwpXnsn6obYgVA4LMuZv2pyPiVxdzqvb2e/PnyU14ACqcECvjexbG6jaQfuDM84PonDx2kkb5/WwN6kSpv4tMKlxMOJJGm52lggU61GNXcX97hcnM4nub+1KJjd/puDU/WcZnq6hJH7P86E0rA6p0KX+7gpFjOcYaGnjy1GtxZi7mu/hbaU+sPHs3lR/r37373a0HMWz05Mp4gOZWIEKZPJJSQT4rJUFjesi4kJagddOUDBMg+4tAMalf/LsvkXubcx73wp5Vq6NyeCqo6V1ACt1X+rz24Zp2zjjeq9ZYTiprB6dEM07WcjnqTaMihFOLeNMSwvM0RvSsCFd3O3Z6oPxnoaW95ztktbVxHivcsL2gCKJ0+oYteQCxxFzABdWjuH9dFOQddKAsiGRNXCeEW4f89BeyEzWeLEzuwfHyT4sCEeGwgYwOHjwAgS9KFwFSVF0p5GRnn9SNQfbqnkdWGG7T5x4t98zjmS2h1wrBOAc0/SJQ517QZTXZFdtrDZdvbbDqdNPYsivOU3hkbSMktyS1JwUUWjkVJZApzDVyZLd5BB0XAHvulRCU1HvaEbs0HTzr16M/VOkNNbkoQEMlb0WV1K4hM0fII9OV73HsxaFQ8+p/nd33iRfVMKCOvH3zavTzbWOI2fCN/BD+1dVzFHGIR3taSPW5xtGGE+pamvvOmcZohwsnrI908LcEjEllWEn5QEvuYzRPbn3LZlcKzmhok/THzSA3sz6v4STy0Trk34fAdIh/oDg9cXvgE5/JpJBGwnLgr1nNTGQO1Zmg0ZKZkNhYJaUz6RQfnJbFXy6fOuD9CeKEJaS+hkQgW9du5uP1uWFQ/FVKm6QDur+uNpZv+pyg4wyruo1BeBSZWqbx3OPmPDzVW2BihuFjRxmS3aTnu7S0V3O27zGdMHn0KJ+gvB6z6m7J3MMWvw/kHYlxIztgGNuvsxK9w1P2mCGvz25JhGW54ZnyCynx+NCGc6F39JYlN0PBrWRtLkyAa3fFvRW1JWIuToOqILyLDTtgvWvtsqECQS8b3rep848WrE0SdQqL2QDswcqEXbDTcKB38F4DCzvt6wZX0Xrmvzq1gtzOheb/OmIseAMaQTnaajm9gPKl1aoWcwySWA5ubzE6C50k6k9c/w5vzShLTzwYRI9Nr1w9hXDz2tg6DROkTOlI7+Vu9FqBMi/ZOAZ3f0GG6sYY0vURy4yhAaWCuyLCsddRU/zO8BY0C6Btq0qYXDtVOY6S43GggQCoYKy2cHcxd5TvwhUiCtwgTj25KCfB0WqbZ+OT3wWAcqwo+WzsS52kEK/x2GJIns3z+pvzZ+u3bvlWRTJ+DHCSnmw=="

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    # Method to send the XML file via POST request
    def process_load_from_file_upload(self, file_path: str):
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            logger.error(f"XML file not found: {file_path}")
            raise FileNotFoundError(f"XML file not found: {file_path}")

        # Increment reference IDs before processing
        new_system_load_id = self.auto_increment_system_load_id(file_path)
        logger.info(f"SystemLoadID incremented to: {new_system_load_id}")

        new_bol_number = self.auto_increment_bol_number(file_path)
        if new_bol_number:
            logger.info(f"BOL Number incremented to: {new_bol_number}")

        new_po_number = self.auto_increment_po_number(file_path)
        if new_po_number:
            logger.info(f"PO Number incremented to: {new_po_number}")

        # Set up query parameters
        params = {
            "fromTMS": "blue_yonder",
            "toTMS": "loadiq"
        }

        logger.info(f"Preparing to upload XML file: {file_path.name}")

        # Open and read the XML file
        with open(file_path, 'rb') as xml_file:
            # Prepare the file for upload
            files = {
                'file': (file_path.name, xml_file, 'application/xml')
            }

            # Read XML Content
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
                logger.info(f"Read XML File Content:\n{xml_content}\n")

            # Send POST request with file attachment using tokens from qa_config.yaml
            request = self.post_request() \
                .set_base_url(self._url) \
                .set_endpoint(self._endpoint) \
                .set_timeout(30) \
                .add_header("Authorization", self._authorization) \
                .add_header("CustomAuthorization", self._custom_autorization) \
                .set_params(params) \
                .set_files(files) \
                .send()

            logger.info(f"XML file uploaded successfully: {file_path.name}")
            logger.info(f"Response Status Code: {request.status_code}")
            print_json("Request Body", request.text)

            return request

    def auto_increment_system_load_id(self, file_path: Union[str, Path]) -> int:
        """
        Increment the <SystemLoadID> value in the given XML file.
        Returns the new SystemLoadID value.

        Args:
            file_path: Path to the XML file (can be str or Path object)

        Returns:
            int: The new incremented SystemLoadID value
        """
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            logger.error(f"XML file not found: {file_path}")
            raise FileNotFoundError(f"XML file not found: {file_path}")

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find the <SystemLoadID> element
        system_load_id_element = root.find("SystemLoadID")
        if system_load_id_element is not None:
            # Increment the value of <SystemLoadID>
            current_id = int(system_load_id_element.text)
            new_id = current_id + 1
            system_load_id_element.text = str(new_id)

            # Save the updated XML file with proper formatting
            ET.indent(tree, space='  ')  # Add indentation to preserve formatting
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            logger.info(f"<SystemLoadID> incremented from {current_id} to {new_id}")
            return new_id
        else:
            logger.error("<SystemLoadID> element not found in the XML file.")
            raise ValueError("<SystemLoadID> element not found in the XML file.")

    def auto_increment_bol_number(self, file_path: Union[str, Path]) -> Union[int, None]:
        """
        Increment the <LoadReferenceNumber> value where LoadReferenceNumberType is "BOL".
        Only increments if the value is numeric.

        Args:
            file_path: Path to the XML file (can be str or Path object)

        Returns:
            int: The new incremented BOL number, or None if not found or not numeric
        """
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            logger.error(f"XML file not found: {file_path}")
            raise FileNotFoundError(f"XML file not found: {file_path}")

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # XPath to find LoadReferenceNumberList where type is BOL
        xpath = './/LoadReferenceNumberList[LoadReferenceNumberType="BOL"]/LoadReferenceNumber'
        bol_element = root.find(xpath)

        if bol_element is not None and bol_element.text:
            bol_value = bol_element.text.strip()
            # Only increment if the value is numeric
            if bol_value.isdigit():
                current_value = int(bol_value)
                new_value = current_value + 1
                bol_element.text = str(new_value)

                # Save the updated XML file with proper formatting
                ET.indent(tree, space='  ')
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                logger.info(f"<LoadReferenceNumber> (BOL) incremented from {current_value} to {new_value}")
                return new_value
            else:
                logger.warning(f"BOL number '{bol_value}' is not numeric, skipping increment.")
                return None
        else:
            logger.info("BOL LoadReferenceNumber element not found in the XML file.")
            return None

    def auto_increment_po_number(self, file_path: Union[str, Path]) -> Union[int, None]:
        """
        Increment the <ShipmentReferenceNumber> value where ShipmentReferenceNumberType is "PO".
        Only increments if the value is numeric.

        Args:
            file_path: Path to the XML file (can be str or Path object)

        Returns:
            int: The new incremented PO number, or None if not found or not numeric
        """
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            logger.error(f"XML file not found: {file_path}")
            raise FileNotFoundError(f"XML file not found: {file_path}")

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # XPath to find ShipmentReferenceNumberList where type is PO
        xpath = './/ShipmentReferenceNumberList[ShipmentReferenceNumberType="PO"]/ShipmentReferenceNumber'
        po_element = root.find(xpath)

        if po_element is not None and po_element.text:
            po_value = po_element.text.strip()
            # Only increment if the value is numeric
            if po_value.isdigit():
                current_value = int(po_value)
                new_value = current_value + 1
                po_element.text = str(new_value)

                # Save the updated XML file with proper formatting
                ET.indent(tree, space='  ')
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                logger.info(f"<ShipmentReferenceNumber> (PO) incremented from {current_value} to {new_value}")
                return new_value
            else:
                logger.warning(f"PO number '{po_value}' is not numeric, skipping increment.")
                return None
        else:
            logger.info("PO ShipmentReferenceNumber element not found in the XML file.")
            return None