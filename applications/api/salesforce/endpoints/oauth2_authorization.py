from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('AuthorizationOauth2')


class AuthorizationOauth2(BaseApi):
    _grant_type = None
    _client_id = None
    _client_secret = None
    _username = None
    _password = None
    _endpoint = "services/oauth2/token?"
    _base_url = None
    _response = None

    @classmethod
    def set_base_url(cls, base_url):
        cls._base_url = base_url
        return cls

    @classmethod
    def set_grant_type(cls, grant_type):
        cls._grant_type = grant_type
        return cls

    @classmethod
    def set_client_id(cls, client_id):
        cls._client_id = client_id
        return cls

    @classmethod
    def set_client_secret(cls, client_secret):
        cls._client_secret = client_secret
        return cls

    @classmethod
    def set_username(cls, username):
        cls._username = username
        return cls

    @classmethod
    def set_password(cls, password):
        cls._password = password
        return cls

    @classmethod
    def get_response(cls):
        return cls._response.get_info()

    @classmethod
    def get_response_json(cls):
        return cls._response.get_response_json()

    @classmethod
    def get_token(cls):
        token = cls.get_response_json().get('access_token')
        logger.info(f"Token: {token}")
        return token

    @classmethod
    def get_instance_url(cls):
        instance_url = cls.get_response_json().get('instance_url')
        logger.info(f"Instance Url: {instance_url}")
        return

    @classmethod
    def get_id(cls):
        _id = cls.get_response_json().get('id')
        logger.info(f"id: {_id}")
        return _id

    @classmethod
    def get_token_type(cls):
        token_type = cls.get_response_json().get('token_type')
        logger.info(f"Token Type: {token_type}")
        return token_type

    @classmethod
    def get_issued_at(cls):
        issued_at = cls.get_response_json().get('issued_at')
        logger.info(f"Issued at: {issued_at}")
        return issued_at

    @classmethod
    def get_signature(cls):
        signature = cls.get_response_json().get('signature')
        logger.info(f"Signature: {signature}")
        return signature

    @classmethod
    def send(cls):
        logger.info(f"Authorization Token")
        params = {
            'grant_type': cls._grant_type,
            'client_id': cls._client_id,
            'client_secret': cls._client_secret,
            'username': cls._username,
            'password': cls._password
        }
        response = (
            cls.post_request()
            .set_base_url(cls._base_url)
            .set_endpoint(cls._endpoint)
            .set_params(params)
            .set_timeout(10)
            .send()
        )

        cls._response = response
        return cls
