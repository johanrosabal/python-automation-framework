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

    @classmethod
    def set_base_url(cls, value):
        cls.base_url = value

    @classmethod
    def get_base_url(cls):
        return cls.base_url

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
