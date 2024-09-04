from tabulate import tabulate
from core.config.logger_config import setup_logger
logger = setup_logger('WEBTestReport')


class WEBTestReport:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def generate_report(self):
        total_tests = len(self.results)
        passed_tests = len([result for result in self.results if result["Status"] == "PASS"])
        failed_tests = total_tests - passed_tests

        logger.info("WEB TEST REPORT")

        if total_tests > 0:
            headers = list(self.results[0].keys())
            formatted_results = [[result[header] for header in headers] for result in self.results]
            logger.info(f"\n{tabulate(formatted_results, headers=headers, tablefmt='grid')}\n Total Tests: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}")

        else:
            logger.error("No tests were executed.")