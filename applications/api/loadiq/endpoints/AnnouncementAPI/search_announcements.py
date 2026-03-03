import json
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from typing import List, Dict, Optional

logger = setup_logger('SearchAnnouncementsEndpoint')

class SearchCondition:
    def __init__(self, field_name: str, field_type: str, operator: str, value: str, value2: Optional[str] = None):
        self.fieldName = field_name
        self.fieldType = field_type
        self.operator = operator
        self.value = value
        self.value2 = value2

class SearchAnnouncementsEndpoint(BaseApi):
    def __init__(self):
        super().__init__()
        self._name = self.__class__.__name__
        self._endpoint = "AnnouncementAPI/SearchAnnouncements"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def search_announcements(self,
                           search_terms: str = None,
                           search_conditions: List[Dict] = None,
                           sort_by: str = None,
                           pre_sort_by: str = None,
                           sort_descending: bool = True,
                           rows_per_page: int = 0,
                           page_number: int = 0,
                           exclude_expired: bool = False):

        search_params = {
            "searchTerms": search_terms,
            "searchConditions": search_conditions,
            "sortBy": sort_by,
            "preSortBy": pre_sort_by,
            "sortDescending": sort_descending,
            "rowsPerPage": rows_per_page,
            "pageNumber": page_number
        }

        # Remove None values from payload
        search_params = {k: v for k, v in search_params.items() if v is not None}

        payload = {
            "cgsSearchParams": search_params
        }

        request = self.post_request() \
            .set_base_url(self.endpoints['user_management']) \
            .set_endpoint(f"{self._endpoint}?excludeExpired={str(exclude_expired).lower()}") \
            .set_timeout(10) \
            .add_header("accept", "text/plain") \
            .add_header("Content-Type", "application/json") \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_json(payload) \
            .send()

        return request
