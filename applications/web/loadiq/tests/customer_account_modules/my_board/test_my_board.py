from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.my_board.BidDetailsPage import BidDetailsPage
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage
from applications.web.loadiq.pages.login.LoginPage import LoginPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test

logger = setup_logger('TestMyBoard')


@pytest.mark.web
@loadiq
class TestMyBoard(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    my_board = MyBoardPage.get_instance()
    shipment_creation = ShipmentCreationPage.get_instance()
    bid_details = BidDetailsPage.get_instance()
    searchBy = "LD25082100024"

    @test(test_case_id="CT-1691", test_description="Verify it's possible to filter all shipments", feature="My Loads",skip=False)
    def test_my_board_filter_shipments(self, load_iq_login_customer_portal):
        self.menu.operations_portal.menu_my_board()
        # 01 Load My Boards Page
        self.my_board.load_page()
        # 02 Apply Filter Criteria: Include Closed, Include Expired, Sort By "Lowest Bid"
        self.my_board.click_include_closed()
        self.my_board.click_include_expired()
        self.my_board.select_sort_by("Lowest Bid")
        # 03 Assert that the first 3 filters are present
        #Very filter are enabled
        assert self.my_board.is_filter_active("Include Closed"), "Include Closed filter is not active."
        assert self.my_board.is_filter_active("Include Expired"), "Include Expired filter is not active."
        assert self.my_board.get_selected_sort_option() == "LowestBid", "Sort option is not set to Lowest Bid."

    @test(test_case_id="CT-1095", test_description="Verify it's possible to search a load", feature="My Loads", skip=False)
    def test_my_board_search_a_tracker_number(self,):
        # 01. Login User
        # self.login.load_page()
        # self.login.login_user(CustomerAccounts.TEST_07)
        # self.login.is_login_successful()

        # 02. Gets My Loads Page
        self.menu.customer_portal.menu_my_board()

        # Verify the page has data
        no_data = self.my_board.no_load_results()
        if not no_data:
            # 03. Type an existing Tracking Number
            tracking_number = self.my_board.get_shipment_tracker_number(1)
            # 04. Search The Tracking Number
            self.my_board.search_by(tracking_number)

            # 05. Get Track Information
            item = self.my_board.get_shipment_item(1)
            search_tracker_number = item[0]
            assert search_tracker_number == tracking_number, f"Tracker Number Incorrect, Expected {tracking_number} and Found {search_tracker_number}"
        else:
            logger.warning("No records found, for execute this test.")


    @test(test_case_id="CT-2552", test_description="Verify search a new shipment",feature="SearchBar", skip=False)
    def test_my_board_operation_search_shipment(self,):
        # 02. User go to "My board" page
        self.menu.operations_portal.menu_my_board()
        self.my_board.load_page()
        self.my_board.click_include_closed()
        self.my_board.click_include_expired()
        # 04. User search an existing load
        self.my_board.search_by(self.searchBy)
        self.my_board._click_search()
        item = self.my_board.get_shipment_item(1)

        # Valides that loadNumber is not null
        assert self.searchBy is not None and self.searchBy.strip() != "", "Value does not exist"
        assert self.searchBy == item[0], f"Shipment Tracking Number not match, current {self.searchBy}, found {item[0]}"

    @test(test_case_id="CT-3909", test_description=" Verify it's possible to check load details and extend",feature="SearchBar", skip=False)
    def test_my_board_operation_bid_extension(self,):
        # 02. User go to "My board" page
        # 02. Gets My Loads Page
        self.menu.customer_portal.menu_my_board()
        # Verify the page has data
        no_data = self.my_board.no_load_results()
        if not no_data:
            # 03. Type an existing Tracking Number
            tracking_number = self.my_board.get_shipment_tracker_number(1)
            # 04. Search The Tracking Number
            self.my_board.search_by(tracking_number)

        self.my_board.click_show_details_my_board()
        # Bid is extended + 30 minutes
        self.my_board.extend_bid_time_avoid()
        self.my_board.extend_bid_time()
        # System shows a popup message with the extension time and validates it.
        expected_message = "Bidding on this shipment is extended by 30 minutes"
        actual_message = self.my_board.get_bidding_confirmation_message()
        assert expected_message in actual_message, f"Expected bidding confirmation not found. Found: '{actual_message}'"

    @test(test_case_id="CT-3886", test_description=" Verify it's possible to check load details and close the bid",feature="SearchBar", skip=False)
    def test_my_board_operation_bid_close(self,load_iq_login_customer_portal):
        # 02. User go to "My board" page
        # 02. Gets My Loads Page
        self.menu.customer_portal.menu_my_board()
        # Verify the page has data
        no_data = self.my_board.no_load_results()
        if not no_data:
            # 03. Type an existing Tracking Number
            tracking_number = self.my_board.get_shipment_tracker_number(1)
            # 04. Search The Tracking Number
            self.my_board.search_by(tracking_number)
        self.my_board.click_show_details_my_board()
        self.my_board.close_bid()
        expected_message = "Bid has been closed successfully."
        actual_message = self.my_board.get_closed_confirmation_message_confirmation_message()
        assert actual_message == expected_message, (
            f"Error: Expected confirmation message '{expected_message}', but got '{actual_message}'"
        )
    @test(test_case_id="CT-3582", test_description="Verify the feedback option (MyBoard)", feature="My Loads",skip=False)
    def test_my_board_search_a_tracker_number(self,):
        # 01. Login User
        # self.login.login_user(CustomerAccounts.TEST_07)
        # 02. Gets My Loads Page
        self.menu.customer_portal.menu_my_board()
        #Send a text and create the feedback
        self.my_board.send_feedback("QA TEST - TESTING FEEDBACK")
        #Confirms the expected label message
        expected_message = "Feedback submitted successfully"
        actual_message = self.my_board.get_feedback_confirmation_message()
        assert expected_message in actual_message, f"Expected feedback confirmation not found. Found: '{actual_message}'"

    @test(test_case_id="CT-3888",test_description="Verify it's possible to check load details and new documents can be added/uploaded",feature="My Loads",skip=False)
    def test_my_board_search_upload_files(self,):
        # Navigate to My Loads page
        self.menu.customer_portal.menu_my_board()

        # Check if there is data available
        no_data = self.my_board.no_load_results()
        if not no_data:
            # Get a valid tracking number from the first load
            tracking_number = self.my_board.get_shipment_tracker_number(1)
            # Search for the load using the tracking number
            self.my_board.search_by(tracking_number)

        # Open the load details view
        self.my_board.click_show_details_my_board()

        # Define files to upload with their descriptions
        files_to_upload = [
            {
                "file_name": "upload_test_document.png",
                "description": "Automation Test Upload-File"
            },
            {
                "file_name": "upload_test_document1.png",
                "description": "Automation Test Upload-File1"
            }
        ]

        # Upload each file and validate confirmation message
        for file in files_to_upload:
            self.my_board.click_upload_documents()
            self.my_board.click_add_file(
                file_name=file["file_name"],
                description=file["description"]
            )

            # Validate that the confirmation message is displayed
            expected_message = "Document successfully uploaded"
            actual_message = self.my_board.get_document_upload_confirmation_message()
            assert expected_message in actual_message, f"Expected upload confirmation not found. Found: '{actual_message}'"

    @test(test_case_id="CT-1692",test_description="Verify it's possible to check load details and assign a carrier",feature="My Loads",skip=False)
    def test_my_board_assign_carrier(self,):
        # Login User
        # Gets My Loads Page
        self.menu.customer_portal.menu_my_board()
        # Verify existing data
        no_data = self.my_board.no_load_results()
        if not no_data:

            tracking_number = self.my_board.get_shipment_tracker_number(1)
            #Search the data
            self.my_board.search_by(tracking_number)
        #Show the data sent
        self.my_board.click_show_details_my_board()
        self.bid_details.click_assign_a_carrier()
        self.bid_details._enter_search_carrier("TEST.DATA")
        self.bid_details._enter_rate("100")
        self.bid_details.click_assign_load()
        #Assert: Validate that the Assign Load button is disabled
        assert self.bid_details.is_assign_load_button_enabled(), "Assign Load button is disabled."







