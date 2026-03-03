import allure
import pytest

from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.config.decorators import softship
from applications.web.softship.pages.masterdata.financial.account.AccountPage import AccountPage
from applications.web.softship.pages.masterdata.financial.account.AccountPageFlow import AccountPageFlow
from core.config.logger_config import setup_logger
from core.utils.decorator import test

logger = setup_logger('TestMasterDataAccount')


@pytest.mark.web
@softship
class TestMasterDataAccount(SoftshipBaseTest):
    """
    Test cases for Account Master Data page.
    URL: /MasterData/detail/Account/0/general
    """

    # Init App
    menu = SoftshipMenu.get_instance()
    account_page = AccountPage.get_instance()

    @allure.title("Create New Account - Required Fields Only")
    @allure.severity(allure.severity_level.CRITICAL)
    @test(test_case_id="ACC-0001", test_description="Create new Account with required fields only")
    def test_create_account_required_fields(self, softship_login_master_data, record_property):
        """
        Test creating a new Account with only required fields.
        Required fields: Account Number, Ship Owner, Type in Bookkeeping, Type of Account
        """
        record_property("test_key", "ACC-0001")

        # Test Data
        account_data = {
            "account_number": "TESTACC001",
            "ship_owner": "CROWLEY",
            "type_bookkeeping": "C",
            "type_account": "GE"
        }

        # Execute test using Fluent Pattern
        AccountPageFlow() \
            .verify_page_loaded() \
            .with_account_number(account_data["account_number"]) \
            .with_ship_owner(account_data["ship_owner"]) \
            .with_type_bookkeeping(account_data["type_bookkeeping"]) \
            .with_type_account(account_data["type_account"]) \
            .save_and_close(pause=2)

        # Logout
        self.menu.logout()

    @test(test_case_id="ACC-0002", test_description="Create new Account with all fields")
    @allure.title("Create New Account - All Fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_account_all_fields(self, softship_login_master_data, record_property):
        """
        Test creating a new Account filling all available fields.
        """
        record_property("test_key", "ACC-0002")

        # Test Data - Complete form
        account_data = {
            "account_number": "TESTACC002",
            "sub_account_number": "SUB001",
            "ship_owner": "CROWLEY",
            "account_name": "Test Account Full",
            "disbursement_account": True,
            "payment": True,
            "protect_account": False,
            "delete_reorganization": False,
            "status_wdl": "1",
            "bookkeeping_number": "BK002",
            "bookkeeping_sub_number": "BKSUB002",
            "type_bookkeeping": "C",
            "type_account": "GE",
            "tramp": False,
            "text_field_1": "Custom Text 1",
            "text_field_2": "Custom Text 2",
            "remark": "Account created by automation test"
        }

        # Execute test using fill_form method
        AccountPageFlow() \
            .load(pause=3) \
            .verify_page_loaded() \
            .fill_form(account_data) \
            .save_and_close(pause=2)

        # Logout
        self.menu.logout()

    @test(test_case_id="ACC-0003", test_description="Validate Account page loads correctly")
    @allure.title("Validate Account Page Load")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_account_page_load(self, softship_login_master_data, record_property):
        """
        Test that the Account page loads correctly and all main elements are visible.
        """
        record_property("test_key", "ACC-0003")

        # Load page and verify elements
        self.account_page.load_page(pause=3)

        # Verify main fields are displayed
        assert self.account_page.verify_account_number_is_displayed(), "Account Number field should be visible"
        assert self.account_page.verify_sub_account_number_is_displayed(), "Sub Account Number field should be visible"
        assert self.account_page.verify_ship_owner_is_displayed(), "Ship Owner field should be visible"
        assert self.account_page.verify_account_name_is_displayed(), "Account Name field should be visible"
        assert self.account_page.verify_disbursement_account_is_displayed(), "Disbursement Account checkbox should be visible"
        assert self.account_page.verify_payment_is_displayed(), "Payment checkbox should be visible"

        # Close without saving
        self.account_page.click_close(pause=1)

        # Logout
        self.menu.logout()

    @test(test_case_id="ACC-0004", test_description="Create Account with Disbursement settings")
    @allure.title("Create Account - Disbursement Settings")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_account_disbursement_settings(self, softship_login_master_data, record_property):
        """
        Test creating an Account with specific disbursement and payment settings.
        """
        record_property("test_key", "ACC-0004")

        # Execute test using Fluent Pattern with specific settings
        AccountPageFlow() \
            .load(pause=3) \
            .verify_page_loaded() \
            .with_account_number("DISBTEST001") \
            .with_ship_owner("CROWLEY") \
            .with_account_name("Disbursement Test Account") \
            .with_disbursement_account(True) \
            .with_payment(True) \
            .with_protect_account(False) \
            .with_type_bookkeeping("EXPENSE") \
            .with_type_account("REVENUE") \
            .with_remark("Account for disbursement testing") \
            .save_and_close(pause=2)

        # Logout
        self.menu.logout()

    @test(test_case_id="ACC-0005", test_description="Create Account with Bookkeeping information")
    @allure.title("Create Account - Bookkeeping Information")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_account_bookkeeping_info(self, softship_login_master_data, record_property):
        """
        Test creating an Account with detailed bookkeeping information.
        """
        record_property("test_key", "ACC-0005")

        # Execute test using Fluent Pattern
        AccountPageFlow() \
            .load(pause=3) \
            .verify_page_loaded() \
            .with_account_number("BKTEST001") \
            .with_ship_owner("CROWLEY") \
            .with_account_name("Bookkeeping Test Account") \
            .with_bookkeeping_number("BK12345") \
            .with_bookkeeping_sub_number("BKSUB12345") \
            .with_type_bookkeeping("EXPENSE") \
            .with_type_account("REVENUE") \
            .with_remark("Account with detailed bookkeeping info") \
            .save_and_close(pause=2)

        # Logout
        self.menu.logout()

    @test(test_case_id="ACC-0006", test_description="Close Account page without saving")
    @allure.title("Close Account Page Without Saving")
    @allure.severity(allure.severity_level.MINOR)
    def test_close_account_without_saving(self, softship_login_master_data, record_property):
        """
        Test closing the Account page without saving any data.
        """
        record_property("test_key", "ACC-0006")

        # Load page, enter some data, then close without saving
        AccountPageFlow() \
            .load(pause=3) \
            .verify_page_loaded() \
            .with_account_number("NOSAVE001") \
            .with_account_name("Should Not Be Saved") \
            .close(pause=1) \
            .confirm_yes(pause=2)

        # Logout
        self.menu.logout()
