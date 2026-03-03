from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.components.menus.support_portal.SupportPortalMenu import SupportPortalMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
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

logger = setup_logger('TestSupportUserCreation')


@pytest.mark.web
@loadiq
class TestSupportUserCreation(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    create_user = CreateUserFormPage.get_instance()
    user_management = UserManagementPage.get_instance()

    @allure.step("{step_name}")
    def take_screenshot(self, step_name: str):
        """Helper method to take screenshots with Allure"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Screenshot - {step_name}",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.title("Verify Successfully Create a User new account (Dispatcher)")
    @allure.description(
        "This module enables the ability to create a new shipment for being tracked on the platform. LOADIQ as source.")
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-2883", name="Jira")
    @allure.testcase("CT-2883")
    @allure.feature("Create User")
    #@pytest.mark.xray('CT-2883')
    @test(test_case_id="CT-2883", test_description="Verify Successfully Create a User new account (Dispatcher)", feature="User Creation", skip=False)
    def test_support_user_creation_dispatcher(self, load_iq_login_support_portal, record_property):
        record_property("test_key", "CT-2883")
        self.take_screenshot("Customer User Logged In")
        file_path = "applications/web/loadiq/data/support_portal/create_user.json"
        test_case_id = "CT-2883"

        # Get test data using helper method instead of fixture
        test_data = JSONDataHelper.load_json_data(file_path, test_case_id
        )
        logger.info(f"Data for CT-2883: {test_data}")
        JSONDataHelper.increment_fields_in_json(file_path, test_case_id,
            ['tmsID', 'accountName', 'firstName', 'lastName', 'email'],
            regex_pattern=r'\d+(?=@)|\d+$'
        )


        # 01. Verify the user is logged into Customer Portal ( Use PreDefine Login Fixture)

        # 02. The user goes to "Creation User" page

        # 03. Validate all the elements present
        missing_elements = self.create_user.verify_all_locators_present()
        self.take_screenshot("Validate All Elements Present on Create User Form Page")
        assert not missing_elements, f"The following elements are missing on the page: {', '.join(missing_elements)}"

        #04. Enter account and point of contact information
        self.create_user.enter_account_information(test_data["accountType"],test_data["tmsID"],test_data["accountName"], test_data["firstName"],test_data["lastName"],test_data["email"],test_data["role"])
        self.take_screenshot("Enter Account information on Create User Form Page")
        #05. Click on Create Account
        self.create_user.click_create_account()

        actual_result = self.create_user.get_alert_text()
        self.take_screenshot("Alert Message after Creating User")
        assert actual_result == "Carrier details added sucessfully." , f"Expected alert text 'Carrier details added sucessfully.' but got '{actual_result}'"

        self.menu.support_portal.menu_user_management()
        self.take_screenshot("User Management Page after Creating User")
        expected_user_data = {
            "Account Name": test_data["accountName"],
            "Account Type": test_data["accountType"],
            "TMS ID": test_data["tmsID"],
            "First Name": test_data["firstName"],
            "Last Name": test_data["lastName"],
            "Email": test_data["email"]
        }

        self.user_management.search_user(test_data["email"])
        actual_user_data = self.user_management.get_user_data_as_dict(test_data["accountName"])
        self.take_screenshot("User created on the User Management Page")

        # Filter actual data to only include fields we want to validate
        filtered_actual_data = {key: actual_user_data[key] for key in expected_user_data.keys() if key in actual_user_data}

        assert filtered_actual_data == expected_user_data, f"The user data in the UI does not match the expected data.\nExpected: {expected_user_data}\nActual: {filtered_actual_data}"
