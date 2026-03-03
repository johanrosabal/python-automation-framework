import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SavePostedLoadEndpoint')


class SavePostedLoadEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "LoadBoardAPI/SavePostedLoad"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def get_response(self, payload):
        logger.info(f"Response [{self._name}]")

        request = self.post_request() \
            .set_base_url(self.endpoints['loadboard']) \
            .set_endpoint(self._endpoint) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .add_header("Content-Type", "application/json") \
            .add_header("Accept", "application/json") \
            .add_header("Accept-Encoding", "gzip,deflate") \
            .set_data(payload) \
            .set_timeout(10) \
            .set_verify(False) \
            .send()

        return request




