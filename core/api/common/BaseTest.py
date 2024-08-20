import pytest
from core.api.utils.ResponseUtils import ResponseUtils
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('BaseTest')


class BaseTest:

    base_url = None

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self, config):
        self.base_url = config.get('api', {}).get('base_url')
        logger.info("BASE URL: " + self.base_url)
        BaseApi.set_base_url(self.base_url)

        yield

    @classmethod
    def response(cls):
        return ResponseUtils()

