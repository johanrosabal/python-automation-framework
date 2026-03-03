import json

import pytest
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

logger = setup_logger('TestBookingsGallery12979')


@pytest.fixture(scope="module")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12979(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3198", test_description="[12979] Reserve a Booking Number", skip=False)
    def test_reserved_booking_number(self, shared_data, user):
        # Extract Data Account Number from Request
        path = "../../data/bookings/CT-3198_reserved_booking_number_gallery.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # Post the Account Number to get the Booking Number Reserved
        response_new_status = self.bookings.get_reserved_booking_number(json=data)

        # Validate Status Code
        self.add_report(
            test_data="CT-3198 | Customer can reserved a booking number",
            status_code=202,
            response=response_new_status
        )

        # Generate Files: Request and Response
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3198_reserved_booking_number"
        )

        # Extract Data From Response: Booking Number
        data_response = JSONReader.text_to_dict(response_new_status.text)
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        # Validate CAT Number Format
        assert re.match(r"^CAT\d{6,8}$", shared_data["crowleyBookingReferenceNumber"]), f"CAT NUMBER INVALID: {shared_data["crowleyBookingReferenceNumber"]}"

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        pending_reason_list = self.bookings_details.get_pending_reason()[0]

        # Assert on UI
        assert (pending_reason_list == "Customer Pre-Assigned"), "Pending Reason Should be 'Customer Pre-Assigned'"
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3198_CustomerPreAssign")

    @test(test_case_id="CT-3199", test_description="[12979] Customer Can Use a Reserved Booking Number", skip=False)
    def test_assign_reserved_booking_number(self, shared_data, user):

        # Used the Reserved Booking Number
        path = "../../data/bookings/CT-3199_booking_number_with_reserve.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Insert Booking Number into Request
        data["crowleyBookingNumber"] = shared_data["crowleyBookingReferenceNumber"]

        # Send Post Request with the Booking Number Reserved
        response_post_booking = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_post_booking,
            filename_prefix="CT-3199_create_a_booking_with_reserved_booking_number"
        )

        self.add_report(
            test_data="CT-3199 | Create a Booking with Reserved Booking Number",
            status_code=202,
            response=response_post_booking
        )

        # Booking Request Reference
        booking_response = json.loads(response_post_booking.text)

        shared_data["electronicCustomerReference"] = booking_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = booking_response['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        # Validate Field Data is Present
        assert shared_data["electronicCustomerReference"], "carrierBookingRequestReference is required"

        # Verify Status Until Booking is Active with the carrier_booking_request_reference value
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=240  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3199_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3199 | Booking Status Update to Active",
            status_code=[200, 303],  # Active Booking Should be 200
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        # self.login.load_page()
        # self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().save_screenshot(description="CT-3199_BookingReserved")

    @test(test_case_id="CT-3200", test_description="[12979] Cannot used reserved booking number", skip=True)
    def test_cannot_used_reserved_booking_number(self, shared_data,user):
        path = "../../data/bookings/CT-3200_customer_can_not_assign_booking_previously_assigned.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        data["crowleyBookingNumber"] = shared_data["crowleyBookingReferenceNumber"]

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        # Send Post Request with the Booking Number Reserved
        response_post_booking = self.bookings.create_booking(json=data)
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_post_booking,
            filename_prefix="CT-3200_cannot_used_reserved_booking_number"
        )

        self.add_report(
            test_data="CT-3200 | Cannot used reserved booking number",
            status_code=202,
            response=response_post_booking
        )

        # Booking Request Reference
        booking_response = json.loads(response_post_booking.text)

        shared_data["electronicCustomerReference"] = booking_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = booking_response['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        # Validate Field Data is Present
        assert shared_data["electronicCustomerReference"], "carrierBookingRequestReference is required"

        # Verify Status Until Booking is Active with the carrier_booking_request_reference value
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=240  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        self.pause(3)

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3200_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3200 | Booking Status Update to Active",
            status_code=[200, 303],  # Active Booking Should be 200
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"
        assert data_response["crowleyBookingReferenceNumber"]!=shared_data["crowleyBookingReferenceNumber"], "Booking Number should be different"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().save_screenshot(description="CT-3200_BookingActive")

    @test(test_case_id="CT-3240", test_description="[12979] Reserve a Booking Number with Invalid CVIF Code", skip=True)
    def test_reserved_booking_number_with_invalid_cvif(self, shared_data, user):
        # Extract Data Account Number from Request
        path = "../../data/bookings/CT-3240_reserved_booking_number_with_invalid_cvif_code.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Post the Account Number to get the Booking Number Reserved
        response_new_status = self.bookings.get_reserved_booking_number(json=data)

        # Validate Status Code
        self.add_report(
            test_data="CT-3240 | Customer cannot reserved a booking number with invalid CVIF Code",
            status_code=400,
            response=response_new_status
        )

        # Generate Files: Request and Response
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3240_customer_cannot_reserved_a_booking_number_with_invalid_cvif_code"
        )

        # Extract Data From Response: Booking Number
        data_response = JSONReader.text_to_dict(response_new_status.text)

        assert data_response["errorCode"] == 400, "Incorrect error code."
        assert data_response["customCode"] == "CROW-072", "Incorrect custom code."
        assert data_response["message"] == " Booking number can't be reserved as the shipper CVIF is not a valid CVIF, please try with a valid shipper CVIF", "Incorrect Message."




