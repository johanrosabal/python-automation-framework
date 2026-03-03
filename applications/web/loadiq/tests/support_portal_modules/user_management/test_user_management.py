from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.components.menus.support_portal.SupportPortalMenu import SupportPortalMenu
from applications.web.loadiq.pages.user_management.UserManagementPage import UserManagementPage
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
import allure
import pytest

from core.utils.json_data_helper import JSONDataHelper

logger = setup_logger('TestUserManagement')

@pytest.mark.web
@loadiq
class TestUserManagement(BaseTest):
    """Test cases for User Management functionality in Support Portal"""
    profile = "qa"
    app_name = "loadiq"
    app_type = "web"

    def setup_method(self):
        """Initialize page objects before each test method"""
        self.menu = LoadIQMenu.get_instance()
        self.user_management = UserManagementPage.get_instance()

    @allure.tag('CT-2884')
    @test(test_case_id="CT-2884", test_description="User Management - View and Disable User", feature="User Management")
    def test_view_and_disable_user(self, load_iq_login_support_portal, load_json_data, record_property):
        """Test case to validate user management functionality including viewing and disabling a user."""
        record_property("test_key", "CT-2884")

        # Get test data
        data_json = JSONDataHelper.load_json_data("applications/web/loadiq/data/support_portal/user_management.json", "CT-2884")
        test_data = data_json["testCases"][0]

        # Navigate to User Management
        self.menu.support_portal.menu_user_management()

        # Search for TMS ID and view details
        self.user_management.search_tms_id(test_data["searchData"]["tmsId"])
        self.user_management.click_view_button()

        # Validate Profile Details section
        assert self.user_management.is_profile_details_visible(), "Profile Details section is not displayed"

        # Validate account details are shown
        account_details = self.user_management.get_account_details()
        assert account_details["name"], "Account Name is not displayed"
        assert account_details["type"], "Account Type is not displayed"

        # Validate Linked TMS IDs section
        assert self.user_management.are_linked_tms_ids_shown(), "Linked TMS IDs section is not displayed"

        # Validate user record
        expected_user = test_data["expectedUser"]
        assert self.user_management.verify_user_record(
            expected_user["firstName"],
            expected_user["lastName"],
            expected_user["role"],
            expected_user["email"],
            expected_user["status"]
        ), "Expected user record not found"

        # Disable user
        self.user_management.disable_user(expected_user["email"])

