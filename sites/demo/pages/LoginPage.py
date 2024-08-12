from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.data import UserDTO

logger = setup_logger('LoginPage')


class LoginPage(BasePage):
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # Locator definitions
        self._input_user_name = (By.NAME, "username", "Input Username")
        self._input_password = (By.NAME, "password", "Input Password")
        self._btn_login = (By.XPATH, "//button[contains(@class,'login-button')]", "Login Button")
        self._select_user_dropdown = (By.XPATH, "//li[contains(@class,'oxd-userdropdown')]", "User Dropdown")
        self._select_logout = (By.XPATH, "//ul[@class='oxd-dropdown-menu']//a[contains(@href, 'logout')]", "user Logout")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoginPage(BaseApp.get_driver())
            cls.name = __class__.__name__
        return cls._instance

    def load_page(self):
        self.go(self.url)
        return self

    def set_user_name(self, username: str):
        (self.send_keys()
         .set_locator(self._input_user_name, self.name)
         .set_text(username)
         )
        return self

    def set_password(self, password: str):
        (self.send_keys()
         .set_locator(self._input_password, self.name)
         .set_text(password)
         )

        return self

    def click_login(self):
        (self.click_element()
         .set_locator(self._btn_login, self.name)
         .single_click())
        return self

    def login_user(self, user: UserDTO):
        self.set_user_name(user.user_name)
        self.set_password(user.user_password)
        self.click_login()
        return self

    def logout_user(self):
        self.click_element().set_locator(self._select_user_dropdown,self.name).single_click()
        self.click_element().set_locator(self._select_logout,self.name).single_click()
