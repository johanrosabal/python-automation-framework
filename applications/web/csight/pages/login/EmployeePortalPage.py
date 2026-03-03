import allure
from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp


logger = setup_logger('EmployeePortalPage')


class EmployeePortalPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the EmployeePortalPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "https://crowley.okta.com/app/salesforce/{sign-code}/sso/saml"  # "app/salesforce/exk1kp55j3k7kXQC20h8/sso/saml"
        # Locator definitions
        self._input_username = (By.NAME, "identifier", "Username Input")
        self._input_password = (By.NAME, "credentials.passcode", "Password Input")
        self._btn_next = (By.XPATH, "//input[@type='submit'][@value='Next']", "Next Button")
        self._btn_verify = (By.XPATH, "//input[@type='submit'][@value='Verify']", "Next Button")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self, sign_code):
        # base_url = BaseApp.get_base_url()
        # Pass the sign code in the relative URL
        relative = self.relative.replace("{sign-code}", sign_code, 1)
        logger.info("LOAD PAGE: " + relative)
        self.navigation().go_to_url(relative)
        return self

    @allure.step("Enter username {username}")
    def enter_username(self, username):
        self.send_keys().set_locator(self._input_username, self._name).set_text(username)

    @allure.step("Enter password {password}")
    def enter_password(self, password):
        self.send_keys().set_locator(self._input_password, self._name).set_text(password)

    @allure.step("Click Next Button")
    def click_next(self, pause=0):
        self.click().set_locator(self._btn_next, self._name).single_click().pause(pause)

    @allure.step("Click Verify Button")
    def click_verify(self, pause=0):
        self.click().set_locator(self._btn_verify, self._name).single_click().pause(pause)
