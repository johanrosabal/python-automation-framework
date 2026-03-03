import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.loadboard.test_session_endpoint import TestSessionEndpoint

logger = setup_logger('TestSession')


@loadiq_loadboard
class TestSession(LoadIQBaseTest):

    session = TestSessionEndpoint.get_instance()

    @test(test_case_id="LOAD-0001", test_description="Test Session")
    def test_session(self):

        # Getting Endpoint Response
        response = self.session.get_response()

        # Validate Standard Response
        self.add_report(test_data=self.test_session, status_code=200, response=response)

        logger.info(f"JWT Token: {BaseApi.get_jwt_access_token()}")
        logger.info(f"Custom Token: {BaseApi.get_jwt_access_token()}")

