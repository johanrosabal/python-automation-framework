import json

import pytest

from core.config.logger_config import setup_logger
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from applications.api.csight.common.CsightBaseTest import CsightBaseTest
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12727(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    @test(test_case_id="CT-4824", test_description="[12727] Cancel an Active Booking", skip=False)
    def test_cancel_an_active_booking(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> BOL COMPLETE
        path = "../../data/bookings/CT-3178_booking_number_with_active_status.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.create_booking(json=data)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-4824_cancel_active_booking"
        )

        self.add_report(
            test_data="CT-4824 | Cancel Active Booking",
            status_code=202,
            response=response_new_status
        )
        # Share Carrier Booking Request Reference
        new_booking = json.loads(response_new_status.text)
        #
        ECR1 = new_booking['electronicCustomerReference']
        CRR1 = new_booking['carrierBookingRequestReference']

        self.pause(10)

        # assert re.match(r"^CustCont\d{12}$", shared_data["ELECTRONIC_CUSTOMER_REFERENCE"]), "electronicCustomerReference with invalid format"
        # # assert re.match(r"^CR\d{16}$", shared_data["CARRIER_BOOKING_REQUEST_REFERENCE"]), "carrierBookingRequestReference with invalid format"
        # assert shared_data.get("CARRIER_BOOKING_REQUEST_REFERENCE"), "carrierBookingRequestReference is required"

        # 02. Verify change status to Active
        # --------------------------------------------------------------------------------------------------------------
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=CRR1,
            expected_status="Active",
            timeout=160
        )

        # Save Response for Status Endpoint
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_status,
            filename_prefix="CT-4824_booking_status_update_to_pending"
        )

        self.add_report(
            test_data="CT-4824 | Booking Status Update to Pending",
            status_code=303,
            response=response_status
        )

    @test(test_case_id="CT-4825", test_description="[12727] Cancel CVIF Not Match", skip=False)
    def test_cancel_with_cvif_not_match(self):

        # Booking not exist used as test
        cat_number = "CAT333339"

        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4825_cancel_cvif_not_match"
        )

        self.add_report(
            test_data="CT-4825 | Cancel CVIF Not Match",
            status_code=400,
            response=response_update_status
        )
        message = new_booking['message']
        errorCode = new_booking['errorCode']

        text = "Booking not found, Please re-check the booking number sent and try-again. For additional help, please reach out to bookingrequests@crowley.com"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4826", test_description="[12727] Booking can not be cancel on BOL Complete", skip=False)
    def test_booking_can_not_be_cancel_status_bol_complete(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> BOL COMPLETE
        # CAT356553

        cat_number = " CAT356553"

        # Sending CANCEL Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4826_booking_can_not_be_cancel_status_bol_complete"
        )

        self.add_report(
            test_data="CT-4826 | Booking can not be cancel with status bol complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        text = "Booking cannot be cancelled, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4827", test_description="[12727] Booking can not be cancel on Export BL Released", skip=False)
    def test_booking_can_not_be_cancel_status_export_bl_release(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> Export BL Released
        # CAT356552

        cat_number = "CAT356552"

        # Sending Update Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4827_booking_can_not_be_cancel_export_bl_release_complete"
        )

        self.add_report(
            test_data="CT-4827 | Booking can not be cancel with status Export BL Release complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        text = "Booking cannot be cancelled, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # # Requires C-Sight BOL pages
    @test(test_case_id="CT-4828", test_description="[12727] Booking can not be cancel on In Progress", skip=False)
    def test_booking_can_not_be_cancel_status_in_progress(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> ReWork
        # CAT356522

        cat_number = "CAT323573"

        # Sending Update Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4828_booking_can_not_be_cancel_in_progress_bol"
        )

        self.add_report(
            test_data="CT-4828 | Booking can not be cancel with status in progress bol complete",
            status_code=400,
            response=response_update_status
        )

        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        # FAIL: It's allowing to pass the validations,
        text = "Booking cannot be cancelled, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4829", test_description="[12727] Booking can not be cancel on Rework", skip=False)
    def test_booking_can_not_be_cancel_status_rework(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> ReWork
        # CAT356547

        cat_number = "CAT322123"

        # Sending Update Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4829_booking_can_not_be_update_rework_complete"
        )

        self.add_report(
            test_data="CT-4829 | Booking can not be update with status Rework complete",
            status_code=400,
            response=response_update_status
        )

        message = new_booking['message']
        errorCode = new_booking['errorCode']
        # MuleSoft will check the status of all related BoLs against that booking. If any of the bol against that booking has any of the below status,
        # then MuleSoft will not update the booking, instead send the synchronous error response to the gallery customer, error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"

        text = "Booking cannot be cancelled, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # FAIL: It's allowing to pass the validations,

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4830", test_description="[12727] Booking Container can not be cancel if equipment is assigned", skip=False)
    def test_booking_container_can_not_be_cancel_if_equipment_is_assigned(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> EQUIPMENT ASSIGNED
        # CAT356520

        cat_number = "CAT356520"

        # Sending Cancel Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4830_booking_can_not_be_cancel_equipment_assigned"
        )

        self.add_report(
            test_data="CT-4830 | Booking can not be cancel with status Equipment Assigned",
            status_code=400,
            response=response_update_status
        )

        # MuleSoft will check if the equipment is assigned to a booking or if the dock receipt number is present on the booking using below queries.
        # If either of the validations are met, then MuleSoft will not update the booking in C Sight, instead,
        # MuleSoft will send the synchronous error response to the customer. The error message should say
        # "Booking cannot be updated, please reach out to bookingrequests@crowley.com for assistance"
        # SELECT Id FROM Equipment__c where Requirement__r.Freight__r.Shipment__r.Booking__c = '<booking_id>'
        # SELECT Id, Shipment__r.Booking__c FROM Dock_Receipt__c where Shipment__r.Booking__c = '<booking_id>'

        message = new_booking['message']
        errorCode = new_booking['errorCode']

        text = "Booking cannot be cancelled, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.

    # Requires C-Sight BOL pages
    @test(test_case_id="CT-4831", test_description="[12727] Booking Vehicle can not be cancel if equipment is assigned", skip=False)
    def test_booking_vehicle_can_not_be_cancel_if_equipment_is_assigned(self):
        # BOOKING ACTIVE -> CHANGE STATUS TO -> EQUIPMENT ASSIGNED
        # CAT356517

        cat_number = "CAT356517"

        # Sending Cancel Body Request
        response_update_status = self.bookings.cancel_booking_with_cat_number(cat_number)

        new_booking = json.loads(response_update_status.text)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_update_status,
            filename_prefix="CT-4831_booking_vehicle_can_not_be_cancel_equipment_assigned"
        )

        self.add_report(
            test_data="CT-4831 | Booking Vehicle can not be cancel with status Equipment Assigned",
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

        text = "Booking cannot be cancelled, please reach out to bookingrequests@crowley.com for assistance"
        assert (text in message), "Error Message not Match or is missing"
        assert (errorCode == 400), "Error code should be 400"
        # PASS : But the message validation has more text specification than the ticket requirement.