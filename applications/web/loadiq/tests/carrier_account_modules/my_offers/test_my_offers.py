from time import sleep

import allure
import json

from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.my_loads.MyLoadsPage import MyLoadsPage
from applications.web.loadiq.pages.my_payments.MyPaymentsPage import MyPaymentsPage
from core.utils.json_data_helper import JSONDataHelper
from applications.web.loadiq.pages.my_offers.MyOffersDetailsPage import MyOffersDetailsPage
from applications.web.loadiq.pages.my_offers.MyOffersPage import MyOffersPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.helpers import generate_future_date
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint

logger = setup_logger('TestMyOffers')

@pytest.mark.web
@loadiq

class TestCarrierMyOffers(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    my_offers = MyOffersPage.get_instance()
    my_loads = MyLoadsPage.get_instance()
    my_offers_details = MyOffersDetailsPage.get_instance()
    my_payments = MyPaymentsPage.get_instance()
    submit_load_endpoint = SubmitLoadEndpoint.get_instance()

    @allure.step("{step_name}")
    def take_screenshot(self, step_name: str):
        """Helper method to take screenshots with Allure"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Screenshot - {step_name}",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.title('Verify that the Expedite field is displayed in My Offers list view')
    @allure.description(
        "Verifies that when a offer created with the Expedite field is displayed in the My Offers list view")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3942", name="Jira")
    @allure.testcase("CT-3942")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3942", test_description="Verify that the Expedite field is displayed in My Offers list view",
          feature="MyOffersDetails", skip=False)
    def test_expedite_field_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3942")
        self.take_screenshot("Carrier User Logged In")
        path = "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json"
        test_data = JSONDataHelper.load_json_data(path, "CT-3942")

        # 1. User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User search for the load offer created by the customer (Load ID: LD25080700007)
        self.my_offers.enter_search_by(test_data["shipment_id"])
        # 3. Click in the Search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Results Displayed")
        # 4. Verifying that the Expedite checkbox is displayed in the shipment
        actual_result = self.my_offers.is_expedite_checked(test_data["shipment_id"])
        assert actual_result is True, "Expedite checkbox is not checked in the My Offers list view"
        self.take_screenshot("Validate Expedite Checkbox is Checked in My Offers List View")

    @allure.title('Verify that the Hazmat details are displayed in My Offers Details page')
    @allure.description(
        "Verifies that when a offer created with the Hazmat details are displayed in the My Offers Details page")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3766", name="Jira")
    @allure.testcase("CT-3766")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3766", test_description="Validate display of Proper Shipping Name in Hazmat details for Carrier user in My Offers",
          feature="MyOffersDetails", skip=False)
    def test_hazmat_details_in_my_offers(self, load_iq_login_carrier_portal, record_property): #DEPENDENCY CT-2054
        record_property("test_key", "CT-3766")
        self.take_screenshot("Carrier User Logged In")
        test_data = JSONDataHelper.load_json_data("applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json", "CT-3766")

        # 1. User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User search for the load offer created by the customer (Load ID: LD25080700007)
        self.my_offers.enter_search_by(test_data["shipment_id"])
        # 3. Click in the Search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Results Displayed")
        # 4. Click on the Shipment ID link to open the My Offers Details page
        self.my_offers.click_accept_reject_button(test_data["shipment_id"])
        self.take_screenshot("Validate My Offers Details Page Loaded")
        # 5. Verifying that the Hazmat details are displayed in the My Offers Details page
        expected_user_data = {
            "UN": test_data["un_na_number"],
            "Hazmat Class": test_data["hazmat_class"],
            "Packing Group": test_data["packing_group"],
            "Phone": test_data["hazmat_contact_number"],
            "Proper Shipping Name": test_data["proper_shipping_name"]
        }
        actual_result = self.my_offers_details.get_hazmat_details()
        assert actual_result == expected_user_data, f'Expected Hazmat details {expected_user_data} but got {actual_result}'
        self.take_screenshot("Validate Hazmat Details are Displayed in My Offers Details Page")

    @allure.title('Verify that the Appointment dates are displayed in My Offers Details page')
    @allure.description(
        "Verifies that when a offer created are displayed in the My Offers Details page")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3515", name="Jira")
    @allure.testcase("CT-3515")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3515", test_description="Verify appointment dates are displayed on the card correctly",
          feature="MyOffersDetails", skip=False)
    def test_appointment_dates_in_my_offers(self, load_iq_login_carrier_portal, record_property): #DEPENDENCY CT-2054
        record_property("test_key", "CT-3515")
        self.take_screenshot("Carrier User Logged In")
        test_data = JSONDataHelper.load_json_data("applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json", "CT-3766")

        # 1. User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User search for the load offer created by the customer (Load ID: LD25080700007)
        self.my_offers.enter_search_by(test_data["shipment_id"])
        # 3. Click in the Search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Results Displayed")
        # 4. Click on the Shipment ID link to open the My Offers Details page
        self.my_offers.click_accept_reject_button(test_data["shipment_id"])
        self.take_screenshot("Validate My Offers Details Page Loaded")
        # 5. Verifying that the Appointment dates are displayed in the My Offers Details page
        expected_user_data = {
            "pickup_Date" : generate_future_date(5),
            "delivery_Date" : generate_future_date(10)
        }
        actual_result = self.my_offers_details.get_appointment_dates()

        # Validate that actual result contains all expected fields and values
        # Extract only the date part (before the time) for comparison
        for key, expected_value in expected_user_data.items():
            assert key in actual_result, f"Expected key '{key}' not found in actual result. Actual keys: {list(actual_result.keys())}"

            # Extract date part from actual result (format: "MM/DD/YYYY HH:MM AM/PM" -> "MM/DD/YYYY")
            actual_date = actual_result[key].split()[0] if ' ' in actual_result[key] else actual_result[key]

            assert actual_date == expected_value, f"Expected {key}: '{expected_value}', but got '{actual_date}' (original: '{actual_result[key]}')"

        self.take_screenshot("Validate Appointment Dates are Displayed in My Offers Details Page")

    @allure.title('[UI] Carrier portal - Verify the feedback option (MyOffers)')
    @allure.description(
        "Verifies that feedback option in My Offers page is working")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3587", name="Jira")
    @allure.testcase("CT-3587")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3587", test_description="Verify appointment dates are displayed on the card correctly",
          feature="MyOffersDetails", skip=False)
    def test_feedback_option_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3587")
        self.take_screenshot("Carrier User Logged In")
        test_data = JSONDataHelper.load_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json", "CT-3587")

        # 1. User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User clicks feedback button
        self.my_payments.click_feedback()
        self.take_screenshot("Validate Feedback Form Loaded")
        # 3. User enters comment
        self.my_payments.enter_comment(test_data["feedback_comment"])
        self.take_screenshot("Validate Feedback Comment was entered")
        # 4. User submits feedback to Support Team
        self.my_payments.click_feedback_submit()
        self.take_screenshot("Validate Feedback Submitted")
        # 5. User submits feedback to Support Team
        self.my_payments.validate_feedback_text()
        self.take_screenshot("Validate Feedback Submitted Success Message")

    @allure.title('[UI] Verify financial details (Load Value) are displayed on the card correctly')
    @allure.description(
        "Verifies that Load Value details are displayed on the card correctly")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3517", name="Jira")
    @allure.testcase("CT-3517")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3517", test_description="Verify financial details (Load Value) are displayed on the card correctly",
          feature="MyOffersDetails", skip=False)
    def test_financial_details_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3517")
        self.take_screenshot("Carrier User Logged In")
        test_data = JSONDataHelper.load_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json", "CT-3517")

        # 1. User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(test_data["shipment_id"])
        self.take_screenshot("Validate Shipment Expanded")
        # 3. User verifies Load Value title
        self.my_offers.check_load_value_elements(test_data["shipment_id"])
        self.take_screenshot("Validate Load Value Elements")

    @allure.title('[UI] Verify mid stops are displayed for multistop loads on the card')
    @allure.description(
        "Verifies that mid stops for multistop loads are displayed on the card correctly")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3519", name="Jira")
    @allure.testcase("CT-3519")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3519",
          test_description="Verify that mid stops for multistop loads are displayed on the card correctly",
          feature="MyOffersDetails", skip=False)
    def test_mid_stops_number_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3519")
        xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/multi_stops/no_imdl/2504133003465_LoadTendered_493936.LoadTendered_TestCarrier.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        assert result.status_code == 200
        load_number = response_dict['data']['loadNumber']

        self.take_screenshot("Carrier User Logged In")
        test_data = JSONDataHelper.load_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json", "CT-3519")

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User verifies Load Value title
        self.my_offers.check_mid_stops_number(load_number, test_data["stops_no"])
        self.take_screenshot("Validate Mid Stops Number")

    @allure.title('[UI] Valid Load - Offer Acceptance modal window')
    @allure.description(
        "Verifies accept tender modal window in my offers")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-1084", name="Jira")
    @allure.testcase("CT-1084")
    @allure.feature("My Offers")
    @test(test_case_id="CT-1084",
          test_description="Verifies accept tender modal window in my offers",
          feature="MyOffersDetails", skip=False)
    def test_accept_modal_window_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-1084")
        xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender/LoadTendered_10000162179_Test_Carrier.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        assert result.status_code == 200
        load_number = response_dict['data']['loadNumber']

        self.take_screenshot("Carrier User Logged In")
        test_data = JSONDataHelper.load_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json", "CT-1084")

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Accept
        self.my_offers.click_accept_tender_button(load_number)
        self.take_screenshot("Validate Click Accept Tender Button")
        # 5. User clicks on Accept
        self.my_offers.check_accept_tender_modal_window(test_data["origin"], test_data["destination"])
        self.take_screenshot("Validate Accept Tender Modal Window")

    @allure.title('[UI] Verify BY offer acceptance functionality')
    @allure.description(
        "Verifies accept tender functionality my offers")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3477", name="Jira")
    @allure.testcase("CT-3477")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3477",
          test_description="Verifies accept tender functionality my offers",
          feature="MyOffersDetails", skip=False)
    def test_accept_tender_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3477")
        xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender/LoadTendered_10000162179_Test_Carrier.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        assert result.status_code == 200
        load_number = response_dict['data']['loadNumber']

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Accept
        self.my_offers.click_accept_tender_button(load_number)
        self.take_screenshot("Validate Click Accept Tender Button")
        # 6. User clicks on Accept
        self.my_offers.click_accept_tender_button_modal_window()
        self.take_screenshot("Validate Click Accept Tender Modal Window")
        # 7. Validate success message
        self.my_offers.validate_accept_tender_success_message()
        self.take_screenshot("Validate Accept Tender Success Message")
        # 8. User navigates to My Loads
        self.menu.carrier_portal.menu_my_loads()
        self.take_screenshot("Validate Navigation to My Loads")
        # 9. User searches by load number
        self.my_loads.enter_search_by(load_number)
        self.my_loads.click_search()
        self.take_screenshot("Validate Load Number Search in My Loads")
        #10. User sees load number in My Loads
        self.my_loads.validate_load_present(load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")

    @allure.title('[UI] Valid Load - Offer Rejection')
    @allure.description(
        "Verifies reject tender functionality my offers")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-1410", name="Jira")
    @allure.testcase("CT-1410")
    @allure.feature("My Offers")
    @test(test_case_id="CT-1410",
          test_description="Verifies reject tender functionality my offers",
          feature="MyOffersDetails", skip=False)
    def test_reject_tender_in_my_offers(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-1410")
        xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender/LoadTendered_10000162179_Test_Carrier.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        assert result.status_code == 200
        load_number = response_dict['data']['loadNumber']

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Reject
        self.my_offers.click_reject_tender_button(load_number)
        self.take_screenshot("Validate Click Reject Tender Button")
        # 6. User clicks on Accept
        self.my_offers.click_reject_tender_button_modal_window()
        self.take_screenshot("Validate Click Reject Tender Modal Window")
        # 7. Validate success message
        self.my_offers.validate_reject_tender_success_message()
        self.take_screenshot("Validate Accept Tender Success Message")
        # 8. User searches by load number in the search bar
        self.my_offers.enter_search_by(load_number)
        self.take_screenshot("Validate Search Input")
        # 9. Validate load is not available in my offers
        self.my_offers.no_load_results()
        self.take_screenshot("Validate Search Button")

    @allure.title('[UI] Validate accept invalid address tenders on BY offers')
    @allure.description(
        "Verifies accepting invalid address tender on BY offers")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3478", name="Jira")
    @allure.testcase("CT-3478")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3478",
          test_description="Verifies accepting invalid address tender on BY offers",
          feature="MyOffersDetails", skip=False)
    def test_accept_bad_address_tender_warning_message(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3478")

        ############## Validate Origin Bad Address Load ##############

        # Create the bad origin address load via API
        origin_xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/bad_address/2505253023641_LoadTendered_913773.BadAddressOrigin.xml"
        origin_result = self.submit_load_endpoint.process_load_from_file_upload(origin_xml_path)
        origin_response_dict = json.loads(origin_result.text)
        assert origin_result.status_code == 200
        origin_load_number = origin_response_dict['data']['loadNumber']

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers(1)
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(origin_load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(origin_load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Accept
        self.my_offers.click_accept_tender_button(origin_load_number)
        self.take_screenshot("Validate Click Accept Tender Button")
        # 6. User clicks on Accept
        self.my_offers.click_accept_tender_button_modal_window()
        self.take_screenshot("Validate Click Accept Tender Modal Window")
        # 7. Validate Bad Address Warning Message
        self.my_offers.validate_bad_address_tender_warning_message()
        self.take_screenshot("Validate Bad Address Warning Message")
        # 8. Click Dismiss Button in Bad Address Warning Message
        self.my_offers.click_dismiss_button_bad_address_tender_modal_window()
        self.take_screenshot("Validate Bad Address Dismiss Button Clicked")
        # 9. Validate success message
        self.my_offers.validate_accept_tender_success_message()
        self.take_screenshot("Validate Accept Tender Success Message")
        # 10. User navigates to My Loads
        self.menu.carrier_portal.menu_my_loads(2)
        self.take_screenshot("Validate Navigation to My Loads")
        # 11. User searches by load number
        self.my_loads.enter_search_by(origin_load_number)
        self.my_loads.click_search()
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 12. User sees load number in My Loads
        self.my_loads.validate_load_present(origin_load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")

        ############## Validate Destination Bad Address Load ##############

         # Create the bad origin address load via API
        destination_xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/bad_address/2505253023641_LoadTendered_913773.BadAddressDestination.xml"
        destination_result = self.submit_load_endpoint.process_load_from_file_upload(destination_xml_path)
        destination_response_dict = json.loads(destination_result.text)
        assert destination_result.status_code == 200
        destination_load_number = destination_response_dict['data']['loadNumber']

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers(1)
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(destination_load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(destination_load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Accept
        self.my_offers.click_accept_tender_button(destination_load_number)
        self.take_screenshot("Validate Click Accept Tender Button")
        # 6. User clicks on Accept
        self.my_offers.click_accept_tender_button_modal_window()
        self.take_screenshot("Validate Click Accept Tender Modal Window")
        # 7. Validate Bad Address Warning Message
        self.my_offers.validate_bad_address_tender_warning_message()
        self.take_screenshot("Validate Bad Address Warning Message")
        # 8. Click Dismiss Button in Bad Address Warning Message
        self.my_offers.click_dismiss_button_bad_address_tender_modal_window()
        self.take_screenshot("Validate Bad Address Dismiss Button Clicked")
        # 9. Validate success message
        self.my_offers.validate_accept_tender_success_message()
        self.take_screenshot("Validate Accept Tender Success Message")
        # 10. User navigates to My Loads
        self.menu.carrier_portal.menu_my_loads(2)
        self.take_screenshot("Validate Navigation to My Loads")
        # 11. User searches by load number
        self.my_loads.enter_search_by(destination_load_number)
        self.my_loads.click_search()
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 12. User sees load number in My Loads
        self.my_loads.validate_load_present(destination_load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")

    @allure.title('[UI] Verify bad address icon display for invalid addresses.')
    @allure.description(
        "[UI] Verifies bad address icon display for invalid addresses.")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3479", name="Jira")
    @allure.testcase("CT-3479")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3479",
          test_description="[UI] Verifies bad address icon display for invalid addresses.",
          feature="MyOffersDetails", skip=False)
    def test_accept_bad_address_tender_icon(self, load_iq_login_carrier_portal, record_property):
        record_property("test_key", "CT-3479")

        ############## Validate Origin Bad Address Load ##############

        # Create the bad origin address load via API
        origin_xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/bad_address/2505253023641_LoadTendered_913773.BadAddressOrigin.xml"
        origin_result = self.submit_load_endpoint.process_load_from_file_upload(origin_xml_path)
        origin_response_dict = json.loads(origin_result.text)
        assert origin_result.status_code == 200
        origin_load_number = origin_response_dict['data']['loadNumber']

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers(1)
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(origin_load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(origin_load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Accept
        self.my_offers.click_accept_tender_button(origin_load_number)
        self.take_screenshot("Validate Click Accept Tender Button")
        # 6. User clicks on Accept
        self.my_offers.click_accept_tender_button_modal_window()
        self.take_screenshot("Validate Click Accept Tender Modal Window")
        # 7. Validate Bad Address Warning Message
        self.my_offers.validate_bad_address_tender_warning_message()
        self.take_screenshot("Validate Bad Address Warning Message")
        # 8. Click Dismiss Button in Bad Address Warning Message
        self.my_offers.click_dismiss_button_bad_address_tender_modal_window()
        self.take_screenshot("Validate Bad Address Dismiss Button Clicked")
        # 9. Validate success message
        self.my_offers.validate_accept_tender_success_message()
        self.take_screenshot("Validate Accept Tender Success Message")
        # 10. User navigates to My Loads
        self.menu.carrier_portal.menu_my_loads(2)
        self.take_screenshot("Validate Navigation to My Loads")
        # 11. User searches by load number
        self.my_loads.enter_search_by(origin_load_number)
        self.my_loads.click_search()
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 12. User sees load number in My Loads
        self.my_loads.validate_load_present(origin_load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 13. User opens load in My Loads
        self.my_loads.select_load(origin_load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 14. User validates Origin Bad Address Icon present
        self.my_loads.validate_origin_bad_address_icon_present()
        self.take_screenshot("Validate Origin Bad Address Present")
        # 15. User Moves Over Origin Bad Address Icon present
        self.my_loads.move_over_origin_bad_address_icon()
        self.my_loads.validate_bad_address_tooltip()
        self.take_screenshot("Validate Bad Address Tooltip Present")

        ############## Validate Destination Bad Address Load ##############

         # Create the bad origin address load via API
        destination_xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/bad_address/2505253023641_LoadTendered_913773.BadAddressDestination.xml"
        destination_result = self.submit_load_endpoint.process_load_from_file_upload(destination_xml_path)
        destination_response_dict = json.loads(destination_result.text)
        assert destination_result.status_code == 200
        destination_load_number = destination_response_dict['data']['loadNumber']

        # 1. User navigates to "My Offers" page
        self.menu.carrier_portal.menu_my_offers(1)
        self.take_screenshot("Validate My Offers Page Loaded")
        # 2. User searches by load number in the search bar
        self.my_offers.enter_search_by(destination_load_number)
        self.take_screenshot("Validate Search Input")
        # 3. User clicks on search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Button")
        # 4. User clicks Accept/Reject button
        self.my_offers.click_accept_reject_button(destination_load_number)
        self.take_screenshot("Validate Shipment Expanded")
        # 5. User clicks on Accept
        self.my_offers.click_accept_tender_button(destination_load_number)
        self.take_screenshot("Validate Click Accept Tender Button")
        # 6. User clicks on Accept
        self.my_offers.click_accept_tender_button_modal_window()
        self.take_screenshot("Validate Click Accept Tender Modal Window")
        # 7. Validate Bad Address Warning Message
        self.my_offers.validate_bad_address_tender_warning_message()
        self.take_screenshot("Validate Bad Address Warning Message")
        # 8. Click Dismiss Button in Bad Address Warning Message
        self.my_offers.click_dismiss_button_bad_address_tender_modal_window()
        self.take_screenshot("Validate Bad Address Dismiss Button Clicked")
        # 9. Validate success message
        self.my_offers.validate_accept_tender_success_message()
        self.take_screenshot("Validate Accept Tender Success Message")
        # 10. User navigates to My Loads
        self.menu.carrier_portal.menu_my_loads(2)
        self.take_screenshot("Validate Navigation to My Loads")
        # 11. User searches by load number
        self.my_loads.enter_search_by(destination_load_number)
        self.my_loads.click_search()
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 12. User sees load number in My Loads
        self.my_loads.validate_load_present(destination_load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 13. User opens load in My Loads
        self.my_loads.select_load(destination_load_number)
        self.take_screenshot("Validate Load Number Search in My Loads")
        # 14. User validates Destination Bad Address Icon present
        self.my_loads.validate_destination_bad_address_icon_present()
        self.take_screenshot("Validate Destination Bad Address Present")
        # 15. User Moves Over Destination Bad Address Icon present
        self.my_loads.move_over_destination_bad_address_icon()
        self.my_loads.validate_bad_address_tooltip()
        self.take_screenshot("Validate Bad Address Tooltip Present")