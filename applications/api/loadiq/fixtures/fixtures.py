import pytest

from core.config.logger_config import setup_logger
from applications.api.loadiq.endpoints.IntegrationTMS.submit_blueyonder_load_file_endpoint import SubmitLoadEndpoint

from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers

logger = setup_logger('Running Fixture')

@pytest.fixture(scope="function")
def load_iq_upload_blueyonder_load():
    def _upload(file_path: str, fromTMS: str, toTMS: str):
        return SubmitLoadEndpoint.get_instance().process_load_from_file_upload(
            file_path, fromTMS, toTMS
        )
    return _upload
