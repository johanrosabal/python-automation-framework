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
        self.relative = "/web/index.php/auth/login"
        # Locator definitions
        self._input_user_name = (By.NAME, "username", "Input Username")
        self._error_user_name = (By.XPATH, "//input[@name=\"username\"]/../../span", "Username error validation")
        self._input_password = (By.NAME, "password", "Input Password")
        self._error_password = (By.XPATH, "//input[@name=\"password\"]/../../span", "Password error validation")
        self._btn_login = (By.XPATH, "//button[contains(@class,'login-button')]", "Login Button")
        self._select_user_dropdown = (By.XPATH, "//li[contains(@class,'oxd-userdropdown')]", "User Dropdown")
        self._select_logout = (By.XPATH, "//ul[@class='oxd-dropdown-menu']//a[contains(@href, 'logout')]", "User Logout")
        self._txt_headline = (By.XPATH, "//h5[contains(@class,'orangehrm-login-title')]", "Login Headline")
        self._link_orange_hrm = (By.XPATH, '//a[text()="OrangeHRM, Inc"]', "Orange HRM Link")
        self._link_forgot_your_password = (By.XPATH, "//p[contains(@class,'orangehrm-login-forgot-header')]", "Forgot Your Password Link")
        self._txt_alert_error = (By.XPATH,"//div[contains(@class,'alert--error')]//p", "Alert Error Message")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoginPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def login_user(self, user: UserDTO):
        self.set_user_name(user.user_name)
        self.set_password(user.user_password)
        self.click_login()
        return self

    def set_user_name(self, username: str):
        self.send_keys() \
            .set_locator(self._input_user_name, self._name)\
            .set_text(username)
        return self

    def set_password(self, password: str):
        (self.send_keys()
         .set_locator(self._input_password, self._name)
         .set_text(password)
         .highlight()
         )

        return self

    def get_alert_error_message(self):

        self.screenshot().set_locator(self._txt_alert_error, self._name).save_highlight(description="Alert Error Message").add_comment("Mensaje de Error")
        return self.get_text().set_locator(self._txt_alert_error, self._name).by_text()

    def get_username_error_message(self):
        return self.get_text().set_locator(self._error_user_name,self._name).by_text()

    def get_password_error_message(self):
        return self.get_text().set_locator(self._error_password,self._name).by_text()

    def click_login(self):
        self.click().set_locator(self._btn_login, self._name).single_click()
        return self

    def get_headline(self):
        return (self.get_text()
                .set_locator(self._txt_headline, self._name)
                .by_text())

    def link_orange_hrm(self):
        self.click().set_locator(self._link_orange_hrm, self._name).single_click().screenshot()
        return self

    def link_forgot_your_password(self):

        self.click().set_locator(self._link_forgot_your_password, self._name).single_click()
        self.send_keys().set_locator().clear().set_encrypt()

        return self

    def logout_user(self):
        self.click().set_locator(self._select_user_dropdown, self._name).single_click()
        self.click().set_locator(self._select_logout, self._name).single_click()
        return self

    def verify_headline(self, headline: str):
        AssertCollector.assert_equal_message(
            expected=headline,
            actual=self.get_headline(),
            message="Login headline.",
            page=self._name,
            method_name="verify_headline"
        )
        return self

    def verify_orange_hrm_link(self, link: str):
        href = self.get_text().set_locator(self._link_orange_hrm, self._name).by_attribute("href")
        AssertCollector.assert_equal_message(
            expected=link,
            actual=href,
            message="Orange HRM Link.",
            page=self._name,
            method_name="verify_orange_hrm_link"
        )
        return self

    def verify_forgot_your_password(self, relative_url):
        base_url = BaseApp.get_base_url()
        current_url = self.navigation().get_current_url()
        AssertCollector.assert_equal_message(
            expected=base_url + relative_url,
            actual=current_url,
            message="Forgot Password Location.",
            page=self._name,
            method_name="verify_forgot_your_password"
        )
        return self

    def verify_user_is_logged(self, relative_url):
        base_url = BaseApp.get_base_url()
        current_url = self.navigation().get_current_url()
        AssertCollector.assert_equal_message(
            expected=base_url + relative_url,
            actual=current_url,
            message="User Signed.",
            page=self._name,
            method_name="verify_user_is_logged"
        )
        return self

    def verify_user_is_logged_out(self, relative_url):
        base_url = BaseApp.get_base_url()
        current_url = self.navigation().get_current_url()
        AssertCollector.assert_equal_message(
            expected=base_url + relative_url,
            actual=current_url,
            message="User Logout.",
            page=self._name,
            method_name="verify_user_is_logged_out"
        )
        return self
