import pytest

from core.config.logger_config import setup_logger
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from applications.api.csight.common.CsightBaseTest import CsightBaseTest, user
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from core.data.sources.JSON_reader import JSONReader
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from applications.web.csight.pages.home.HomePage import HomePage
from applications.api.csight.utils.csight_helper import extract_cvif_code

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12802(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3187", test_description="[12802] Create Booking Vehicle Terminal USCHT to PRSJU with Credit Status", skip=True)
    def test_create_a_booking_vehicle_active_status_changed_to_pending_with_credit_status(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3187

        path = "../../data/bookings/CT-3187_booking_with_USCHT_to_PRSJU_to_pending_status_with_credit.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Use this fields for Update Booking
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3187 | Create Booking Vehicle Terminal USCHT to PRSJU with Pending Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3187_pending_booking_vehicle_terminal_uscht_prsju_with_credit_status"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=carrier_booking_request_reference,
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-057'],
            timeout=230
        )

        self.add_report(
            test_data="CT-3187 | Get Booking Vehicle Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3187_get_booking_vehicle_pending"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        crowley_booking_reference_number = dict_status["crowleyBookingReferenceNumber"]

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        c_sight_pending_reason = self.bookings_details.get_pending_reason()
        assert (c_sight_status == "Pending"), "Booking Status Incorrect"
        assert (c_sight_pending_reason[0] == "Vehicle / CNC DocumentsApprove"), "Incorrect Pending Reason"

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3187_booking_vehicle_active"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3187_booking_cargo_details"
        )

        self.bookings_details.scroll().to_top()

    @test(test_case_id="CT-3188", test_description="[12802] Create Booking Vehicle Terminal USCHT to PRSJU without Credit Status", skip=False)
    def test_create_a_booking_vehicle_active_status_changed_to_pending_without_credit_status(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3188

        path = "../../data/bookings/CT-3187_booking_with_USCHT_to_PRSJU_should_pass_to_pending_status_without_credit.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Use this fields for Update Booking
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3188 | Create Booking Vehicle Terminal USCHT to PRSJU without Pending Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3188_pending_booking_vehicle_terminal_uscht_prsju_without_credit_status"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=carrier_booking_request_reference,
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-057'],
            timeout=230
        )

        self.add_report(
            test_data="CT-3188 | Get Booking Vehicle Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3188_get_booking_vehicle_pending"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        crowley_booking_reference_number = dict_status["crowleyBookingReferenceNumber"]

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        c_sight_pending_reason = self.bookings_details.get_pending_reason()

        assert (c_sight_status == "Pending"), "Booking Status Incorrect"
        assert (c_sight_pending_reason[0] == "Vehicle / CNC DocumentsApprove"), "Incorrect Pending Reason"

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3188_booking_vehicle_active"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3188_booking_cargo_details"
        )

        self.bookings_details.scroll().to_top()
