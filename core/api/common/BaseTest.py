import pytest
from applications.api.salesforce.endpoints.oauth2_authorization import AuthorizationOauth2
from core.api.utils.ResponseUtils import ResponseUtils
from core.api.common.BaseApi import BaseApi
from core.api.report.APITestReport import APITestReport
from core.config.logger_config import setup_logger

logger = setup_logger('BaseTest')


class BaseTest:
    base_url = None
    base_token_url = None
    grant_type = None
    client_id = None
    client_secret = None
    username = None
    password = None
    report = APITestReport()

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self, config):
        # Base Url for Endpoints
        self.base_url = config.get('api', {}).get('base_url')
        logger.info("BASE URL: " + self.base_url)
        # Base Url for Authorization Token
        self.base_token_url = config.get('api', {}).get('base_token_url')
        logger.info("BASE TOKEN URL: " + self.base_token_url)
        # Attributes
        self.grant_type = config.get('api', {}).get('grant_type')
        self.client_id = config.get('api', {}).get('client_id')
        self.client_secret = config.get('api', {}).get('client_secret')
        # User Credentials
        self.username = config.get('user', {}).get('username')
        self.password = config.get('user', {}).get('password')

        # Getting Authorization Token
        BaseApi.set_base_url(self.base_url)
        # response = (
        #     AuthorizationOauth2
        #     .set_base_url(self.base_token_url)
        #     .set_client_id(self.client_id)
        #     .set_grant_type(self.grant_type)
        #     .set_client_secret(self.client_secret)
        #     .set_username(self.username)
        #     .set_password(self.password)
        #     .send()
        #     .get_info()
        # )

        yield

    @classmethod
    def validations(cls, response):
        return ResponseUtils(response)

    @classmethod
    def add_report(cls, test_name, url, method, response, error_message=None):
        response_time = response.elapsed.total_seconds() * 1000  # Convert to milliseconds
        cls.report.add_result(
            test_name=test_name,
            url=url,
            method=method,
            status_code=response.status_code,
            response_time=response_time,
            response_body=response.json(),
            error_message=error_message
        )

    @classmethod
    def teardown_class(cls):
        # Create Report on Console
        print("teardown_class")
        cls.report.generate_report()
