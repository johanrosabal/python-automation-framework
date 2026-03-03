import json
import re

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
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12799(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3210", test_description="[12799] Create a Booking Number above Over 250K Insured amount", skip=False)
    def test_create_a_booking_above_250k_with_insured_amount(self, shared_data, user):
        path = "../../data/bookings/CT-3210_create_booking_above_250k_insured_amount.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3210_create_booking_above_250k"
        )

        self.add_report(
            test_data="CT-3210 | Create a Booking Number above Over 250K Insured amount",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$",shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3210_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3210 | Booking Status Update to Active",
            status_code=[303, 202, 200],
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Active", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3210_Booking_Active")
        csight_status = self.bookings_details.get_booking_status()

        assert (csight_status == "Active"), "Status Booking Incorrect"

        self.bookings_details\
            .click_tab_optional_services()\
            .screenshot()\
            .save_screenshot(description="CT-3210_optional_services_tab")

        csight_cargo_marine = self.bookings_details.tab_content_optional_services_details.get_cargo_marine()
        assert (csight_cargo_marine == "Over $250k Cargo Value (custom quote)")

    @test(test_case_id="CT-3242", test_description="[12799] Create a booking over 250K Marine Cargo Insurance with Rates Available", skip=False)
    def test_create_a_booking_over_250k_marine_cargo_insurance_with_rates_available(self, shared_data, user):
        path = "../../data/bookings/CT-3242_create_booking_above_250k_without_insurance_fields.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3242_create_a_booking_over_250k_marine_cargo_insurance_with_rates_available"
        )

        self.add_report(
            test_data="CT-3242 | Create a booking over 250K Marine Cargo Insurance with Rates Available",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3242_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3242 | Booking Status Update to Active",
            status_code=[303, 202, 200],
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3242_Booking_Pending")
        csight_status = self.bookings_details.get_booking_status()

        assert (csight_status == "Pending"), "Status Booking Incorrect"

        self.bookings_details \
            .click_tab_optional_services() \
            .screenshot() \
            .save_screenshot(description="CT-3242_optional_services_tab")

        csight_cargo_marine = self.bookings_details.tab_content_optional_services_details.get_cargo_marine()
        assert (csight_cargo_marine == "Over $250k Cargo Value (custom quote)")

    # Checkout 3243
    @test(test_case_id="CT-3243", test_description="[12799] Create a booking with the Insurance Amount and Pricing Amount without Rates Available", skip=False)
    def test_create_a_booking_with_the_insurance_amount_and_pricing_amount_without_rates_available(self, shared_data, user):
        path = "../../data/bookings/CT-3242_create_booking_above_250k_without_insurance_fields.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3243_create_a_booking_with_the_insurance_amount_and_pricing_amount_without_rates_available"
        )

        self.add_report(
            test_data="CT-3243 | Create a booking with the Insurance Amount and Pricing Amount without Rates Available",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3243_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3243 | Booking Status Update to Active",
            status_code=[303, 202, 200],
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3243_Booking_Pending")
        csight_status = self.bookings_details.get_booking_status()

        assert (csight_status == "Pending"), "Status Booking Incorrect"

        self.bookings_details \
            .click_tab_optional_services() \
            .screenshot() \
            .save_screenshot(description="CT-3243_optional_services_tab")

        csight_cargo_marine = self.bookings_details.tab_content_optional_services_details.get_cargo_marine()
        assert (csight_cargo_marine == "Over $250k Cargo Value (custom quote)")

    # Checkout 3244
    @test(test_case_id="CT-3244", test_description="[12799] Create a booking with the Insurance Amount and Without Pricing Amount with Rates", skip=False)
    def test_create_a_booking_with_the_insurance_amount_and_pricing_amount_without_pricing_with_rates_available(self, shared_data, user):
        path = "../../data/bookings/CT-3242_create_booking_above_250k_without_insurance_fields.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3244_create_a_booking_with_the_insurance_amount_and_pricing_amount_without_pricing_with_rates_available"
        )

        self.add_report(
            test_data="CT-3244 | Create a booking with the Insurance Amount and Without Pricing Amount with Rates",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$",shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3244_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-3244 | Booking Status Update to Active",
            status_code=[303, 202, 200],
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3243_Booking_Pending")
        csight_status = self.bookings_details.get_booking_status()

        assert (csight_status == "Pending"), "Status Booking Incorrect"

        self.bookings_details \
            .click_tab_optional_services() \
            .screenshot() \
            .save_screenshot(description="CT-3244_optional_services_tab")

        csight_cargo_marine = self.bookings_details.tab_content_optional_services_details.get_cargo_marine()
        assert (csight_cargo_marine == "Over $250k Cargo Value (custom quote)")

    @test(test_case_id="CT-4835", test_description="[12722] Create a Booking Number above Over 250K Without Insured amount and Missing Rates", skip=False)
    def test_create_a_booking_above_250k_without_insurance_fields_and_missing_rates(self, shared_data, user):
        path = "../../data/bookings/CT-3242_create_booking_above_250k_with_insurance_fields_and_rates_not_available.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-4835_create_a_booking_above_250k_without_insurance_fields_and_missing_rates"
        )

        self.add_report(
            test_data="CT-4835 | Create a Booking Number above Over 250K Without Insured amount and Missing Rates",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        #
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        # Validate Response data format
        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300,  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-4835_booking_status_update_to_active"
        )

        self.add_report(
            test_data="CT-4835 | Booking Status Update to Active",
            status_code=[303, 202, 200],
            response=response_status
        )

        # Validations
        data_response = JSONReader.text_to_dict(response_status.text)
        assert data_response["carrierBookingRequestReference"].startswith("CR"), "Invalid format in 'carrierBookingRequestReference'"
        assert data_response["crowleyBookingReferenceNumber"].startswith("CAT"), "Invalid format in 'crowleyBookingReferenceNumber'"
        assert data_response["status"] == "Pending", f"Unexpected status: {response_status['status']}"

        # UI Verification
        self.search_menu.search_booking(data_response["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3242_Booking_Active")
        csight_status = self.bookings_details.get_booking_status()

        assert (csight_status == "Pending"), "Status Booking Incorrect"

        self.bookings_details \
            .click_tab_optional_services() \
            .screenshot() \
            .save_screenshot(description="CT-4835_optional_services_tab")

        csight_cargo_marine = self.bookings_details.tab_content_optional_services_details.get_cargo_marine()
        assert (csight_cargo_marine == "Over $250k Cargo Value (custom quote)")

    @test(test_case_id="CT-4834", test_description="[12722] Create a Booking Number above Over 250K With Insured amount and Missing Rates", skip=False)
    def test_create_a_booking_above_250k_with_insurance_fields_and_missing_rates(self, shared_data):
        path = "../../data/bookings/CT-3209_create_booking_above_250k_without_insurance_fields_and_missing_rates.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-4834_create_a_booking_above_250k_with_insurance_fields_and_missing_rates"
        )

        self.add_report(
            test_data="CT-4834 | Create a Booking Number above Over 250K With Insured amount and Missing Rates",
            status_code=202,
            response=response_new_status
        )

        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        #
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']
