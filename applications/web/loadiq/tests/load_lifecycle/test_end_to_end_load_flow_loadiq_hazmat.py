from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import allure
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage
from applications.web.loadiq.pages.my_loads.MyLoadsPage import MyLoadsPage
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.my_offers.MyOffersDetailsPage import MyOffersDetailsPage
from applications.web.loadiq.pages.shipment_creation.create_shipment.CreateShipmentPage import CreateShipmentPage
from applications.web.loadiq.pages.my_offers.MyOffersPage import MyOffersPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.helpers import generate_future_date

logger = setup_logger('TestCustomerShipmentCreation')


@pytest.mark.web
@loadiq
class TestCustomerShipmentCreation(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    shipment_creation = ShipmentCreationPage.get_instance()
    create_shipment = CreateShipmentPage.get_instance()
    my_offers = MyOffersPage.get_instance()
    my_offers_details = MyOffersDetailsPage.get_instance()
    my_board = MyBoardPage.get_instance()
    my_loads = MyLoadsPage.get_instance()


    @allure.step("{step_name}")
    def take_screenshot(self, step_name: str):
        """Helper method to take screenshots with Allure"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Screenshot - {step_name}",
            attachment_type=allure.attachment_type.PNG
        )

    shipment_number = None

    @allure.title("Verify it's possible to create a new hazmat shipment - First Come, First Served")
    @allure.description("This module enables the ability to create a new hazmat shipment with first-come appointments. LOADIQ as source.")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-2054", name="Jira")
    @allure.testcase("CT-2054")
    @allure.feature("Shipment Creation")
    @test(test_case_id="CT-2054",test_description="Verify it's possible to create a new hazmat shipment - First Come, First Served",feature="Shipment Creation",skip=False)
    def test_customer_create_shipment_first_come_with_hazmat(self, load_iq_login_customer_portal, load_json_data,save_json_data, record_property):
        record_property("test_key", "CT-2054")

        # Upload data from json data
        test_data = load_json_data("applications/web/loadiq/data/load_lifecycle/hazmat_load_lifecycle.json", "CT-2054")
        logger.info(f"Data for CT-2054: {test_data}")

        self.menu.customer_portal.menu_shipment_creation()
        self.shipment_creation.click_create_shipment()
        tracking_number = self.create_shipment.get_shipment_tracker_number()

        # ORIGIN TAB
        self.create_shipment.click_origin_information()
        origin_location = test_data["origin"]["location"]
        self.create_shipment.tab_origin_information.enter_origin_location(
            name=origin_location["name"],
            location=origin_location["location"],
            address=origin_location["address"],
            address_line_2=origin_location["address_line_2"]
        )
        origin_contact = test_data["origin"]["contact"]
        self.create_shipment.tab_origin_information.enter_contact(
            name=origin_contact["name"],
            phone=origin_contact["phone"],
            email=origin_contact["email"]
        )
        origin_pickup = test_data["origin"]["pickup_appointment"]
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(origin_pickup["from_day_offset"]),
            to_day=generate_future_date(origin_pickup["to_day_offset"]),
            open_hours=origin_pickup["open_time"]["hours"],
            open_minutes=origin_pickup["open_time"]["minutes"],
            close_hours=origin_pickup["close_time"]["hours"],
            close_minutes=origin_pickup["close_time"]["minutes"]
        )
        self.create_shipment.tab_origin_information.click_increase_open_time_origen()
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB
        self.create_shipment.click_destination_information()
        dest_location = test_data["destination"]["location"]
        self.create_shipment.tab_destination_information.enter_destination_location(
            name=dest_location["name"],
            location=dest_location["location"],
            address=dest_location["address"],
            address_line_2=dest_location["address_line_2"]
        )
        dest_contact = test_data["destination"]["contact"]
        self.create_shipment.tab_destination_information.enter_contact(
            name=dest_contact["name"],
            phone=dest_contact["phone"],
            email=dest_contact["email"]
        )
        dest_pickup = test_data["destination"]["pickup_appointment"]
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(dest_pickup["from_day_offset"]),
            to_day=generate_future_date(dest_pickup["to_day_offset"]),
            open_hours=dest_pickup["open_time"]["hours"],
            open_minutes=dest_pickup["open_time"]["minutes"],
            close_hours=dest_pickup["close_time"]["hours"],
            close_minutes=dest_pickup["close_time"]["minutes"]
        )
        self.create_shipment.tab_destination_information.click_open_calendar()
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB
        self.create_shipment.click_shipment_details()
        shipment_details = test_data["shipment_details"]
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment=shipment_details["equipment"],
            freight_class=shipment_details["freight_class"],
            po_number=shipment_details["po_number"],
            bill_of_landing_number=shipment_details["bill_of_lading_number"],
            pick_up_number=shipment_details["pick_up_number"],
            shipment_instructions=shipment_details["shipment_instructions"]
        )
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB
        self.create_shipment.click_freight_items()
        freight_item = test_data["freight"]["freight_item"]
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight=freight_item["gross_weight"],
            weight_type=freight_item["weight_type"],
            handling_unit_count=freight_item["handling_unit_count"],
            select_handling_unit_type=freight_item["select_handling_unit_type"],
            commodity_value=freight_item["commodity_value"]
        )
        dimension = test_data["freight"]["dimension"]
        self.create_shipment.tab_freight_items.enter_dimension(
            length=dimension["length"],
            width=dimension["width"],
            height=dimension["height"],
            uom=dimension["uom"],
            commodity_description=dimension["commodity_description"]
        )
        hazmat = test_data["freight"]["hazmat"]
        self.create_shipment.tab_freight_items.enter_hazmat(
            un_na_number=hazmat["un_na_number"],
            hazmat_class=hazmat["hazmat_class"],
            hazmat_contact_number=hazmat["hazmat_contact_number"],
            packing_group=hazmat["packing_group"],
            proper_shipping_name=hazmat["proper_shipping_name"]
        )
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB
        self.create_shipment.click_bid_parameters()
        bid_params = test_data["bid_parameters"]
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate=bid_params["book_it_now_rate"],
            bid_expiration_date=generate_future_date(bid_params["bid_expiration_offset_days"]),
            hours=bid_params["bid_expiration_time"]["hours"],
            minutes=bid_params["bid_expiration_time"]["minutes"]
        )
        upload_file = bid_params["upload_file"]
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name=upload_file["file_name"],
            description=upload_file["description"]
        )
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        self.create_shipment.tab_bid_parameters.click_save_and_submit()
        # Final verification of the load creation
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        assert self.my_board.shipment_exists(tracking_number), f"Shipment with tracking number '{tracking_number}' was not found."
        save_json_data("applications/web/loadiq/data/load_lifecycle/hazmat_load_lifecycle.json", "CT-2054","shipment_id", tracking_number)
        # User Log Out
        self.menu.customer_portal.menu_log_out()
        self.take_screenshot("Validate Customer User Logged Out")



    @allure.title("Validate that a user can bid on a new load created by a customer")
    @allure.description("The goal of this test case is validate that the user can BID in a new Load Created by the customer user.")
    @allure.tag("LOADIQ", "Bid a new Load")
    @allure.link("https://crowley.atlassian.net/browse/CT-3796", name="Jira")
    @allure.testcase("CT-3796")
    @allure.feature("My Offers")
    @test(test_case_id="CT-3796", test_description="Validate that a user can bid on a new load created by a customer", feature="Shipment Creation", skip=False)
    def test_carrier_bid_offer(self,load_json_data,load_iq_login_carrier_portal, record_property):

        record_property("test_key", "CT-2054")
        self.take_screenshot("Validate Carrier User is Logged")
        # Get test data and retrieve the saved shipment_id
        test_data = load_json_data("applications/web/loadiq/data/load_lifecycle/hazmat_load_lifecycle.json", "CT-2054")
        logger.info(f"Data for CT-2054: {test_data}")

        # User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page Loaded")
        # User search for the load offer created by the customer (Load ID: #)
        self.my_offers.enter_search_by(test_data["shipment_id"])
        # Click in the Search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Results Displayed")
        #Click in the button Accept/Reject
        self.my_offers.click_accept_reject_button(test_data["shipment_id"])
        #Click in the Bid Details button
        self.my_offers_details.click_bid_details_button()
        self.take_screenshot("Validate Bid Details of the Load")
        #Enter the bid amount
        self.my_offers_details.enter_bid_amount("1000")
        #Enter the expiration date
        self.my_offers_details.enter_expiration_date("08/06/2025")
        #Enter the expiration time
        self.my_offers_details.enter_time_hour("11")
        self.my_offers_details.enter_time_minute("59")
        #self.my_offers_details.click_time_period_button()
        self.take_screenshot("Validate Bid Amount and Expiration Date/Time Entered")
        # Click in the Place Bid button
        self.my_offers_details.click_place_bid_button()
        # Click in the Yes, Confirm button
        self.my_offers_details.click_yes_confirm_button()
        #Verify that the success message is displayed
        text = self.my_offers_details.get_success_message_text()
        assert "Bid successfully placed. Shipper has been notified" in text, f"Expected success message not found. Found: '{text}'"
        self.take_screenshot("Validate Success Message Displayed")
        #Click in the OK button
        self.my_offers_details.click_ok_button()
        self.take_screenshot("Validate Confirmation Message Displayed")
        #User Log Out
        self.menu.carrier_portal.menu_log_out()
        self.take_screenshot("Validate Carrier User is Logged Out")

    @allure.title("Validate that the customer can accept the bid offer")
    @allure.description("This test case validate that the customer can accept a load that the carrier has just bided.")
    @allure.tag("LOADIQ", "Accept Bid Offer")
    @allure.link("https://crowley.atlassian.net/browse/CT-4436", name="Jira")
    @allure.testcase("CT-4436")
    @allure.feature("My Board")
    @test(test_case_id="CT-4436", test_description="Validate that the customer can accept the bid offer", feature="Shipment Creation", skip=False)
    def test_customer_accept_offer(self, load_iq_login_customer_portal, load_json_data, record_property):
        record_property("test_key", "CT-2054")
        self.take_screenshot("Validate Customer User is Logged")
        # Get test data and retrieve the saved shipment_id
        test_data = load_json_data("applications/web/loadiq/data/load_lifecycle/hazmat_load_lifecycle.json", "CT-2054")
        logger.info(f"Data for CT-2054: {test_data}")
        # Go to My Board menu
        self.menu.customer_portal.menu_my_board()
        self.take_screenshot("Validate My Board Page is Loaded")
        #Search for the shipment using the shipment_id
        self.my_board.search_by(test_data["shipment_id"])
        #Validate that the shipment is displayed in the My Board page
        item = self.my_board.get_shipment_item(1)
        assert test_data["shipment_id"] == item[0], f"Shipment Tracking Number not match, current {test_data["shipment_id"]}, found {item[0]}"
        self.take_screenshot("Validate Shipment is Displayed in My Board Page")
        # Click on the Show Details button for the shipment
        self.my_board.click_show_details_my_board()
        self.take_screenshot("Validate Shipment Details are Displayed")
        # Click on the Accept Offer button
        self.my_board.click_first_row_accept_offer_button()
        # Click on the Yes, Accept button in the modal
        self.my_board.click_btn_yes_modal()
        self.take_screenshot("Validate Accept Offer Confirmation Modal is Displayed")
        self.pause(5)
        #User Log Out
        self.menu.customer_portal.menu_log_out()
        self.take_screenshot("Validate Customer User is Logged Out")

    @allure.title("Validate that the carrier user can accept the tender of a customer that had accepted the offer of the bid")
    @allure.description("The goal of this test case is validate that the carrier user can Accept a tender of a customer that have accepted a offer.")
    @allure.tag("LOADIQ", "Accept Tender")
    @allure.link("https://crowley.atlassian.net/browse/CT-4442", name="Jira")
    @allure.testcase("CT-4442")
    @allure.feature("My Offers")
    @test(test_case_id="CT-4442", test_description="Validate that the carrier user can accept the tender of a customer that had accepted the offer of the bid", feature="Shipment Creation", skip=False)
    def test_carrier_accept_tender(self, load_iq_login_carrier_portal, load_json_data, record_property):
        record_property("test_key", "CT-2054")
        self.take_screenshot("Validate Carrier User is Logged")
        # Get test data and retrieve the saved shipment_id
        test_data = load_json_data("applications/web/loadiq/data/load_lifecycle/hazmat_load_lifecycle.json", "CT-2054")
        logger.info(f"Data for CT-2054: {test_data}")
        # User navigate to "My Offers" page
        self.menu.carrier_portal.menu_my_offers()
        self.take_screenshot("Validate My Offers Page is Loaded")
        # User search for the load offer created by the customer
        self.my_offers.enter_search_by(test_data["shipment_id"])
        # Click in the Search button
        self.my_offers.click_search()
        self.take_screenshot("Validate Search Results Displayed")
        # Click in the button Accept/Reject
        self.my_offers.click_accept_reject_button(test_data["shipment_id"])
        self.take_screenshot("Validate Accept/Reject Details are Displayed")
        # Click on the Accept Tender button
        self.my_offers_details.click_accept_tender_details_button()
        # Click on the Accept Tender button in the modal
        self.my_offers_details.click_btn_accept_tender_modal()
        self.take_screenshot("Validate Accept Tender Confirmation Modal is Displayed")
        actual_text = self.my_offers_details.get_alert_message_text()
        expected_text = "Tender accepted successfully."
        assert expected_text in actual_text, f"Expected '{expected_text}' but got '{actual_text}'"
        self.take_screenshot("Validate Tender Accepted Successfully Message is Displayed")
        #Click on the My Loads menu
        self.menu.carrier_portal.menu_my_loads(2)
        #Search for the load using the shipment_id
        self.my_loads.enter_search_by(test_data["shipment_id"])
        #Click in the Search button
        self.my_loads.click_search()
        self.take_screenshot("Validate Search Results Displayed in My Loads Page")

