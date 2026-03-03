
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SearchMyOffersEndpoint')

class SearchMyOffersEndpoint(BaseApi):
    def __init__(self):
        super().__init__()
        self._name = self.__class__.__name__
        self._endpoint = "LoadBoardAPI/SearchMyOffers"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def search_my_offers(self, is_draft: bool, search_terms: str, rows_per_page: int, page_number: int,
                         sort_by: str, sort_descending: bool, search_conditions: list,
                         include_closed_loads: bool = False):
        params = {
            'includeClosedLoads': include_closed_loads,
        }

        data = {
            "isDraft": is_draft,
            "searchTerms": search_terms,
            "rowsPerPage": rows_per_page,
            "pageNumber": page_number,
            "sortBy": sort_by,
            "sortDescending": sort_descending,
            "searchConditions": search_conditions
        }
        request = self.post_request() \
            .set_base_url(self.endpoints['loadboard']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_params(params)\
            .set_json(data) \
            .send()
        return request
