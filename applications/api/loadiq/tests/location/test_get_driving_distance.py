import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.location.get_driving_distance_endpoint import GetDrivingDistanceEndpoint

logger = setup_logger('TestDrivingDistance')


@loadiq_location
class TestDrivingDistance(LoadIQBaseTest):

    get_driving_distance = GetDrivingDistanceEndpoint.get_instance()

    @test(test_case_id="LOAD-0001", test_description="Test Search Location Name")
    def test_search_location_name(self):

        # Getting Endpoint Response
        response = self.get_driving_distance.get_response(
            from_longitude=-80.13042329999999,
            from_latitude=25.7904657,
            to_longitude=-77.485395,
            to_latitude=38.991487
        )

        # Validate Standard Response
        self.add_report(test_data=self.test_search_location_name, status_code=200, response=response)
