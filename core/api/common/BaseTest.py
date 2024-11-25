import pytest
from tabulate import tabulate
from core.utils.helpers import print_json
from core.api.report.APITestReport import APITestReport
from core.config.logger_config import setup_logger

logger = setup_logger('BaseTest')


@pytest.mark.usefixtures("load_yaml_config")
class BaseTest:

    report = APITestReport()

    @classmethod
    def add_report(cls, test_data, status_code, response, errors=None):
        table = []
        errors_list = []

        if response is None:
            errors_list.append("Api Response is None")

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

        print_json("Request Body", response.request.body)
        print_json("Request Response", response.text)

        table.append(result)

        headers = list(table[0].keys())
        formatted_results = [[result[header] for header in headers] for result in table]
        logger.info("\n" + tabulate(formatted_results, headers=headers, tablefmt='pretty'))
        cls.report.add_result(result)
        if errors_list:
            pytest.fail("\n".join(errors_list))

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
