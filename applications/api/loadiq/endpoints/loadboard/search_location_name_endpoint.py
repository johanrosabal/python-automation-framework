from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SavePostedLoadEndpoint')


class SearchLocationNameEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "LocationAPI/SearchLocationName"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def get_response_location(self, location_name: str):
        logger.info(f"Response [{self._name}]")

        params = {
            'partialName': location_name
        }

        # This Endpoint is Exclusive for 'location' Module
        request = self.get_request() \
            .set_base_url(self.endpoints['location']) \
            .set_endpoint(self._endpoint) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .add_header("Content-Type", "application/json") \
            .add_header("Accept", "application/json") \
            .add_header("Accept-Encoding", "gzip,deflate") \
            .set_params(params)\
            .send()

        return request
