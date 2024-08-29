import pytest

from applications.api.salesforce.endpoints.bookings_endpoint import Bookings
from applications.api.salesforce.endpoints.oauth2_authorization import AuthorizationOauth2
from core.config.logger_config import setup_logger
from core.api.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.table_formatter import TableFormatter

logger = setup_logger('AuthorizationToken')


class TestAuthorizationToken(BaseTest):

    authorization = AuthorizationOauth2
    bookings = Bookings().get_instance()

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

    @test(test_case_id="TOK-0002", test_description="Test get Booking Confirmation")
    def test_generate_access_token(self):

        token = self.authorization.get_token()
        request = self.bookings.get_confirmation(token=token, booking_id="CAT376130")
        response = request.get_info()

        # Standard Validations: Status Code and Content Type
        # self.validations(response) \
        #     .verify_status_success_code(201, print_response_text=False)

        print(response)





