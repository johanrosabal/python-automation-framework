import pytest

from core.api.common.BaseTest import BaseTest
from core.config.logger_config import setup_logger
from applications.api.salesforce.endpoints.quoting_request import QuotingRequest
from core.data.sources.JSON_reader import JSONReader
from core.utils.decorator import test
logger = setup_logger('TestQuotation')


class TestQuotation(BaseTest):

    @test(test_case_id="API-0001", test_description="01. Port to Port Container")
    @pytest.mark.usefixtures("initialize_api_config")
    def test_api_01_port_to_port_container(self, initialize_api_config):

        # 01. Data: Body Request
        data = JSONReader().set_file_path("../data/quotation/Api_01_PortToPortContainer.json").read_file()
        # 02. Setting Authorization and Instance Endpoint
        client_id = initialize_api_config["client_id"]
        client_secret = initialize_api_config["client_secret"]
        quotation = QuotingRequest().get_instance(client_id, client_secret)
        # 03. Sending POST Request
        response = quotation.send_quotation_request(json=data).get_response()
        # 04. Validate Standard Response
        self.add_report(test_data=self.test_api_01_port_to_port_container, status_code=201, response=response)
