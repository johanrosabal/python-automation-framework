import pytest
from applications.api.salesforce.endpoints.authorization_oauth2 import AuthorizationOauth2
from core.config.logger_config import setup_logger
from core.api.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.table_formatter import TableFormatter

logger = setup_logger('AuthorizationToken')


class TestAuthorizationToken(BaseTest):

    authorization = AuthorizationOauth2

    @test(test_case_id="TOK-0001", test_description="Test get token access")
    def test_generate_access_token(self):
        self.authorization.get_token()
        self.authorization.get_instance_url()
        self.authorization.get_id()
        self.authorization.get_token_type()
        self.authorization.get_issued_at()
        self.authorization.get_signature()

        json = self.authorization.get_response_json()
        TableFormatter().prepare_single_item(json).to_grid()
