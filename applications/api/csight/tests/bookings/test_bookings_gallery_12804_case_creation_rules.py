import pytest

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
from applications.api.csight.utils.csight_helper import extract_cvif_code
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12804(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3189", test_description="[12804] Create a Booking with Rates Not Available should open a case in Pricing Queue", skip=True)
    def test_create_a_booking_with_rates_not_available_case_pricing_queue(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3189

        # PRECONDITION: create a new booking on Active Status
        path = "../../data/bookings/CT-3189_booking_with_rates_not_available.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3189 | Create a Booking Container with Rates Not Available Case Pricing Queue",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3189_active_booking_container_case_pricing_queue"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)

        shared_data["electronicCustomerReference"] = dict_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = dict_response["carrierBookingRequestReference"]

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-006'],
            timeout=230
        )

        self.add_report(
            test_data="CT-3189 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3189_get_booking_container_pending_status"
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)
        # Extract Data From Response: Booking Number
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"
        assert data_response["pendingDetails"][0]["Code"] == "CROW-006", "Pending reason not match"
        assert data_response["pendingDetails"][0]["Details"] == "Rates not available", "Pending reason not match"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        c_sight_status = self.bookings_details.get_booking_status()
        c_sight_pending_reason = self.bookings_details.get_pending_reason()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3180_Booking_Update_Status")
        assert (c_sight_status == "Pending"), "Booking Status Incorrect"
        assert (c_sight_pending_reason[0] == "Rates not available"), "Pending Reason Incorrect"

        self.bookings_details.click_tab_cases()
        self.bookings_details.screenshot().save_screenshot(description="CT-3180_Booking_Case_Owner")
        c_sight_case_owner = self.bookings_details.tab_content_cases_details.get_case_owner(index=1)

        assert (c_sight_case_owner == "Pricing Inquiry/Request"), "Incorrect Case Owner"

    @test(test_case_id="CT-3190", test_description="[12804] Create Booking Any Other Pending Reason go to Specialty Queue 3", skip=False)
    def test_create_a_booking_with_any_other_pending_reason_go_to_specialty_queue_3(self,shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3190

        path = "../../data/bookings/CT-3190_booking_number_with_any_other_pending_reason_go_to_specialty_queue_3.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3190 | Create a Booking Container Any Other Pending Reason go to Specialty Queue 3",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3190_active_booking_container_any_other_pending_reason_go_to_specialty_queue_3"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)

        shared_data["electronicCustomerReference"] = dict_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = dict_response["carrierBookingRequestReference"]

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-029'],
            timeout=230
        )

        self.add_report(
            test_data="CT-3190 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3190_get_booking_container_pending_status"
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)
        # Extract Data From Response: Booking Number
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"
        assert data_response["pendingDetails"][0]["Code"] == "CROW-029", "Pending reason not match"
        assert data_response["pendingDetails"][0]["Details"] == "Booking UI Portal Validation Failed", "Pending reason not match"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        c_sight_status = self.bookings_details.get_booking_status()
        c_sight_pending_reason = self.bookings_details.get_pending_reason()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3190_Booking_Container_Status")
        assert (c_sight_status == "Pending"), "Booking Status Incorrect"
        assert (c_sight_pending_reason[0] == "Booking UI Portal Validation Failed"), "Pending Reason Incorrect"

        self.bookings_details.click_tab_cases()
        self.bookings_details.screenshot().save_screenshot(description="CT-3190_Booking_Case_Owner")
        c_sight_case_owner = self.bookings_details.tab_content_cases_details.get_case_owner(index=1)

        assert (c_sight_case_owner == "Specialty Queue 3"), "Incorrect Case Owner"
