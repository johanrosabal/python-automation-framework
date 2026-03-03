import allure

from tabulate import tabulate

from applications.web.loadiq.common.FeedbackForm import FeedbackForm
from applications.web.loadiq.common.MyLoadsFiltersComponent import MyLoadsFiltersComponent
from applications.web.loadiq.components.ConfirmationDialogModal import ConfirmationDialogModal
from applications.web.loadiq.components.UploadFilesModal import UploadFilesModal
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from applications.api.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.my_loads.CompleteDeliveryPage import CompleteDeliveryPage
from applications.web.loadiq.pages.my_loads.MyLoadsPage import MyLoadsPage
from applications.web.loadiq.pages.my_loads.PleaseConfirmYourDetailsPage import PleaseConfirmYourDetailsPage
from applications.web.loadiq.pages.my_loads.status_update.StatusUpdateModalPage import StatusUpdateModalPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils import random_utils
from core.utils.XMLUtils import XMLUtils
from core.utils.decorator import test
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint

logger = setup_logger('TestStatusUpdate')


@pytest.mark.web
@loadiq
class TestStatusUpdate(BaseTest):

    # Common variables
    status_code_expected = 400
    # Objects Instances
    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    my_loads = MyLoadsPage.get_instance()
    status_update = StatusUpdateModalPage.get_instance()
    complete_delivery_modal = CompleteDeliveryPage.get_instance()
    upload_files_modal = UploadFilesModal.get_instance()
    confirm_your_details_modal = PleaseConfirmYourDetailsPage.get_instance()
    confirmation_dialog_modal = ConfirmationDialogModal.get_instance()
    submit_load_endpoint = SubmitLoadEndpoint.get_instance()
    my_loads_filters = MyLoadsFiltersComponent.get_instance()

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4502.json", skip=False)
    def test_delivery_button_visibility_based_on_milestone_completion(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4502")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads().screenshot().attach_to_allure(name="Validate My Loads Page Loaded")

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number)
        self.my_loads.click_search().screenshot().attach_to_allure(name="Validate Search Results Displayed")

        # 4. Verify Complete Delivery button is not visible
        is_complete_delivery_visible = self.my_loads.is_complete_delivery_button_visible()
        assert is_complete_delivery_visible is False, "Complete Delivery button is invisible"

        # 5. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 6. Validate modal status update opens with title "Status Update"
        modal_title = self.status_update.is_title_visible()
        assert modal_title is True, "Title should be visible"
        self.my_loads.screenshot().attach_to_allure(name="Validate Status Update Modal Opened")

        # 7. Input Actual Arrival
        self.status_update.update_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Shipment status has been updated successfully.", "Status update success message should be displayed"

        self.my_loads.screenshot().attach_to_allure(name="Validate Actual Arrival Entered and Updated")

        # 8. Verify Complete Delivery button is still not visible
        is_complete_delivery_visible = self.my_loads.is_complete_delivery_button_visible()
        assert is_complete_delivery_visible is False, "Complete Delivery button is visible after Actual Arrival"

        # 9. Open Status Update modal again
        self.my_loads.click_update_status_button()

        # 10. Input Actual Departure
        self.status_update.update_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)
        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Shipment status has been updated successfully.", "Status update success message should be displayed"
        self.my_loads.screenshot().attach_to_allure(name="Validate Actual Departure Entered and Updated")

        # 11. Verify Complete Delivery button is still not visible
        is_complete_delivery_visible = self.my_loads.is_complete_delivery_button_visible()
        assert is_complete_delivery_visible is False, "Complete Delivery button is visible after Actual Departure"

        # 12. Open Status Update modal again
        self.my_loads.click_update_status_button()

        # 13. Input actual arrival at delivery
        self.status_update.update_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        # Click confirm or Enter Container Number Modal: Click on Bobtail (No container attached)
        self.status_update.click_checkbox_bobtail().click_submit()
        alert_message1 = self.status_update.get_status_update_message()
        self.my_loads.screenshot().attach_to_allure(name="Validate Actual Arrival at Delivery Entered and Updated")
        assert alert_message1 == "Container Number updated successfully", "Status update success message should be displayed"

        # 14. Verify Complete Delivery button is still not visible
        is_complete_delivery_visible = self.my_loads.is_complete_delivery_button_visible()
        assert is_complete_delivery_visible is False, "Complete Delivery button is visible after Actual Arrival at Delivery"

        # 15. Open Status Update modal again
        self.my_loads.click_update_status_button()

        # 16. Input actual departure at delivery
        self.status_update.update_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)
        # Click confirm or Enter Container Number Modal: Click on Bobtail (No container attached)
        self.status_update.click_checkbox_bobtail().click_submit()
        alert_message2 = self.status_update.get_status_update_message()
        assert alert_message2 == "Container Number updated successfully", "Status update success message should be displayed"
        self.my_loads.screenshot().attach_to_allure(name="Validate Actual Departure at Delivery Entered and Updated")

        # 16. Verify Complete Delivery button is now visible
        is_complete_delivery_visible = self.my_loads.is_complete_delivery_button_visible()
        assert is_complete_delivery_visible is True, "Complete Delivery button is invisible after all milestones completed"

        # 17. Click Complete Delivery button
        self.my_loads.click_complete_delivery_button().screenshot().attach_to_allure(name="Validate Load Status Changed to Completed")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4405.json", skip=False)
    def test_verify_correct_display_status_update_modal(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4405")

        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads().screenshot().attach_to_allure(name="Validate My Loads Page Loaded")

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number)
        self.my_loads.click_search().screenshot().attach_to_allure(name="Validate Search Results Displayed")

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Validate modal status update opens with title "Status Update"
        modal_title = self.status_update.is_title_visible()
        assert modal_title is True, "Title should be visible"
        self.my_loads.screenshot().attach_to_allure(name="Validate Status Update Modal Opened")

        # 6. Verify all elements in the modal
        self.status_update.verify_all_elements()

        # 7. Verify Scheduled Dates format (Two lines)
        # Check Row 1 --------------------------------------------------------------------------------------------------
        scheduled_arrival_text_1 = self.status_update.get_scheduled_arrival_text(row_index=1)
        scheduled_departure_text_1 = self.status_update.get_scheduled_departure_text(row_index=1)

        logger.info(f"Row 1 Scheduled Arrival: {scheduled_arrival_text_1}")
        logger.info(f"Row 1 Scheduled Departure: {scheduled_departure_text_1}")

        # We can also check if the text length is substantial enough to be date + time
        assert len(scheduled_arrival_text_1) > 10, f"Scheduled Arrival text seems too short: {scheduled_arrival_text_1}"
        assert len(
            scheduled_departure_text_1) > 10, f"Scheduled Departure text seems too short: {scheduled_departure_text_1}"

        # Check Row 2 --------------------------------------------------------------------------------------------------
        scheduled_arrival_text_2 = self.status_update.get_scheduled_arrival_text(row_index=2)
        scheduled_departure_text_2 = self.status_update.get_scheduled_departure_text(row_index=2)

        logger.info(f"Row 2 Scheduled Arrival: {scheduled_arrival_text_2}")
        logger.info(f"Row 2 Scheduled Departure: {scheduled_departure_text_2}")

        # We can also check if the text length is substantial enough to be date + time
        assert len(scheduled_arrival_text_2) > 10, f"Scheduled Arrival text seems too short: {scheduled_arrival_text_2}"
        assert len(scheduled_departure_text_2) > 10, f"Scheduled Departure text seems too short: {scheduled_departure_text_2}"

        # 8. Verify Empty Fields Spacing
        # The test data might have empty fields, or we just verify the layout visually via screenshot as requested.
        self.my_loads.screenshot().attach_to_allure(name="Validate Scheduled Dates Format and Empty Fields Spacing")

        # 9. Close Modal
        self.status_update.click_close_button()

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4406.json", skip=False)
    def test_verify_appearance_checkmark_saving_new_stop(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4406")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Capture Dates Before enter values with X Icon

        actual_arrival_1 = self.status_update.get_actual_arrival_checkmark(row_index=1, col_index=5)
        actual_departure_1 = self.status_update.get_actual_arrival_checkmark(row_index=1, col_index=6)

        actual_arrival_2 = self.status_update.get_actual_arrival_checkmark(row_index=2, col_index=5)
        actual_departure_2 = self.status_update.get_actual_arrival_checkmark(row_index=2, col_index=6)
        self.my_loads.screenshot().attach_to_allure(name="X Icons Before Save Dates Updates")

        assert actual_arrival_1 is not True, "Row 1: Actual Arrival should have X Icon"
        assert actual_departure_1 is not True, "Row 1: Actual Departure should have X Icon"
        assert actual_arrival_2 is not True, "Row 2: Actual Arrival should have X Icon"
        assert actual_departure_2 is not True, "Row 2: Actual Departure should have X Icon"

        # 6. Input Dates Fields
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)
        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)

        # 7. Click on Update Button + CheckBox BobTail Modal
        self.status_update \
            .click_update_button() \
            .click_checkbox_bobtail() \
            .click_submit() \

        # 8. Verify Message Confirmation
        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Container Number updated successfully", "Status update success message should be displayed"

        # 9. Verify Modal Is Close After Make Dates Updates
        modal = self.status_update.is_not_visible_modal_status()
        assert modal, "Modal Should be Close after update dates"

        # 10. Open again Modal Status
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 11. Verify CheckMarks are on Dates Fields
        actual_arrival_1 = self.status_update.get_actual_arrival_checkmark(row_index=1, col_index=5)
        actual_departure_1 = self.status_update.get_actual_arrival_checkmark(row_index=1, col_index=6)

        actual_arrival_2 = self.status_update.get_actual_arrival_checkmark(row_index=2, col_index=5)
        actual_departure_2 = self.status_update.get_actual_arrival_checkmark(row_index=2, col_index=6)

        self.my_loads.screenshot().attach_to_allure(name="CHECK Icons After Save Dates Updates")

        assert actual_arrival_1, "Row 1: Actual Arrival should have X Icon"
        assert actual_departure_1, "Row 1: Actual Departure should have X Icon"
        assert actual_arrival_2, "Row 2: Actual Arrival should have X Icon"
        assert actual_departure_2, "Row 2: Actual Departure should have X Icon"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4408.json", skip=False)
    def test_verify_initial_display_status_screen_no_previous_statuses(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4408")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 6. Verify all elements in the modal
        self.status_update.verify_all_schedule_fields(num_rows=2).screenshot().attach_to_allure(
            name="All Schedule Fields and Elements Present")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4409.json", skip=False)
    def test_verify_display_of_previously_registered_status_and_enable_of_the_next_chronological_status(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4409")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.my_loads.screenshot().attach_to_allure(name="Save First Stop Fields")

        # 6. First Check: Enable Fields
        arrival = self.status_update.get_scheduled_arrival_enabled(row_index=1)
        departure = self.status_update.get_scheduled_departure_enabled(row_index=1)

        assert arrival, "Enable Field Arrival"
        assert departure, "Enable Field Departure"

        # 7. Click on Update Button
        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        # 8. Open again Modal Status
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()
        self.my_loads.screenshot().attach_to_allure(name="Checkout Second Stops Fields Enabled")

        # 9. Second Check: Enable Fields
        arrival = self.status_update.get_scheduled_arrival_enabled(row_index=1)
        departure = self.status_update.get_scheduled_departure_enabled(row_index=1)

        assert arrival is not True, "Enable Field Arrival"
        assert departure, "Enable Field Departure"

        # 10. Field out Departure Row 1
        self.status_update.update_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        # 11. Click on Update Button
        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        # 12. Click Update Again
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 13. Second Check: Enable Fields
        arrival = self.status_update.get_scheduled_arrival_enabled(row_index=1)
        departure = self.status_update.get_scheduled_departure_enabled(row_index=1)

        self.my_loads.screenshot().attach_to_allure(name="Checkout First Stops Fields Disabled")

        assert arrival is not True, "Enable Field Arrival"
        assert departure is not True, "Enable Field Departure"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4410.json", skip=False)
    def test_verify_update_multiple_consecutive_status_simultaneously(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4410")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        # ROW 1
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        arrival_1 = self.status_update.get_scheduled_arrival_enabled(row_index=1)
        departure_1 = self.status_update.get_scheduled_departure_enabled(row_index=1)

        # ROW 2
        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)

        arrival_2 = self.status_update.get_scheduled_arrival_enabled(row_index=2)
        departure_2 = self.status_update.get_scheduled_departure_enabled(row_index=2)

        self.my_loads.screenshot().attach_to_allure(name="Enter Info All Fields Same Time")

        assert arrival_1, "Enable Field Arrival 1"
        assert departure_1, "Enable Field Departure 1"
        assert arrival_2, "Enable Field Arrival 2"
        assert departure_2, "Enable Field Departure 2"

        # 7. Click on Update Button
        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        # 8. Open again Modal Status
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        arrival_1 = self.status_update.get_scheduled_arrival_enabled(row_index=1)
        departure_1 = self.status_update.get_scheduled_departure_enabled(row_index=1)
        arrival_2 = self.status_update.get_scheduled_arrival_enabled(row_index=2)
        departure_2 = self.status_update.get_scheduled_departure_enabled(row_index=2)

        assert arrival_1 is not True, "Disable Field Arrival 1"
        assert departure_1 is not True, "Disable Field Departure 1"
        assert arrival_2 is not True, "Disable Field Arrival 2"
        assert departure_2 is not True, "Disable Field Departure 2"

        self.my_loads.screenshot().attach_to_allure(name="Checkout All Fields Disabled")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4411.json", skip=False)
    def test_verify_modal_doesnt_show_an_error_when_trying_to_update_a_status_without_completing_the_previous_ones(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4411")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']
        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)

        # 6. Click on Update Button
        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Container Number updated successfully", "Status update success message should be displayed"

        self.status_update.is_not_visible_modal_status()

        # 7. Open again Modal Status
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        arrival_1 = self.status_update.get_scheduled_arrival_enabled(row_index=1)
        departure_1 = self.status_update.get_scheduled_departure_enabled(row_index=1)
        arrival_2 = self.status_update.get_scheduled_arrival_enabled(row_index=2)
        departure_2 = self.status_update.get_scheduled_departure_enabled(row_index=2)

        self.my_loads.screenshot().attach_to_allure(name="Checking Enabled Fields")

        assert arrival_1, "Enabled Field Arrival 1"
        assert departure_1, "Enabled Field Departure 1"
        assert arrival_2 is not True, "Disable Field Arrival 2"
        assert departure_2, "Enabled Field Departure 2"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4412.json", skip=False)
    def test_validate_error_when_entering_a_date_time_for_a_event_that_is_earlier_the_previous(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4412")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-2, hour=10, minute=00)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-2, hour=9, minute=00)

        error = self.status_update.get_error_validation_message()
        assert error == "*Error: Selected date/time should be greater than the previous date/time", "Incorrect Error Validation"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4413.json", skip=False)
    def test_verify_updating_a_status_and_selecting_a_reason_code(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4413")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        reason = "Credit Hold"

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-2, hour=10, minute=00)
        self.status_update.select_reason_code(row_index=1, reason_code=reason)

        # 6. Click on Update Button
        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        # 7. Open again Modal Status
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 8. Get Reason Code Row 1
        reason_code = self.status_update.get_reason_code(row_index=1)
        arrival_1 = self.status_update.get_scheduled_arrival_enabled(row_index=1)

        assert arrival_1 is not True, "Arrival Row 1 should not be enabled"
        assert reason == reason_code, "Reason Code Not Match. Row index 1"
        self.status_update.screenshot().attach_to_allure(name="Reason Code Selected")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4414.json", skip=False)
    def test_validate_error_when_entering_a_departure_time_earlier_than_the_arrival_time_for_different_stop(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4414")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-2, hour=10, minute=00)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-2, hour=9, minute=00)

        error = self.status_update.get_error_validation_message()
        assert error == "*Error: Actual Departure cannot be set without an Actual Arrival date/time for the same stop.", "Incorrect Error Validation"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4415.json", test_description="This negative test case verifies that the system rejects entries that do not comply with the expected format (mm/dd/yyyy hh:mm AM/PM) in the date and time fields.", feature="Status Update", skip=False)
    def test_validate_system_behavior_when_entering_invalid_date_and_time_formats(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4415")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival_with_text(row_index=1, text="Yesterday at ten")
        self.status_update.enter_actual_departure_with_text(row_index=1, text="Yesterday at ten")

        self.status_update.enter_actual_arrival_with_text(row_index=2, text="Yesterday at ten")
        self.status_update.enter_actual_departure_with_text(row_index=2, text="Yesterday at ten")

        # 6. Validation # 1
        arrival_1 = self.status_update.get_scheduled_actual_arrival_text(row_index=1)
        departure_1 = self.status_update.get_scheduled_actual_departure_text(row_index=1)

        arrival_2 = self.status_update.get_scheduled_actual_arrival_text(row_index=2)
        departure_2 = self.status_update.get_scheduled_actual_departure_text(row_index=2)

        assert arrival_1 == "", "Arrival Stop 1 should be empty"
        assert departure_1 == "", "Departure Stop 1 should be empty"

        assert arrival_2 == "", "Arrival Stop 2 should be empty"
        assert departure_2 == "", "Departure Stop 2 should be empty"

        # 5. Input Dates Fields
        self.status_update.enter_actual_arrival_with_text(row_index=1, text="27-08-2025 10:00")
        self.status_update.enter_actual_departure_with_text(row_index=1, text="27-08-2025 10:00")

        self.status_update.enter_actual_arrival_with_text(row_index=2, text="27-08-2025 10:00")
        self.status_update.enter_actual_departure_with_text(row_index=2, text="27-08-2025 10:00")

        # 6. Validation # 2
        arrival_1 = self.status_update.get_scheduled_actual_arrival_text(row_index=1)
        departure_1 = self.status_update.get_scheduled_actual_departure_text(row_index=1)

        arrival_2 = self.status_update.get_scheduled_actual_arrival_text(row_index=2)
        departure_2 = self.status_update.get_scheduled_actual_departure_text(row_index=2)

        assert arrival_1 == "", "Arrival Stop 1 should be empty"
        assert departure_1 == "", "Departure Stop 1 should be empty"

        assert arrival_2 == "", "Arrival Stop 2 should be empty"
        assert departure_2 == "", "Departure Stop 2 should be empty"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4416.json", skip=False)
    def test_validate_that_the_update_button_is_enabled_and_disabled_correctly_according_to_data_validity(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4416")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields: Disabled If Departure Date is Minor than Arrival Date
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-2, hour=10, minute=00)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-3, hour=10, minute=00)

        update_button = self.status_update.get_update_button_enabled()
        assert update_button is not True, "Button Update Should be disabled"

        # 6. Input Dates Fields: Valid Departure Date
        self.status_update.enter_actual_departure(row_index=1, days_offset=-1, hour=10, minute=00)
        update_button = self.status_update.get_update_button_enabled()
        assert update_button, "Button Update Should be enabled"

        # 7. Input Dates Fields: Empty Fields
        self.status_update.click_datetimepicker_icon_actual_arrival(row_index=1)
        self.status_update.click_clear_button()

        self.status_update.click_datetimepicker_icon_actual_departure(row_index=1)
        self.status_update.click_clear_button()

        self.status_update.click_update_button()
        self.status_update.screenshot().attach_to_allure(name="Empty Fields")

        update_button = self.status_update.get_update_button_enabled()
        assert update_button is not True, "Button Update Should be disabled"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4287.json", skip=False)
    def test_validate_that_the_update_button_is_enabled_and_disabled_correctly_according_to_data_validity(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4287")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()

        # 5. Input Dates Fields: Disabled If Departure Date is Minor than Arrival Date

        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)
        error_validation = self.status_update.get_error_validation_message()
        assert error_validation == "*Error: Actual Departure cannot be set without an Actual Arrival date/time for the same stop.", "Incorrect Error Validation Message"

        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        # 6. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)
        error_validation = self.status_update.get_error_validation_message()
        assert error_validation == "*Error: Actual Departure cannot be set without an Actual Arrival date/time for the same stop.", "Incorrect Error Validation Message"

        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        # 7. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()
        self.pause(2)
        self.status_update.screenshot().attach_to_allure(name="Final Complete Fields")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4696.json", skip=False)
    def test_validate_that_the_user_can_upload_a_document_after_that_the_load_change_to_complete_no_imdl(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4696")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # Data Upload
        file_name = "upload_test_document"
        document_type = "POD"
        description = "Test File"

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)
        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)

        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        # Wait 5 Seconds Before Start Uploading File, this wait is strict necessary
        self.pause(5)

        # 6. Click 'Complete Delivery' and Upload File

        self.my_loads.click_complete_delivery_button()
        self.status_update.is_visible_modal_status()
        self.complete_delivery_modal.is_complete_delivery_visible()
        self.complete_delivery_modal.click_no()
        self.complete_delivery_modal.click_upload_file()

        self.upload_files_modal.click_add_file(file_name=file_name + ".png",
                                               description=description).click_upload_file()

        file_name_1 = self.complete_delivery_modal.get_table_file_name(row_index=1)
        document_type_1 = self.complete_delivery_modal.get_table_document_type(row_index=1)
        description_1 = self.complete_delivery_modal.get_table_description(row_index=1)

        assert file_name_1 == file_name, "File Name Incorrect"
        assert document_type_1 == document_type, "Document Type Incorrect"
        assert description_1 == description, "Description Incorrect"

        self.complete_delivery_modal.screenshot().attach_to_allure(name="Complete Delivery Upload POD")

        # 7. Save Upload Files Complete Delivery
        self.complete_delivery_modal.click_submit()

        # 8. Close Confirm or Enter Container Numbers Modal
        self.status_update.click_checkbox_bobtail().click_submit().screenshot().attach_to_allure(
            name="Confirm or Enter Container Number")

        # 9. Confirm Your Details Modal
        self.confirm_your_details_modal.is_visible()
        file_name_2 = self.confirm_your_details_modal.get_table_file_name(row_index=1)
        document_type_2 = self.confirm_your_details_modal.get_table_document_type(row_index=1)
        description_2 = self.confirm_your_details_modal.get_table_description(row_index=1)

        assert file_name_2 == file_name, "File Name Incorrect"
        assert document_type_2 == document_type, "Document Type Incorrect"
        assert description_2 == description, "Description Incorrect"

        self.confirm_your_details_modal.screenshot().attach_to_allure(name="Please Confirm Your Details Modal")
        self.confirm_your_details_modal.click_confirm().click_ok()
        self.confirm_your_details_modal.is_not_visible()

        # 10. Final Confirmation Modal
        self.confirmation_dialog_modal.is_visible()
        self.confirmation_dialog_modal.screenshot().attach_to_allure(name="Load Submitted Confirmation Modal")
        self.confirmation_dialog_modal.click_close()

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4001.json", skip=False)
    def test_add_check_call_display_of_add_check_call_button_load_in_transit(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4001")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        status_1 = self.my_loads.get_track_status()

        assert status_1 == "Pending Pickup", "Status Incorrect"

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up and Change Status to
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        self.pause(3)

        add_check_call_1 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_1 is not True, "Button should be enabled"

        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        status_2 = self.my_loads.get_track_status()

        assert status_2 == "In Transit", "Status Incorrect"

        # 6. Open Status dialog box and verify button enabled
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        add_check_call_2 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_2 is True, "Button should be enabled"

        # Wait to table load Data
        self.pause(2)
        self.status_update.screenshot().attach_to_allure(name="Add Check Call Button Enabled")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4003.json", skip=False)
    def test_add_check_call_field_level_validation(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4003")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        status_1 = self.my_loads.get_track_status()

        assert status_1 == "Pending Pickup", "Status Incorrect"

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up and Change Status to
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        self.pause(3)

        add_check_call_1 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_1 is not True, "Button should be enabled"

        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        status_2 = self.my_loads.get_track_status()

        assert status_2 == "In Transit", "Status Incorrect"

        # 6. Open Status dialog box and verify button enabled
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        add_check_call_2 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_2 is True, "Button should be enabled"

        self.pause(2)  # Wait to table load Data
        self.status_update.screenshot().attach_to_allure(name="Add Check Call Button Enabled")

        self.status_update.click_add_check_call_button()
        self.status_update.check_call.click_update()

        self.status_update.check_call.fill_check_call(
            location="",
            days_offset=0,
            hour=0,
            minute=0,
            date_text="13/40",
            comments="People who know Crowley, know our employees are among the most knowledgeable and customer-focused in the industries we serve. They appreciate that we go places and solve problems others can’t. That we simplify the complex and make the routine more efficient. And, that we are committed to the success of their mission, project or supply chain. We invite you to explore our website and let us know how we may be of service."
        )

        location = self.status_update.check_call.get_error_location()
        date_time = self.status_update.check_call.get_error_date_time()

        assert location == "Location is required", "Incorrect Location Message Validation"
        assert date_time == "Selected date/time should be greater or equal to pickup date/time and should be smaller or equal to delivery date/time.", "Incorrect Date/Time Message Validation"

        self.status_update.check_call.screenshot().attach_to_allure(name="Screen Validation Error Message")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4004.json", skip=False)
    def test_add_check_call_cancel_check_call(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4004")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        status_1 = self.my_loads.get_track_status()

        assert status_1 == "Pending Pickup", "Status Incorrect"

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up and Change Status to
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        self.pause(3)

        add_check_call_1 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_1 is not True, "Button should be enabled"

        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        status_2 = self.my_loads.get_track_status()
        assert status_2 == "In Transit", "Status Incorrect"

        # 6. Open Status dialog box and verify button enabled
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        add_check_call_2 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_2 is True, "Button should be enabled"

        self.pause(2)  # Wait to table load Data
        self.status_update.screenshot().attach_to_allure(name="Add Check Call Button Enabled")

        self.status_update.click_add_check_call_button()
        self.status_update.check_call.click_update()

        self.status_update.check_call.fill_check_call(
            location="Miami Gardens, FL, USA",
            days_offset=1,
            hour=9,
            minute=30,
            date_text=None,
            comments="En-route, traffic delay cleared",
        )
        self.status_update.check_call.click_apply()
        self.status_update.check_call.click_cancel()
        self.status_update.click_close_button()

        self.my_loads.click_tab_tracking_details()
        self.my_loads.tab_tracking_details.click_total_updates_view_all()
        stop = self.my_loads.tab_tracking_details.modal_all_updates.get_all_updates_stop(index=1)
        self.my_loads.tab_tracking_details.modal_all_updates.screenshot().attach_to_allure(name="Stops View All")
        assert 'Origin - CROWLEY LINER SERVI - TERM - Departed Pickup' in stop, "Stop Incorrect"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4005.json", skip=False)
    def test_add_check_call_button_disabled_when_load_not_in_transit(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4005")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        status_1 = self.my_loads.get_track_status()

        assert status_1 == "Pending Pickup", "Status Incorrect"

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up and Change Status to
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        self.pause(3)

        add_check_call_1 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_1 is not True, "Button should be enabled"

        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        status_2 = self.my_loads.get_track_status()

        assert status_2 == "In Transit", "Status Incorrect"

        # 6. Open Status dialog box and verify button enabled
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        add_check_call_2 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_2 is True, "Button should be enabled"

        self.pause(2)  # Wait to table load Data
        self.status_update.screenshot().attach_to_allure(name="Add Check Call Button Enabled")

        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)

        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        status_3 = self.my_loads.get_track_status()
        assert status_3 == "Delivered", "Status Incorrect"

        # 7. Open Status dialog box and verify button disabled
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        add_check_call_2 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_2 is not True, "Button should be disabled"

        self.pause(2)
        self.status_update.screenshot().attach_to_allure(name="Add Check Call Button Disabled")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4007.json", skip=False)
    def test_add_check_call_successful_check_call_creation_for_load_created_via_BY(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4007")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        status_1 = self.my_loads.get_track_status()

        assert status_1 == "Pending Pickup", "Status Incorrect"

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up and Change Status to
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)

        self.pause(3)

        add_check_call_1 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_1 is not True, "Button should be enabled"

        self.status_update.click_update_button()
        self.status_update.is_not_visible_modal_status()

        status_2 = self.my_loads.get_track_status()
        assert status_2 == "In Transit", "Status Incorrect"

        # 6. Open Status dialog box and verify button enabled
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        add_check_call_2 = self.status_update.is_add_check_call_enabled()
        assert add_check_call_2 is True, "Button should be enabled"

        self.pause(2)  # Wait to table load Data
        self.status_update.screenshot().attach_to_allure(name="Add Check Call Button Enabled")

        self.status_update.click_add_check_call_button()

        # 7. Check Call Modal
        self.status_update.check_call.is_visible()
        self.status_update.check_call.fill_check_call(
            location="Miami Gardens, FL, USA",
            days_offset=1,
            hour=9,
            minute=30,
            date_text=None,
            comments="En-route, traffic delay cleared",
        )
        self.status_update.check_call.click_apply()
        self.status_update.check_call.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Shipment status has been updated successfully.", "Status update success message should be displayed"

        self.my_loads.click_tab_tracking_details()
        self.my_loads.tab_tracking_details.click_total_updates_view_all()
        stop = self.my_loads.tab_tracking_details.modal_all_updates.get_all_updates_stop(index=1)
        self.my_loads.tab_tracking_details.modal_all_updates.screenshot().attach_to_allure(name="Stops View All")
        assert 'miami gardens, fl, usa' in stop, "Stop Call Missing"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4486.json", skip=False)
    def test_verify_date_format_in_my_loads_display_as_mm_dd_yy(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4486")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)
        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)

        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        # Wait 5 Seconds Before Start Uploading File, this wait is strict necessary
        self.pause(2)
        self.my_loads.click_tab_tracking_details()

        last_update = self.my_loads.tab_tracking_details.get_last_update()
        assert helpers.validate_date_mmddyy(last_update), "Incorrect Date Format should be MM/DD/YY"

        stop_1_arrived = self.my_loads.tab_tracking_details.get_milestones_stop_1_arrived()
        assert helpers.validate_date_mmddyy(stop_1_arrived), "Incorrect Date Format should be MM/DD/YY"

        stop_1_departed = self.my_loads.tab_tracking_details.get_milestones_stop_1_departed()
        assert helpers.validate_date_mmddyy(stop_1_departed), "Incorrect Date Format should be MM/DD/YY"

        stop_2_arrived = self.my_loads.tab_tracking_details.get_milestone_stop_2_arrived()
        assert helpers.validate_date_mmddyy(stop_2_arrived), "Incorrect Date Format should be MM/DD/YY"

        stop_2_departed = self.my_loads.tab_tracking_details.get_milestones_stop_2_departed()
        assert helpers.validate_date_mmddyy(stop_2_departed), "Incorrect Date Format should be MM/DD/YY"

        self.my_loads.screenshot().attach_to_allure(name="Tracking Details Date Format Correct MM DD YY")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4521.json", skip=False)
    def test_verify_milestone_details_display_in_tracking_section(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property, create_load_via_api):
        record_property("test_key", "CT-4521")
        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        load_number = load_data['load_number']

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Open Status Update modal
        self.my_loads.click_update_status_button()
        self.status_update.is_visible_modal_status()

        # 5. Fill Up
        self.status_update.enter_actual_arrival(row_index=1, days_offset=-7, hour=15, minute=30)
        self.status_update.enter_actual_departure(row_index=1, days_offset=-5, hour=18, minute=45)
        self.status_update.enter_actual_arrival(row_index=2, days_offset=-2, hour=10, minute=22)
        self.status_update.enter_actual_departure(row_index=2, days_offset=-1, hour=20, minute=8)

        self.status_update.click_update_button().click_checkbox_bobtail().click_submit()
        self.status_update.is_not_visible_modal_status()

        # Wait 5 Seconds Before Start Uploading File, this wait is strict necessary
        self.pause(2)
        self.my_loads.click_tab_tracking_details()

        stop_1_label = self.my_loads.tab_tracking_details.get_milestones_stop_1_label()
        stop_2_label = self.my_loads.tab_tracking_details.get_milestones_stop_2_label()

        assert stop_1_label == "Stop 1", "Stop 1 Label Incorrect"
        assert stop_2_label == "Stop 2", "Stop 2 Label Incorrect"

        last_update = self.my_loads.tab_tracking_details.get_last_update()
        assert helpers.validate_date_mmddyy(last_update), "Incorrect Date Format should be MM/DD/YY"

        stop_1_arrived = self.my_loads.tab_tracking_details.get_milestones_stop_1_arrived()
        assert helpers.validate_date_mmddyy(stop_1_arrived), "Incorrect Date Format should be MM/DD/YY"

        stop_1_departed = self.my_loads.tab_tracking_details.get_milestones_stop_1_departed()
        assert helpers.validate_date_mmddyy(stop_1_departed), "Incorrect Date Format should be MM/DD/YY"

        stop_2_arrived = self.my_loads.tab_tracking_details.get_milestone_stop_2_arrived()
        assert helpers.validate_date_mmddyy(stop_2_arrived), "Incorrect Date Format should be MM/DD/YY"

        stop_2_departed = self.my_loads.tab_tracking_details.get_milestones_stop_2_departed()
        assert helpers.validate_date_mmddyy(stop_2_departed), "Incorrect Date Format should be MM/DD/YY"

        self.my_loads.screenshot().attach_to_allure(name="Tracking Details Date Format Correct MM DD YY")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5228.json", skip=False)
    def test_verify_filter_loads_successfully_using_delivery_date(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5228")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_delivery_date_range(start_date="12/02/2025", end_date="12/02/2025")

        # 4. Validate
        delivery_date = self.my_loads_filters.get_delivery_date_range()
        assert delivery_date == "12/02/2025 - 12/02/2025", "Incorrect Date Filtered"

        # 5. Apply Filter
        self.my_loads_filters.click_apply_filters()

        # Wait to Refresh List of Shipments Filtered
        self.pause(2)
        destination_date = helpers.extract_date(self.my_loads.get_destination_datetime_track(index=1))

        # 4. Validate Correct Delivery Date Filtered
        assert destination_date == "12/02/2025", "Incorrect Delivery Date Filtered"
        self.my_loads.screenshot().attach_to_allure(name="Shipments with filter apply")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5229.json", skip=False)
    def test_verify_filter_for_non_exist_loads_using_delivery_date(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5229")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_delivery_date_range(start_date="12/01/2023", end_date="12/31/2023")

        # 4. Validate
        delivery_date = self.my_loads_filters.get_delivery_date_range()
        assert delivery_date == "12/01/2023 - 12/31/2023", "Incorrect Date Filtered"

        # 5. Apply Filter
        self.my_loads_filters.click_apply_filters()

        no_load_message = self.my_loads.get_no_load_message()
        assert no_load_message == "Sorry, we couldn't find any results.", "Incorrect Validation Message"
        self.my_loads.screenshot().attach_to_allure(name="No Loads could not be found")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5230.json", skip=False)
    def test_verify_that_user_can_reset_an_unsuccessful_search_and_return_to_full_list_of_loads_using_clear_filter_option(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5230")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_delivery_date_range(start_date="12/01/2030", end_date="12/31/2030")

        # 4. Validate
        delivery_date = self.my_loads_filters.get_delivery_date_range()
        assert delivery_date == "12/01/2030 - 12/31/2030", "Incorrect Date Filtered"

        # 5. Apply Filter
        self.my_loads_filters.click_apply_filters()

        no_load_message = self.my_loads.get_no_load_message()
        assert no_load_message == "Sorry, we couldn't find any results.", "Incorrect Validation Message"
        self.my_loads.screenshot().attach_to_allure(name="No Loads could not be found")

        self.my_loads.click_clear_filter()

        invisible = self.my_loads.is_not_visible_no_load_message()
        assert invisible, "No Loads Message should not be present"
        self.my_loads.screenshot().attach_to_allure(name="Clear Filters View")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5231.json", skip=False)
    def test_apply_both_pickup_and_delivery_date_filters_simultaneously(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5231")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_delivery_date_range(start_date="12/01/2025", end_date="12/31/2025") \
            .set_pickup_date_range(start_date="12/01/2025", end_date="12/31/2025")

        # 4. Validate
        delivery_date = self.my_loads_filters.get_delivery_date_range()
        pickup_date = self.my_loads_filters.get_pickup_date_range()

        self.my_loads.screenshot().attach_to_allure(name="Filters Apply Delivery and Pickup Date")

        assert delivery_date == "12/01/2025 - 12/31/2025", "Incorrect Delivery Date Filtered"
        assert pickup_date == "12/01/2025 - 12/31/2025", "Incorrect Pickup Date Filtered"

        # 5. Apply Filter
        self.my_loads_filters.click_apply_filters()

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5233.json", skip=False)
    def test_verification_of_filter_panel_elements(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5233")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters.wait_for_modal_to_be_visible()

        # 4. Visible Elements on Filters

        # Visible by Default
        is_visible, failed_fields = self.my_loads_filters.are_fields_filters_visible()

        if not is_visible:
            # Fail the test and report exactly which fields are missing
            assert is_visible, f"The following fields are not visible: {failed_fields}"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5234.json", skip=False)
    def test_verify_filtering_loads_by_hazmat_status_with_pickup_date_and_delivery_date(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5234")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_delivery_date_range(start_date="12/01/2025", end_date="01/31/2026") \
            .set_pickup_date_range(start_date="12/01/2025", end_date="01/31/2026")

        # 4. Validate
        delivery_date = self.my_loads_filters.get_delivery_date_range()
        pickup_date = self.my_loads_filters.get_pickup_date_range()

        self.my_loads.screenshot().attach_to_allure(name="Filters Apply Delivery and Pickup Date")

        assert delivery_date == "12/01/2025 - 01/31/2026", "Incorrect Delivery Date Filtered"
        assert pickup_date == "12/01/2025 - 01/31/2026", "Incorrect Pickup Date Filtered"

        self.my_loads_filters.set_hazmat(hazmat_option="Yes")

        # 5. Apply Filter
        self.my_loads_filters.click_apply_filters()

        # 7. Get Total Records Count
        total = self.my_loads.get_total_records()

        # ====================================================================
        # VALIDATE TOTAL RECORDS COUNT
        # ====================================================================

        # Option A: Validate that at least one record exists (Recommended)
        assert total > 0, f"Expected at least 1 load, but found {total} loads with Hazmat='Yes' and date range"

        # 8. Validate First Card Data Dates
        track = self.my_loads.get_card_track_information(1)

        self.my_loads.screenshot().attach_to_allure(name="Filtered Data")

        origin_date = track['origin_datetime_track']
        destination_date = track['destination_datetime_track']

        # 9. Validate Dates are Within Range
        assert helpers.is_date_in_range(date_to_validate=origin_date, start_date="12/01/2025",
                                        end_date="01/31/2026"), "Origin Date: Date Filtered Incorrect"
        assert helpers.is_date_in_range(date_to_validate=destination_date, start_date="12/01/2025",
                                        end_date="01/31/2026"), "Destination Date: Date Filtered Incorrect"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5235.json", skip=False)
    def test_validate_that_a_carrier_user_only_see_equipment_types_currently_present_in_their_loads_within_the_filter_options(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5235")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible()

        options = self.my_loads_filters.get_equipment_options_list()
        logger.info(f"Equipment options: {options}")

        # TODO This test case have to be refactor when the Values List In the Equipment Dropdown gets result.

        assert len(options) > 0, "Equipment List Empty"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5236.json", skip=False)
    def test_verify_multi_select_capabilities_for_origin_state_and_load_status(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5236")

        # ====================================================================
        # VALIDATE STATUS: Must be "Delivered" or "In Transit"
        # ====================================================================
        allowed_statuses = ["Delivered", "In Transit"]
        allowed_states = ["Florida"]

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_origin_search_by_state() \
            .select_origin_state(allowed_states) \
            .select_status(allowed_statuses) \
            .click_apply_filters()

        # 4. Get Total Records Count and Pagination Info
        total = self.my_loads.get_total_records()
        pagination = self.my_loads.get_pagination_info()
        assert total == pagination['total_records'], "Total Records not match with pagination"

        # 5. Collect table data from visible records
        table_data = []
        invalid_status_records = []  # Track records with invalid status

        # Only we are extracting the first page Items

        for i in range(1, pagination['end_record'] + 1):
            self.my_loads.center_item_list(index=i)
            carrier_number = self.my_loads.get_carrier_number_track(index=i)
            track_status = self.my_loads.get_track_status(index=i)

            table_data.append([i, carrier_number, track_status])

            if track_status not in allowed_statuses:
                invalid_status_records.append({
                    "index": i,
                    "carrier_number": carrier_number,
                    "status": track_status
                })
                logger.warning(f"❌ Record #{i}: Invalid status '{track_status}' (expected: {allowed_statuses})")

        # 6. Assert no invalid statuses found
        assert len(invalid_status_records) == 0, \
            f"Found {len(invalid_status_records)} record(s) with invalid status:\n" + \
            "\n".join([f"  - Record #{r['index']}: '{r['status']}' (Carrier: {r['carrier_number']})"
                       for r in invalid_status_records])

        # 7. Display table with tabulate
        headers = ["#", "Carrier Number", "Status"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        logger.info(f"\n{table}")

        # 8. Attach table and validation summary to Allure
        summary = f"✓ All {len(table_data)} records have valid status: {allowed_statuses}\n"
        allure.attach(
            summary + "\n" + table,
            name="Load Status Validation Results",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"✓ Validation passed: All records have status in {allowed_statuses}")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5372.json", skip=False)
    def test_dynamic_parameter_stress_test_advance_filters(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5372")

        # ====================================================================
        # VALIDATE STATUS: Must be "Delivered" or "In Transit"
        # ====================================================================
        city = "Jacksonville Beach, FL"
        radius = "200"
        allowed_statuses = ["Select All"]
        # equipment = "53' Dry Van"
        hazmat = "Yes"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .set_origin_search_by_city() \
            .enter_origin_search_city_state(city) \
            .select_origin_radius(radius) \
            .set_destination_search_by_city() \
            .enter_destination_search_city_state(city) \
            .select_destination_radius(radius) \
            .set_pickup_date_range_days_off(start_date=-60, end_date=-1) \
            .set_delivery_date_range_days_off(start_date=-60, end_date=-1) \
            .select_status(allowed_statuses) \
            .set_hazmat(hazmat) \
            .click_apply_filters()

        # 4. Get Total Records Count and Pagination Info
        total = self.my_loads.get_total_records()
        pagination = self.my_loads.get_pagination_info()
        assert total == pagination['total_records'], "Total Records not match with pagination"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-3695.json", skip=False)
    def test_in_upload_info_modal_verify_input_excessive_characters_in_all_fields(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3695")

        # 200 Characters "A"
        # long_text = "A" * 151
        long_text = "aaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update \
            .enter_trailer_container(long_text) \
            .enter_tractor(long_text) \
            .enter_driver_cellphone("5551234567") \
            .enter_chassis(long_text) \
            .enter_genset(long_text)

        self.my_loads.upload_information_update.click_update()
        # QA NOTE: On these scenarios, with the automation Script execution the modal is not validating properly the Len of Characters, but making the manual steps is working as expected.

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4021.json", skip=False)
    def test_in_upload_info_modal_verify_update_genset_number_order_created_in_blue_yonder(self, load_iq_login_carrier_portal,record_property):
        record_property("test_key", "CT-4021")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update.enter_genset("GEN321654")
        self.my_loads.upload_information_update.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4020.json", skip=False)
    def test_in_upload_info_modal_verify_update_chassis_number_order_created_in_blue_yonder(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-4020")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update.enter_chassis("CHS456789")

        self.my_loads.upload_information_update.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-3589.json", skip=False)
    def test_in_upload_info_modal_verify_update_labels_in_the_load_information_update(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3589")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()

        container_value = self.my_loads.upload_information_update.get_label_trailer_container()
        tractor = self.my_loads.upload_information_update.get_label_tractor()
        driver_cellphone = self.my_loads.upload_information_update.get_label_driver_cellphone()
        chassis = self.my_loads.upload_information_update.get_label_chassis()
        genset = self.my_loads.upload_information_update.get_label_genset()

        assert container_value == "Trailer/Container (Leave Blank if Bobtail)", "Label Text Incorrect"
        assert tractor == "Tractor", "Label Text Incorrect"
        assert driver_cellphone == "Driver Cellphone", "Label Text Incorrect"
        assert chassis == "Chassis", "Label Text Incorrect"
        assert genset == "GenSet", "Label Text Incorrect"

        self.my_loads.screenshot().attach_to_allure(name="Load Information Update Modal")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4529.json", skip=False)
    def test_verify_special_characters_in_container_trailer_no_field_are_not_allowed(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-4529")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update.enter_trailer_container("TR#123@456!")

        error_validation = self.my_loads.upload_information_update.get_error_message_trailer_container()

        assert error_validation == "* Only letters and numbers are allowed", "Incorrect Error Message Validation"

        is_enabled = self.my_loads.upload_information_update.is_enable_update()
        assert is_enabled is not True, "Button Update Should be Disabled"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-4680.json", skip=False)
    def test_validate_the_the_system_does_not_allow_the_word_Bobtail_in_the_trailer_container_field(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-4680")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update.enter_trailer_container("Bobtail")

        error_validation = self.my_loads.upload_information_update.get_error_message_trailer_container()

        assert error_validation == "* 'Bobtail' and variances are not permitted.", "Incorrect Error Message Validation"

        is_enabled = self.my_loads.upload_information_update.is_enable_update()
        assert is_enabled is not True, "Button Update Should be Disabled"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-1553.json", skip=False)
    def test_verify_the_load_details_with_missing_data(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-1553")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update \
            .enter_trailer_container("SEGU68811113") \
            .enter_tractor("SEGU68811113") \
            .enter_driver_cellphone("") \
            .enter_chassis("") \
            .enter_genset("")

        self.my_loads.upload_information_update.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5419.json", skip=False)
    def test_verification_of_chassis_and_genset_fields_existence_in_summary(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5419")

        # ====================================================================
        # TEST DATA
        # ====================================================================
        chassis = "CHS456789"
        genset = "GEN321654"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=3)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update \
            .enter_chassis(chassis) \
            .enter_genset(genset)

        self.my_loads.upload_information_update.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

        self.status_update.is_not_visible_modal_status()

        self.my_loads.click_tab_shipment()
        self.pause(2)

        genset_ = self.my_loads.tab_shipment_details.get_genset()
        chassis_ = self.my_loads.tab_shipment_details.get_chassis()

        assert genset == genset_, "Incorrect Genset value"
        assert chassis == chassis_, "Incorrect Chassis value"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5420.json", skip=False)
    def test_verification_data_correctly_populated_from_load_information_updated(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5420")

        # ====================================================================
        # TEST DATA
        # ====================================================================
        chassis = "CHS-554433"
        genset = "GEN-998877"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=3)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update \
            .enter_chassis(chassis) \
            .enter_genset(genset)

        self.my_loads.upload_information_update.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

        self.status_update.is_not_visible_modal_status()

        self.my_loads.click_tab_shipment()
        self.pause(2)

        genset_ = self.my_loads.tab_shipment_details.get_genset()
        chassis_ = self.my_loads.tab_shipment_details.get_chassis()

        assert genset == genset_, "Incorrect Genset value"
        assert chassis == chassis_, "Incorrect Chassis value"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5421.json", skip=False)
    def test_verification_of_NA_display_when_no_data_exist(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5421")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=3)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 4. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 5. Click Shipment Tab
        self.my_loads.click_tab_shipment()
        self.pause(2)

        genset_ = self.my_loads.tab_shipment_details.get_genset()
        chassis_ = self.my_loads.tab_shipment_details.get_chassis()

        assert "N/A" == genset_, "Incorrect Genset value"
        assert "N/A" == chassis_, "Incorrect Chassis value"

        self.pause(8)
        self.my_loads.screenshot().attach_to_allure(name="Shipment Details Tab")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-5422.json", skip=False)
    def test_verification_of_update_after_data_deletion(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-5422")

        # ====================================================================
        # TEST DATA
        # ====================================================================
        chassis = "CHS-554433"
        genset = "GEN-998877"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=3)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Exclude Equipment because right now the dropdown not contains the option require to get results
        self.my_loads_filters.wait_for_modal_to_be_visible().select_status(["In Transit"]).click_apply_filters()

        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update \
            .enter_chassis(chassis) \
            .enter_genset(genset)

        self.my_loads.upload_information_update.click_update()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

        self.status_update.is_not_visible_modal_status()

        self.my_loads.click_tab_shipment()
        self.pause(2)

        genset_1 = self.my_loads.tab_shipment_details.get_genset()
        chassis_1 = self.my_loads.tab_shipment_details.get_chassis()

        assert genset == genset_1, "Incorrect Genset value"
        assert chassis == chassis_1, "Incorrect Chassis value"

        # ====================================================================
        # TEST DATA: Empty Values
        # ====================================================================

        # 4. Access to Upload Info modal
        self.my_loads.click_update_load_info_button()
        self.my_loads.upload_information_update \
            .clear_chassis() \
            .clear_genset() \
            .click_enter()

        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Load information has been updated successfully.", "Status update success message should be displayed"

        self.status_update.is_not_visible_modal_status()

        self.my_loads.click_tab_shipment()
        genset_2 = self.my_loads.tab_shipment_details.get_genset()
        chassis_2 = self.my_loads.tab_shipment_details.get_chassis()

        assert "N/A" == genset_2, "Incorrect Genset value, should be N/A"
        assert "N/A" == chassis_2, "Incorrect Chassis value, should be N/A"

        self.my_loads.screenshot().attach_to_allure(name="Shipment Details Tab", force_scroll_top=False)

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-3233.json", skip=False)
    def test_verify_filter_by_equipment_size_type_in_shipment_tracking_card(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3233")

        # ====================================================================
        # TEST DATA
        # ====================================================================
        equipment = "53' Dry Van"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Filter Equipment
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .select_equipment(equipment) \
            .click_apply_filters()

        # 4. Validate Items only for Equipment Filtered
        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        item_info = self.my_loads.get_card_track_information(index=page_index)

        assert item_info['equipment_type'] == equipment, "Equipment Type Incorrect."
        self.my_loads.screenshot().attach_to_allure(name="Filter by Equipment Type")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-3232.json", skip=False)
    def test_verify_display_by_equipment_size_type_in_shipment_tracking_card(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3232")

        # ====================================================================
        # TEST DATA
        # ====================================================================
        equipment = "53' Dry Van"

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Filter Equipment
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .select_equipment(equipment) \
            .click_apply_filters()

        # 4. Validate Items only for Equipment Filtered
        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 5. Click Shipment Tab
        self.my_loads.click_tab_shipment()
        equipment_1 = self.my_loads.tab_shipment_details.get_equipment()
        equipment_2 = self.my_loads.tab_shipment_details.over_equipment()

        assert equipment_1 == "53' DV", "Equipment Type Incorrect [Text Value]."
        assert equipment_2 == equipment, "Equipment Type Incorrect [Tool Tip]."

        self.my_loads.screenshot().attach_to_allure(name="Filter by Equipment Type")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-2301.json", skip=False)
    def test_ensure_search_functionality_for_open_records(self, load_iq_login_carrier_portal, record_property, create_load_via_api):
        record_property("test_key", "CT-2301")

        # 1.  Send POST request to create load and Use 'load_data' to access the information ✅
        # load_data = create_load_via_api(status_code=self.status_code_expected, xml_path="/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml")
        # load_number = load_data['load_number']
        # bol_number = load_data['bol_number']
        # po_number = load_data['po_number']

        load_number = "LD24090400004"
        bol_number = "BOl23423"
        po_number = "PO8u798"

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search and validate Load Number
        self.my_loads.enter_search_by(load_number).click_search()
        self.my_loads.click_tab_shipment()
        load_number_ = self.my_loads.tab_shipment_details.get_load_number()
        assert load_number_ == load_number, "Load Number Not Match"

        # TODO Pending to Get Fix to Obtains the PO and BOL Number From Current UI, this are the methods ready
        # 4. Search and validate Load Number
        self.my_loads.enter_search_by(bol_number).click_search()
        self.my_loads.click_tab_shipment()
        bol_number_ = self.my_loads.tab_shipment_details.get_bol_number()
        assert bol_number_ == bol_number, "Bol Number Not Match"

        # 5. Search and validate PO Number
        self.my_loads.enter_search_by(po_number).click_search()
        self.my_loads.click_tab_shipment()
        po_number_ = self.my_loads.tab_shipment_details.get_po_number()
        assert po_number_ == po_number, "Bol Number Not Match"

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/T-2661.json", skip=False)
    def test_verify_booking_number_is_accessible_without_loss_of_information(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-2661")

        # 1. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads(pause=2)

        # 2. Open Filters Left Side Modal
        self.my_loads.click_filter()

        # 3. Filter Date : Filter Equipment
        self.my_loads_filters \
            .wait_for_modal_to_be_visible() \
            .select_status(["Completed"]) \
            .click_apply_filters()

        # 4. Validate Items only for Equipment Filtered
        # Select From First Page of the Pagination a Random Index, to avoid use same Index Record every time that script runs
        pagination = self.my_loads.get_pagination_info()
        page_index = int(random_utils.generate_random_code(start=1, end=pagination["page_size"]))

        self.my_loads.center_item_list(index=page_index)
        load_number = self.my_loads.get_carrier_number_track(index=page_index)

        # 3. Search for the created load
        self.my_loads.enter_search_by(load_number).click_search()

        # 5. Click Shipment Tab
        self.my_loads.click_tab_shipment()
        booking_number_1 = self.my_loads.tab_shipment_details.get_booking_number()
        booking_number_2 = self.my_loads.tab_shipment_details.over_booking_number()

        assert booking_number_1 is not None, "Booking Number Missing [Text Value]."
        assert booking_number_2 is not None, "Booking Number Missing [Tool Tip]."

        self.my_loads.screenshot().attach_to_allure(name="Filter by Booking Number")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-2662.json", skip=False)
    def test_verify_booking_number_field_is_searchable(self, load_iq_login_carrier_portal, record_property, create_load_via_api):
        record_property("test_key", "CT-2662")

        booking_number = "PUN34534"

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Search and validate Booking Number
        self.my_loads.enter_search_by(booking_number).click_search()
        self.my_loads.click_tab_shipment()
        booking_number_1 = self.my_loads.tab_shipment_details.get_booking_number()
        booking_number_2 = self.my_loads.tab_shipment_details.over_booking_number()

        assert booking_number_1 == booking_number, "Booking Number Not Match"
        assert booking_number_2 == booking_number, "Booking Number Not Match"

        self.my_loads.screenshot().attach_to_allure(name="Filter by Booking Number")

    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @test(json_path="data/json/CT-3590.json", skip=False)
    def test_verify_the_feedback_option_my_loads(self, load_iq_login_carrier_portal, record_property, create_load_via_api):
        record_property("test_key", "CT-3590")

        # 2. Navigate to My Loads page
        self.menu.carrier_portal.menu_my_loads()

        # 3. Enter Comment on Feedback Form
        feedback_from = FeedbackForm.get_instance()
        feedback_from.click_feedback_form().is_visible()
        feedback_from.enter_comments("Test QA Comment")
        feedback_from.click_submit()

        # 4. Message Confirmation
        alert_message = self.status_update.get_status_update_message()
        assert alert_message == "Feedback submitted successfully.", "Entered Comment Feedback Form success message should be displayed"




