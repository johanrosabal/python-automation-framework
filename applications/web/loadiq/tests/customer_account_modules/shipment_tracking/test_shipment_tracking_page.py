from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.shipment_creation.create_shipment.CreateShipmentPage import CreateShipmentPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from applications.web.loadiq.pages.shipment_tracking.ShipmentTrackingPage import ShipmentTrackingPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
import time


logger = setup_logger('TestCustomerShipmentCreation')


@pytest.mark.web
@loadiq
class TestCustomerShipmentCreation(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    shipment_creation = ShipmentCreationPage.get_instance()
    create_shipment = CreateShipmentPage.get_instance()
    my_board = MyBoardPage.get_instance()
    tracking = ShipmentTrackingPage.get_instance()
    loadclosed = "BY_10004000006"
    loadhazmat = "MC_3001245"

    @test(test_case_id="CT-3669", test_description="Verify loads card displays 'Crowley' for customer user",feature="Shipment Tracking", skip=False)
    def test_customer_tracking_card_page(self, load_iq_login_customer_portal):
        # Log in to the shipment tracking page (Customer portal)
        self.menu.customer_portal.menu_shipment_tracking()
        # Search a valid test input
        self.tracking.enter_search_by(search_by=self.loadclosed)
        self.tracking.click_search()
        # Verify lab  is present with the name
        assert self.tracking.get_text_card_label() == "Crowley", "Expected card information 'Crowley' is not present on the page"
        
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-4682", test_description="Verify document tab on shipment tracking (Download)", feature="Shipment Tracking", skip=False)
    def test_customer_tracking_download_documents(self,load_iq_login_customer_portal ):
        #Log in to the shipment tracking page (Customer portal)
        self.menu.customer_portal.menu_shipment_tracking()
        #Search a valid test input
        self.tracking.enter_search_by(search_by=self.loadclosed)
        self.tracking.click_search()
        self.tracking.click_document_details()
        #Click view button and verify button that is present
        self.tracking.click_download_image()
        assert self.tracking.is_download_document_present(), "View document button is not present on the page"
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-2689",test_description="Verify that the Customer User Updates Booking Number in Shipment Tracking",feature="Shipment Tracking", skip=False)
    def test_customer_tracking_update_booking_number(self, load_iq_login_customer_portal):
        # Open correct portal
        self.menu.customer_portal.menu_shipment_tracking()
        # Find a new available load
        tracking_number = self.tracking.get_tracking_number(1)
        self.tracking.enter_search_by(search_by=tracking_number)
        self.tracking.click_search()
        # Call the method that generate the new booking number
        new_booking_number = self.tracking.update_booking_number()
        # Get the confirmation message
        confirmation_text = self.tracking.get_booking_number_update_confirmation()
        # Verify the got message
        assert "Booking Number saved successfully" in confirmation_text, \
            f"Expected confirmation message not found. Received: '{confirmation_text}'"
        time.sleep(4)
        # Close the page
        self.menu.customer_portal.menu_log_out()

    # @test(test_case_id="CT-1687", test_description="Verify it's possible to cancel an order",feature="Shipment Tracking", skip=True)
    # def test_customer_tracking_cancel_tracking_number(self,load_iq_login_customer_portal ):
    #     #Open customer portal and move to shipment tracking
    #     self.menu.customer_portal.menu_shipment_tracking()
    #     #Ship date filter is performed
    #     self.tracking.double_click_sort_by_status(2)
    #     #Search an existing tracking number into the table
    #     tracking_number = self.tracking.get_tracking_number(1)
    #     self.tracking.enter_search_by(search_by=tracking_number)
    #     #Searched load is cancelled
    #     self.tracking.click_search()
    #     self.tracking.click_cancel_and_cancel_screen()
    #     confirmation_text = self.tracking.get_text_cancel_confirmation()
    #     # Assert that the confirmation message contains expected text
    #     assert "Load has been cancelled successfully." in confirmation_text, \
    #         f"Expected confirmation message not found. Expected: '{confirmation_text}'"
    #     self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-4250", test_description="Verify Shipment Tracking - 'Hazmat Details' tab",feature="Shipment Tracking", skip=False)
    def test_customer_tracking_hazmat_details(self,load_iq_login_customer_portal ):
        #Open customer portal and move to shipment tracking
        self.menu.customer_portal.menu_shipment_tracking()
        #Search an existing tracking number into the table
        self.tracking.enter_search_by(search_by=self.loadhazmat)
        self.tracking.click_search()
        #Move to the hazmat that and start getting the columns.
        self.tracking.click_hazmat_tab()
        texts = self.tracking.get_all_hazmat_column()
        #Verifies the expected texts according to the expected ones.
        expected_texts = {
            "Freight Item": "Freight Item",
            "UN/NA Number": "UN/NA Number",
            "Hazmat Class": "Hazmat Class",
            "Packing Group": "Packing Group",
            "Phone": "Phone",
            "Proper Shipping Name": "Proper Shipping Name"
        }
        for column_name, expected_text in expected_texts.items():
            actual_text = texts.get(column_name)
            print(f"{column_name}: Got: '{actual_text}', Expected: '{expected_text}'")
            assert actual_text == expected_text, f"Not found in '{column_name}'"
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-2636", test_description="Verify New 'Stop Details' tab in Shipment Tracking", feature="Shipment Tracking", skip=False)
    def test_customer_tracking_stop_tab(self,load_iq_login_customer_portal ):
        #Log in to the shipment tracking page (Customer portal)
        self.menu.customer_portal.menu_shipment_tracking()
        # Search a valid test input
        self.tracking.enter_search_by(search_by=self.loadclosed)
        self.tracking.click_search()
        self.tracking.click_stop_details()
        #Verify tab is present with the name
        assert self.tracking.get_text_stop_details_tab() == "Stop Details".strip(), "Expected tab name is not present on the page"
        assert self.tracking.is_stop_details_modal_present(), "Stop Details modal is not present on the page"
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-1688", test_description="[UI] Verify document tab on shipment tracking (View)", feature="Shipment Tracking", skip=False)
    def test_customer_tracking_view_documents(self,load_iq_login_customer_portal ):
        #Log in to the shipment tracking page (Customer portal)
        self.menu.customer_portal.menu_shipment_tracking()
        #Search a valid test input
        self.tracking.enter_search_by(search_by=self.loadclosed)
        self.tracking.click_search()
        self.tracking.click_document_details()
        #Click view button and verify that button is present
        self.tracking.click_view_image()
        assert self.tracking.is_view_document_present(), "View document button is not present on the page"