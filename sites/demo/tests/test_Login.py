from core.ui.common.BaseTest import BaseTest
from sites.demo.pages.LoginPage import LoginPage


class TestLogin(BaseTest):
    username = str("Admin")
    password = str("admin123")

    def test_login(self):
        (LoginPage.get_instance()
         .load_page()
         .set_user_name(self.username)
         .set_password(self.password)
         .click_login()
         )

