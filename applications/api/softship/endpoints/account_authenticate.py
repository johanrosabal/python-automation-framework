import allure

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
import json

logger = setup_logger('AccountAuthenticate')


class AccountAuthenticate(BaseApi):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = AccountAuthenticate()
            cls.name = __class__.__name__
            cls.endpoint = "MasterData/account/Authenticate"
        return cls._instance

    @allure.step("Get Authentication:")
    def get_authentication(self, username, password):
        logger.info(f"[{self.name}]:Get User Account Authentication")

        payload = json.dumps({
            "captcha": "",
            "captchaId": "",
            "password": password,
            "userName": username
        })

        response = self.post_request() \
            .set_endpoint(self.endpoint) \
            .add_header("Content-Type", "application/json") \
            .set_data(payload) \
            .set_timeout(15) \
            .send()

        # Attach the full response to Allure report
        allure.attach(
            payload,  # Response content
            name="Request Body",  # Name of the attachment
            attachment_type=allure.attachment_type.JSON  # Content type for better formatting in the report
        )

        # Attach the full response to Allure report
        allure.attach(
            response.response.text,  # Response content
            name="Response Body",  # Name of the attachment
            attachment_type=allure.attachment_type.JSON  # Content type for better formatting in the report
        )

        # Log status code directly in the Allure step
        with allure.step(f"Status Code: {response.response.status_code}"):
            logger.info(f"Response Status Code: {response.response.status_code}")

        # Log status code directly in the Allure step
        with allure.step(f"Elapsed: {response.response.elapsed} "):
            logger.info(f"Response Elapsed: {response.response.elapsed}")

        # Log status code directly in the Allure step
        with allure.step(f"Endpoint: {response.response.url} "):
            logger.info(f"Endpoint: {response.response.url}")

        # Log status code directly in the Allure step
        with allure.step(f"Cookies: {response.response.cookies} "):
            logger.info(f"Cookies: {response.response.cookies}")

        return response.response
