import json
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.my_loads.MyLoadsPage import MyLoadsPage
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint
from applications.web.loadiq.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers


logger = setup_logger('TestAccessorialsFlat')

@pytest.mark.web
@loadiq
class TestAccessorialsFlat(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    accessorials = MyLoadsPage.get_instance()
    submit_load_endpoint = SubmitLoadEndpoint.get_instance()

    @classmethod
    def setup_class(self):
        # Load test data once for the entire class
        xml_path = "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        self.load_number = response_dict['data']['loadNumber']
        assert result.status_code == 200

    @test(test_case_id="CT-3053", test_description="Verify it's possible to add an flat accessorial - Origin Detention", feature="Accessorial", skip=False)
    def test_my_loads_accessorials_flat_origin(self, load_iq_login_carrier_portal):


        #Navigate to the "My Loads" page in the Carrier Portal
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        #"Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        #Validate that the load was found (the "not found" message should not appear)
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Origin Detention",
            rates="12",
            comments="test",
        )
        self.accessorials.request_accessorials.click_submit()
        #Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        # Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()

    @test(test_case_id="CT-3128", test_description="Verify it's possible to add an flat accessorial - Destination Detention", feature="Accessorial", skip=False)
    def test_my_loads_accessorials_flat_detention(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        # "Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        # Validates the load search result via text UI.
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Destination Detention",
            rates="12",
            comments="test",
        )
        self.accessorials.request_accessorials.click_submit()
        # Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        # Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()

    @test(test_case_id="CT-3129", test_description="Verify it's possible to add an flat accessorial - Lumper", feature="Accessorial", skip=False)
    def test_my_loads_accessorials_flat_lumper(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        # "Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        # Validates the load search result via text UI.
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Lumper",
            rates="12",
            comments="test",
        )
        self.accessorials.request_accessorials.click_submit()
        # Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        # Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()

    @test(test_case_id="CT-3130", test_description="Verify it's possible to add an flat accessorial - Driver Assist", feature="Accessorial", skip=False)
    def test_my_loads_accessorials_flat_assist(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        # "Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        # Validates the load search result via text UI.
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Driver Assist",
            rates="12",
            comments="test",
        )
        self.accessorials.request_accessorials.click_submit()
        # Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        # Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()

    @test(test_case_id="CT-3131", test_description="Verify it's possible to add an flat accessorial - Layover", feature="Accessorial", skip=False)
    def test_my_loads_accessorials_flat_layover(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        # "Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        # Validates the load search result via text UI.
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Layover",
            rates="12",
            comments="test",
        )
        self.accessorials.request_accessorials.click_submit()
        # Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        # Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()

    @test(test_case_id="CT-3132", test_description="Verify it's possible to add an flat accessorial - Other", feature="Accessorial", skip=False)
    def test_my_loads_accessorials_flat_other(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        # "Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        # Validates the load search result via text UI.
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Other",
            rates="12",
            comments="test",
        )
        self.accessorials.request_accessorials.click_submit()
        # Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        # Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()

    @test(test_case_id="CT-2305", test_description="Verify it's possible to add an flat accessorial+attachedfile",feature="Accessorial", skip=False)
    def test_my_loads_attached_file(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.accessorials.load_page()
        # "Search a valid load"
        self.accessorials.enter_search_by(search_by=self.load_number)
        self.accessorials.click_search()
        # Validates the load search result via text UI.
        actual_message = self.accessorials.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # "Open accessorial page and creates a new accessorial"
        self.accessorials.request_accessorials.click_generate_accessorial()
        self.accessorials.request_accessorials.click_flat_rate()
        self.accessorials.request_accessorials.enter_accessorials_items_flat(
            dropdown="Other",
            rates="12",
            comments="test",
        )
        # "Open accessorial page and add a new file"
        self.accessorials.request_accessorials.click_upload()
        self.accessorials.request_accessorials.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )
        self.accessorials.request_accessorials.click_submit()
        # Validate the confirmation message(pop-up) after request submission.
        expected_message_confirmation = "Your Accessorial has been successfully submitted. It has been sent to the shipper for Approval."
        actual_message = self.accessorials.validate_accessorial_popup()
        assert expected_message_confirmation in actual_message, f"Expected success message not found. Found: '{actual_message}'"
        #Close the confirmation popup
        self.accessorials.request_accessorials.click_popup_ok()
