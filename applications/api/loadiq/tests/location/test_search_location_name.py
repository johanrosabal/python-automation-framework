import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.location.search_location_name_endpoint import SearchLocationNameEndpoint

logger = setup_logger('TestSearchLocationName')


@loadiq_location
class TestSearchLocationName(LoadIQBaseTest):

    search_location_name = SearchLocationNameEndpoint.get_instance()

    @test(test_case_id="LOAD-0001", test_description="Test Search Location Name")
    def test_search_location_name(self):

        # Getting Endpoint Response
        response = self.search_location_name.get_response('Miami')

        # Validate Standard Response
        self.add_report(test_data=self.test_search_location_name, status_code=200, response=response)