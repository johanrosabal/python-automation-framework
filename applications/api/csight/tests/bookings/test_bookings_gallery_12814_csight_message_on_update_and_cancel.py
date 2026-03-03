import pytest

from applications.web.csight.pages.bookings.BookingsPage import BookingsPage
from applications.web.csight.pages.bookings.CreateBookingPage import CreateBookingPage
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
class TestBookingsGallery12814(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    create_booking = CreateBookingPage.get_instance()
    bookings_landing = BookingsPage.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3234", test_description="[12814] Booking Update and Verify C-Sight Display the Alert Message Reason", skip=False)
    def test_booking_update_verify_csight_display_alert_message_reason(self, shared_data, user):
        path = "../../data/bookings/CT-3234_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Load CSigh UI
        self.login.load_page()
        self.login.login_user(user=user)

        # Get CVIF Account
        # --------------------------------------------------------------------------------------------------------------
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        # Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3234 | Create a Booking Container Active Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3234_active_booking_container_active"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        shared_data["electronicCustomerReference"] = dict_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3234 | Get Booking Container Active Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3234_get_booking_container_active_status"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification

        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        # c_sight_status = self.bookings_details.get_booking_status()
        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3234_booking_container_new_to_active")
        # assert (c_sight_status == "Active"), "Booking Status Incorrect"

        # Click on Update Button on Booking Details
        self.bookings_details.buttons.click_update()
        # Origin Destination Click on Bill to Party 'Same as Booking Party' checkbox
        self.create_booking.origin_destination.click_checkbox_bill_to_party_same_as_booking_party()
        # Select Bill to Party Type:  Shipper
        self.create_booking.origin_destination.select_bill_to_party_bill_to_party_type("Shipper")

        # UPDATE BOOKING API
        data["cargos"][0]["containerDetails"]["equipmentIsoCode"] = "42G0"

        response_new_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=data_response["crowleyBookingReferenceNumber"],
            shipperCvif=shared_data["shipperCvif"],
            carrierBookingRequestReference=data_response["carrierBookingRequestReference"],
            json=data
        )
        self.add_report(
            test_data="CT-3234 | UPDATE Booking Equipment Code",
            status_code=[200, 202, 303],
            response=response_new_status
        )

        # Click on Next
        self.create_booking.click_next()
        # Click on OK Button on Modal Dialog Box
        self.create_booking.click_modal_ok()
        # Click on Cargo 1: Hazardous
        self.create_booking.cargo_details.select_radio_hazardous_booking(index=1, text="No")
        # Click on Cargo 1: Waste
        self.create_booking.cargo_details.select_radio_waste(index=1, text="No")
        # Click on Cargo 1: RCRA
        self.create_booking.cargo_details.select_radio_RCRA(index=1, text="No")
        # Click on Next on Cargo Details
        self.create_booking.click_next()
        # Click on Next on Routes
        self.create_booking.click_next()

        modal_text = self.create_booking.get_modal_text()
        assert (modal_text == f"Booking {data_response["crowleyBookingReferenceNumber"]} was updated via a Customer API request. Please review the latest changes and make any necessary adjustments.")
        self.create_booking.screenshot().pause(3).save_screenshot(description="CT-3234_booking_container_updates_modal_text")

    @test(test_case_id="CT-3235", test_description="[12814] Booking Cancel and Verify C-Sight Display the Alert Message Reason", skip=False)
    def test_booking_cancel_verify_csight_display_alert_message_reason(self, shared_data, user):

        path = "../../data/bookings/CT-3234_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Load CSigh UI
        self.login.load_page()
        self.login.login_user(user=user)

        # Get CVIF Account
        # --------------------------------------------------------------------------------------------------------------
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        # Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3235 | Create a Booking Container Active Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3235_active_booking_container_active"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        shared_data["electronicCustomerReference"] = dict_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3235 | Get Booking Container Active Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3235_get_booking_container_active_status"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # Load Booking Page
        self.bookings_landing.load_page()
        # Search Booking Number
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3235_booking_container_new_to_active"
        )
        # Click on Update Button on Booking Details
        self.bookings_details.buttons.click_update()

        # Origin Destination Click on Bill to Party 'Same as Booking Party' checkbox
        self.create_booking.origin_destination.click_checkbox_bill_to_party_same_as_booking_party()
        # Select Bill to Party Type:  Shipper
        self.create_booking.origin_destination.select_bill_to_party_bill_to_party_type("Shipper")

        # Send Cancel Request
        response_new_status = self.bookings.cancel_booking_with_cat_number(
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            shipperCvif=shared_data["shipperCvif"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
        )

        self.add_report(
            test_data="CT-3235 | CANCEL Booking Vehicle Status New",
            status_code=202,
            response=response_new_status
        )

        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Cancel",
            timeout=230
        )

        self.add_report(
            test_data="CT-3235 | Get Booking Container Cancel Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3235_get_booking_container_cancel_status"
        )

        # Click on Next on Cargo Details
        self.create_booking.click_next()

        modal_text = self.create_booking.get_modal_text()
        assert (modal_text == f"Booking {data_response["crowleyBookingReferenceNumber"]} was cancelled via a Customer API request. Please review the latest changes and make any necessary adjustments.")
        self.create_booking.screenshot().pause(3).save_screenshot(
            description="CT-3235_booking_container_cancel_modal_text"
        )
