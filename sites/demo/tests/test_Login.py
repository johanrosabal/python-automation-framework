
from core.data.UserDTO import UserDTO
from core.ui.common.BaseTest import BaseTest
from sites.demo.pages.LoginPage import LoginPage
from core.utils.decorator import test


class TestLogin(BaseTest):
    user_dto = UserDTO(user_name="Admin", user_password="admin123")

    @test(test_case_id="HRM-0001", test_description="Description of Test 1.")
    def test_login(self):
        (LoginPage.get_instance()
         .load_page()
         .set_user_name(self.user_dto.user_name)
         .set_password(self.user_dto.user_password)
         .click_login()
         .logout_user()
         )

    @test(test_case_id="HRM-0002", test_description="Description of Test 2.")
    def test_login_dto(self):
        (LoginPage
         .get_instance()
         .load_page()
         .login_user(self.user_dto)
         .logout_user()
         )

