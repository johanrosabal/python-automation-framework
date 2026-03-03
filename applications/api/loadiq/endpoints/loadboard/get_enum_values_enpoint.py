from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('GenerateLoadNumberEndpoint')


class GetEnumValuesEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "/LoadBoardAPI/GetEnumValues"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def get_response(self, enum_type):
        logger.info(f"Response [{self._name}]")

        params = {
            'enumType': enum_type,
        }

        request = self.get_request() \
            .set_base_url(self.endpoints['loadboard']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_params(params) \
            .send()

        return request

