import pytest

from core.config.logger_config import setup_logger

logger = setup_logger('BaseTest')


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == 'call':
        outcome = 'PASSED' if call.excinfo is None else 'FAILED'
        test_case_id = getattr(item.function, 'test_case_id', 'No ID')
        test_description = getattr(item.function, 'test_description', 'No Description')
        logger.info(
            "\n****************************************************************************************************" +
            "\n\tTest Name: " + str(item.name) +
            "\n----------------------------------------------------------------------------------------------------" +
            "\n\t\t- Test Case ID: " + str(test_case_id) +
            "\n\t\t- Description: " + str(test_description) +
            "\n\t\t- Result: " + str(outcome) +
            "\n****************************************************************************************************"
        )
        for handler in logger.handlers:
            handler.flush()  # Ensure logs are flushed to the output

