import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('ToggleUserAccessInOktaEndpoint')

class ToggleUserAccessInOktaEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "UserManagementAPI/ToggleUserAccessInOkta"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def toggle_user_access(self, email: str, enable: bool):
        params = {
            "email": email,
            "enable": enable
        }

        request = self.get_request() \
            .set_base_url(self.endpoints['user_management']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("accept", "text/plain") \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_params(params) \
            .send()

        return request

    def toggle_user_access_without_email(self, enable: bool):
        params = {
            "enable": enable
        }

        request = self.get_request() \
            .set_base_url(self.endpoints['user_management']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("accept", "text/plain") \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_params(params)

        # send the request and get the response
        response = request.send()

        # Verify that the response is none
        if response is None:
            logger.error("No response received from the API")
            return None

        return response

        # Get the object response
        api_response = response.get_response()

        if api_response is None:
            logger.error("Failed to get API response")
            return None

        return api_response
