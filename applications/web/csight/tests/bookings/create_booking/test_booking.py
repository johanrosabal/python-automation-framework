import allure

from applications.web.csight.components.menus.CSightMenu import CSightMenu
from applications.web.csight.components.modals.ModalComponent import ModalComponent
from applications.web.csight.pages.bookings.create_booking.CargoDetailsComponent import CargoDetailsComponent
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.bookings.BookingsPage import BookingsPage
from applications.web.csight.pages.bookings.CreateBookingPage import CreateBookingPage
from applications.web.csight.config.decorators import csight
from applications.web.csight.fixtures.fixtures import *
from applications.web.csight.pages.equipment_events.create_equipment_events.CreateEquipmentEventsPage import CreateEquipmentEventsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from core.config.logger_config import setup_logger
from applications.web.csight.pages.salesforce.SalesForcePage import SalesForcePage
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import extract_test_id

logger = setup_logger('TestBooking')


@pytest.fixture(scope="session")
def booking_data():
    path = "../../../data/bookings/CT-2209_create_booking_container_single_reefer.json"
    data = JSONReader().import_json(path)
    data = helpers.parse_dynamic_dates_values(data)
    return data


@pytest.fixture(scope="session")
def equipment_event_data():
    path = "../../../data/equipment_events/CT-2783.json"
    data = JSONReader().import_json(path)
    data = helpers.parse_dynamic_dates_values(data)
    return data


@pytest.fixture(scope="session")
def shared_data():
    return {}


BOOKING_CONTAINERS = [
    "../../../data/bookings/CT-2209_create_booking_container_single_reefer.json",
    "../../../data/bookings/CT-4137_create_booking_container_multiple_reefer.json"
]


