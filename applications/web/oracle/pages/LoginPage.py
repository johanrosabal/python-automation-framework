import allure

from applications.web.oracle.pages.OracleCloudPage import OracleCloudPage
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('LoginPage')


class LoginPage(OracleCloudPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Relative URL
        self.relative = "/"
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._input_user_name = (By.XPATH, "//input[@name='userid']", "Input Username")
        self._input_password = (By.XPATH, "//input[@name='password']", "Input Password")
        self._btn_login = (By.XPATH, "//button[text()='Sign In ']", "Login Button")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoginPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    @allure.step("Enter username: {username}")
    def enter_user_name(self, username):
        (self.send_keys()
         .set_locator(self._input_user_name, self._name)
         .set_text(username)
         )
        return self

    @allure.step("Enter password: {password}")
    def enter_password(self, password):
        self.send_keys()\
         .set_locator(self._input_password, self._name)\
         .set_text(password)
        return self

    @allure.step("Click on Login Button")
    def click_login(self):
        self.click()\
            .set_locator(self._btn_login, self._name) \
            .screenshot(name="Login Cloud Page") \
            .single_click() \
            .pause(3)
        return self

    def login_user(self, user: UserDTO):
        with allure.step("Enter Credentials"):
            self.enter_user_name(user.user_name)
            self.enter_password(user.user_password)
            self.click_login()
            return self

    @allure.step("Verify Welcome Page")
    def verify_welcome_title(self):
        actual = self.get_title()
        expected = "Welcome"

        # Take Screenshot
        self.screenshot().attach_to_allure(name="Welcome Page", page=self._name).pause(5)

        # Assert with a custom error message
        assert actual == expected, f"Error: Expected page title '{expected}' but found '{actual}'"

