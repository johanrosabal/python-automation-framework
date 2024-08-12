from core.config.logger_config import setup_logger

logger = setup_logger('Decorator')


def test(test_case_id: str, test_description: str):
    def decorator(func):
        func.test_case_id = test_case_id
        func.test_description = test_description
        logger.info("Case ID: " + test_case_id + " - Description: " + test_description)
        return func

    return decorator
