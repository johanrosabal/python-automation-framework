import pytest
import json

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
class TestBookingsGallery12805(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3178", test_description="[12805] Create a Booking Container with 'New' Status and Changed to 'Active'", skip=False)
    def test_create_a_booking_container_new_status_changed_to_active(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3178
        path = "../../data/bookings/CT-3178_booking_container_port_to_port_new_to_active.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3178 | Create a Booking Container 'New' to 'Active' Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3178_active_booking_container_new_to_active"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=carrier_booking_request_reference,
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3178 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3178_get_booking_container_new_to_active"
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
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3178_booking_container_new_to_active")
        assert (c_sight_status == "Active"), "Booking Status Incorrect"

    @test(test_case_id="CT-3179", test_description="[12805] Create a Booking Container with 'Active' Status and Changed to 'Cancel'", skip=True)
    def test_create_a_booking_container_new_active_changed_to_cancel(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3179

        # Precondition Test Case CT-3178 have an Active Booking
        # Parameters:
        # crowleyBookingReferenceNumber: CATXXXXXX
        # carrierBookingRequestReference: CRXXXXXXXXXXXXXXXX
        # shipperCvif: 5780713

        self.bookings.cancel_booking_with_cat_number(
            crowleyBookingNumber=shared_data['crowleyBookingReferenceNumber'],
            carrierBookingRequestReference=shared_data['carrierBookingRequestReference'],
            shipperCvif=shared_data['shipperCvif']
        )

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data['carrierBookingRequestReference'],
            expected_status="Cancel",
            timeout=230
        )

        self.add_report(
            test_data="CT-3179 | Get Booking Container Status",
            status_code=[202, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3179_get_booking_container_active_changed_to_cancel"
        )

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data['crowleyBookingReferenceNumber'])
        c_sight_status = self.bookings_details.get_booking_status()
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3179_booking_container_active_to_cancel")
        assert (c_sight_status == "Cancel"), "Booking Status Incorrect"

    @test(test_case_id="CT-3180", test_description="[12805] Create a Booking Container with 'Active' Status and Changed to 'Pending'",skip=True)
    def test_create_a_booking_container_new_active_changed_to_pending(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3180

        # PRECONDITION: create a new booking on Active Status
        path = "../../data/bookings/CT-3178_booking_container_port_to_port_new_to_active.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3180 | Create a Booking Container 'New' to 'Active' Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3180_active_booking_container_new_to_active"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)

        shared_data["electronicCustomerReference"] = dict_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = dict_response["carrierBookingRequestReference"]

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3180 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3180_get_booking_container_new_to_active"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        path = "../../data/bookings/CT-3180_booking_container_port_to_port_update_pending.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        data["electronicCustomerReference"] = shared_data["electronicCustomerReference"]

        # Update Booking with other Location to Force Pending Reason to Rate Not Available
        # --------------------------------------------------------------------------------------------------------------
        # Update Post
        response_update_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            shipperCvif=shared_data["shipperCvif"], json=data
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-3180_booking_update_status"
        )

        self.add_report(
            test_data="CT-3180 | Booking Update Status",
            status_code=202,
            response=response_update_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_update_status.text)

        # Extract Data From Response: Booking Number
        shared_data["electronicCustomerReference"] = data_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingNumber"] = data_response["crowleyBookingNumber"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingNumber"]}")

        assert shared_data["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert shared_data["crowleyBookingNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"

        # Validate New Status
        response_pending_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-006'],
            timeout=230
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_pending_status,
            filename_prefix="CT-3180_booking_pending_status"
        )

        self.add_report(
            test_data="CT-3180 | Booking Pending Status",
            status_code=[202, 200],
            response=response_pending_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_pending_status.text)
        # Extract Data From Response: Booking Number
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith(
            "CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith(
            "CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        c_sight_status = self.bookings_details.get_booking_status()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3180_Booking_Update_Status")
        assert (c_sight_status == "Pending"), "Booking Status Incorrect"

    @test(test_case_id="CT-3181", test_description="[12805] Create a Booking Vehicle with 'New' Status and Changed to 'Active'", skip=True)
    def test_create_a_booking_vehicle_new_status_changed_to_active(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3181

        path = "../../data/bookings/CT-3181_booking_vehicle_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3181 | Create a Booking Vehicle 'New' to 'Active' Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3181_active_booking_vehicle_new_to_active"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=carrier_booking_request_reference,
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3181 | Get Booking Vehicle Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3181_get_booking_vehicle_new_to_active"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        crowley_booking_reference_number = dict_status["crowleyBookingReferenceNumber"]

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith(
            "CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith(
            "CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        assert (c_sight_status == "Active"), "Booking Status Incorrect"

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3181_booking_vehicle_new_to_active"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3181_booking_cargo_details"
        )

    @test(test_case_id="CT-3182", test_description="[12805] Create a Booking Vehicle with 'Active' Status and Changed to 'Pending'", skip=True)
    def test_create_a_booking_vehicle_active_status_changed_to_pending(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3182

        path = "../../data/bookings/CT-3181_booking_vehicle_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Use this fields for Update Booking
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3182 | Create a Booking Vehicle 'Active' to 'Pending' Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3182_active_booking_vehicle_active_to_pending"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=carrier_booking_request_reference,
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3182 | Get Booking Vehicle Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3182_get_booking_vehicle_new_to_active"
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
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        assert (c_sight_status == "Active"), "Booking Status Incorrect"

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3182_booking_vehicle_active"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3182_booking_cargo_details"
        )

        self.bookings_details.scroll().to_top()
        # Send an Update Location to Convert Active Booking to Pending
        path = "../../data/bookings/CT-3182_booking_vehicle_port_to_port_update.json"
        update_data = JSONReader.import_json(path)
        update_data = parse_dynamic_dates_values(update_data)
        update_data["electronicCustomerReference"] = shared_data["electronicCustomerReference"]

        response_update_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            shipperCvif=shared_data["shipperCvif"], json=update_data
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-3182_booking_update_status_pending"
        )

        self.add_report(
            test_data="CT-3182 | Booking Update Status Pending",
            status_code=202,
            response=response_update_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_update_status.text)

        # Extract Data From Response: Booking Number
        shared_data["electronicCustomerReference"] = data_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingNumber"] = data_response["crowleyBookingNumber"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingNumber"]}")

        assert shared_data["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert shared_data["crowleyBookingNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"

        # Validate New Status
        response_pending_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-057'],
            timeout=230
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_pending_status,
            filename_prefix="CT-3182_booking_pending_status"
        )

        self.add_report(
            test_data="CT-3182 | Booking Pending Status",
            status_code=[202, 200],
            response=response_pending_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_pending_status.text)
        # Extract Data From Response: Booking Number
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        c_sight_status = self.bookings_details.get_booking_status()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3182_booking_vehicle_pending"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3182_booking_cargo_details_pending"
        )

        self.bookings_details.scroll().to_top()
        assert (c_sight_status == "Pending"), "Booking Status Incorrect"

    @test(test_case_id="CT-3183",test_description="[12805] Create a Booking Vehicle with 'Active' Status and Changed to 'Cancel'", skip=True)
    def test_create_a_booking_vehicle_new_active_changed_to_cancel(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3183

        # Precondition Test Case CT-3181 have an Vehicle Booking
        # Parameters:
        # crowleyBookingReferenceNumber: CATXXXXXX
        # carrierBookingRequestReference: CRXXXXXXXXXXXXXXXX
        # shipperCvif: 5780713

        self.bookings.cancel_booking_with_cat_number(
            crowleyBookingNumber=shared_data['crowleyBookingReferenceNumber'],
            carrierBookingRequestReference=shared_data['carrierBookingRequestReference'],
            shipperCvif=shared_data['shipperCvif']
        )

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data['carrierBookingRequestReference'],
            expected_status="Cancel",
            timeout=230
        )

        self.add_report(
            test_data="CT-3183 | Get Booking Vehicle Status",
            status_code=[200, 202, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3183_get_booking_vehicle_active_changed_to_cancel"
        )

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data['crowleyBookingReferenceNumber'])
        c_sight_status = self.bookings_details.get_booking_status()
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3183_booking_vehicle_active_to_cancel")
        assert (c_sight_status == "Cancel"), "Booking Status Incorrect"

    @test(test_case_id="CT-3184", test_description="[12805] Create a Booking Break Bulk with 'New' Status and Changed to 'Active'", skip=True)
    def test_create_a_booking_breakbulk_new_status_changed_to_active(self):
        # https://crowley.atlassian.net/browse/CT-3184

        path = "../../data/bookings/CT-3184_booking_breakbulk_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3184 | Create a Booking Break Bulk with 'New' Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3184_active_booking_breakbulk_port_to_port"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.get_booking_status_with_carrier_request_reference(carrier_booking_request_reference)
        self.pause(5)
        self.add_report(
            test_data="CT-3184 | Get Booking Break Bulk Status",
            status_code=200,
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3184_get_booking_breakbulk_status"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        crowley_booking_reference_number = dict_status["crowleyBookingReferenceNumber"]

        # 03. Getting Initial Status 'New' on Booking Record
        response_new_status = self.bookings.get_booking_status_confirm_with_cat_number(
            cat_number=crowley_booking_reference_number)
        self.add_report(
            test_data="CT-3184 | Get Booking Break Bulk Status New",
            status_code=200,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3184_get_booking_breakbulk_status_new"
        )

        # 03. Checking Confirm endpoint with CAT Number
        # --------------------------------------------------------------------------------------------------------------
        # Wait for booking change status from 'New' to 'Active'
        response_confirm = self.bookings.wait_for_status_change_with_carrier_booking_request(
            cat_number=crowley_booking_reference_number,
            timeout=240,
            expected_status="Pending"
        )

        self.add_report(
            test_data="CT-3184 | Get Booking Break Bulk Confirm Status Active",
            status_code=200,
            response=response_confirm
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_confirm,
            filename_prefix="CT-3184_get_booking_breakbulk_confirm_status_active"
        )

        dict_confirm_status = JSONReader.text_to_dict(response_confirm.text)
        confirm_status = dict_confirm_status["status"]
        logger.info(f"Booking Break Bulk  Change......: {confirm_status}")

    @test(test_case_id="CT-3185", test_description="[12805] Create a Booking Break Bulk with 'Active' Status and Changed to 'Pending'", skip=True)
    def test_create_a_booking_break_bulk_active_status_changed_to_pending(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3185

        path = "../../data/bookings/CT-3184_booking_breakbulk_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Use this fields for Update Booking
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["electronicCustomerReference"] = data["electronicCustomerReference"]

        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        self.add_report(
            test_data="CT-3185 | Create a Booking Break Bulk 'Active' to 'Pending' Status",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3185_active_booking_break_bulk_active_to_pending"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        # electronic_customer_reference = dict_response["electronicCustomerReference"]
        carrier_booking_request_reference = dict_response["carrierBookingRequestReference"]

        # 04. Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=carrier_booking_request_reference,
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3185 | Get Booking Break Bulk Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3185_get_booking_break_bulk_new_to_active"
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
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        assert (c_sight_status == "Active"), "Booking Status Incorrect"

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3185_booking_break_bulk_active"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3185_booking_cargo_details"
        )

        self.bookings_details.scroll().to_top()
        # Send an Update Location to Convert Active Booking to Pending
        path = "../../data/bookings/CT-3185_booking_breakbulk_port_to_port_update.json"
        update_data = JSONReader.import_json(path)
        update_data = parse_dynamic_dates_values(update_data)
        update_data["electronicCustomerReference"] = shared_data["electronicCustomerReference"]

        response_update_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            shipperCvif=shared_data["shipperCvif"], json=update_data
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-3185_booking_update_status_pending"
        )

        self.add_report(
            test_data="CT-3185 | Booking Update Status Pending",
            status_code=202,
            response=response_update_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_update_status.text)

        # Extract Data From Response: Booking Number
        shared_data["electronicCustomerReference"] = data_response["electronicCustomerReference"]
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingNumber"] = data_response["crowleyBookingNumber"]

        logger.info(F"Booking Number: {shared_data["crowleyBookingNumber"]}")

        assert shared_data["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert shared_data["crowleyBookingNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"

        # Validate New Status
        response_pending_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-057'],
            timeout=230
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_pending_status,
            filename_prefix="CT-3185_booking_pending_status"
        )

        self.add_report(
            test_data="CT-3185 | Booking Pending Status",
            status_code=[202, 200],
            response=response_pending_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_pending_status.text)
        # Extract Data From Response: Booking Number
        shared_data["carrierBookingRequestReference"] = data_response["carrierBookingRequestReference"]
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        c_sight_status = self.bookings_details.get_booking_status()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3185_booking_vehicle_pending"
        )

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.get_cargo_details().click_commodity_accordion()

        self.bookings_details.screenshot().pause(3).save_screenshot(
            description="CT-3185_booking_cargo_details_pending"
        )

        self.bookings_details.scroll().to_top()
        assert (c_sight_status == "Pending"), "Booking Status Incorrect"

    @test(test_case_id="CT-3186", test_description="[12805] Create a Booking Break Bulk with 'Active' Status and Changed to 'Cancel'", skip=True)
    def test_create_a_booking_break_bulk_active_changed_to_cancel(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3186

        # Precondition Test Case CT-3184 have a Break Bulk Booking
        # Parameters:
        # crowleyBookingReferenceNumber: CATXXXXXX
        # carrierBookingRequestReference: CRXXXXXXXXXXXXXXXX
        # shipperCvif: 5780713

        self.bookings.cancel_booking_with_cat_number(
            crowleyBookingNumber=shared_data['crowleyBookingReferenceNumber'],
            carrierBookingRequestReference=shared_data['carrierBookingRequestReference'],
            shipperCvif=shared_data['shipperCvif']
        )

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data['carrierBookingRequestReference'],
            expected_status="Cancel",
            timeout=230
        )

        self.add_report(
            test_data="CT-3186 | Get Booking Vehicle Status",
            status_code=[202, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3186_get_booking_vehicle_active_changed_to_cancel"
        )

        # UI Verification
        self.login.load_page()
        self.login.login_user(user=user)
        self.search_menu.search_booking(shared_data['crowleyBookingReferenceNumber'])
        c_sight_status = self.bookings_details.get_booking_status()
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3186_booking_vehicle_active_to_cancel")
        assert (c_sight_status == "Cancel"), "Booking Status Incorrect"
