from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage
from applications.web.loadiq.fixtures.fixtures import *
from core.utils.fixtures import *
from applications.web.loadiq.pages.shipment_creation.create_shipment.CreateShipmentPage import CreateShipmentPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.helpers import generate_future_date
from core.utils.json_data_helper import JSONDataHelper

logger = setup_logger('TestCustomerShipmentCreation')


@pytest.mark.web
@loadiq
class TestCustomerShipmentCreation(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    shipment_creation = ShipmentCreationPage.get_instance()
    create_shipment = CreateShipmentPage.get_instance()
    my_board = MyBoardPage.get_instance()

    shipment_number = None

    # Standard ---------------------------------------------------------------------------------------------------------
    @test(test_case_id="CT-1498", test_description="Verify Create a new shipment: First Come, First Served", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_first_come(self, load_iq_login_customer_portal, record_property):
        record_property("test_key", "CT-1498")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(5),
            to_day=generate_future_date(10),
            open_hours="01",
            open_minutes="00",
            close_hours="13",
            close_minutes="00",
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(10),
            to_day=generate_future_date(15),
            open_hours="11",
            open_minutes="00",
            close_hours="23",
            close_minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class=" Class 50 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    @test(test_case_id="CT-1737", test_description="Verify Create a new shipment: Pre-Schedule", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_pre_schedule(self, record_property):
        record_property("test_key", "CT-1737")

        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_pre_scheduled(
            from_day=generate_future_date(10),
            hours="23",
            minutes="00"
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_pre_scheduled(
            from_day=generate_future_date(10),
            hours="23",
            minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class=" Class 60 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    @test(test_case_id="CT-1739", test_description="Verify Create a new shipment: Call for Appointment", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_call_for_appointment(self, record_property):
        record_property("test_key", "CT-1739")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: Call For Appointment" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_call_for_appointment(
            to_day=generate_future_date(10),
            point_of_contact=True
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_call_for_appointment(
            to_day=generate_future_date(10),
            point_of_contact=True
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class= " Class 50 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    # Hazmat -----------------------------------------------------------------------------------------------------------
    @test(test_case_id="CT-2054", test_description="Verify it's possible to create a new hazmat shipment - First Come, First Served", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_first_come_with_hazmat(self, load_iq_login_customer_portal, record_property):
        record_property("test_key", "CT-2054")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(5),
            to_day=generate_future_date(10),
            open_hours="01",
            open_minutes="00",
            close_hours="13",
            close_minutes="00"
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(10),
            to_day=generate_future_date(15),
            open_hours="11",
            open_minutes="00",
            close_hours="23",
            close_minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class=" Class 55 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )

        # 07.03 Adds Hazmat Information
        self.create_shipment.tab_freight_items.enter_hazmat(
            un_na_number="1234567890",
            hazmat_class="Class 3 - Flammable Liquids",
            hazmat_contact_number="1141850001",
            packing_group="Group 2 - Moderate Danger",
            proper_shipping_name="Lithium ion batteries"
        )

        # 07.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

        JSONDataHelper.save_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json",
            "CT-3766",
            shipment_id=tracking_number,
            un_na_number="1234567890",
            hazmat_class="Class 3 - Flammable Liquids",
            hazmat_contact_number="1141850001",
            packing_group="Group 2 - Moderate Danger",
            proper_shipping_name="Lithium ion batteries"
        )

        JSONDataHelper.save_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json",
            "CT-3515",
            pickup_Date = generate_future_date(5),
            delivery_Date = generate_future_date(10)
        )

    @test(test_case_id="CT-2055", test_description="Verify it's possible to create a new hazmat shipment - Pre-Scheduled", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_pre_schedule_with_hazmat(self, record_property):
        record_property("test_key", "CT-2055")

        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_pre_scheduled(
            from_day=generate_future_date(10),
            hours="23",
            minutes="00"
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_pre_scheduled(
            from_day=generate_future_date(10),
            hours="11",
            minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class=" Class 65 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )

        # 07.03 Adds Hazmat Information
        self.create_shipment.tab_freight_items.enter_hazmat(
            un_na_number="1234567890",
            hazmat_class="Class 3 - Flammable Liquids",
            hazmat_contact_number="1141850001",
            packing_group="Group 2 - Moderate Danger",
            proper_shipping_name="Lithium ion batteries"
        )

        # 07.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    @test(test_case_id="CT-2056", test_description="Verify it's possible to create a new hazmat shipment - Call for Appointment", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_call_for_appointment_with_hazmat(self, record_property):
        record_property("test_key", "CT-2056")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: Call For Appointment" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_call_for_appointment(
            to_day=generate_future_date(10),
            point_of_contact=True
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_call_for_appointment(
            to_day=generate_future_date(10),
            point_of_contact=True
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class=" Class 50 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )

        # 07.03 Adds Hazmat Information
        self.create_shipment.tab_freight_items.enter_hazmat(
            un_na_number="1234567890",
            hazmat_class="Class 3 - Flammable Liquids",
            hazmat_contact_number="1141850001",
            packing_group="Group 2 - Moderate Danger",
            proper_shipping_name = "Lithium ion batteries"
        )

        # 07.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    # Temperature ------------------------------------------------------------------------------------------------------
    @test(test_case_id="CT-2058", test_description="Verify Create a new shipment: - First Come, First Served Controlled with Temperature", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_first_come_with_temperature(self, record_property):
        record_property("test_key", "CT-2058")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(5),
            to_day=generate_future_date(10),
            open_hours="01",
            open_minutes="00",
            close_hours="13",
            close_minutes="00"
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(10),
            to_day=generate_future_date(15),
            open_hours="11",
            open_minutes="00",
            close_hours="23",
            close_minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details_with_temperature(
            equipment="53' Temperature Controlled",
            freight_class=" Class 50 ",
            low_temperature=-10,
            high_temperature=9,
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    @test(test_case_id="CT-2059", test_description="Verify Create a new shipment: Pre-Schedule with Temperature", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_pre_schedule_with_temperature(self, record_property):
        record_property("test_key", "CT-2059")

        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_pre_scheduled(
            from_day=generate_future_date(10),
            hours="23",
            minutes="00"
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_pre_scheduled(
            from_day=generate_future_date(10),
            hours="23",
            minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details_with_temperature(
            equipment="3' Temperature Controlled",
            freight_class=" Class 110 ",
            low_temperature=-10,
            high_temperature=9,
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    @test(test_case_id="CT-2060", test_description="Verify Create a new shipment: Call for Appointment with Temperature", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_call_for_appointment_with_temperature(self, record_property):
        record_property("test_key", "CT-2060")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: Call For Appointment" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_call_for_appointment(
            to_day=generate_future_date(10),
            point_of_contact=True
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: Pre-Scheduled" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_call_for_appointment(
            to_day=generate_future_date(10),
            point_of_contact=True
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details_with_temperature(
            equipment="3' Temperature Controlled",
            freight_class=" Class 110 ",
            low_temperature=-10,
            high_temperature=9,
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

    # Search -----------------------------------------------------------------------------------------------------------
    @test(test_case_id="CT-2256", test_description="Verify it's possible to search a load", feature="Shipment Creation", skip=False)
    def test_customer_shipment_creation_search_a_tracker_number(self, record_property):
        record_property("test_key", "CT-2256")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

        # 02. Loads Shipment Creation Page
        self.menu.customer_portal.menu_shipment_creation()

        # 03. User clicks on "Create Shipment" button
        self.shipment_creation.click_create_shipment()

        # 04. Reading Current Tracking Number
        tracking_number = self.create_shipment.get_shipment_tracker_number()

        # ORIGIN TAB ---------------------------------------------------------------------------------------------------
        # 05. User should complete "Original Information" Tab Form
        self.create_shipment.click_origin_information()

        # 05.01 Fills Up "Origin Information" Section
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami",
            location="Miami",
            address="Miami, FL, USA",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(5),
            to_day=generate_future_date(10),
            open_hours="01",
            open_minutes="00",
            close_hours="13",
            close_minutes="00"
        )

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 06. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 06.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="22554 Stafford",
            location="22554 Stafford",
            address="Stafford, VA 22554, USA",
            address_line_2="N/A"
        )
        # 06.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 06.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(10),
            to_day=generate_future_date(15),
            open_hours="11",
            open_minutes="00",
            close_hours="23",
            close_minutes="00"
        )

        # 06.04 Clicks on "Save For Later" Button
        self.create_shipment.tab_destination_information.click_save_for_later()

        no_data = self.shipment_creation.no_load_results()
        if not no_data:
            # 07. Type Existing Tracking Number
            # tracking_number = self.shipment_creation.get_shipment_tracker_number(1)

            # 08. Search The Tracking Number
            self.shipment_creation.search_by(tracking_number)

            # 09. Get Track Information
            item = self.shipment_creation.get_shipment_item(1)
            search_tracker_number = item[0]
            assert search_tracker_number == tracking_number, f"Tracker Number Incorrect, Expected {tracking_number} and Found {search_tracker_number}"
        else:
            logger.warning("No records found, for execute this test.")

        # Sign Out User
        self.menu.logout()

    @test(test_case_id="CT-3792", test_description="Validate the new creation of a load indicating that is expedite in the new checkbox", feature="Shipment Creation", skip=False)
    def test_customer_create_shipment_first_come_expedite(self, load_iq_login_customer_portal, record_property,  save_json_data):
        record_property("test_key", "CT-3792")
        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

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
        self.create_shipment.tab_origin_information.enter_origin_location(
            name="Miami, FL 3313",
            location="Miami, FL 3313",
            address="Miami, FL 33131, USA",
            address_line_2="N/A"
        )
        # 04.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_origin_information.enter_contact(
            name="John",
            phone="1141850000",
            email="bob@flinstones.com"
        )

        # 04.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_origin_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(5),
            to_day=generate_future_date(10),
            open_hours="01",
            open_minutes="00",
            close_hours="13",
            close_minutes="00"
        )

        # 04.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_origin_information.click_save_and_continue()

        # DESTINATION TAB ----------------------------------------------------------------------------------------------
        # 05. User should complete "Destination Information" Tab Form
        self.create_shipment.click_destination_information()
        # 05.01 Fill Ups "Destination Information" Section
        self.create_shipment.tab_destination_information.enter_destination_location(
            name="Los Angeles, CA 90012",
            location="Los Angeles, CA 90012",
            address="Los Angeles, CA 90012",
            address_line_2="N/A"
        )
        # 05.02 Fills Up "Contact Information" Section
        self.create_shipment.tab_destination_information.enter_contact(
            name="Damian",
            phone="9988779936",
            email="test@hotmail.com"
        )

        # 05.03 Fill Up "Pick Up Appointment: First Come, First Served" Information
        self.create_shipment.tab_destination_information.enter_pickup_appointment_first_come_first_serve(
            from_day=generate_future_date(10),
            to_day=generate_future_date(15),
            open_hours="11",
            open_minutes="00",
            close_hours="23",
            close_minutes="00"
        )
        self.create_shipment.tab_destination_information.check_expedite()

        # 05.04 Clicks on "Save & Continue" Button
        self.create_shipment.tab_destination_information.click_save_and_continue()

        # SHIPMENT DETAILS TAB -----------------------------------------------------------------------------------------
        # 06. User should complete "Shipment Details" Tab Form
        self.create_shipment.click_shipment_details()
        # 06.01 Fills Up "Shipment Details"
        self.create_shipment.tab_shipment_details.enter_shipment_details(
            equipment="Container",
            freight_class=" Class 50 ",
            po_number="1234",
            bill_of_landing_number="1234",
            pick_up_number="1234",
            shipment_instructions="Shipment Automation Test"
        )
        # 06.02 Clicks on "Save & Continue" Button
        self.create_shipment.tab_shipment_details.click_save_and_continue()

        # FREIGHT ITEMS TAB -----------------------------------------------------------------------------------------
        # 07. User should complete "Freight" Tab Form
        self.create_shipment.click_freight_items()
        # 07.01 Fills Up "Freight Line Item (1)" section
        self.create_shipment.tab_freight_items.enter_freight_item(
            gross_weight="100",
            weight_type="Lb",
            handling_unit_count="1",
            select_handling_unit_type="Pallet",
            commodity_value="10000"
        )
        # 07.02 Fills Up "Dimension" section
        self.create_shipment.tab_freight_items.enter_dimension(
            length="121",
            width="212",
            height="222",
            uom="Inch",
            commodity_description="Shipment Automation Test"
        )
        # 07.03 Clicks on "Save & Continue" Button
        self.create_shipment.tab_freight_items.click_save_and_continue()

        # BID PARAMETERS TAB -------------------------------------------------------------------------------------------
        # 08. User should complete "Freight" Tab Form
        self.create_shipment.click_bid_parameters()

        # 08.01 Fills Up "Bid Parameters" section
        self.create_shipment.tab_bid_parameters.enter_bid_parameters(
            book_it_now_rate="100",
            bid_expiration_date=generate_future_date(),
            hours="23",
            minutes="00"
        )

        # 08.02 Upload a File
        self.create_shipment.tab_bid_parameters.click_upload()
        self.create_shipment.tab_bid_parameters.click_add_file(
            file_name="upload_test_document.png",
            description="Automation Test Upload"
        )

        # 08.03 Read File Table Information
        self.create_shipment.tab_bid_parameters.get_table_document_item(1)
        # 08.04 Save & Submit Information
        self.create_shipment.tab_bid_parameters.click_save_and_submit()

        # 09 Search New Shipment
        self.my_board.load_page()
        self.my_board.search_by(tracking_number)
        item = self.my_board.get_shipment_item(1)
        assert tracking_number == item[0], f"Shipment Tracking Number not match, current {tracking_number}, found {item[0]}"

        save_json_data(
            "applications/web/loadiq/data/carrier_portal/my_offers/test_my_offers.json",
            "CT-3942",
            "shipment_id",
            tracking_number
        )
