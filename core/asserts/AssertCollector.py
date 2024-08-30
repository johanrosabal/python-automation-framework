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
        text = "Expected value [" + str(expected) + "] | Actual value [" + str(actual) + "]"
        if expected == actual:
            if page != "" and method_name != "":
                logger.info("[" + page + "][" + method_name + "]" + "[Validation]: " + message + " | " + text)
            else:
                logger.info("[Validation]: " + message + " | " + text)
        assert expected == actual, ("[" + page + "][" + method_name + "]" + "[Not Match]: " + text)
