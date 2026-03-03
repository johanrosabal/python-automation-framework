import allure

from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.config.decorators import softship
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.pages.bookings.bookings.CommonElementsBookingsPage import CommonElementsBookingsPage
from applications.web.softship.pages.bookings.bookings.GeneralDataTabPage import GeneralDataTabPage
from applications.web.softship.pages.bookings.bookings.BookingHomePage import BookingsHomePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import user
from core.utils.decorator import test
from core.utils import helpers
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('TestBookingsPagesValidations')


@pytest.fixture(scope="class")
def general_data_tab():
    path = helpers.get_file_path("general_data.json")
    data = JSONReader().import_json(path)
    logger.info(f"[Fixture] 'general data tab' data: {data}")
    return data


@pytest.mark.web
@softship
class TestBookingsPagesValidations(SoftshipBaseTest):

    # Init App
    menu = SoftshipMenu.get_instance()
    home_page = BookingsHomePage.get_instance()
    booking_information_page = CommonElementsBookingsPage.get_instance()
    general_data = GeneralDataTabPage.get_instance()

    @test(test_case_id="CT-1536", test_description="Validate booking home page", feature="Bookings Home Page")
    def test_validate_home_page_elements(self, softship_login_booking, record_property):
        record_property("test_key", "CT-1536")
        record_property("testplankey", "CT-1276")

        # 01. Go to Booking Page
        self.home_page.load_page()
        # 02. Validate the presence of all the elements
        self.home_page.validate_locators()

    @test(test_case_id="CT-1537", test_description="Validate booking information section", feature="Bookings Home Page")
    def test_validate_booking_information_section_elements(self, softship_login_booking, record_property):
        record_property("test_key", "CT-1537")
        record_property("testplankey", "CT-1276")

        # 01. Go to Booking Page
        self.home_page.load_page()
        # 02. Click on create button
        self.home_page.click_create()
        # 03. Validate booking information section
        self.booking_information_page.validate_information_status()

    @test(test_case_id="CT-1538", test_description="Validate booking header information ", feature="Bookings Home Page")
    def test_validate_header_during_booking_process(self, softship_login_booking, general_data_tab, record_property):
        record_property("test_key", "CT-1538")
        record_property("testplankey", "CT-1276")
        data = general_data_tab['tests']['header_tab']
        # 01. Go to Booking Page
        self.home_page.load_page()
        # 02. Click on create button
        self.home_page.click_create()
        # 03. Validate booking information section
        self.general_data.validate_general_tab_elements(data['from_receipt_term'], data['from_location_zip'], data['from_location_name'], data['to_delivery_term'], data['to_location_zip'], data['to_location_name'])