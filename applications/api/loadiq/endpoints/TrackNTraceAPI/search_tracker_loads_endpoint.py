import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SearchTrackerLoadsEndpoint')

class SearchTrackerLoadsEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "TrackNTraceAPI/SearchTrackedLoads"

    def post_search_loads(self, includeClosedLoads: bool, searchType: str, searchTerms: str, rowsPerPage: int, pageNumber: int, sortBy: str, sortDescending: bool, searchConditions: list):

        params = {
            "includeClosedLoads": includeClosedLoads,
            "searchType": searchType
        }

        data = {
            "searchTerms": searchTerms,
            "rowsPerPage": rowsPerPage,
            "pageNumber": pageNumber,
            "sortBy": sortBy,
            "sortDescending": sortDescending,
            "searchConditions": searchConditions
        }

        request = self.post_request() \
            .set_base_url(self.endpoints['trackntrace']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_params(params) \
            .set_json(data) \
            .send()

        return request