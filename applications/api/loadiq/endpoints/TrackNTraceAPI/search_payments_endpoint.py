import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SearchPaymentsEndpoint')

class SearchPaymentsEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "TrackNTraceAPI/SearchPayments"

    def post_search_payment(self, isDraft: bool, searchTerms: str, rowsPerPage: int, pageNumber: int, sortDescending: bool):

        data = {
            "isDraft": isDraft,
            "searchTerms": searchTerms,
            "rowsPerPage": rowsPerPage,
            "pageNumber": pageNumber,
            "sortDescending": sortDescending
        }

        request = self.post_request() \
            .set_base_url(self.endpoints['trackntrace']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_json(data) \
            .send()

        return request