from enum import Enum

import allure
from selenium.webdriver.common.by import By
from applications.web.loadiq.common.LoadIQPage import LoadIQPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.asserts.AssertCollector import AssertCollector

logger = setup_logger('LoginPage')


class LoginPage(LoadIQPage):

    def __init__(self, driver):
        """
        Initialize the LoginPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self._relative = "/login"
        # Locator definitions
        self._input_user_name = (By.NAME, "username", "Username [Input]")
        self._input_password = (By.NAME, "password", "Password [Input]")
        self._checkbox_remember_me = (By.NAME, "remember", "Password [Input]")
        self._btn_sign_in = (By.XPATH, "//input[@type='submit']", "Sign In [Button]")
        self._link_need_help = (By.XPATH, "//a[text()='Need help signing in?']", "Need help signing in? [Link]")
        self._menu_profile = (By.XPATH, "//ul[contains(@class,'profile-menu')]", "Menu Profile [is visible]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoginPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self._relative)
        self.navigation().go(base_url, self._relative)
        return self

    # Custom Load Page for API Load IQ Folder
    def load_page_with_base_url(self, base_url: str):
        # Setting Driver Session on Custom Load Page
        BaseApp.set_driver(self._driver)

        url = base_url + self._relative
        logger.info("LOAD PAGE: " + url)

        self._driver.get(url)
        return self

    def login_user(self, account_enum):
        # Validate Enum Argument
        if not isinstance(account_enum, Enum):
            raise ValueError("Invalid account type. Must be an Enum member.")

        # Extract username from the Enum value
        credentials = account_enum.value
        username = credentials["username"]
        password = credentials["password"]
        logger.info(f"Logging in with username: {username} and password: {password}")

        # Login User
        with allure.step("Enter Credentials"):
            self.enter_user_name(username)
            self.enter_password(password)
            self.click_sign_in()
            return self

    @allure.step("Enter username: {username}")
    def enter_user_name(self, username: str):
        (self.send_keys()
         .set_locator(self._input_user_name, self._name, explicit_wait=15)
         .set_text(username)
         )

        return self

    @allure.step("Enter password: {password}")
    def enter_password(self, password: str):
        self.send_keys() \
            .set_locator(self._input_password, self._name, explicit_wait=15) \
            .set_text(password) \
            .screenshot(name="Entering Password")
        return self

    @allure.step("Click on Login Button")
    def click_sign_in(self):
        self.click() \
            .set_locator(self._btn_sign_in, self._name) \
            .single_click()
        return self

    def verify_title(self):
        AssertCollector.assert_equal_message(
            'LoadIQ',
            self.navigation().get_title(),
            "Login Page Title Match.",
            self._name,
            self.method_name()
        )

    def is_login_successful(self):

        if self.element().is_present(self._menu_profile, timeout=5):
            logger.info("User is logged!")
            return True
        else:
            logger.warning("User is not logged!")
            return False
