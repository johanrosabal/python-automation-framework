import pytest
import requests

from core.utils.config_loader import load_config
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
    def GET(cls, endpoint, params=None, headers=None, verify=False):
        url = f"{BaseApi.get_base_url()}/{endpoint}"
        logger.info(f"GET: {url}")
        response = requests.get(
            url=url,
            params=params,
            headers=headers,
            verify=False  # Inactive SSL Certificates
        )

        return response

    @classmethod
    def POST(cls, endpoint, data=None, json=None, headers=None):
        url = f"{BaseApi.get_base_url()}/{endpoint}"
        logger.info(f"POST: {url}")
        response = requests.post(
            url=url,
            data=data,
            json=json,
            headers=headers,
            verify=False  # Inactive SSL Certificates
        )

        return response

    @classmethod
    def PUT(cls, endpoint, data=None, json=None, headers=None):
        url = f"{BaseApi.get_base_url()}/{endpoint}"
        logger.info(f"PUT: {url}")
        response = requests.put(
            url=url,
            data=data,
            json=json,
            headers=headers,
            verify=False  # Inactive SSL Certificates
        )

        return response

    @classmethod
    def PATCH(cls, endpoint, data=None, json=None, headers=None):
        url = f"{BaseApi.get_base_url()}/{endpoint}"
        logger.info(f"PATCH: {url}")
        response = requests.put(
            url=url,
            data=data,
            json=json,
            headers=headers,
            verify=False  # Inactive SSL Certificates
        )

        return response

    @classmethod
    def DELETE(cls, endpoint, headers=None):
        url = f"{BaseApi.get_base_url()}/{endpoint}"
        logger.info(f"DELETE: {url}")
        response = requests.delete(
            url=url,
            headers=headers,
            verify=False  # Inactive SSL Certificates
        )
        return response
