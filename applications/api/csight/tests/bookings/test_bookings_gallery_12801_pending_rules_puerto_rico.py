import json
import re
import pytest

from applications.web.csight.pages.bookings.CreateBookingPage import CreateBookingPage
from applications.web.csight.pages.login.EmployeePortalPage import EmployeePortalPage
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

logger = setup_logger('TestBookingsGallery12801')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12801(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()
    create_booking = CreateBookingPage.get_instance()
    employeePortalPage = EmployeePortalPage.get_instance()

    @test(test_case_id="CT-3239", test_description="[12801] Voyage Rules: Southbound -> Puerto Rico -> USJAX -> PRSJU", skip=False)
    def test_create_active_booking_southbound_USJAX_PRSJU(self, shared_data, user, record_property):
        record_property("test_key", "CT-3239")
        # S = Southbound (Load port is USA).
        # For API Southbound bookings (Load port is USA), from the given ready date, the last available voyage on the routes returned should be selected.
        # If no voyages are available within the given ready date, select the last available voyage within the next 30 days.

        # Import Data
        path = "../../data/bookings/3239_active_bookings_booking_south_bound_1.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3239_voyage_rules_southbound_usjax_prsju"
        )

        self.add_report(
            test_data="CT-3239 | Voyage Rules: Southbound -> Puerto Rico -> USJAX -> PRSJU",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        booking_response = json.loads(response_new_status.text)
        #
        shared_data["electronicCustomerReference"] = booking_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = booking_response['carrierBookingRequestReference']

        # PASS: VERIFY AGAINST MANUAL BOOKING

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        # Validate Field Data is Present
        assert shared_data["electronicCustomerReference"], "carrierBookingRequestReference is required"

        # Verify Status Until Booking is Active with the carrier_booking_request_reference value
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3239_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3239 | Booking Status Update to Active",
            status_code=[200, 303],  # Active Booking Should be 200
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.bookings_details.click_tab_routes_details()
        commercial_route = self.bookings_details.tab_content_routes_details.get_commercial_route()
        empty_pickup = commercial_route['empty_pick_up']['line_2']
        empty_return = commercial_route['empty_return']['line_1']

        # USJAX Validation
        assert ("JACKSONVILLE" in empty_pickup), "Empty Pick Up not Match"
        # PRSJU Validation
        assert ("SAN JUAN" in empty_return), "Empty Return not Match"
        # Screenshot for Routes Details
        self.bookings_details.screenshot().save_screenshot(description="CT_3239_route_details")

        # Review Routes Available For Current Booking
        self.bookings_details.click_update()

        #  EDIT MODE -> ORIGIN-DESTINATION -----------------------------------------------------------------------------
        # Edit Mode: Bill To Party -> Same as Booking Party
        self.create_booking.origin_destination.click_checkbox_bill_to_party_same_as_booking_party()
        # Edit Mode: Bill To Party -> Bill To Party Type
        self.create_booking.origin_destination.select_bill_to_party_bill_to_party_type("Shipper")
        # Next
        self.create_booking.click_next()
        self.create_booking.click_modal_ok()

        #  EDIT MODE -> CARGO DETAILS ----------------------------------------------------------------------------------
        # MARK RADIO BUTTONS
        self.create_booking.cargo_details\
            .select_radio_hazardous_booking(index=1, text="No")\
            .select_radio_waste(index=1, text="No")\
            .select_radio_RCRA(index=1, text="No")
        self.create_booking.click_next()

        self.create_booking.scroll().to_bottom()

        # EDIT MODE -> ROUTES ------------------------------------------------------------------------------------------
        # Select Last Information
        count = self.create_booking.routes.get_routes_count()
        item_last_information = self.create_booking.routes.get_route_item_information(index=count)

        item_value = self.create_booking.routes.get_select_route_item_information()
        self.create_booking.screenshot().save_screenshot(description="CT-3239_route_selected")

        self.create_booking.click_cancel_update()
        self.create_booking.click_confirm_cancellation()
        self.create_booking.click_close_modal()

        # Routes Last Item Validation
        assert (item_value is True), "Last Item should be selected"
        assert ("JACKSONVILLE PORT AUTHORITY" in item_last_information['Origin Terminal']), "Routes: Original Terminal not Match"
        assert ("ISLA GRAND TERMINAL (SJUT001)" in item_last_information['Destination Terminal']), "Routes: Destination Terminal not Match"
        assert (commercial_route['port_origin']['voyage'] == item_last_information['Voyage Number']), "Routes: Voyage Validation not Match"
        assert (commercial_route['port_origin']['vessel'] == item_last_information['Vessel Name']), "Routes: Vessel Name Validation not Match"

    @test(test_case_id="CT-3241", test_description="[12801] Voyage Rules: Southbound -> Puerto Rico -> PRSJU -> USJAX", skip=False)
    def test_create_active_booking_northbound_PRSJU_USJAX(self, shared_data, user, record_property):
        record_property("test_key", "CT-3241")
        # Northbound (Load port is not USA).
        # For northbound bookings originated from San Juan going to Jacksonville or if its moving from San Juan to USCHT, pick the first available voyage .

        # Import Data
        path = "../../data/bookings/3241_active_bookings_booking_north_bound_1.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3241_voyage_rules_southbound_prsju_usjax"
        )

        self.add_report(
            test_data="CT-3241 | Voyage Rules: Southbound -> Puerto Rico -> PRSJU -> USJAX",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        booking_response = json.loads(response_new_status.text)
        #
        shared_data["electronicCustomerReference"] = booking_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = booking_response['carrierBookingRequestReference']

        # PASS: VERIFY AGAINST MANUAL BOOKING

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        # Validate Field Data is Present
        assert shared_data["electronicCustomerReference"], "carrierBookingRequestReference is required"

        # Verify Status Until Booking is Active with the carrier_booking_request_reference value
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3241_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3241 | Booking Status Update to Active",
            status_code=[200, 303],  # Active Booking Should be 200
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.bookings_details.click_tab_routes_details()
        commercial_route = self.bookings_details.tab_content_routes_details.get_commercial_route()
        empty_pickup = commercial_route['empty_pick_up']['line_2']
        empty_return = commercial_route['empty_return']['line_1']

        # PRSJU Validation
        assert ("SAN JUAN" in empty_pickup), "Empty Empty not Match"

        # USJAX Validation
        assert ("JACKSONVILLE" in empty_return), "Empty Return Up not Match"

        # Screenshot for Routes Details
        self.bookings_details.screenshot().save_screenshot(description="CT_3241_route_details")

        # Review Routes Available For Current Booking
        self.bookings_details.click_update()

        #  EDIT MODE -> ORIGIN-DESTINATION -----------------------------------------------------------------------------
        # Edit Mode: Bill To Party -> Same as Booking Party
        self.create_booking.origin_destination.click_checkbox_bill_to_party_same_as_booking_party()
        # Edit Mode: Bill To Party -> Bill To Party Type
        self.create_booking.origin_destination.select_bill_to_party_bill_to_party_type("Shipper")
        # Select Radio Button : Cleared Customs at first US Port of Entry -> Yes
        self.create_booking.origin_destination.select_cleared_customs_at_first_us_port_entry(text="Yes")
        # Next
        self.create_booking.click_next()
        self.create_booking.click_modal_ok()

        #  EDIT MODE -> CARGO DETAILS ----------------------------------------------------------------------------------
        # MARK RADIO BUTTONS
        self.create_booking.cargo_details \
            .select_radio_hazardous_booking(index=1, text="No") \
            .select_radio_waste(index=1, text="No") \
            .select_radio_RCRA(index=1, text="No")
        self.create_booking.click_next()

        self.create_booking.scroll().to_bottom()

        # EDIT MODE -> ROUTES ------------------------------------------------------------------------------------------
        # Select Last Information: Select First Route
        item_first_information = self.create_booking.routes.get_route_item_information(index=1)

        item_value = self.create_booking.routes.get_select_route_item_information()
        self.create_booking.screenshot().save_screenshot(description="CT-3241_route_selected")

        self.create_booking.click_cancel_update()
        self.create_booking.click_confirm_cancellation()
        self.create_booking.click_close_modal()

        # Routes Last Item Validation
        assert (item_value is True), "Item Selected should be the first one"
        assert ("ISLA GRAND TERMINAL (SJUT001)" in item_first_information['Origin Terminal']), "Routes: Original Terminal not Match"
        assert ("JACKSONVILLE PORT AUTHORITY" in item_first_information['Destination Terminal']), "Routes: Destination Terminal not Match"
        assert (commercial_route['port_origin']['voyage'] == item_first_information['Voyage Number']), "Routes: Voyage Validation not Match"
        assert (commercial_route['port_origin']['vessel'] == item_first_information['Vessel Name']), "Routes: Vessel Name Validation not Match"

    @test(test_case_id="CT-3245", test_description="[12801] Voyage Rules: Northbound -> Puerto Rico PRSJU -> USCHT", skip=False)
    def test_create_active_booking_northbound_PRSJU_USCHT(self,shared_data, user, record_property):
        record_property("test_key", "CT-3245")
        # Northbound (Load port is not USA).
        # For northbound bookings originated from San Juan going to Jacksonville or if its moving from San Juan to USCHT, pick the first available voyage .

        # Import Data
        path = "../../data/bookings/3245_active_bookings_booking_north_bound_2.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # CSigh Login User
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3245_voyage_rules_southbound_prsju_uscht"
        )

        self.add_report(
            test_data="CT-3245 | Voyage Rules: Southbound -> Puerto Rico -> PRSJU -> USCHT",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        booking_response = json.loads(response_new_status.text)
        #
        shared_data["electronicCustomerReference"] = booking_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = booking_response['carrierBookingRequestReference']

        # PASS: VERIFY AGAINST MANUAL BOOKING

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        # Validate Field Data is Present
        assert shared_data["electronicCustomerReference"], "carrierBookingRequestReference is required"

        # Verify Status Until Booking is Active with the carrier_booking_request_reference value
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3245_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3245 | Booking Status Update to Active",
            status_code=[200, 303],  # Active Booking Should be 200
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = data_response["crowleyBookingReferenceNumber"]

        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.bookings_details.click_tab_routes_details()
        commercial_route = self.bookings_details.tab_content_routes_details.get_commercial_route()
        empty_pickup = commercial_route['empty_pick_up']['line_2']
        empty_return = commercial_route['empty_return']['line_2']

        # PRSJU Validation
        assert ("SAN JUAN" in empty_pickup), "Empty Empty not Match"

        # USJAX Validation
        assert ("EDDYSTONE" in empty_return), "Empty Return Up not Match"

        # Screenshot for Routes Details
        self.bookings_details.screenshot().save_screenshot(description="CT_3245_route_details")

        # Review Routes Available For Current Booking
        self.bookings_details.click_update()

        #  EDIT MODE -> ORIGIN-DESTINATION -----------------------------------------------------------------------------
        # Edit Mode: Bill To Party -> Same as Booking Party
        self.create_booking.origin_destination.click_checkbox_bill_to_party_same_as_booking_party()
        # Edit Mode: Bill To Party -> Bill To Party Type
        self.create_booking.origin_destination.select_bill_to_party_bill_to_party_type("Shipper")
        # Select Radio Button : Cleared Customs at first US Port of Entry -> Yes
        self.create_booking.origin_destination.select_cleared_customs_at_first_us_port_entry(text="Yes")
        # Next
        self.create_booking.click_next()
        self.create_booking.click_modal_ok()

        #  EDIT MODE -> CARGO DETAILS ----------------------------------------------------------------------------------
        # MARK RADIO BUTTONS
        self.create_booking.cargo_details \
            .select_radio_hazardous_booking(index=1, text="No") \
            .select_radio_waste(index=1, text="No") \
            .select_radio_RCRA(index=1, text="No")
        self.create_booking.click_next()

        self.create_booking.scroll().to_bottom()

        # EDIT MODE -> ROUTES ------------------------------------------------------------------------------------------
        # self.pause(2)

        # Select Last Information: Select First Route
        item_first_information = self.create_booking.routes.get_route_item_information(index=1)

        item_value = self.create_booking.routes.get_select_route_item_information()
        self.create_booking.screenshot().save_screenshot(description="CT-3245_route_selected")

        self.create_booking.click_cancel_update()
        self.create_booking.click_confirm_cancellation()
        self.create_booking.click_close_modal()

        # Routes Last Item Validation
        assert (item_value is True), "Item Selected should be the first one"
        assert ("ISLA GRAND TERMINAL (SJUT001)" in item_first_information['Origin Terminal']), "Routes: Original Terminal not Match"
        assert ("Eddystone / Chester, PA" in item_first_information['Destination City / State']), "Routes: Destination Terminal not Match"
        assert (commercial_route['port_origin']['voyage'] == item_first_information['Voyage Number']), "Routes: Voyage Validation not Match"
        assert (commercial_route['port_origin']['vessel'] == item_first_information['Vessel Name']), "Routes: Vessel Name Validation not Match"
