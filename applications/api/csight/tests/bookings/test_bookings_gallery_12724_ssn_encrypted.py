import pytest
import json
import re

from core.config.logger_config import setup_logger
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from applications.api.csight.common.CsightBaseTest import CsightBaseTest, user
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from applications.web.csight.pages.home.HomePage import HomePage
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12724(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3246", test_description="[12724] Create Booking with SSN Encrypted at each party level", skip=False)
    def test_create_a_booking_with_ssn_encrypted_at_each_party_level(self, shared_data, user, record_property):
        record_property("test_key", "CT-3239")

        path = "../../data/bookings/CT-3245_booking_ssn_encrypted_at_each_party_level_3.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3246 | Create a Booking with SSN Encrypted",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3246_create_a_booking_with_ssn_encrypted"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)

        # Read response fields
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data["carrierBookingRequestReference"], "carrierBookingRequestReference is required"

        # Wait until Booking Change Status to Active
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=230
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3246_ActiveBookingSSNEncrypted")

