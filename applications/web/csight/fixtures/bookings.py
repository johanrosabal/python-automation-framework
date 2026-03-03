
from typing import Dict, Any

import pytest
import allure
import time

from applications.web.csight.components.modals.ModalComponent import ModalComponent
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.bookings.CreateBookingPage import CreateBookingPage
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers

# Global Variable
if not hasattr(pytest, 'BOOKING_RESULTS'):
    pytest.BOOKING_RESULTS = []


@pytest.fixture
def booking_creation(request) -> Dict[str, Any]:

    start_time = time.time()

    # Save Booking Number and Booking Status
    booking_number = None
    booking_status = "-"
    booking_message = None
    test_status = "IN_PROGRESS"

    # Activate pytest_sessionfinish
    request.config._booking_report_enabled = True

    # Load JSON Data
    data = JSONReader().import_json(request.param)
    booking_data = helpers.parse_dynamic_dates_values(data)

    # Read Test Case ID
    tests = booking_data.get("tests", {})

    test_case_id = tests.get("idTC", "No idTC provided")
    title = tests.get("title", "No title provided")
    description = tests.get("description", "No description provided")
    tag = tests.get("tag", "No tag provided")
    feature = tests.get("feature", "No feature provided")
    severity = tests.get("severity", "No severity provided")

    link_href = tests.get("link", {}).get("url", "No url provided")
    link_name = test_case_id + " - " + title

    # if test_case_id and link_name:
    #     allure.dynamic.testcase(link_name)

    if title:
        allure.dynamic.title(test_title=title)

    if description:
        allure.dynamic.tag(description)

    if tag:
        allure.dynamic.tag(tag)

    if feature:
        allure.dynamic.feature(feature)

    if severity:
        allure.dynamic.severity(severity)

    if link_href:
        allure.dynamic.link(url=link_href, name=link_name)

    result = {
        "test_case_id": test_case_id,
        "booking_data": booking_data,
        "route": None,
        "booking_number": booking_number,
        "booking_status": booking_status,
        "test_status": test_status
    }

    # Load Pages Instances
    booking_details = BookingDetailsPage.get_instance()
    create_booking_page = CreateBookingPage.get_instance()
    modal = ModalComponent.get_instance()

    # Load Create Booking Page
    create_booking_page.load_page().set_booking_data(data=booking_data)
    # [ORIGIN-DESTINATION TAB] -------------------------------------------------------------------------------------
    # Complete Booking : Booking Party + Bill to Party + Shipping Details + Account Details + Origin + Destination

    create_booking_page.origin_destination \
        .fill_booking_party() \
        .fill_bill_to_party() \
        .fill_shipping_details() \
        .fill_account_details() \
        .fill_origin_details() \
        .fill_destination_details() \
        .fill_stops() \
        .fill_stops_intermediate() \
        .screenshot().attach_to_allure(name=f"{test_case_id}_01_Create_Booking_Origin_Destination")

    # Next to Cargo Details Form + Proceed Modal Button
    create_booking_page.click_next()

    # Capture Booking Number and Status
    if modal.is_visible():
        booking_number = modal.get_booking_number()
        booking_status = modal.get_booking_status()
        booking_message = modal.get_booking_reason()

        assert (booking_number.startswith("CAT")), "Booking Number Incorrect"
        assert (booking_status == 'Pending'), "Booking Status is not match."
        assert (booking_message == 'Booking Incomplete'), "Booking Message not match."

    result["booking_number"] = booking_number
    result["booking_status"] = booking_status
    result["booking_message"] = booking_message

    create_booking_page.click_proceed()

    # CARGO_DETAILS TAB---------------------------------------------------------------------------------------------
    if create_booking_page.cargo_details.is_visible_cargo_details(result=result):

        create_booking_page.cargo_details.process_cargo_type()
        create_booking_page.cargo_details.fill_operational_services()
        create_booking_page.cargo_details.screenshot().attach_to_allure(name=f"{test_case_id}_02_Create_Booking_Cargo_Information")
        # Next to Routes
        create_booking_page.click_next()

        # ROUTES TAB----------------------------------------------------------------------------------------------------

        if create_booking_page.routes.check_rates_not_available_and_skip(result=result) is not True:
            result['routes'] = create_booking_page.routes.click_and_get_route_item_information()
            create_booking_page.routes.screenshot().attach_to_allure(name=f"{test_case_id}_03_Create_Booking_Route_Selected")
            # Next to Other Details
            create_booking_page.click_next()

            # OTHER DETAILS TAB----------------------------------------------------------------------------------------------------
            create_booking_page.other_details.close_modal_hazardous_validation()
            create_booking_page.other_details.fill_consignee_details()
            create_booking_page.other_details.enter_booking_remarks_remark()
            create_booking_page.other_details.enter_itn_number()
            create_booking_page.other_details.screenshot().attach_to_allure(name=f"{test_case_id}_04_Create_Booking_Other_Details")
            create_booking_page.click_create_booking()
            create_booking_page.other_details.screenshot().attach_to_allure(name=f"{test_case_id}_05_Create_Booking_Confirmation")

            if modal.is_visible():
                booking_number = modal.get_booking_number()
                booking_status = modal.get_booking_status()
                booking_message = modal.get_modal_message()

                assert (booking_number.startswith("CAT")), "Booking Number Incorrect"
                assert (booking_status != ''), "Booking Status missing."
                assert (booking_message != ''), "Booking Message missing."

                result["booking_number"] = booking_number
                result["booking_status"] = booking_status
                result["booking_message"] = booking_message

                if booking_status == 'Active':
                    result["test_status"] = "PASS"

                if booking_status == 'Pending':
                    result["test_status"] = "FAIL"

                # Close Modal
                modal.click_close()
                booking_details.screenshot().attach_to_allure(name="CT-2209_04_Create_Details")
        else:
            create_booking_page.routes.screenshot().pause(3).attach_to_allure(name=f"{test_case_id}_03_Rates_Not_Available")
    else:
        create_booking_page.cargo_details.screenshot().pause(3).attach_to_allure(name=f"{test_case_id}_01_Origin_Destination")

    # Save results on Global variable
    pytest.BOOKING_RESULTS.append(result)

    end_time = time.time()
    duration_sec = end_time - start_time

    allure.attach(
        f"Execution time: {duration_sec:.2f} seconds",
        name="Duration",
        attachment_type=allure.attachment_type.TEXT
    )

    return result
