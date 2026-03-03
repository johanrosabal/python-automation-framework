import json
from applications.api.loadiq.config.decorators import *
from conftest import load_iq_yaml_blueyonder_config
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from pathlib import Path

logger = setup_logger('LoadTenderXMLUploadEndpoint')

# Class to handle the request of a Load Tender via XML
@loadiq_devtmsexchange
class SubmitLoadEndpoint(BaseApi):

    # Receives base URL and authentication details
    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "/TMSExchangeAPI/TestProcessLoadFromFileUpload"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    # Method to send the XML file via POST request
    def process_load_from_file_upload(self, file_path: str, fromTMS: str, toTMS: str):
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            logger.error(f"XML file not found: {file_path}")
            raise FileNotFoundError(f"XML file not found: {file_path}")

        # Set up query parameters
        params = {
            "fromTMS": fromTMS,
            "toTMS": toTMS
        }

        logger.info(f"Preparing to upload XML file: {file_path.name}")
        logger.info(f"Parameters - fromTMS: {fromTMS}, toTMS: {toTMS}")

        # Open and read the XML file
        with open(file_path, 'rb') as xml_file:
            # Prepare the file for upload
            files = {
                'file': (file_path.name, xml_file, 'application/xml')
            }

            # Send POST request with file attachment using tokens from qa_config.yaml
            request = self.post_request() \
                .set_base_url(self.endpoints["tmsexchange"]) \
                .set_endpoint(self._endpoint) \
                .set_timeout(30) \
                .add_header("Authorization", self.client_id) \
                .add_header("CustomAuthorization", self.client_secret) \
                .set_params(params) \
                .set_files(files) \
                .send()

            logger.info(f"XML file uploaded successfully: {file_path.name}")
            logger.info(f"Response Status Code: {request.status_code}")

            return request


