from tabulate import tabulate
from core.config.logger_config import setup_logger
logger = setup_logger('APITestReport')


class APITestReport:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def generate_report(self):
        total_tests = len(self.results)
        passed_tests = len([result for result in self.results if result["Status"] == "PASS"])
        failed_tests = total_tests - passed_tests

        logger.info("API TEST REPORT")

        if total_tests > 0:
            headers = list(self.results[0].keys())
            formatted_results = [[result[header] for header in headers] for result in self.results]
            logger.info(f"\n{tabulate(formatted_results, headers=headers, tablefmt='grid')}\n Total Tests: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}")

        else:
            logger.error("No tests were executed.")


# Example
# report = APITestReport()
# report.add_result("Get User", "https://api.example.com/users/1", "GET", 200, 150, {"id": 1, "name": "John Doe"})
# report.add_result("Create User", "https://api.example.com/users", "POST", 201, 200, {"id": 2, "name": "Jane Doe"})
# report.add_result("Update User", "https://api.example.com/users/2", "PUT", 404, 180, {}, "User not found")
#
# Example Generate Report
# report.generate_report()
