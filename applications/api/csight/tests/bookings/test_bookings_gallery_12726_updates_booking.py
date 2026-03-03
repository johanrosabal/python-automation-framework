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
from applications.api.csight.utils.csight_helper import extract_cvif_code
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from applications.web.csight.pages.home.HomePage import HomePage
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('TestBookingsGallery12726')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12726(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3236", test_description="[12726] Send Booking Update with incorrect booking number", skip=True)
    def test_send_booking_update_with_incorrect_booking_number(self, shared_data):
        crowley_booking_Number = "CAT999999"
        # Just as reference we take a Active Request to try to Send a Booking but the number is not valid
        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Set Booking Number
        data["crowleyBookingNumber"] = crowley_booking_Number

        # Shipper Account for Gallery
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        # Missing Booking Number
        # response_update_status = self.bookings.update_booking_with_carrier_request_reference("")
        response_update_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=crowley_booking_Number,
            carrierBookingRequestReference="CR9591846138571438",
            shipperCvif=shared_data["shipperCvif"],
            json=data
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-3236_send_booking_update_without_missing_booking_number"
        )

        self.add_report(
            test_data="CT-3236 | Send Booking Update with incorrect booking number",
            status_code=400,
            response=response_update_status
        )

        new_booking = json.loads(response_update_status.text)

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        assert (errorCode == 400), "Error code should be 400"
        assert (message == f"Booking not found, Please re-check the booking number sent and try-again. For additional help, please reach out to bookingrequests@crowley.com {crowley_booking_Number}"), "Error Message not Match"

    @test(test_case_id="CT-3237", test_description="[12726] Update Platform Booking should not created through API channel", skip=True)
    def test_update_platform_booking_not_allow_booking_not_created_through_api_channel(self, shared_data):
        # https://crowley2--uat.sandbox.lightning.force.com/lightning/r/Feedback__c/a14dh000004eIOvAAM/view
        # PRECONDITION: CREATE A MANUAL BOOKING ON C-SIGHT
        # TEST 1: CAT40000575
        # IMPORTANT NOTE: The carrierBookingRequestReference is not possible to get it when user creates a manual booking,
        # so, we can send empty that require argument and the expected validation

        # Put Here a Manual Booking Created then apply API update to see the validation
        crowley_booking_Number = "CAT40000575"

        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        data["agreementReference"] = ""
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API"
        # Set Booking Number
        data["crowleyBookingNumber"] = crowley_booking_Number
        # Shipper Account for Gallery
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        response_update_status = self.bookings.update_booking_with_cat_number(
            crowleyBookingNumber=crowley_booking_Number,
            carrierBookingRequestReference="",
            shipperCvif=shared_data["shipperCvif"],
            json=data
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-3237_update_platform_booking_not_allow_booking_not_created_through_api_channel"
        )

        self.add_report(
            test_data="CT-3237 | Update Platform Booking should not created through API channel",
            status_code=400,
            response=response_update_status
        )

        new_booking = json.loads(response_update_status.text)

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        assert (errorCode == 400), "Error code should be 400"
        assert (message == "CarrierBookingRequestReference is missing, please send the booking update with the correct carrierBookingRequestReference"), "Error Message not Match"

        # MuleSoft will check in C Sight if the booking that needs to be updated in C Sight was originally created by API or not.
        # MuleSoft will us the below for the same. In this case send error message as
        # "Booking cannot be updated as the original booking was not created through API channel, please reach out to bookingrequests@crowley.com for assistance".
        # FAIL: iT'S ALLOWING TO SENT UPDATES OUT THE SCOPE. CAT335032

    @test(test_case_id="CT-3238", test_description="[12726] Update Booking on valid booking number", skip=True)
    def test_update_booking_on_valid_booking(self, shared_data, user):
        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        # BOOKING ACTIVE -> CHANGE STATUS TO -> BOL COMPLETE
        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        # path = "../../data/bookings/CT-3104_booking_number_with_vehicle_dimensions_happy_path_kgs.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3238_create_active_booking_number"
        )

        self.add_report(
            test_data="CT-3238 | Create Active Booking Number",
            status_code=202,
            response=response_new_status
        )
        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)

        shared_data["electronicCustomerReference"] = new_booking['electronicCustomerReference']
        shared_data["carrierBookingRequestReference"] = new_booking['carrierBookingRequestReference']

        assert re.match(r"^CustCont\d{12}$", shared_data["electronicCustomerReference"]), "electronicCustomerReference with invalid format"
        assert re.match(r"^CR\d{14,16}$", shared_data["carrierBookingRequestReference"]), "carrierBookingRequestReference with invalid format"
        assert shared_data.get("carrierBookingRequestReference"), "carrierBookingRequestReference is required"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        self.add_report(
            test_data="CT-3238 | Get Booking Container Status",
            status_code=[200, 303],
            response=response_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-3238_get_booking_container_new_to_active"
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]

        # Shipper Account for Gallery
        shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])

        # Override Equipment Code
        data["cargos"][0]["containerDetails"]["equipmentIsoCode"] = "CC40"  # CC40 | 22G1

        response_update = self.bookings.update_booking_with_cat_number(
            shipperCvif=shared_data["shipperCvif"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            json=data
        )

        self.add_report(
            test_data="CT-3238 | Get Booking Container Update",
            status_code=[202, 303],
            response=response_update
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update,
            filename_prefix="CT-3238_get_booking_container_update"
        )

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status_2 = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=300  # Wait until: 3 minutes 180s | 4 minutes 240s | 5 minutes 300s
        )

        self.add_report(
            test_data="CT-3238 | Get Booking Container Update Status",
            status_code=[200, 303],
            response=response_status_2
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status_2,
            filename_prefix="CT-3238_get_booking_container_update_status"
        )

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        self.search_menu.screenshot().pause(3).save_screenshot(description="CT-3238_Booking_Updated_Active")

        csight_status = self.bookings_details.get_booking_status()

        self.bookings_details.click_tab_cargo_details()\
            .tab_content_cargo_details\
            .click_commercial_container_details()\
            .screenshot()\
            .save_screenshot(description="CT_3238_cargo_details_content")

        cargo_title = self.bookings_details.tab_content_cargo_details.get_commercial_container_summary_title(index=1)

        assert (csight_status == "Active"), "Status Booking Incorrect"
        assert (cargo_title == "1. 40' CHASSIS * 1"), "Incorrect Equipment Code"

    @test(test_case_id="CT-4812", test_description="[12559] Update CVIF Not Match", skip=False)
    def test_update_with_cvif_not_match(self, shared_data):
        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        data["agreementReference"] = ""
        data["bookingRemarks"] = "BOOKING NOT FOUND"

        # Precondition
        # 1. Valid Existing Booking
        # 2. Valid Carrier Booking Request Reference
        # 3. Invalid CVIF Code

        # Booking not exist used as test
        shared_data["crowleyBookingReferenceNumber"] = "CAT40001425"
        shared_data["carrierBookingRequestReference"] = "CR5201258740671219"

        # Shipper Account for Gallery
        # shared_data["shipperCvif"] = extract_cvif_code(data["parties"][0]['code'])
        shared_data["shipperCvif"] = "01010101"

        response_update_status = self.bookings.update_booking_with_cat_number(
            shipperCvif=shared_data["shipperCvif"],
            crowleyBookingNumber=shared_data["crowleyBookingReferenceNumber"],
            carrierBookingRequestReference=shared_data["carrierBookingRequestReference"],
            json=data
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-3207_prebook_update_gallery"
        )

        self.add_report(
            test_data="CT-3207 | Update CVIF Not Match",
            status_code=202,
            response=response_update_status
        )

    # PASS: IS CREATING A BRAND-NEW BOOKING

    # MuleSoft will check in C Sight if the booking that needs to be updated is available in C Sight or not. If not,
    # then MuleSoft will not create/ update the booking, instead, MuleSoft will send the synchronous error response to the gallery customer.
    # "Booking not found, Please re-check the booking number sent and try-again. For additional help, please reach out to bookingrequests@crowley.com".
    # Select Id from Booking__c where Booking_Number__c= 'CAT007276' AND Available_for_Booking__c = false AND Source__c != null
    # Booking not found, Please re-check the booking number sent and try-again. For additional help, please reach out to bookingrequests@crowley.com

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4817", test_description="[12559] Booking can not be updated on BOL Complete", skip=True)
    def test_booking_can_not_be_update_status_bol_complete(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> BOL COMPLETE
        # CAT356553

        cat_number = "CAT356553"

        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Passing same Electronic Customer Reference
        data["electronicCustomerReference"] = "CustCont250623161657"
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API BOL COMPLETE"
        # Sending Update Body Request
        response_update_status = self.bookings.update_booking_with_cat_number(cat_number, json=data)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4817_booking_can_not_be_update_status_bol_complete"
        )

        self.add_report(
            test_data="CT-4817 | Booking can not be update with status bol complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        text = "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4818", test_description="[12559] Booking can not be updated on Export BL Released", skip=True)
    def test_booking_can_not_be_update_status_export_bl_release(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> Export BL Released
        # CAT356552

        cat_number = "CAT356552"

        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Passing same Electronic Customer Reference
        data["electronicCustomerReference"] = "CustCont250623163403"
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API EXPORT BL RELEASED"
        # Sending Update Body Request
        response_update_status = self.bookings.update_booking_with_cat_number(cat_number, json=data)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4818_booking_can_not_be_update_export_bl_release_complete"
        )

        self.add_report(
            test_data="CT-4818 | Booking can not be update with status Export BL Release complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        # PASS : But the message validation has more text specification than the ticket requirement.
        text = "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4820", test_description="[12559] Booking can not be updated on In Progress", skip=True)
    def test_booking_can_not_be_update_status_in_progress(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> ReWork
        # CAT356522

        cat_number = "CAT323573"

        path = "../../data/bookings/CT-3213_booking_number_with_active_status_40_Cube_Dry.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Passing same Electronic Customer Reference
        data["electronicCustomerReference"] = "CustCont250623164643"
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API REWORK"

        # Sending Update Body Request
        response_update_status = self.bookings.update_booking_with_cat_number(cat_number, json=data)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4820_booking_can_not_be_update_in_progress_bol"
        )

        self.add_report(
            test_data="CT-4820 | Booking can not be update with status in progress bol complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        # FAIL: It's allowing to pass the validations,
        text = "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4821", test_description="[12559] Booking can not be updated on Rework", skip=True)
    def test_booking_can_not_be_update_status_rework(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> ReWork
        # CAT356547
        # For this Scenario it's important to make sure the Booking BOL Status is on Re-Work

        cat_number = "CAT322123"

        path = "../../data/bookings/CT-3213_booking_number_with_active_status_40_Cube_Dry.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Passing same Electronic Customer Reference
        data["electronicCustomerReference"] = "CustCont250623164643"
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API REWORK"

        # Sending Update Body Request
        response_update_status = self.bookings.update_booking_with_cat_number(cat_number, json=data)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4821_booking_can_not_be_update_rework_complete"
        )

        self.add_report(
            test_data="CT-4821 | Booking can not be update with status Rework complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        # FAIL: It's allowing to pass the validations,
        text = "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4822", test_description="[12559] Booking Container can not be updated if equipment is assigned", skip=True)
    def test_booking_container_can_not_be_update_if_equipment_is_assigned(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> EQUIPMENT ASSIGNED
        # CAT356520

        cat_number = "CAT356520"

        path = "../../data/bookings/CT-3213_booking_number_with_active_status_40_Cube_Dry.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Passing same Electronic Customer Reference
        data["electronicCustomerReference"] = "CustCont250623164643"
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API REWORK"

        # Sending Update Body Request
        response_update_status = self.bookings.update_booking_with_cat_number(cat_number, json=data)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4822_booking_container_can_not_be_update_equipment_assigned"
        )

        self.add_report(
            test_data="CT-4822 | Booking Container can not be update with status Equipment Assigned",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # MuleSoft will check if the equipment is assigned to a booking or if the dock receipt number is present on the booking using below queries.
        # If either of the validations are met, then MuleSoft will not update the booking in C Sight, instead,
        # MuleSoft will send the synchronous error response to the customer. The error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        # SELECT Id FROM Equipment__c where Requirement__r.Freight__r.Shipment__r.Booking__c = '<booking_id>'
        # SELECT Id, Shipment__r.Booking__c FROM Dock_Receipt__c where Shipment__r.Booking__c = '<booking_id>'

        text = "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4823", test_description="[12559] Booking Vehicle can not be updated if equipment is assigned", skip=True)
    def test_booking_vehicle_can_not_be_update_if_equipment_is_assigned(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> EQUIPMENT ASSIGNED
        # CAT356517

        cat_number = "CAT356517"

        path = "../../data/bookings/CT-3213_booking_number_with_active_status_40_Cube_Dry.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)
        # Passing same Electronic Customer Reference
        data["electronicCustomerReference"] = "CustCont250623164643"
        data["bookingRemarks"] = "BOOKING UPDATE THROUGH API REWORK"

        # Sending Update Body Request
        response_update_status = self.bookings.update_booking_with_cat_number(cat_number, json=data)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4823_booking_vehicle_can_not_be_update_equipment_assigned"
        )

        self.add_report(
            test_data="CT-4823 | Booking Vehicle can not be update with status Equipment Assigned",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # MuleSoft will check if the equipment is assigned to a booking or if the dock receipt number is present on the booking using below queries.
        # If either of the validations are met, then MuleSoft will not update the booking in C Sight, instead,
        # MuleSoft will send the synchronous error response to the customer. The error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        # SELECT Id FROM Equipment__c where Requirement__r.Freight__r.Shipment__r.Booking__c = '<booking_id>'
        # SELECT Id, Shipment__r.Booking__c FROM Dock_Receipt__c where Shipment__r.Booking__c = '<booking_id>'

        text = "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.



