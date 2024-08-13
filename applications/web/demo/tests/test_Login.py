from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from applications.web.demo.pages.LoginPage import LoginPage
from core.ui.common.BaseTest import BaseTest, user
from core.utils.decorator import test

logger = setup_logger('TestLogin')


class TestLogin(BaseTest):

    LoginPage = LoginPage.get_instance()

    @test(test_case_id="HRM-0001", test_description="Verify Login Page headline")
    def test_login_headline(self):
        self.LoginPage.load_page()
        self.LoginPage.verify_headline("Login")

    @test(test_case_id="HRM-0002", test_description="Verify the Orange HRM Link match")
    def test_login_link(self):
        self.LoginPage.verify_orange_hrm_link("http://www.orangehrm.com/")

    @test(test_case_id="HRM-0003", test_description="Verify the Forgot Your Password Link")
    def test_login_forgot_your_password(self):
        self.LoginPage.link_forgot_your_password()
        self.LoginPage.verify_forgot_your_password("/web/index.php/auth/requestPasswordResetCode")
        self.get_back()

    @test(test_case_id="HRM-0004", test_description="Login user with valid credentials.")
    def test_login_valid_user(self, user):
        self.LoginPage.login_user(user)
        self.LoginPage.verify_user_is_logged("/web/index.php/dashboard/index")

    @test(test_case_id="HRM-0005", test_description="Log out user.")
    def test_log_out_user(self):
        self.LoginPage.logout_user()
        self.LoginPage.verify_user_is_logged_out("/web/index.php/auth/login")
