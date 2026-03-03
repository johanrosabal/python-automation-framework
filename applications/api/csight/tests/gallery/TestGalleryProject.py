import json
import re

import pytest
from core.utils.decorator import test
from core.utils import helpers
from core.utils.helpers import parse_dynamic_dates_values
from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from applications.web.csight.pages.home.HomePage import HomePage
from applications.api.csight.common.CsightBaseTest import CsightBaseTest, user
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from applications.api.csight.utils.csight_helper import extract_cvif_code

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12722(CsightBaseTest):

    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\gallery"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    def precondition_load_c_sight(self, user):
        self.login.load_page()
        self.login.login_user(user=user)

    @test(test_case_id="CT-3198", test_description="[12979] Reserve a Booking Number", skip=False)
    def test_reserved_booking_number(self, shared_data, user):
        # Extract Data Account Number from Request
        path = "../../data/bookings/CT-3198_reserved_booking_number_gallery.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

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
            filename_prefix="CT-3198_customer_can_reserved_a_booking_number"
        )

        # Extract Data From Response: Booking Number
        data_response = JSONReader.text_to_dict(response_new_status.text)
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        # Validate CAT Number Format
        assert re.match(r"^CAT\d{8}$", shared_data["crowleyBookingReferenceNumber"]), f"CAT NUMBER INVALID: {shared_data["crowleyBookingReferenceNumber"]}"

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        # UI Verification
        self.pause(5)
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        pending_reason_list = self.bookings_details.get_pending_reason()[0]
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3198_CustomerPreAssign")

        # Assert on UI
        assert (pending_reason_list == "Customer Pre-Assigned"), "Pending Reason Should be 'Customer Pre-Assigned'"

    @test(test_case_id="CT-3199", test_description="[12979] Customer can Reserved a Booking Number", skip=False)
    def test_assign_reserved_booking_number(self, shared_data, user):

        # Used the Reserved Booking Number
        path = "../../data/bookings/CT-3199_booking_number_with_reserve.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Insert Booking Number into Request
        data["crowleyBookingNumber"] = shared_data["crowleyBookingReferenceNumber"]

        # Send Post Request with the Booking Number Reserved
        response_post_booking = self.bookings.create_booking_page(json=data)
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

        self.pause(3)

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
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().save_screenshot(description="CT-3199_BookingReserved")

    @test(test_case_id="CT-3192", test_description="[12728] Create Container Booking Number", skip=False)
    def test_create_active_booking_container(self, shared_data, user):
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3178_booking_number_with_active_status_20_Chassis.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking_page(json=data)
        self.add_report(
            test_data="CT-3192 | Create Active Container Booking Number Port to Port",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-3192_create_active_container_booking_number_port_to_port"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(create_base_booking_number.text)

        # Read response fields
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"] ), "electronicCustomerReference with invalid format"
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
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3192_ActiveBookingContainer")

    @test(test_case_id="CT-31X1", test_description="[12559] Update Container Booking Number", skip=False)
    def test_update_active_booking_container(self, shared_data, user):
        path = "../../data/bookings/CT-3213_booking_number_with_active_status_40_Cube_Dry.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Extract Shipper CVIF
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        # Set up CusCont Number Reference
        data["electronicCustomerReference"] = shared_data["electronicCustomerReference"]

        # Update Post
        response_update_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            shipperCvif=shared_data["shipperCvif"]
        , json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-31X1_update_active_container_booking_number_port_to_port"
        )

        self.add_report(
            test_data="CT-31X1 | Update Active Container Booking Number Port to Port",
            status_code=202,
            response=response_update_status
        )

        # Booking Request Response
        booking_response = json.loads(response_update_status.text)

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", booking_response['electronicCustomerReference']), "electronicCustomerReference with invalid format"
        assert booking_response['crowleyBookingNumber'].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"

        # Validate Field Data is Present
        assert booking_response['electronicCustomerReference'], "carrierBookingRequestReference is required"
        assert booking_response['crowleyBookingNumber'], "carrierBookingRequestReference is required"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data["crowleyBookingNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-31X1_UpdatedBooking")

    @test(test_case_id="CT-31X2", test_description="[12559] Cancel Booking Number", skip=False)
    def test_cancel_active_booking_container(self, shared_data, user):

        # Sending Update Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            shipperCvif=shared_data["shipperCvif"]
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-31X2_booking_can_not_be_update_rework_complete"
        )

        self.add_report(
            test_data="CT-31X2 | Cancel Booking Number Port to Port",
            status_code=202,
            response=response_update_status
        )

        cancel_booking = json.loads(response_update_status.text)
        assert cancel_booking["crowleyBookingNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert cancel_booking["message"] == "Your request to cancel booking is received and is being processed"

        # Wait until Booking Change Status to Active
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Cancel",
            timeout=230
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-31X2_booking_cancel_status"
        )

        self.add_report(
            test_data="CT-31X2 | Booking Cancel Status",
            status_code=202,
            response=response_update_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Cancel", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-31X2_CancelBooking")

    @test(test_case_id="CT-31X3", test_description="[12728] Create Electric Vehicle New Booking Number", skip=False)
    def test_create_pending_booking_electric_new_vehicle(self, shared_data, user):
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3201_booking_number_with_vehicle_new_electric_dimensions_happy_lbs.json"
        # path = "../../data/bookings/CT-3104_booking_number_with_vehicle_used_electric_dimensions_happy_path_lbs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking_page(json=data)
        self.add_report(
            test_data="CT-31X3 | Create Active Vehicle New Electric Booking Number Port to Port",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-31X3_create_active_vehicle_new_electric_booking_number_port_to_port"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(create_base_booking_number.text)

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
            expected_status="Pending",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
            expected_pending_reason_codes=["CROW-044"]  # Vehicle Inspection Report Required
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-31X3_booking_status_update_to_pending"
        )

        self.add_report(
            test_data="CT-31X3 | Booking Status Update to Pending",
            status_code=200,
            response=response_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-31X3_PendingBookingVehicleNewElectric")
        self.bookings_details.click_pending_reason_approved(1)
        self.bookings_details.click_approved_pending_reason_yes()
        self.search_menu.screenshot().pause(1).save_screenshot(description="CT-31X3_PendingBookingVehicleNewElectricYesConfirmation")
        self.bookings_details.click_approved_confirmation_update()
        self.bookings_details.screenshot().pause(5).save_screenshot(description="CT-31X3_PendingBookingVehicleNewElectricStatus")

    @test(test_case_id="CT-31X5", test_description="[12728] Create Electric Vehicle Used Booking Number", skip=False)
    def test_create_pending_booking_electric_used_vehicle(self, shared_data, user):
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3104_booking_number_with_vehicle_used_electric_dimensions_happy_path_lbs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking_page(json=data)
        self.add_report(
            test_data="CT-31X5 | Create Active Vehicle Used Electric Booking Number Port to Port",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-31X5_create_active_vehicle_used_electric_booking_number_port_to_port"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(create_base_booking_number.text)

        # Read response fields
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"] ), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data["carrierBookingRequestReference"], "carrierBookingRequestReference is required"

        # Wait until Booking Change Status to Active
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
            expected_pending_reason_codes=["CROW-044"]  # Vehicle Inspection Report Required
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-31X5_booking_status_update_to_pending"
        )

        self.add_report(
            test_data="CT-31X5 | Booking Status Update to Pending",
            status_code=200,
            response=response_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-31X5_PendingBookingVehicleUsedElectric")
        self.bookings_details.click_pending_reason_approved(1)
        self.bookings_details.click_approved_pending_reason_yes()
        self.search_menu.screenshot().pause(1).save_screenshot(description="CT-31X5_PendingBookingVehicleUsedElectricYesConfirmation")
        self.bookings_details.click_approved_confirmation_update()
        self.bookings_details.screenshot().pause(5).save_screenshot(description="CT-31X5_PendingBookingVehicleUsedElectricStatus")

    @test(test_case_id="CT-31X4", test_description="[12728] Create Gasoline Vehicle New Booking Number", skip=False)
    def test_create_pending_booking_gasoline_new_vehicle(self, shared_data, user):
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3203_booking_number_with_vehicle_new_gasoline_dimensions_lbs.json"

        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking_page(json=data)
        self.add_report(
            test_data="CT-31X4 | Create Active Vehicle New Gasoline Booking Number Port to Port",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-31X4_create_active_vehicle_new_gasoline_booking_number_port_to_port"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(create_base_booking_number.text)

        # Read response fields
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"] ), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data["carrierBookingRequestReference"], "carrierBookingRequestReference is required"

        # Wait until Booking Change Status to Active
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-31X4_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-31X4 | Booking Status Update to Active",
            status_code=[200, 303],
            response=response_status
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
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-31X4_PendingBookingVehicleNewElectric")

    @test(test_case_id="CT-3245", test_description="[12724] Create Booking with SSN Encrypted at each party level", skip=False)
    def test_create_a_booking_with_ssn_encrypted_at_each_party_level(self, shared_data, user):
        path = "../../data/bookings/CT-3245_booking_ssn_encrypted_at_each_party_level_3.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking_page(json=data)

        self.add_report(
            test_data="CT-3245 | Create a Booking with SSN Encrypted",
            status_code=[200,202, 303],
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3245_create_a_booking_with_ssn_encrypted"
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
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3245_ActiveBookingSSNEncrypted")

    @test(test_case_id="CT-3191", test_description="[12728] User can not upload a document if booking number does not exist", skip=False)
    def test_user_can_not_upload_a_document_booking_not_exist(self, shared_data):

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3192_user_can_upload_a_docx_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = "CAT999999"

        response_new_status = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3191_user_can_not_upload_a_document_booking_not_exist"
        )

        self.add_report(
            test_data="CT-3191 | User can not upload a Docx Document if booking not exist",
            status_code=400,
            response=response_new_status
        )

        confirmation_status_2 = json.loads(response_new_status.text)
        assert (confirmation_status_2["OrderDataResponse"]["Result"] == "Fail", "Docx document was should not be uploaded")
        assert (confirmation_status_2["OrderDataResponse"]["ErrorCode"] == "400", "Error Code Should be 400")
        assert (confirmation_status_2["OrderDataResponse"]["ErrorMessage"] == "Booking CAT999999 not Available in CSIGHT", "Error Message not Match")

    @test(test_case_id="CT-3192", test_description="[12728] User can upload a Docx Document", skip=False)
    def test_user_can_upload_a_docx_document(self, shared_data):
        # # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        # path = "../../data/bookings/CT-3178_booking_number_with_active_status_20_Chassis.json"
        # data = JSONReader.import_json(path)
        # data = parse_dynamic_dates_values(data)
        #
        # # Get Response Booking Creation
        # create_base_booking_number = self.bookings.create_booking(json=data)
        #
        # # Share Carrier Booking Request Reference
        # new_booking = json.loads(create_base_booking_number.text)
        #
        # # Read response fields
        # shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']
        #
        # # Wait until Booking Change Status to Active
        # response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
        #     carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
        #     expected_status="Active",
        #     timeout=230
        # )
        #
        # # Validate Response Fields
        # data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = shared_data["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3192_user_can_upload_a_docx_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response_new_status = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3192_user_can_upload_a_docx_document"
        )

        self.add_report(
            test_data="CT-3192 | User can upload a Docx Document",
            status_code=200,
            response=response_new_status
        )

        confirmation_status_2 = json.loads(response_new_status.text)
        assert (confirmation_status_2["OrderDataResponse"]["Result"] == "Success", "Docx document was not uploaded")

    @test(test_case_id="CT-3193", test_description="[12728] User can upload a Doc Document", skip=False)
    def test_user_can_upload_a_doc_document(self, shared_data):

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3193_user_can_upload_a_doc_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response_new_status = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3193_user_can_upload_a_doc_document"
        )

        self.add_report(
            test_data="CT-3193 | User can upload a doc document",
            status_code=200,
            response=response_new_status
        )

        confirmation_status_2 = json.loads(response_new_status.text)
        assert (confirmation_status_2["OrderDataResponse"]["Result"] == "Success", "doc document was not uploaded")

    @test(test_case_id="CT-3194", test_description="[12728] User can upload a xls Document", skip=False)
    def test_user_can_upload_a_xls_document(self, shared_data):

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3194_user_can_upload_a_xls_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response_new_status = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3194_user_can_upload_a_xls_document"
        )

        self.add_report(
            test_data="CT-3194 | User can upload a xls document",
            status_code=200,
            response=response_new_status
        )

        confirmation_status_2 = json.loads(response_new_status.text)
        assert (confirmation_status_2["OrderDataResponse"]["Result"] == "Success", "xls document was not uploaded")

    @test(test_case_id="CT-3195", test_description="[12728] User can upload a xlsx Document", skip=False)
    def test_user_can_upload_a_xlsx_document(self, shared_data):

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3195_user_can_upload_a_xlsx_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response_new_status = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3195_user_can_upload_a_xlsx_document"
        )

        self.add_report(
            test_data="CT-3195 | User can upload a xlsx document",
            status_code=200,
            response=response_new_status
        )

        confirmation_status_2 = json.loads(response_new_status.text)
        assert (confirmation_status_2["OrderDataResponse"]["Result"] == "Success", "xlsx document was not uploaded")

    @test(test_case_id="CT-3196", test_description="[12728] User can upload a PDF Document", skip=False)
    def test_user_can_upload_a_pdf_document(self, shared_data):

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3196_user_can_upload_a_pdf_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response_new_status = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3196_user_can_upload_a_pdf_document"
        )

        self.add_report(
            test_data="CT-3196 | User can upload a PDF document",
            status_code=200,
            response=response_new_status
        )

        confirmation_status_2 = json.loads(response_new_status.text)
        assert (confirmation_status_2["OrderDataResponse"]["Result"] == "Success", "pdf document was not uploaded")






