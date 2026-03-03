import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SaveLoadDocumentEndpoint')


class SaveLoadDocumentEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "LoadBoardAPI/SavePostedLoad"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def post_document(self, is_deleted: bool, load_document_id: str, document_type: str, document_format: str,
                      content: str, document_name: str, date_created: str, posted_load_id: int):

        data = {
            "isdeleted": is_deleted,
            "loadDocumentId": load_document_id,
            "documentType": document_type,
            "documentFormat": document_format,
            "content": content,
            "documentName": document_name,
            "dateCreated": date_created,
            "postedLoadid": posted_load_id
        }

        json_data = json.dumps(data, default=str, indent=4)

        request = self.post_request() \
            .set_base_url(self.endpoints['loadboard']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_json(json_data) \
            .send()

        return request