@pytest.mark.web
@csight
class TestBooking(BaseTest):
    bookings = BookingsPage.get_instance()
    booking_details = BookingDetailsPage.get_instance()
    create_booking_page = CreateBookingPage.get_instance()
    cargo_details = CargoDetailsComponent.get_instance()
    create_equipment_events = CreateEquipmentEventsPage.get_instance()
    menu = CSightMenu.get_instance()
    modal = ModalComponent.get_instance()
    search_menu = SearchMenu.get_instance()
    salesforce = SalesForcePage.get_instance()

    @pytest.mark.parametrize("path", BOOKING_CONTAINERS, indirect=True, ids=[extract_test_id(path) for path in BOOKING_CONTAINERS])
    @test(test_case_id="CT-2209", test_description="[2209] Validate Single Dry/Reefer container booking creation ", feature="Booking", skip=False)
    def test_create_booking(self, csight_login, path, shared_data):
        # Import Data
        data = JSONReader().import_json(path)
        booking_data = helpers.parse_dynamic_dates_values(data)

        # Load Create Booking Page
        self.create_booking_page.load_page().set_booking_data(data=booking_data)
        # [ORIGIN-DESTINATION TAB] -------------------------------------------------------------------------------------
        # Complete Booking : Booking Party + Bill to Party + Shipping Details + Account Details + Origin + Destination
        self.create_booking_page.origin_destination \
            .fill_booking_party() \
            .fill_bill_to_party() \
            .fill_shipping_details() \
            .fill_account_details() \
            .fill_origin_details() \
            .fill_destination_details().screenshot().save_screenshot(description="CT-2209_01_Create_Booking_Origin_Destination")

        # Next to Cargo Details Form + Proceed Modal Button
        self.create_booking_page.click_next().click_proceed()

        # CARGO_DETAILS TAB---------------------------------------------------------------------------------------------
        self.create_booking_page.cargo_details.process_cargo_type()
        self.create_booking_page.cargo_details.fill_operational_services()
        self.create_booking_page.cargo_details.screenshot().save_screenshot(description="CT-2209_02_Create_Booking_Cargo_Information")
        # Next to Routes
        self.create_booking_page.click_next()

        # ROUTES TAB----------------------------------------------------------------------------------------------------
        route = self.create_booking_page.routes.click_and_get_route_item_information()
        self.create_booking_page.routes.screenshot().save_screenshot(description="CT-2209_03_Create_Booking_Route_Selected")
        # Next to Other Details
        self.create_booking_page.click_next()

        # OTHER DETAILS TAB----------------------------------------------------------------------------------------------------
        self.create_booking_page.other_details.fill_consignee_details()
        self.create_booking_page.other_details.enter_booking_remarks_remark()
        self.create_booking_page.other_details.enter_itn_number()
        self.create_booking_page.other_details.screenshot().save_screenshot(description="CT-2209_04_Create_Booking_Other_Details")
        self.create_booking_page.click_create_booking()
        self.create_booking_page.other_details.screenshot().save_screenshot(description="CT-2209_05_Create_Booking_Confirmation")

        self.modal.is_visible()
        booking_number = self.modal.get_booking_number()
        booking_status = self.modal.get_booking_status()
        booking_message = self.modal.get_modal_message()

        shared_data["booking_number"] = booking_number
        shared_data["booking_status"] = booking_status

        assert (booking_number.startswith("CAT")), "Booking Number Incorrect"
        assert (booking_status == 'Active'), "Booking Status is not match."
        assert (booking_message == 'You will be notified via email once the booking has been confirmed.'), "Booking Message not match."

        # Close Modal
        self.modal.click_close()
        self.booking_details.screenshot().save_screenshot(description="CT-2209_04_Create_Details")

        return self

    @allure.title("Create a gate in full Container")
    @allure.description("This test creates a gate event for a full container in the Equipment Events module.")
    @allure.tag("CSIGHT")
    @allure.link("https://crowley.atlassian.net/browse/CT-2783", name="Jira")
    @allure.testcase("CT-2783")
    @allure.feature("Create a gate in full Container")
    @test(test_case_id="CT-2783", test_description="Create a gate in full Container", feature="Equipment Events", skip=True)
    def test_gate_in_equipment_events(self, csight_login, shared_data, equipment_event_data):
        # shared_data["booking_number"] = "KOSU2501632"
        # Create Equipment Event Page
        self.create_equipment_events.load_page()
        # Enter Equipment Information
        self.create_equipment_events.fill_equipment_information(event_equipment_data=equipment_event_data, booking_number=shared_data["booking_number"])
        self.create_equipment_events.screenshot().save_screenshot(description="CT_2783_01_Create_Equipment_Event")
        # Save Data
        self.create_equipment_events.click_create_equipment_event()
        # Wait Modal Confirmation
        self.modal.is_visible()
        self.create_equipment_events.screenshot().save_screenshot(description="CT_2783_02_Create_Equipment_Event_Confirmation")
        self.modal.click_modal_event_number()
        self.create_equipment_events.screenshot().save_screenshot(description="CT_2783_03_Create_Equipment_Event_Details")

        # Booking Details Information
        self.search_menu.search_booking(shared_data["booking_number"])
        self.search_menu.screenshot().pause(4).save_screenshot(description="CT_2783_04_Booking_Details")
        csight_status = self.booking_details.get_booking_status()

        assert (csight_status == "Active"), "Status Booking Incorrect"

        # Booking Details > Cargo Details
        self.booking_details.click_tab_cargo_details()
        self.booking_details.tab_content_cargo_details.screenshot().save_screenshot(description="CT_2783_05_Cargo_Details")

        # Reading Important Fields to Validate: Equipment Number , Receive Date, Seal No.
        equipment_number = self.booking_details.tab_content_cargo_details.get_operational_equipment_details_equipment_number()
        receive_date = self.booking_details.tab_content_cargo_details.get_operational_equipment_details_receive_date()
        seal_no = self.booking_details.tab_content_cargo_details.get_operational_equipment_details_seal_no()

        # Extracting JSON Data to Assert
        equipment_details = equipment_event_data["tests"]["data"]["equipment_details"]

        # Assertions For Equipment Event
        assert (equipment_number == equipment_details["container_id"]), "Incorrect Equipment Code"
        assert (seal_no == equipment_details["seals"][0]), "Incorrect Seal Number"
        assert ("[Gate In Full]" in receive_date), "Incorrect Receive Date"

