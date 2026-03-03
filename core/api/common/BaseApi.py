import time

import requests

from core.api.actions.Delete import Delete
from core.api.actions.Get import Get
from core.api.actions.Patch import Patch
from core.api.actions.Post import Post
from core.api.actions.Put import Put
from core.config.logger_config import setup_logger

logger = setup_logger('BaseApi')


class BaseApi:
    base_url = None
    base_token_url = None

    endpoints = None
    modules = None
    jwt_access_token = None
    custom_token = None
    client_secret = None
    client_id = None

    @classmethod
    def set_base_url(cls, value):
        cls.base_url = value

    @classmethod
    def get_base_url(cls):
        return cls.base_url

    @classmethod
    def set_endpoints(cls, value):
        cls.endpoints = value

    @classmethod
    def get_endpoints(cls):
        return cls.endpoints

    @classmethod
    def set_modules(cls, value):
        cls.modules = value

    @classmethod
    def get_modules(cls):
        return cls.modules

    @classmethod
    def set_jwt_access_token(cls, value):
        cls.jwt_access_token = value

    @classmethod
    def get_jwt_access_token(cls):
        return cls.jwt_access_token

    @classmethod
    def set_client_id(cls, value):
        cls.client_id = value

    @classmethod
    def get_client_id(cls):
        return cls.client_id

    @classmethod
    def set_client_secret(cls, value):
        cls.client_secret = value

    @classmethod
    def get_client_secret(cls):
        return cls.client_secret

    @classmethod
    def set_custom_token(cls, value):
        cls.custom_token = value

    @classmethod
    def get_custom_token(cls):
        return cls.custom_token

    @classmethod
    def set_base_token_url(cls, value):
        cls.base_token_url = value

    @classmethod
    def get_base_token_url(cls):
        return cls.base_token_url

    @classmethod
    def post_request(cls):
        return Post(BaseApi.get_base_url())

    @classmethod
    def get_request(cls):
        return Get(BaseApi.get_base_url())

    @classmethod
    def put_request(cls):
        return Put(BaseApi.get_base_url())

    @classmethod
    def patch_request(cls):
        return Patch(BaseApi.get_base_url())

    @classmethod
    def delete_request(cls):
        return Delete(BaseApi.get_base_url())

    @staticmethod
    def pause(seconds):
        logger.info("Pause: " + str(seconds))
        time.sleep(seconds)

