import pytest

from applications.web.csight.components.menus.CSightMenu import CSightMenu
from core.data.sources.JSON_reader import JSONReader
from core.ui.common.BaseTest import BaseTest, user
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.bookings.BookingsPage import BookingsPage
from applications.web.csight.pages.bookings.CreateBookingPage import CreateBookingPage
from applications.web.csight.config.decorators import csight
from core.config.logger_config import setup_logger
from applications.web.csight.pages.login.EmployeePortalPage import EmployeePortalPage
from core.utils import helpers
from core.utils.decorator import test


@pytest.fixture(scope="session")
def booking_data():
    data = JSONReader().import_json(helpers.get_file_path("booking_creation.json"))
    return helpers.parse_dynamic_dates_values(data)




@pytest.mark.web
@csight
class TestLogin(BaseTest):
    login = LoginPage.get_instance()
    employee_portal = EmployeePortalPage.get_instance()
    create_booking_page = CreateBookingPage.get_instance()
    booking_details = BookingDetailsPage.get_instance()

    bookings = BookingsPage.get_instance()
    menu = CSightMenu.get_instance()

    @test(test_case_id="00001", test_description="Sign in with Logistics Account", feature="Login", skip=False)
    def test_login_user(self, user):
        # Login User
        self.login.load_page()
        self.login.login_user(user=user)

    @test(test_case_id="00002", test_description="Booking: Origin - Destination", feature="Login", skip=False)
    def test_booking_origin_destination(self, booking_data):
        # Origin Destination: Booking Party
        # self.menu.click_menu_bookings()
        self.create_booking_page.load_page()
        # ORIGIN-DESTINATION -------------------------------------------------------------------------------------------
        # self.create_booking.origin_destination.load_tab()
        # Complete Booking Party Section
        booking_party = booking_data['tests']['booking']['origin_destination']['booking_party']

        self.create_booking_page.origin_destination.fill_booking_party(
            booking_account=booking_party["booking_account"],
            address=booking_party["address"],
            contact_name=booking_party["contact_name"],
            phone=booking_party["phone_number"],
            email=booking_party["email"]
        )

        # Complete Bill to Par
        bill_to_party = booking_data['tests']['booking']['origin_destination']['bill_to_party']

        self.create_booking_page.origin_destination.fill_bill_to_party(
            same_as_booking_party=bill_to_party["same_as_booking_party"],
            bill_to_account=bill_to_party["bill_to_account"],
            address=bill_to_party["address"],
            contact_name=bill_to_party["contact_name"],
            bill_to_party_type=bill_to_party["bill_to_party_type"],
            phone=bill_to_party["phone_number"],
            email=bill_to_party["email"]
        )

        # Enter Shipping Details
        shipping_details = booking_data['tests']['booking']['origin_destination']['shipping_details']
        self.create_booking_page.origin_destination.enter_cargo_ready_for_transport(
            shipping_details["cargo_ready_for_transport"]
        )

        # Complete Account Details
        account_details = booking_data['tests']['booking']['origin_destination']['account_details']
        self.create_booking_page.origin_destination.fill_account_details(
            same_as_booking_party=account_details["same_as_booking_party"],
            same_as_bill_to_party=account_details["same_as_bill_to_party"],
            search_using_account_name=account_details["search_using_account_name"],
            search_using_contract_number=account_details["search_using_contract_number"],
            account_name=account_details["account_name"],
            address=account_details["address"],
            contact_name=account_details["contact_name"],
            phone=account_details["phone_number"],
            email=account_details["email"],
            contract_number=account_details["contract_number"]
        )
        # Origin Details -----------------------------------------------------------------------------------------------
        origin_details_pick_up_address = booking_data['tests']['booking']['origin_destination']['origin_details_pick_up_address']
        self.create_booking_page.origin_destination.enter_origin_details(origin_details_pick_up_address["origin"])
        self.create_booking_page.origin_destination.select_origin_details(origin_details_pick_up_address["origin"])

        self.create_booking_page.origin_destination.enter_origin_country_cargo(origin_details_pick_up_address["origin_country_cargo"])
        self.create_booking_page.origin_destination.select_origin_country_cargo(origin_details_pick_up_address["origin_country_cargo"])

        self.create_booking_page.origin_destination.click_checkbox_crowley_trucking_for_pick_up(origin_details_pick_up_address["crowley_trucking_pickup"])

        # Destination Details ------------------------------------------------------------------------------------------
        destination_details_final_delivery_address = booking_data['tests']['booking']['origin_destination']['destination_details_final_delivery_address']
        self.create_booking_page.origin_destination.enter_destination_details(destination_details_final_delivery_address["final_destination"])
        self.create_booking_page.origin_destination.select_destination_details(destination_details_final_delivery_address["final_destination"])
        self.create_booking_page.origin_destination.click_checkbox_crowley_trucking_for_delivery(destination_details_final_delivery_address["crowley_trucking_pickup"])
        self.create_booking_page.click_next()
        self.create_booking_page.click_proceed()

        # Cargo -------------------------------------------------------------------------------------------
        cargo_details = booking_data['tests']['booking']['cargo_details']
        self.create_booking_page.cargo_details.process_cargo_type(cargo_details['cargo_type'])




    @test(test_case_id="00003", test_description="Booking: Origin - Destination", feature="Login", skip=False)
    def test_booking_single_reefer_container(self, single_reefer_data):
        # Origin Destination: Booking Party
        # self.menu.click_menu_bookings()
        self.create_booking_page.load_page()
        # ORIGIN-DESTINATION -------------------------------------------------------------------------------------------
        # self.create_booking.origin_destination.load_tab()
        # Complete Booking Party Section
        booking_party = single_reefer_data['tests']['booking']['origin_destination']['booking_party']

        self.create_booking_page.origin_destination.fill_booking_party(
            booking_account=booking_party["booking_account"],
            address=booking_party["address"],
            contact_name=booking_party["contact_name"],
            phone=booking_party["phone_number"],
            email=booking_party["email"]
        )

        # Complete Bill to Par
        bill_to_party = single_reefer_data['tests']['booking']['origin_destination']['bill_to_party']

        self.create_booking_page.origin_destination.fill_bill_to_party(
            same_as_booking_party=bill_to_party["same_as_booking_party"],
            bill_to_account=bill_to_party["bill_to_account"],
            address=bill_to_party["address"],
            contact_name=bill_to_party["contact_name"],
            bill_to_party_type=bill_to_party["bill_to_party_type"],
            phone=bill_to_party["phone_number"],
            email=bill_to_party["email"]
        )

        # Enter Shipping Details
        shipping_details = single_reefer_data['tests']['booking']['origin_destination']['shipping_details']
        self.create_booking_page.origin_destination.enter_cargo_ready_for_transport(
            shipping_details["cargo_ready_for_transport"]
        )

        # Complete Account Details
        account_details = single_reefer_data['tests']['booking']['origin_destination']['account_details']
        self.create_booking_page.origin_destination.fill_account_details(
            same_as_booking_party=account_details["same_as_booking_party"],
            same_as_bill_to_party=account_details["same_as_bill_to_party"],
            search_using_account_name=account_details["search_using_account_name"],
            search_using_contract_number=account_details["search_using_contract_number"],
            account_name=account_details["account_name"],
            address=account_details["address"],
            contact_name=account_details["contact_name"],
            phone=account_details["phone_number"],
            email=account_details["email"],
            contract_number=account_details["contract_number"]
        )
        # Origin Details -----------------------------------------------------------------------------------------------
        origin_details_pick_up_address = single_reefer_data['tests']['booking']['origin_destination']['origin_details_pick_up_address']
        self.create_booking_page.origin_destination.enter_origin_details(origin_details_pick_up_address["origin"])
        self.create_booking_page.origin_destination.select_origin_details(origin_details_pick_up_address["origin"])

        self.create_booking_page.origin_destination.enter_origin_country_cargo(origin_details_pick_up_address["origin_country_cargo"])
        self.create_booking_page.origin_destination.select_origin_country_cargo(origin_details_pick_up_address["origin_country_cargo"])

        self.create_booking_page.origin_destination.click_checkbox_crowley_trucking_for_pick_up(origin_details_pick_up_address["crowley_trucking_pickup"])

        # Destination Details ------------------------------------------------------------------------------------------
        destination_details_final_delivery_address = single_reefer_data['tests']['booking']['origin_destination']['destination_details_final_delivery_address']
        self.create_booking_page.origin_destination.enter_destination_details(destination_details_final_delivery_address["final_destination"])
        self.create_booking_page.origin_destination.select_destination_details(destination_details_final_delivery_address["final_destination"])
        self.create_booking_page.origin_destination.click_checkbox_crowley_trucking_for_delivery(destination_details_final_delivery_address["crowley_trucking_pickup"])
        self.create_booking_page.click_next()
        self.create_booking_page.click_proceed()

        # Cargo -------------------------------------------------------------------------------------------
        cargo_details = single_reefer_data['tests']['booking']['cargo_details']
        self.create_booking_page.cargo_details.process_cargo_type(cargo_details['cargo_type'])