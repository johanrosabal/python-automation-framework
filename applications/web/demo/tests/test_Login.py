from core.config.logger_config import setup_logger
from applications.web.demo.pages.LoginPage import LoginPage
from core.ui.common.BaseTest import BaseTest, user
from core.utils.decorator import test

logger = setup_logger('TestLogin')


class TestLogin(BaseTest):

    loginPage = LoginPage.get_instance()

    @test(test_case_id="HRM-0001", test_description="Description of Test 1.")
    def test_login(self, user):
        (self.loginPage
         .load_page()
         .set_user_name(user.user_name)
         .set_password(user.user_password)
         .click_login()
         .logout_user()
         )

    @test(test_case_id="HRM-0002", test_description="Description of Test 2.")
    def test_login_dto(self, user):
        (self.loginPage
         .load_page()
         .login_user(user)
         .logout_user()
         )
