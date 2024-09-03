from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('QuotingRequest')


class QuotingRequest(BaseApi):

    @classmethod
    def get_instance(cls, client_id, client_secret):
        if not hasattr(cls, '_instance'):
            cls._instance = QuotingRequest()
            cls.name = __class__.__name__
            cls.endpoint = "v1/quotingRequest"
            cls.client_id = client_id
            cls.client_secret = client_secret
        return cls._instance

    def send_quotation_request(self, data=None, json=None):
        logger.info(f"[{self.name}]: Post Quotation Request")
        response = (self.post_request()
                    .set_base_url(self.base_url)
                    .set_endpoint(self.endpoint)
                    .add_header("Accept", "application/json")
                    .add_header("Content-Type", "application/json")
                    .add_header("Accept-Encoding", "gzip,deflate")
                    .add_header("client_id", self.client_id)
                    .add_header("client_secret", self.client_secret)
                    .set_json(json)
                    .set_data(data)
                    .set_timeout(15)
                    .set_allow_redirects(False)
                    .send())
        return response
