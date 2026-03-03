from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('Post')


class UsersEndpoint(BaseApi):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = UsersEndpoint()
            cls.name = __class__.__name__
            cls.endpoint = "users/"
        return cls._instance

    def create_user(self,json=None):
        logger.info(f"[{self.name}]: Create an User")

        response = self.post_request() \
            .set_endpoint(self.endpoint) \
            .add_header("Content-Type", "application/json") \
            .set_json(json) \
            .set_timeout(15) \
            .send()

        return response

    def get_user_information(self, id_user):
        logger.info(f"[{self.name}]: Get Users Information")
        response = self.get_request()\
            .set_endpoint(f"{self.endpoint}{id_user}")\
            .add_header("Content-Type", "application/json")\
            .set_timeout(10)\
            .send()

        return response

    def get_users_information(self):
        logger.info(f"[{self.name}]: Get Users Information")
        response = self.get_request() \
            .set_endpoint(self.endpoint) \
            .add_header("Content-Type", "application/json")\
            .set_timeout(10)\
            .send()

        return response

    def edit_user_information(self, id_user=None, json=None):
        logger.info(f"[{self.name}]: Edit User Information")
        response = self.put_request()\
            .set_endpoint(f"{self.endpoint}{id_user}")\
            .add_header("Content-Type", "application/json")\
            .set_json(json)\
            .set_timeout(10)\
            .send()

        return response

    def delete_user_information(self, id_user=None):
        logger.info(f"[{self.name}]: Edit User Information")
        response = self.delete_request() \
            .set_endpoint(f"{self.endpoint}{id_user}") \
            .add_header("Content-Type", "application/json") \
            .set_timeout(10) \
            .send()

        return response
