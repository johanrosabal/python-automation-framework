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
class TestBookingsGallery12800(CsightBaseTest):

    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\gallery"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3247", test_description="Create Gasoline Moto New Booking Number", skip=False)
    def test_create_booking_gasoline_new_moto(self, shared_data, user, record_property):
        record_property("test_key", "CT-3247")
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3247_booking_new_moto_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking(json=data)
        self.add_report(
            test_data="CT-3247 | Create a Booking Moto for New Commodity",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-3247_create_active_moto_new_gasoline_booking_number_port_to_port"
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
            filename_prefix="CT-3247_booking_new_moto_port_to_port.json"
        )

        self.add_report(
            test_data="CT-3247 | Create a New Moto Booking",
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
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(5).save_screenshot(description="CT-3247_Active_Booking_New_Motom")

        # Bookings Details
        status = self.bookings_details.get_booking_status()


        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.tab_content_cargo_details.click_commodity_accordion()
        commodity = self.bookings_details.tab_content_cargo_details.get_commodity_vehicle_details_rating_commodity_category()
        self.bookings_details.screenshot().save_screenshot(description="CT-3247 Commodity Details")


        assert (status == "Active"), "Booking Status Incorrect"
        assert (commodity == "Motorcycles - New"), "Commodity Type Incorrect"

    @test(test_case_id="CT-3248", test_description="Create Gasoline Moto Used Booking Number", skip=False)
    def test_create_booking_gasoline_used_moto(self, shared_data, user, record_property):
        record_property("test_key", "CT-3248")
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3248_booking_used_moto_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking(json=data)
        self.add_report(
            test_data="CT-3248 | Create a Booking Moto for Used Commodity",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-3248_create_active_moto_used_gasoline_booking_number_port_to_port"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(create_base_booking_number.text)

        # Read response fields
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",
                        shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data[
            "carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
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
            filename_prefix="CT-3248_booking_used_moto_port_to_port.json"
        )

        self.add_report(
            test_data="CT-3248 | Create a Used Moto Booking",
            status_code=[200, 303],
            response=response_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith(
            "CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith(
            "CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(5).save_screenshot(description="CT-3248_Active_Booking_Used_Moto")

        # Bookings Details
        status = self.bookings_details.get_booking_status()

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.tab_content_cargo_details.click_commodity_accordion()
        commodity = self.bookings_details.tab_content_cargo_details.get_commodity_vehicle_details_rating_commodity_category()
        self.bookings_details.screenshot().save_screenshot(description="CT-3248 Commodity Details")

        assert (status == "Active"), "Booking Status Incorrect"
        assert (commodity == "Motorcycles - Used"), "Commodity Type Incorrect"

    @test(test_case_id="CT-3249", test_description="Create Gasoline Moto Vintage Booking Number", skip=False)
    def test_create_booking_gasoline_vintage_moto(self, shared_data, user, record_property):
        record_property("test_key", "CT-3249")
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3249_booking_vintage_moto_port_to_port.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # Get Response Booking Creation
        create_base_booking_number = self.bookings.create_booking(json=data)
        self.add_report(
            test_data="CT-3249 | Create a Booking Moto for Vintage Commodity",
            status_code=202,
            response=create_base_booking_number
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=create_base_booking_number,
            filename_prefix="CT-3249_create_active_moto_vintage_gasoline_booking_number_port_to_port"
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(create_base_booking_number.text)

        # Read response fields
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",
                        shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data[
            "carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
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
            filename_prefix="CT-3249_booking_vintage_moto_port_to_port.json"
        )

        self.add_report(
            test_data="CT-3249 | Create a Vintage Moto Booking",
            status_code=[200, 303],
            response=response_status
        )

        # Validate Response Fields
        data_response = JSONReader.text_to_dict(response_status.text)

        # Extract Data From Response: Booking Number
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]
        logger.info(F"Booking Number: {shared_data["crowleyBookingReferenceNumber"]}")

        assert data_response["carrierBookingRequestReference"].startswith(
            "CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith(
            "CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(5).save_screenshot(description="CT-3249_Active_Booking_Vintage_Moto")

        # Bookings Details
        status = self.bookings_details.get_booking_status()

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.tab_content_cargo_details.click_commodity_accordion()
        commodity = self.bookings_details.tab_content_cargo_details.get_commodity_vehicle_details_rating_commodity_category()
        self.bookings_details.screenshot().save_screenshot(description="CT-3248 Commodity Details")

        assert (status == "Active"), "Booking Status Incorrect"
        assert (commodity == "Motorcycles - Vintage"), "Commodity Type Incorrect"