from selenium.webdriver.common.by import By
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.load_board.LoadBoardPage import LoadBoard
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage
from applications.web.loadiq.fixtures.fixtures import *
from core.utils.fixtures import *                                 
from applications.web.loadiq.pages.shipment_creation.create_shipment.CreateShipmentPage import CreateShipmentPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.helpers import generate_future_date

logger = setup_logger('TestCustomerShipmentCreationPage')


@pytest.mark.web
@loadiq
class TestCustomerShipmentCreationPage(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    shipment_creation = ShipmentCreationPage.get_instance()
    create_shipment = CreateShipmentPage.get_instance()
    my_board = MyBoardPage.get_instance()
    load_board=LoadBoard.get_instance()
    shipment_number = None

    @test(test_case_id="CT-3795", test_description="Validate the Load when the load was created activating the Expedite option in the Destination information on My Board function", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_and_expedite(self, load_iq_login_customer_portal, load_json_data, record_property):
        record_property("test_key", "CT-3795")

        # Get test data from fixture filtered by CT-1234
        data_json = load_json_data("applications/web/loadiq/data/load_lifecycle/load_lifecycle_expedite.json")
        data = helpers.get_test_case_data_by_id(data_json, "CT-3795")
        logger.info(f"Data for CT-3795: {data}")

        # 02. User go to "Shipment Creation" page
        self.menu.customer_portal.menu_shipment_creation()

        # 03. User clicks on "Create Shipment" button
        self.shipment_creation.click_create_shipment()

        # Reading Current Tracking Number
        tracking_number = self.create_shipment.get_shipment_tracker_number()

        # ORIGIN TAB ---------------------------------------------------------------------------------------------------
        # 04. User should complete "Original Information" Tab Form
        self.create_shipment.click_origin_information()

        # 04.01 Fills Up "Origin Information" Section
        origin_location = data["origin"]["location"]
        self.create_shipment.tab_origin_information.enter_origin_location(
            name=origin_location["name"],
            location=origin_location["location"],
            address=origin_location["address"],
            address_line_2=origin_location["address_line_2"]
        )

        # 04.02 Fills Up "Contact Information" Section
        origin_contact = data["origin"]["contact"]
        self.create_shipment.tab_origin_information.enter_contact(
            name=origin_contact["name"],
            phone=origin_contact["phone"],
            email=origin_contact["email"]
        )

        # 04.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        origin_pickup = data["origin"]["pickup_appointment"]
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(origin_pickup["from_day_offset"]),
            to_day=generate_future_date(origin_pickup["to_day_offset"]),
            open_hours=origin_pickup["open_time"]["hours"],
            open_minutes=origin_pickup["open_time"]["minutes"],
            close_hours=origin_pickup["close_time"]["hours"],
            close_minutes=origin_pickup["close_time"]["minutes"]
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()

        # 05.01 Fill Ups "Destination Information" Section
        dest_location = data["destination"]["location"]
        self.create_shipment.tab_destination_information.enter_destination_location(
            name=dest_location["name"],
            location=dest_location["location"],
            address=dest_location["address"],
            address_line_2=dest_location["address_line_2"]
        )

        # 05.02 Fills Up "Contact Information" Section
        dest_contact = data["destination"]["contact"]
        self.create_shipment.tab_destination_information.enter_contact(
            name=dest_contact["name"],
            phone=dest_contact["phone"],
            email=dest_contact["email"]
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        dest_pickup = data["destination"]["pickup_appointment"]
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(dest_pickup["from_day_offset"]),
            to_day=generate_future_date(dest_pickup["to_day_offset"]),
            open_hours=dest_pickup["open_time"]["hours"],
            open_minutes=dest_pickup["open_time"]["minutes"],
            close_hours=dest_pickup["close_time"]["hours"],
            close_minutes=dest_pickup["close_time"]["minutes"]
        )

        # Expedite checkbox enabled
        self.create_shipment.tab_destination_information.check_expedite()

        # Validates Expedite checkbox exists
        assert self.create_shipment.tab_destination_information.get_expedite_element() is not None, \
            "Expedite checkbox does not exist on the page."

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()

        # 06.01 Fills Up "Shipment Details"
        shipment_details = data["shipment_details"]
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment=shipment_details["equipment"],
            freight_class=shipment_details["freight_class"],
            po_number=shipment_details["po_number"],
            bill_of_landing_number=shipment_details["bill_of_lading_number"],
            pick_up_number=shipment_details["pick_up_number"],
            shipment_instructions=shipment_details["shipment_instructions"]
        )

        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -------------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()

        # 07.01 Fills Up "Freight Line Item (1)" section
        freight_item = data["freight"]["freight_item"]
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight=freight_item["gross_weight"],
            weight_type=freight_item["weight_type"],
            handling_unit_count=freight_item["handling_unit_count"],
            select_handling_unit_type=freight_item["select_handling_unit_type"],
            commodity_value=freight_item["commodity_value"]
        )

        # 07.02 Fills Up "Dimension" section
        dimension = data["freight"]["dimension"]
        self.create_shipment.tab_freight_items.enter_dimension(
            length=dimension["length"],
            width=dimension["width"],
            height=dimension["height"],
            uom=dimension["uom"],
            commodity_description=dimension["commodity_description"]
        )

        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        bid_params = data["bid_parameters"]
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate=bid_params["book_it_now_rate"],
            bid_expiration_date=generate_future_date(bid_params["bid_expiration_offset_days"]),
            hours=bid_params["bid_expiration_time"]["hours"],
            minutes=bid_params["bid_expiration_time"]["minutes"]
        )

        # 08.02 Upload a File
        upload_file = bid_params["upload_file"]
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name=upload_file["file_name"],
            description=upload_file["description"]
        )
        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()
        # Step 01: Load the customer's load board
        self.my_board.load_page()
        # Step 02: Search for the shipment using the tracking number
        self.my_board.search_by(tracking_number)
        #Validate that the load was found (the "not found" message should not appear)
        actual_message = self.my_board.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # Step 05: Log out from the Customer Portal
        self.menu.customer_portal.menu_log_out()

    @test(test_case_id="CT-3792", test_description="Validate the new creation of a load indicating that is expedite in the new checkbox in Shipment creation function", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_and_expedite_verification(self, load_iq_login_customer_portal, load_json_data, record_property):
        record_property("test_key", "CT-3792")

        # Get test data from fixture filtered by CT-1234
        data_json = load_json_data("applications/web/loadiq/data/load_lifecycle/load_lifecycle_and_expedite_verification.json")
        data = helpers.get_test_case_data_by_id(data_json, "CT-3792")
        logger.info(f"Data for CT-3792: {data}")

        # 02. User go to "Shipment Creation" page
        self.menu.customer_portal.menu_shipment_creation()

        # 03. User clicks on "Create Shipment" button
        self.shipment_creation.click_create_shipment()

        # Reading Current Tracking Number
        tracking_number = self.create_shipment.get_shipment_tracker_number()

        # ORIGIN TAB ---------------------------------------------------------------------------------------------------
        # 04. User should complete "Original Information" Tab Form
        self.create_shipment.click_origin_information()

        # 04.01 Fills Up "Origin Information" Section
        origin_location = data["origin"]["location"]
        self.create_shipment.tab_origin_information.enter_origin_location(
            name=origin_location["name"],
            location=origin_location["location"],
            address=origin_location["address"],
            address_line_2=origin_location["address_line_2"]
        )

        # 04.02 Fills Up "Contact Information" Section
        origin_contact = data["origin"]["contact"]
        self.create_shipment.tab_origin_information.enter_contact(
            name=origin_contact["name"],
            phone=origin_contact["phone"],
            email=origin_contact["email"]
        )

        # 04.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        origin_pickup = data["origin"]["pickup_appointment"]
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(origin_pickup["from_day_offset"]),
            to_day=generate_future_date(origin_pickup["to_day_offset"]),
            open_hours=origin_pickup["open_time"]["hours"],
            open_minutes=origin_pickup["open_time"]["minutes"],
            close_hours=origin_pickup["close_time"]["hours"],
            close_minutes=origin_pickup["close_time"]["minutes"]
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()

        # 05.01 Fill Ups "Destination Information" Section
        dest_location = data["destination"]["location"]
        self.create_shipment.tab_destination_information.enter_destination_location(
            name=dest_location["name"],
            location=dest_location["location"],
            address=dest_location["address"],
            address_line_2=dest_location["address_line_2"]
        )

        # 05.02 Fills Up "Contact Information" Section
        dest_contact = data["destination"]["contact"]
        self.create_shipment.tab_destination_information.enter_contact(
            name=dest_contact["name"],
            phone=dest_contact["phone"],
            email=dest_contact["email"]
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        dest_pickup = data["destination"]["pickup_appointment"]
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(dest_pickup["from_day_offset"]),
            to_day=generate_future_date(dest_pickup["to_day_offset"]),
            open_hours=dest_pickup["open_time"]["hours"],
            open_minutes=dest_pickup["open_time"]["minutes"],
            close_hours=dest_pickup["close_time"]["hours"],
            close_minutes=dest_pickup["close_time"]["minutes"]
        )
        #Expedite checkbox enabled
        self.create_shipment.tab_destination_information.check_expedite()

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()

        # 06.01 Fills Up "Shipment Details"
        shipment_details = data["shipment_details"]
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment=shipment_details["equipment"],
            freight_class=shipment_details["freight_class"],
            po_number=shipment_details["po_number"],
            bill_of_landing_number=shipment_details["bill_of_lading_number"],
            pick_up_number=shipment_details["pick_up_number"],
            shipment_instructions=shipment_details["shipment_instructions"]
        )

        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -------------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()

        # 07.01 Fills Up "Freight Line Item (1)" section
        freight_item = data["freight"]["freight_item"]
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight=freight_item["gross_weight"],
            weight_type=freight_item["weight_type"],
            handling_unit_count=freight_item["handling_unit_count"],
            select_handling_unit_type=freight_item["select_handling_unit_type"],
            commodity_value=freight_item["commodity_value"]
        )

        # 07.02 Fills Up "Dimension" section
        dimension = data["freight"]["dimension"]
        self.create_shipment.tab_freight_items.enter_dimension(
            length=dimension["length"],
            width=dimension["width"],
            height=dimension["height"],
            uom=dimension["uom"],
            commodity_description=dimension["commodity_description"]
        )

        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        bid_params = data["bid_parameters"]
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate=bid_params["book_it_now_rate"],
            bid_expiration_date=generate_future_date(bid_params["bid_expiration_offset_days"]),
            hours=bid_params["bid_expiration_time"]["hours"],
            minutes=bid_params["bid_expiration_time"]["minutes"]
        )

        # 08.02 Upload a File
        upload_file = bid_params["upload_file"]
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name=upload_file["file_name"],
            description=upload_file["description"]
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)

        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # Verify the shipment appears in the customer's loadboard and log out
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        # Validate that the load was found (the "not found" message should not appear)
        actual_message = self.my_board.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        # CARRIER FLOW (manual login)
        # Log in as carrier and search for the shipment
        self.login.login_user(CarrierAccounts.TEST_20).is_login_successful()
        self.menu.carrier_portal.menu_load_board()
        self.load_board.enter_search_by(tracking_number)
        #Validate that the load was found (the "not found" message should not appear)
        actual_message = self.my_board.validate_load_not_found()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found, but it was expected to be present."
        )
        self.load_board.click_search()

        # Validate that the 'Expedite' field is marked as true
        assert self.load_board.is_expedite_true(), "'Expedite' field is not present."

    @test(test_case_id="CT-1694", test_description="Verify it's possible to search a load on shipment creation", feature="Shipment Creation", skip=False)
    def test_customer_shipment_creation_load_search(self,load_iq_login_customer_portal):
        # 01. Verify the user is logged into Customer Portal
        # 02. Loads Shipment Creation Page
        self.menu.customer_portal.menu_shipment_creation()
        # Verify if data is present
        no_data = self.shipment_creation.no_load_results()
        if not no_data:
            tracking_number = self.shipment_creation.get_shipment_tracker_number(1)
            # Search the load number
            self.shipment_creation.search_by(tracking_number)

            # Simple assertion to verify the search result contains the tracking number
            search_result = self.shipment_creation.get_shipment_tracker_number(1)
            assert tracking_number == search_result, f"Expected tracking number '{tracking_number}' not found in search results."

    @test(test_case_id="CT-3583", test_description="Verify it's possible to search a load on shipment creation", feature="Shipment Creation", skip=False)
    def test_shipment_creation_feedback_creation(self,load_iq_login_customer_portal):
        # ("Navigates to 'My payments' page...")
        self.menu.customer_portal.menu_shipment_creation()
        # CLick the feedback button on my payments
        self.shipment_creation.click_feedback_button()
        # Click cancel button and reopen the feedback table .
        self.shipment_creation.click_feedback_button_cancel()
        self.shipment_creation.click_feedback_button()
        # Send data to the table and submit message
        self.shipment_creation.enter_feedback_comment("QA TEST - TESTING FEEDBACK")
        self.shipment_creation.click_feedback_button_submit()
        # Assert that the actual message contains the expected phrase
        actual_message = self.shipment_creation.validate_feedback_text()
        # Expected phrase that should always be part of the message
        expected_text = "Feedback submitted successfully"
        # Assert that the actual message contains the expected phrase
        assert expected_text in actual_message, (
            f"Error: Expected message to contain '{expected_text}', but got '{actual_message}'."
        )