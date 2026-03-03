from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('TestSessionEndpoint')


class TestSessionEndpoint(BaseApi):

    def __init__(self):
        super().__init__()  # Llama al constructor de BaseApi si es necesario
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "/LoadBoardAPI/TestSession"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def get_response(self):
        logger.info(f"Response [{self._name}]")

        endpoints = self.get_endpoints()
        logger.info(f"Loadboard {endpoints["loadboard"]}")

        logger.info(f"JWT Token----: {BaseApi.get_jwt_access_token()}")
        logger.info(f"Custom Token----: {BaseApi.get_jwt_access_token()}")

        request = self.get_request() \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("accept", "text/plain") \
            .send()

        return request
