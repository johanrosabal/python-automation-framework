import pytest
from tabulate import tabulate
from core.utils.helpers import print_json
from core.api.report.APITestReport import APITestReport
from core.config.logger_config import setup_logger
import time

logger = setup_logger('BaseTest')


@pytest.mark.usefixtures("load_yaml_config")
class BaseTest:

    report = APITestReport()

    @classmethod
    def add_report(cls, test_data, status_code, response, errors=None):
        table = []
        errors_list = []
        actual_status = None
        url = None
        method = None
        time_elapsed = None

        request_body = None
        response_body = None

        # Soporte para múltiples códigos de estado
        if isinstance(status_code, str) and "|" in status_code:
            expected_status_codes = [int(code.strip()) for code in status_code.split("|")]
        elif isinstance(status_code, (list, tuple)):
            expected_status_codes = list(map(int, status_code))
        else:
            expected_status_codes = [int(status_code)]

        if response is None:
            errors_list.append("Api Response is None")
        else:
            if isinstance(response, dict):
                if isinstance(response.get("errorCode"), int):
                    actual_status = response["errorCode"]
                    url = response.get("url")
                    method = response.get("method")
                    time_elapsed = response.get("elapsed")
                    request_body = response.get("response").text if response.get("response") else None
                    response_body = response.get("request")
                elif isinstance(response.get("status_code"), int):
                    actual_status = response["status_code"]
                elif isinstance(response.get("status"), int):
                    actual_status = response["status"]
            else:
                if hasattr(response, "status_code") and isinstance(response.status_code, int):
                    actual_status = response.status_code
                    url = response.request.url if hasattr(response.request, "url") else None
                    method = response.request.method if hasattr(response.request, "method") else None
                    time_elapsed = response.elapsed.total_seconds() if hasattr(response, "elapsed") else None
                    request_body = response.request.body if hasattr(response.request, "body") else None
                    response_body = response.text if hasattr(response, "text") else None
                elif hasattr(response, "errorCode") and isinstance(response.errorCode, int):
                    actual_status = response.errorCode

            if actual_status is None:
                errors_list.append("No valid status code found in response")

        if actual_status not in expected_status_codes:
            errors_list.append(f"Expected Status Code(s): {expected_status_codes}, actual value: {actual_status}")

        if errors:
            errors_list.extend(errors)

        if isinstance(test_data, str):
            if "|" in test_data:
                parts = [part.strip() for part in test_data.split("|", 1)]
                test_case_id = parts[0]
                test_description = parts[1] if len(parts) > 1 else parts[0]
            else:
                test_case_id = test_description = test_data
        else:
            test_case_id = getattr(test_data, "test_case_id", str(test_data))
            test_description = getattr(test_data, "test_description", str(test_data))

        result = {
            "Test Case ID": test_case_id,
            "Test Name": test_description,
            "Status": "PASS" if actual_status in expected_status_codes and not errors_list else "FAIL",
            "URL": url,
            "Method": method,
            "Status Code": actual_status,
            "Response Time (s)": time_elapsed,
            "Errors": errors_list if errors_list else "-"
        }

        print_json("Request Body", request_body)
        print_json("Request Response", response_body)

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

    @staticmethod
    def pause(seconds):
        logger.info("Pause: " + str(seconds))
        time.sleep(seconds)
