import pytest

from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.login.LoginPage import LoginPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from applications.web.loadiq.config.sub_application import CustomerAccounts

logger = setup_logger('TestLogin')


@pytest.mark.web
@loadiq
class TestLogin(BaseTest):
    login = LoginPage.get_instance()
    menu = LoadIQMenu.get_instance()

    @test(test_case_id="TEST-0001", test_description="Load IQ Sign In", feature="Login")
    def test_sign_in_customer_account(self):
        self.login.load_page()
        self.login.login_user(CustomerAccounts.TEST_07)
        self.menu.logout()