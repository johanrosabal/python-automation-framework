from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.shipment_creation.create_shipment.CreateShipmentPage import CreateShipmentPage
from applications.web.loadiq.pages.shipment_tracking.ShipmentTrackingPage import ShipmentTrackingPage
from core.utils.json_data_helper import JSONDataHelper
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage
from applications.web.loadiq.pages.login.LoginPage import LoginPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test

logger = setup_logger('TestCustomerShipmentCreation')

@pytest.mark.web
@loadiq
class TestCustomerShipmentCreationHazmatTab(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    shipment_creation = ShipmentCreationPage.get_instance()
    create_shipment = CreateShipmentPage.get_instance()
    my_board = MyBoardPage.get_instance()
    tracking = ShipmentTrackingPage.get_instance()
    loadclosed = "LD24091100002"
    loadhazmat = "MC_3001245"
    loadLD = "LD24053000003"

    @pytest.mark.test(test_case_id="CT-4730",test_description="Verify that the hazmat information of a shipment created in Load IQ matches the information displayed in Hazmat Details",feature="Shipment Tracking",skip=False)
    def test_tracking_hazmat_information(self, load_iq_login_customer_portal):
        # Path to the JSON file
        json_path = r"applications/web/loadiq/data/carrier_portal/my_loads/json_data_process.json"
        # Load data from JSON
        test_data = JSONDataHelper.load_json_data(json_path)
        expected_data = test_data["tests"][0]["data"]  # Extract only the relevant data
        # Navigate to the Shipment Tracking module
        self.menu.customer_portal.menu_shipment_tracking()
        self.tracking.enter_search_by(search_by=expected_data["shipment_id"])
        self.tracking.click_search()
        self.tracking.click_hazmat_tab()
        # Get Hazmat information from the UI
        hazmat_info = self.tracking.get_all_hazmat_information()
        # Validate that the data matches
        assert hazmat_info == expected_data, (
            f"\nHazmat data mismatch:\n"
            f"Expected:\n{expected_data}\n"
            f"Actual:\n{hazmat_info}\n"
        )
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-3584", test_description="Customer portal - Verify the feedback option (ShipmentTracking)", feature="Shipment Tracking",skip=False)
    def test_shipment_tracking_feedback(self,load_iq_login_customer_portal):
        # Login User
        # self.login.login_user(CustomerAccounts.TEST_07)
        # 02. Gets shipment tracking Page
        self.menu.customer_portal.menu_shipment_tracking()
        #Send a text and create the feedback
        self.tracking.send_feedback("QA TEST - TESTING FEEDBACK")
        #Confirms the expected label message
        expected_message = "Feedback submitted successfully"
        actual_message = self.tracking.get_feedback_confirmation_message()
        assert expected_message in actual_message, f"Expected feedback confirmation not found. Found: '{actual_message}'"
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-2275", test_description="Verify the load details/Finance on Shipment Tracking (Fuel)",feature="Shipment Tracking", skip=False)
    def test_shipment_tracking_fuel_finance(self,load_iq_login_customer_portal):
        self.menu.customer_portal.menu_shipment_tracking()
        self.tracking.enter_search_by(search_by=self.loadLD)
        self.tracking.click_search()
        self.tracking.click_finance_details_tab()
        fuel_info = self.tracking.get_fuel_info()
        assert fuel_info["label"] == "Fuel", f"Expected text: 'Fuel', but got '{fuel_info['label']}'"
        assert fuel_info["value"] == "$0.00", f"Expected value:' $0.00 ', but got '{fuel_info['value']}'"
        self.menu.customer_portal.menu_log_out()