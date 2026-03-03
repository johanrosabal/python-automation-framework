from applications.api.loadiq.endpoints.IntegrationTMS.submit_blueyonder_load_file_endpoint import SubmitLoadEndpoint
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseBlueYonder
from core.utils.decorator import test
from applications.api.loadiq.config.decorators import loadiq_devtmsexchange
from core.config.logger_config import setup_logger
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint
import os
from pathlib import Path

logger = setup_logger('TestSubmitBlueYonderLoad')


@loadiq_devtmsexchange
class TestSubmitBlueYonderLoad(LoadIQBaseBlueYonder):

    submit_load_tender_endpoint = SubmitLoadEndpoint.get_instance()
    submit_load_endpoint = SubmitLoadEndpoint.get_instance()

    @test(test_case_id="CT-2703", test_description="Verify BlueYonder integration")
    def test_submit_load_tender(self, load_iq_yaml_blueyonder_config):
        xml_path = "applications/api/loadiq/data/loadtender/LoadTendered_test.LoadTendered.xml"
        
        logger.info(f"Submitting load tender from: {xml_path}")

        # Send the XML file via Post request
        response = self.submit_load_tender_endpoint.process_load_from_file_upload(xml_path)
        
        logger.info(f"HTTP Status Code: {response.status_code}")
        assert response.status_code == 200, f"Error HTTP: {response.status_code} - {response.text}"
        
        json_data = response.json()
        logger.info(f"Full response: {json_data}")
        
        logger.info(f"Success: {json_data.get('success')}")
        logger.info(f"Message: {json_data.get('message')}")
        
        data = json_data.get("data", {})
        logger.info(f"Load Number: {data.get('loadNumber')}")
        
        assert json_data["success"] is True, "Unsuccessful response"
        assert "loadNumber" in data, "LoadNumber is not present"
        assert data["success"] is True, "Field 'data.success' is not True"