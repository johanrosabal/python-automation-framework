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
    searchBy = "LD25062600005"

    @test(test_case_id="CT-1095", test_description="Verify it's possible to search a load", feature="My Loads", skip=False)
    def test_my_board_search_a_tracker_number(self, load_iq_login_operations_portal):
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
        # Sign Out User
        # self.menu.logout()

    @test(test_case_id="CT-1691", test_description="Verify it's possible to filter all shipments", feature="My Loads", skip=False)
    def test_my_board_filter_shipments(self,):
        self.menu.operations_portal.menu_my_board()
        # 01 Load My Boards Page
        self.my_board.load_page()
        # 02 Search a Load Tracking Number that is closed
        # self.my_board.search_by("LD25011700001")
        # 03 Apply Filter CriteriaL Include true, Expired true, Sort By "Lowest Bid"
        self.my_board.click_include_closed()
        self.my_board.click_include_expired()
        self.my_board.select_sort_by("Lowest Bid")
        self.pause(15)

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

        # Validar que loadNumber no sea nulo o esté vacío
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
        self.my_board.extend_bid_time_avoid()
        self.my_board.extend_bid_time()

    @test(test_case_id="CT-3886", test_description=" Verify it's possible to check load details and close the bid",feature="SearchBar", skip=False)
    def test_my_board_operation_bid_close(self,):
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

    @test(test_case_id="CT-3582", test_description="Verify the feedback option (MyBoard)", feature="My Loads",skip=False)
    def test_my_board_search_a_tracker_number(self,):
        # 01. Login User
        # self.login.login_user(CustomerAccounts.TEST_07)
        # 02. Gets My Loads Page
        self.menu.customer_portal.menu_my_board()
        #Send a text and create the feedback
        self.my_board.send_feedback("QA TEST - TESTING FEEDBACK")

    @test(test_case_id="CT-3887", test_description="Verify it's possible to check load details and download all documents", feature="My Loads",skip=False)
    def test_my_board_search_extend_bid(self,):
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
        self.my_board.extend_bid_time_avoid()
        self.my_board.extend_bid_time()

    @test(test_case_id="CT-3888",test_description="Verify it's possible to check load details and new documents can be added/downloaded",feature="My Loads",skip=False)
    def test_my_board_search_upload_files(self,):
        # Login User
        # self.login.load_page()
        # self.login.login_user(CustomerAccounts.TEST_07)
        # self.login.is_login_successful()

        #Gets My Loads Page
        self.menu.customer_portal.menu_my_board()

        #Verifica si hay datos en la página
        no_data = self.my_board.no_load_results()
        if not no_data:
            # 04. Obtiene un número de rastreo existente
            tracking_number = self.my_board.get_shipment_tracker_number(1)
            # 05. Busca el número de rastreo
            self.my_board.search_by(tracking_number)

        #Muestra los detalles del envío
        self.my_board.click_show_details_my_board()

        #Sube archivos con nombre y description personalizados
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

        for file in files_to_upload:
            self.my_board.click_upload_documents()
            self.my_board.click_add_file(
                file_name=file["file_name"],
                description=file["description"]
            )

