from selenium.webdriver.common.by import By

from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.data import UserDTO

logger = setup_logger('LoginPage')

class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/login"
        # Locator definitions
        self._input_email = (By.NAME, "email", "Input email")
        self._input_password = (By.NAME, "password", "Input password")
        self._btn_login = (By.ID, "login-submit-button", "Login Button")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoginPage(BaseApp.get_driver())
            cls.name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def enter_email(self, email):
        self.send_keys().set_locator(self._input_email).set_text(email)
        return self

    def enter_password(self, password):
        self.send_keys().set_locator(self._input_password).set_text(password)
        return self

    def click_login(self):
        self.click().set_locator(self._btn_login).single_click().pause(3)
        return self

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self



