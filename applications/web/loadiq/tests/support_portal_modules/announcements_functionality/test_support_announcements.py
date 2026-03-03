from time import sleep

from applications.web.loadiq.common.DateUtils import DateUtils
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.components.menus.support_portal.SupportPortalMenu import SupportPortalMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.announcements.AnnouncementesPage import AnnouncementsPage
from applications.web.loadiq.pages.create_user.CreateUserFormPage import CreateUserFormPage
from applications.web.loadiq.pages.user_management.UserManagementPage import UserManagementPage
from applications.web.loadiq.pages.shipment_creation.ShipmentCreationPage import ShipmentCreationPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.json_data_helper import JSONDataHelper
from applications.web.loadiq.pages.my_board.MyBoardPage import MyBoardPage

from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers
import allure

logger = setup_logger('TestSupportAnnouncements')


@pytest.mark.web
@loadiq
class TestSupportAnnouncements(BaseTest):

    menu = LoadIQMenu.get_instance()
    announcements_page = AnnouncementsPage.get_instance()

    @allure.step("{step_name}")
    def take_screenshot(self, step_name: str):
        """Helper method to take screenshots with Allure"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Screenshot - {step_name}",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.title("[UI] Verify Add/View announcements in LoadIQ(Support Portal)")
    @allure.description(
        "[UI] Verify Add/View announcements in LoadIQ(Support Portal)")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3678", name="Jira")
    @allure.testcase("CT-3678")
    @allure.feature("Announcements")
    #@pytest.mark.xray('CT-3678')
    @test(test_case_id="CT-3678", test_description="[UI] Verify Add/View announcements in LoadIQ(Support Portal)", feature="User Creation", skip=False)
    def test_support_check_announcements_page(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-3678")
        self.take_screenshot("Customer User Logged In")
        #file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-3678"

        # 01. The user goes to "Announcements" page
        self.menu.support_portal.menu_announcements(1)
        self.take_screenshot("Validate Announcements Page Loaded")

        # 02. Check Announcements table columns
        self.announcements_page.check_announcements_table_columns()
        self.take_screenshot("Validate Announcements Table Columns")

        # 03. Check Start Date and End Date formats mm/dd/yyyy HH:mm
        self.announcements_page.check_start_date_end_date_formats()
        self.take_screenshot("Validate Announcements Start and End Formats")

    @allure.title("[UI] Verify it's possible to create announcements in LoadIQ (Support Portal)")
    @allure.description(
        "Verifies it's possible to create announcements in LoadIQ (Support Portal)")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3679", name="Jira")
    @allure.testcase("CT-3679")
    @allure.feature("Announcements")
    # @pytest.mark.xray('CT-3679')
    @test(test_case_id="CT-3679", test_description="Verifies it's possible to create announcements in LoadIQ (Support Portal)",
          feature="User Creation", skip=False)
    def test_support_create_announcement(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-3679")
        self.take_screenshot("Customer User Logged In")
        # file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-3679"

        # 01. The user goes to "Announcements" page
        self.menu.support_portal.menu_announcements(1)
        self.take_screenshot("Validate Announcements Page Loaded")

        # 02. Click Add Announcements Button
        self.announcements_page.click_add_announcements_button()
        self.take_screenshot("Validate Click Add Announcements button")

        # 03. Check Add Announcements Window
        self.announcements_page.check_add_announcements_window()
        self.take_screenshot("Validate Add Announcements Window elements")

        # 04. Select Announcement Type Dropdown
        self.announcements_page.add_announcements_select_type("Informative")
        self.take_screenshot("Validate Select Announcement Type Dropdown")

        # 05. Enter Announcement Message
        message = "Announcement Message QA Test"
        self.announcements_page.add_announcements_enter_message(message)
        self.take_screenshot("Validate Enter Announcement Message")

        # 06. Enter Start Date
        start_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 0)
        self.announcements_page.add_announcements_enter_start_date(start_date)
        self.take_screenshot("Validate Enter Announcement Start Date")

        # 06. Enter End Date
        end_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 7)
        self.announcements_page.add_announcements_enter_end_date(end_date)
        self.take_screenshot("Validate Enter Announcement End Date")

        # 07. Click Create Button
        self.announcements_page.click_add_announcements_create_button()
        self.take_screenshot("Validate Click Add Announcements Create Button")

        # 08. Validate Success Message
        self.announcements_page.validate_announcement_added_success_message()
        self.take_screenshot("Validate Add Announcements Success Message")

    @allure.title("[UI] Verify announcement field accepts  500 Characters")
    @allure.description(
        "[UI] Verify announcement field accepts  500 Characters")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-4674", name="Jira")
    @allure.testcase("CT-4674")
    @allure.feature("Announcements")
    # @pytest.mark.xray('CT-4674')
    @test(test_case_id="CT-4674",
          test_description="[UI] Verify announcement field accepts  500 Characters",
          feature="User Creation", skip=False)
    def test_support_create_announcement_500_characters(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-4674")
        self.take_screenshot("Customer User Logged In")
        # file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-4674"

        # 01. The user goes to "Announcements" page
        self.menu.support_portal.menu_announcements(1)
        self.take_screenshot("Validate Announcements Page Loaded")

        # 02. Click Add Announcements Button
        self.announcements_page.click_add_announcements_button()
        self.take_screenshot("Validate Click Add Announcements button")

        # 03. Check Add Announcements Window
        self.announcements_page.check_add_announcements_window()
        self.take_screenshot("Validate Add Announcements Window elements")

        # 04. Select Announcement Type Dropdown
        self.announcements_page.add_announcements_select_type("Informative")
        self.take_screenshot("Validate Select Announcement Type Dropdown")

        # 05. Enter Announcement Message
        message = "Add Announcement Message 500 Characters - Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede moll"
        self.announcements_page.add_announcements_enter_message(message)
        self.take_screenshot("Validate Enter Announcement Message")

        # 06. Get Announcement Message Entered
        message_entered = self.announcements_page.add_announcements_get_message_entered()
        assert (len(message_entered) == 500)

        # 07. Enter Start Date
        start_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 0)
        self.announcements_page.add_announcements_enter_start_date(start_date)
        self.take_screenshot("Validate Enter Announcement Start Date")

        # 08. Enter End Date
        end_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 7)
        self.announcements_page.add_announcements_enter_end_date(end_date)
        self.take_screenshot("Validate Enter Announcement End Date")

        # 09. Click Create Button
        self.announcements_page.click_add_announcements_create_button()
        self.take_screenshot("Validate Click Add Announcements Create Button")

        # 10. Validate Success Message
        self.announcements_page.validate_announcement_added_success_message()
        self.take_screenshot("Validate Add Announcements Success Message")

    @allure.title("[UI] Verify announcement field rejects input over 500 Characters")
    @allure.description(
        "[UI] Verify announcement field rejects input over 500 Characters")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-4675", name="Jira")
    @allure.testcase("CT-4675")
    @allure.feature("Announcements")
    # @pytest.mark.xray('CT-4675')
    @test(test_case_id="CT-4675",
          test_description="[UI] Verify announcement field rejects input over 500 Characters",
          feature="User Creation", skip=False)
    def test_support_create_announcement_over_500_characters(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-4675")
        self.take_screenshot("Customer User Logged In")
        # file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-4675"

        # 01. The user goes to "Announcements" page
        self.menu.support_portal.menu_announcements(1)
        self.take_screenshot("Validate Announcements Page Loaded")

        # 02. Click Add Announcements Button
        self.announcements_page.click_add_announcements_button()
        self.take_screenshot("Validate Click Add Announcements button")

        # 03. Check Add Announcements Window
        self.announcements_page.check_add_announcements_window()
        self.take_screenshot("Validate Add Announcements Window elements")

        # 04. Select Announcement Type Dropdown
        self.announcements_page.add_announcements_select_type("Informative")
        self.take_screenshot("Validate Select Announcement Type Dropdown")

        # 05. Enter Announcement Message
        message = "Add Announcement Message 510 Characters - Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede moll pede moll"
        self.announcements_page.add_announcements_enter_message(message)
        self.take_screenshot("Validate Enter Announcement Message")

        # 06. Get Announcement Message Entered
        message_entered = self.announcements_page.add_announcements_get_message_entered()
        assert (len(message_entered) == 500)

        # 07. Enter Start Date
        start_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 0)
        self.announcements_page.add_announcements_enter_start_date(start_date)
        self.take_screenshot("Validate Enter Announcement Start Date")

        # 08. Enter End Date
        end_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 7)
        self.announcements_page.add_announcements_enter_end_date(end_date)
        self.take_screenshot("Validate Enter Announcement End Date")

        # 09. Click Create Button
        self.announcements_page.click_add_announcements_create_button()
        self.take_screenshot("Validate Click Add Announcements Create Button")

        # 10. Validate Success Message
        self.announcements_page.validate_announcement_added_success_message()
        self.take_screenshot("Validate Add Announcements Success Message")

    @allure.title("[UI] Verify valid input with shorter announcements")
    @allure.description(
        "[UI] Verify valid input with shorter announcements")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-4676", name="Jira")
    @allure.testcase("CT-4676")
    @allure.feature("Announcements")
    # @pytest.mark.xray('CT-4676')
    @test(test_case_id="CT-4676",
          test_description="[UI] Verify valid input with shorter announcements",
          feature="User Creation", skip=False)
    def test_support_create_announcement_shorter_characters(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-4676")
        self.take_screenshot("Customer User Logged In")
        # file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-4676"

        # 01. The user goes to "Announcements" page
        self.menu.support_portal.menu_announcements(1)
        self.take_screenshot("Validate Announcements Page Loaded")

        # 02. Click Add Announcements Button
        self.announcements_page.click_add_announcements_button()
        self.take_screenshot("Validate Click Add Announcements button")

        # 03. Check Add Announcements Window
        self.announcements_page.check_add_announcements_window()
        self.take_screenshot("Validate Add Announcements Window elements")

        # 04. Select Announcement Type Dropdown
        self.announcements_page.add_announcements_select_type("Informative")
        self.take_screenshot("Validate Select Announcement Type Dropdown")

        # 05. Enter Announcement Message
        message = "Add Announcement Message 100 Characters - Lorem ipsum dolor sit amet, consect etuer adipiscing elit."
        self.announcements_page.add_announcements_enter_message(message)
        self.take_screenshot("Validate Enter Announcement Message")

        # 06. Get Announcement Message Entered
        message_entered = self.announcements_page.add_announcements_get_message_entered()
        assert (len(message_entered) == 100)

        # 07. Enter Start Date
        start_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 0)
        self.announcements_page.add_announcements_enter_start_date(start_date)
        self.take_screenshot("Validate Enter Announcement Start Date")

        # 08. Enter End Date
        end_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 7)
        self.announcements_page.add_announcements_enter_end_date(end_date)
        self.take_screenshot("Validate Enter Announcement End Date")

        # 09. Click Create Button
        self.announcements_page.click_add_announcements_create_button()
        self.take_screenshot("Validate Click Add Announcements Create Button")

        # 10. Validate Success Message
        self.announcements_page.validate_announcement_added_success_message()
        self.take_screenshot("Validate Add Announcements Success Message")

    @allure.title("[UI] Verify Date/Time validation on announcement creation (Support Portal)")
    @allure.description(
        "[UI] Verify Date/Time validation on announcement creation (Support Portal)")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-3680", name="Jira")
    @allure.testcase("CT-3680")
    @allure.feature("Announcements")
    # @pytest.mark.xray('CT-3680')
    @test(test_case_id="CT-3680",
          test_description="[UI] Verify Date/Time validation on announcement creation (Support Portal)",
          feature="User Creation", skip=False)
    def test_support_create_announcement_validate_date_time(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-3680")
        self.take_screenshot("Customer User Logged In")
        # file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-3680"

        # 01. The user goes to "Announcements" page
        self.menu.support_portal.menu_announcements(1)
        self.take_screenshot("Validate Announcements Page Loaded")

        # 02. Click Add Announcements Button
        self.announcements_page.click_add_announcements_button()
        self.take_screenshot("Validate Click Add Announcements button")

        # 03. Enter End Date
        end_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 1)
        self.announcements_page.add_announcements_enter_end_date(end_date)
        self.take_screenshot("Validate Enter Announcement End Date")

        # 04. Enter Start Date
        start_date = DateUtils.generate_date("%m/%d/%Y %H:%M", 2)
        self.announcements_page.add_announcements_enter_start_date_future(start_date)
        self.take_screenshot("Validate Enter Announcement Start Date")

        # 05. Validate error message Datetime
        self.announcements_page.validate_add_announcement_start_end_datetime_error_message()
        self.take_screenshot("Validate Add Announcement Start/End Datetime Error Message")

