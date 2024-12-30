import allure
import pytest

from core.config.logger_config import setup_logger

logger = setup_logger('Decorator')


def test(test_case_id: str, test_description: str, feature: str = "", skip=False):
    if skip:
        return pytest.mark.skip(reason=f"Skipping test: {test_description}.")

    @allure.feature(feature)
    @allure.title(f"{test_case_id} | {test_description}")
    def decorator(func):
        func.test_case_id = test_case_id
        func.test_description = test_description
        logger.debug("Case ID: " + test_case_id + " - Description: " + test_description)
        return func

    return decorator


