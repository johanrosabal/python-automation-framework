import json
import re

import pytest

from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from core.config.logger_config import setup_logger
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from applications.api.csight.common.CsightBaseTest import CsightBaseTest, user
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from core.data.sources.JSON_reader import JSONReader
from applications.web.csight.pages.login.LoginPage import LoginPage

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestUI(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="00001", test_description="Sign in with UAT C-Sight", feature="Login", skip=False)
    def test_login_user(self, user):
        # Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # CAT081088 | Vehicle
        # CAT498426 | Container
        self.search_menu.is_not_visible_spinner()
        self.search_menu.search_booking("CAT081088")

        # x2 = self.bookings_details.get_account()
        # x3 = self.bookings_details.get_contract_number()
        # x4 = self.bookings_details.get_origin()
        # x5 = self.bookings_details.get_pre_carriage_mode()
        # x6 = self.bookings_details.get_final_destination()
        # x7 = self.bookings_details.get_on_carriage_mode()
        # x8 = self.bookings_details.get_booking_source()
        # x9 = self.bookings_details.get_quote_number()
        # x10 = self.bookings_details.get_equipment_substitution()
        # pending_reason_list = self.bookings_details.get_pending_reason()
        # x11 = self.bookings_details.get_cargo_ready_for_transport()
        # x12 = self.bookings_details.get_booking_initiated_on()
        # x13 = self.bookings_details.get_booking_active_date()
        # x14 = self.bookings_details.get_booking_by()
        # x15 = self.bookings_details.get_contact()
        # x16 = self.bookings_details.get_payment_terms()
        # x17 = self.bookings_details.get_reserved_BOL_Number()
        # x18 = self.bookings_details.get_softship_booking_number()
        # x20 = self.bookings_details.get_primary_booking()
        # x21 = self.bookings_details.get_original_booking_number()

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()
