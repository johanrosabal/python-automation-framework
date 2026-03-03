import json

import pytest
import re

from core.config.logger_config import setup_logger
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from applications.api.csight.common.CsightBaseTest import CsightBaseTest
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('BaseTest')


@pytest.fixture(scope="module")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12792(CsightBaseTest):
    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    @test(test_case_id="CT-3199", test_description="[12792] Booking as Customer Pre Assign", skip=False)
    def test_create_a_booking_customer_pre_assign(self, shared_data):
        path = "../../data/bookings/CT-3198_reserved_booking_number_gallery.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        response_new_status = self.bookings.get_reserved_booking_number(json=data)

        self.add_report(
            test_data="CT-3199 | Customer can reserved a booking number",
            status_code=202,
            response=response_new_status
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_new_status,
            filename_prefix="CT-3199_customer_can_reserved_a_booking_number"
        )

        dict_response = JSONReader.text_to_dict(response_new_status.text)
        cat_number = dict_response["crowleyBookingReferenceNumber"]
        shared_data["CAT_NUMBER"] = cat_number

        # Validate CAT Number Format
        assert re.match(r"^CAT\d{6}$", cat_number), f"CAT NUMBER INVALID: {cat_number}"
        logger.info(F"CAT NUMBER VALID: {cat_number}")

        #  New Booking Pending Reason “Customer Pre-Assigned” should be created in salesforce.
        #  Whenever an API booking is created in Salesforce with status as “Pending” and with Pending Reason as “Customer Pre-Assigned”
        #  FAIL ==> UI VERIFICATION: Booking will be shown with No data in C sight UI, and only resume button should be shown.
        #  FAIL ==> Once the User clicks on the Resume button then automatically the booking Pending Reason should be changed to "Booking Incomplete".

