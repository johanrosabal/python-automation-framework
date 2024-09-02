import json

import pytest
from tabulate import tabulate
from core.utils.helpers import print_json_response
from core.utils.table_formatter import TableFormatter
from applications.api.salesforce.endpoints.oauth2_authorization import AuthorizationOauth2
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
    def add_report(cls, test_data, status_code, response, errors=None):
        table = []
        errors_list = []

        if response.status_code != status_code:
            errors_list.append(f"Status Code should be {status_code}, actual values is {response.status_code}")

        if errors:
            errors_list.extend(errors)

        result = {
            "Test Case ID": test_data.test_case_id,
            "Test Name": test_data.test_description,
            "Status": "PASS" if response.status_code == status_code and not errors_list else "FAIL",
            "URL": response.url,
            "Method": response.request.method,
            "Status Code": response.status_code,
            "Response Time (s)": response.elapsed.total_seconds(),
            "Errors": errors_list if errors_list else "-"
        }

        print_json_response(response.json())

        table.append(result)

        headers = list(table[0].keys())
        formatted_results = [[result[header] for header in headers] for result in table]
        logger.info("\n" + tabulate(formatted_results, headers=headers, tablefmt='pretty'))
        cls.report.add_result(result)
        if errors:
            pytest.fail("\n".join(errors))

    @classmethod
    def teardown_class(cls):
        # Create Report on Console
        cls.report.generate_report()

    @classmethod
    def assert_group_equals(cls, response=None, expected_values=None, response_list=False, response_item=0):

        errors = []
        for field, expected_value in expected_values:
            if response_list:
                actual_value = response.json()[response_item].get(field)
            else:
                actual_value = response.json().get(field)

            if actual_value != expected_value:
                errors.append(f"Expected '{field}' to be '{expected_value}', but got '{actual_value}'")
        return errors
