# @staticmethod
import pytest
from core.config.logger_config import setup_logger

logger = setup_logger('AssertsCollector')


# collector = AssertCollector()
# collector.assert_equal(title, self.get_title())
# collector.assert_all()

class AssertCollector:
    def __init__(self):
        self.errors = []

    def assert_group_equal(self, expected, actual):
        try:
            assert expected == actual, "[Asserts]: Expected value should be [" + expected + "] not [" + actual + "]"
        except AssertionError as e:
            self.errors.append(str(e))

    def assert_group_true(self, condition, message):
        try:
            assert condition, message
        except AssertionError as e:
            self.errors.append(str(e))

    def assert_all(self):
        if self.errors:
            pytest.fail("\n".join(self.errors))

    @staticmethod
    def assert_equal(expected, actual):
        assert expected == actual, "[Asserts]: Expected value should be [" + expected + "] not [" + actual + "]"

    @staticmethod
    def assert_equal_message(expected, actual, message, page="", method_name=""):
        error_message = f"Validation: {message} | Expected value [{expected}] | Actual value [{actual}]"
        log_message = f"[{page}][{method_name}]" if page and method_name else ""

        try:
            assert expected == actual, f"{log_message}[Not Match]: {error_message}"
            logger.info(f"{log_message}[Validation]: {message} | {error_message}")
        except AssertionError as e:
            logger.error(str(e))
            raise


