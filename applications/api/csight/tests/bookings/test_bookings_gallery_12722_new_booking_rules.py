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
class TestBookingsGallery12722(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3201", test_description="[12722] Create a Booking Number with New Electric Vehicle Dimensions in LBS", skip=False)
    def test_create_a_booking_new_electric_vehicle_dimensions_limit_within_validation_lbs(self, shared_data, user):
        # For New always used 0 on Dimensions

        # Extract Data Account Number from Request
        path = "../../data/bookings/CT-3201_booking_number_with_vehicle_new_electric_dimensions_happy_lbs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        # Validate Status Code
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3201_create_booking_vehicle_dimensions_libs"
        )

        # Generate Files: Request and Response
        self.add_report(
            test_data="CT-3201 | Create a Booking with Vehicle Dimensions LBS",
            status_code=202,
            response=response_new_status
        )

        # Extract Data From Response: Booking Number
        data_response = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = data_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = data_response['carrierBookingRequestReference']

        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data.get("carrierBookingRequestReference"), "carrierBookingRequestReference is required"

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-044'],  # CROW-037 - Haz Secondary Approval Required | CROW-044 - Vehicle Inspection Report Required
            timeout=230
        )

        self.add_report(
            test_data="CT-3202 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3202_get_booking_container_new_to_active"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.search_menu.is_not_visible_spinner()

        c_sight_status = self.bookings_details.get_booking_status()
        c_sight_pending_reasons = self.bookings_details.get_pending_reason()[0]

        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3201_Booking_Update_Status")

        assert (c_sight_status == "Pending"), "Booking Status Incorrect"
        assert (c_sight_pending_reasons == "Vehicle Inspection Report RequiredApprove"), "Booking Pending Reason Incorrect"

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.tab_content_cargo_details.click_commodity_accordion()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3201_Booking_Cargo_Details")

    @test(test_case_id="CT-3202", test_description="[12722] Create a Booking Number with Used Electric Vehicle Dimensions in LBS", skip=False)
    def test_create_a_booking_used_electric_vehicle_dimensions_limit_within_validation_lbs(self, shared_data, user):
        # For New always used 0 on Dimensions

        # Extract Data Account Number from Request
        path = "../../data/bookings/CT-3202_booking_number_with_vehicle_used_electric_dimensions_happy_path_lbs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        # Validate Status Code
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3202_create_booking_used_electric_vehicle_dimensions_libs"
        )

        # Generate Files: Request and Response
        self.add_report(
            test_data="CT-3202 | Create a Booking Used Electric Vehicle Dimensions LBS",
            status_code=202,
            response=response_new_status
        )

        # Extract Data From Response: Booking Number
        data_response = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = data_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = data_response['carrierBookingRequestReference']

        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data.get("carrierBookingRequestReference"), "carrierBookingRequestReference is required"

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Pending",
            expected_pending_reason_codes=['CROW-044'],  # CROW-037 - Haz Secondary Approval Required | CROW-044 - Vehicle Inspection Report Required
            timeout=230
        )

        self.add_report(
            test_data="CT-3202 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3202_get_booking_container_new_to_active"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])

        c_sight_status = self.bookings_details.get_booking_status()
        c_sight_pending_reasons = self.bookings_details.get_pending_reason()[0]

        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3202_Booking_Update_Status")

        assert (c_sight_status == "Pending"), "Booking Status Incorrect"
        assert (c_sight_pending_reasons == "Vehicle Inspection Report RequiredApprove"), "Booking Pending Reason Incorrect"

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.tab_content_cargo_details.click_commodity_accordion()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3202_Booking_Cargo_Details")

    @test(test_case_id="CT-3203", test_description="[12722] Create a Booking Number with New Gasoline Vehicle Dimensions in LBS", skip=False)
    def test_create_a_booking_new_gasoline_vehicle_dimensions_limit_within_validation_lbs(self, shared_data, user):
        # For New always used 0 on Dimensions

        # Extract Data Account Number from Request
        path = "../../data/bookings/CT-3203_booking_number_with_vehicle_new_gasoline_dimensions_lbs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        # Validate Status Code
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3201_create_booking_new_gasoline_vehicle_dimensions_libs"

        )

        # Generate Files: Request and Response
        self.add_report(
            test_data="CT-3203 | Create a Booking New Gasoline Vehicle Dimensions LBS",
            status_code=202,
            response=response_new_status
        )

        # Extract Data From Response: Booking Number
        data_response = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = data_response['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = data_response['carrierBookingRequestReference']

        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,17}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data.get("carrierBookingRequestReference"), "carrierBookingRequestReference is required"

        # Check Status to get CAT Number in response
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=230
        )

        self.add_report(
            test_data="CT-3203 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3203_get_booking_container_new_to_active"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])

        c_sight_status = self.bookings_details.get_booking_status()

        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3203_Booking_Update_Status")

        assert (c_sight_status == "Active"), "Booking Status Incorrect"

        self.bookings_details.click_tab_cargo_details()
        self.bookings_details.tab_content_cargo_details.click_commodity_accordion()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3203_Booking_Cargo_Details")

    @test(test_case_id="CT-3104", test_description="[12722] Create a Booking Number with Used Gasoline Vehicle Dimensions in LBS", skip=False)
    def test_create_a_booking_used_gasoline_vehicle_dimensions_limit_within_validation_lbs(self, shared_data, user):
        path = "../../data/bookings/CT-3104_booking_number_with_vehicle_dimensions_happy_path_kgs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)
        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3104_create_booking_vehicle_dimensions_happy_path_kgs"
        )

        self.add_report(
            test_data="CT-3104 | Create a Booking with Vehicle Dimensions Happy Path KGS",
            status_code=202,
            response=response_new_status
        )

        # NOTE: lIMIT 6802.72 -> 14997.43 lb (2.57 libs Of Difference to reach the limit with KGS Convertion)

        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert shared_data.get("carrierBookingRequestReference"), "carrierBookingRequestReference is required"

    @test(test_case_id="CT-3105", test_description="[12722] Create a Booking Number with Used Electric Vehicle Dimensions over the limit validation Width", skip=False)
    def test_create_a_booking_used_electric_vehicle_dimensions_over_limit_validation_width(self):
        path = "../../data/bookings/CT-3105_booking_number_with_vehicle_dimensions_over_limit_width.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3105_create_booking_with_vehicle_over_dimensions_width"
        )

        self.add_report(
            test_data="CT-3105 | Create a Booking with Vehicle Over Dimensions width",
            status_code=400,
            response=response_new_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # # 'cargos/notInContainerDetails/width' is more than 7.4 where cargos/notInContainerDetails/widthUom = FT
        assert (message == "The given dimensions are not acceptable for a vehicle booking, please change the cargoType as BREAKBULK and re-try the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"

    @test(test_case_id="CT-3106", test_description="[12722] Create a Booking Number with Used Electric Vehicle Dimensions over the limit validation Length", skip=False)
    def test_create_a_booking_used_electric_vehicle_dimensions_over_limit_validation_length(self):
        path = "../../data/bookings/CT-3106_booking_number_with_vehicle_dimensions_over_limit_length.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3106_create_booking_with_vehicle_over_dimensions_length"
        )

        self.add_report(
            test_data="CT-3106 | Create a Booking with Vehicle Over Dimensions length",
            status_code=400,
            response=response_new_status,
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # PASS
        # 'cargos/notInContainerDetails/length' is more than 38 where cargos/notInContainerDetails/lengthUom = FT or
        assert (message == "The given dimensions are not acceptable for a vehicle booking, please change the cargoType as BREAKBULK and re-try the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"

    @test(test_case_id="CT-3107", test_description="[12722] Create a Booking Number with Used Electric Vehicle Dimensions over the limit validation Height", skip=False)
    def test_create_a_booking_used_electric_vehicle_dimensions_over_limit_validation_height(self):
        path = "../../data/bookings/CT-3107_booking_number_with_vehicle_dimensions_over_limit_height.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3107_create_booking_with_vehicle_over_dimensions_height"
        )

        self.add_report(
            test_data="CT-3107 | Create a Booking with Vehicle Over Dimensions Height",
            status_code=400,
            response=response_new_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # PASS
        # 'cargos/notInContainerDetails/height' is more than 6.10 where 'cargos/notInContainerDetails/heightUom' = FT or
        assert (message == "The given dimensions are not acceptable for a vehicle booking, please change the cargoType as BREAKBULK and re-try the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"

    @test(test_case_id="CT-3208", test_description="[12722] Validate Booking Number cannot accept more than one Hazmat per Container Equal Containers", skip=False)
    def test_create_a_booking_cannot_accept_more_than_one_hazmat_equal_containers(self, shared_data):
        path = "../../data/bookings/CT-3208_booking_number_cannot_accept_more_than_one_hazmat_per_container_equal_containers.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3208_create_booking_number_cannot_accept_more_than_one_hazmat_per_container"
        )

        self.add_report(
            test_data="CT-3208 | Validate Booking Number cannot accept more than one Hazmat per Container",
            status_code=400,
            response=response_new_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        assert (message == "Only 1 hazardous container is allowed, please make necessary changes and resubmit the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"

    @test(test_case_id="CT-3209", test_description="[12722] Create a Booking Number with Used Electric Vehicle Dimensions over the limit validation Volume", skip=False)
    def test_create_a_booking_used_electric_vehicle_dimensions_over_limit_validation_volume(self):
        path = "../../data/bookings/CT-3209_booking_number_with_vehicle_dimensions_over_limit_volume.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3107_create_booking_with_vehicle_over_dimensions_height"
        )

        self.add_report(
            test_data="CT-3107 | Create a Booking with Vehicle Over Dimensions Height",
            status_code=400,
            response=response_new_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # PASS
        # 'cargos/notInContainerDetails/height' is more than 6.10 where 'cargos/notInContainerDetails/heightUom' = FT or
        assert (message == "The given dimensions are not acceptable for a vehicle booking, please change the cargoType as BREAKBULK and re-try the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"

    @test(test_case_id="CT-3211", test_description="[12722] Validate a Booking Number cannot accept more than one Cargo Type", skip=False)
    def test_validate_a_booking_number_cannot_accept_more_than_one_cargo_type(self, shared_data):
        path = "../../data/bookings/CT-3211_booking_number_single_cargo_type_1.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3211_validate_a_booking_number_cannot_accept_more_than_one_cargo_type"
        )

        self.add_report(
            test_data="CT-3211 | Validate a Booking Number cannot accept more than one Cargo Type",
            status_code=400,
            response=response_new_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # Customer will be sending only a single cargo type in the booking request.
        # If the booking request contains multiple cargo types, then MuleSoft should send the synchronous error response to the customer.
        assert (message == "The Booking contains multiple cargo type , The given dimensions are not acceptable for a vehicle booking, please change the cargoType as BREAKBULK and re-try the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"

    @test(test_case_id="CT-3212", test_description="[12722] Validate Booking Number cannot accept more than one Hazmat per Container Different Containers", skip=False)
    def test_create_a_booking_cannot_accept_more_than_one_hazmat_different_containers(self, shared_data):
        path = "../../data/bookings/CT-3212_booking_number_cannot_accept_more_than_one_hazmat_per_container_different_containers.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        new_booking = json.loads(response_new_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3212_create_booking_number_cannot_accept_more_than_one_hazmat_per_container_different_containers"
        )

        self.add_report(
            test_data="CT-3212 | Validate Booking Number cannot accept more than one Hazmat per Container Different Containers",
            status_code=400,
            response=response_new_status
        )

        # PASS
        # If cargos/cargoType is CONTAINER and isHazMatBooking = true and cargos/containerDetails/equipmentQuantity is more than 1,
        # then MuleSoft will not create the booking in C Sight. Instead, MuleSoft will send the synchronous error response to
        # the customer as 'Only 1 hazardous container is allowed, please make necessary changes and resubmit the request'

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        assert (message == "Only 1 hazardous container is allowed, please make necessary changes and resubmit the request"), "Error Message not Match"
        assert (errorCode == 400), "Error code should be 400"


