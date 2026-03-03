import json

import allure

from applications.api.softship.data.account import Api_account_select
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('AccountSelect')


class AccountSelect(BaseApi):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = AccountSelect()
            cls.name = __class__.__name__
            cls.endpoint = "MasterData/account/Select"
        return cls._instance

    @allure.step("Select Agency:")
    def select_agency(self, cookie_value, payload):

        cookies = {
            'Softship.MasterData.Session': cookie_value
        }

        response = self.post_request() \
            .set_endpoint(self.endpoint) \
            .add_header("Content-Type", "application/json") \
            .add_header("Accept", "application/json") \
            .add_header("Accept-Encoding", "gzip,deflate") \
            .set_cookies(cookies) \
            .set_json(payload) \
            .set_timeout(15) \
            .send()

        payload = json.dumps(payload)
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
