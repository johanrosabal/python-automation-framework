from selenium.webdriver.common.by import By
import allure
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.data.UserDTO import UserDTO
from core.utils.encryptation_utils import decode_base64

logger = setup_logger('SignInSSOPage')


class SignInSSOPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the SignInSSOPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/app/UserHome?iss=https%3A%2F%2Fcrowley.okta.com&session_hint=AUTHENTICATED"
        # Locator definitions
        self._input_user_name = (By.XPATH, "//input[@name='identifier']", "User Name [Input]")
        self._input_password = (By.XPATH,"//input[@name='credentials.passcode']","Password [Input]")
        self._btn_show_password = (By.XPATH,"//span[@class='password-toggle']","Show Password [Eye Button]")
        self._btn_next = (By.XPATH, "//input[@value='Next']", "Next [Button]")
        self._btn_verify = (By.XPATH, "//input[@value='Verify']", "Verify [Button]")
        self._link_forgot_password = (By.XPATH,"//a[contains(@class,'forgot-password')]", "Forgot password [Link]")
        self._link_verify_with_something_else= (By.XPATH, "//a[contains(@class,'switchAuthenticator')]", "Verify with something else")
        self._link_back_to_sign_in = (By.XPATH, "//a[contains(@class,'cancel')]", "Back to sign in")
        self._btn_push_notification = (By.XPATH,"//a[contains(@aria-label,'push notification to the Okta Verify')]","Push Notification with Okta [Button]")
        self._menu_profile_name = (By.XPATH, "//span[contains(@class,'forceSocialPhoto')] | //div[contains(@class,'user-name')]", "Menu Profile [is visible]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def load_okta_page(self):
        base_url = "https://crowley.okta.com"
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    @allure.step("Enter username: {username}")
    def enter_user_name(self, username: str):
        self.send_keys() \
            .set_locator(self._input_user_name, self._name) \
            .set_encrypt() \
            .set_text(username)
        return self

    @allure.step("Enter password: {password}")
    def enter_password(self, password: str):
        self.send_keys() \
            .set_locator(self._input_password, self._name) \
            .set_encrypt() \
            .set_text(password) \
            .screenshot(name="Entering Password")
        return self

    @allure.step("Click on NEXT Button")
    def click_next(self):
        self.click() \
            .set_locator(self._btn_next, self._name) \
            .single_click()
        return self

    @allure.step("Click on VERIFY Button")
    def click_verify(self):
        self.click() \
            .set_locator(self._btn_verify, self._name) \
            .single_click()
        return self

    def click_show_password(self):
        self.click() \
            .set_locator(self._btn_show_password, self._name) \
            .single_click()
        return self

    def click_link_forgot_password(self):
        self.click() \
            .set_locator(self._link_forgot_password, self._name) \
            .single_click()
        return self

    def click_link_verify_with_something_else(self):
        self.click() \
            .set_locator(self._link_verify_with_something_else, self._name) \
            .single_click()
        return self

    def click_link_back_to_sign_in(self):
        self.click() \
            .set_locator(self._link_back_to_sign_in, self._name) \
            .single_click()
        return self

    def click_push_notification(self):
        self.click() \
            .set_locator(self._btn_push_notification, self._name) \
            .single_click()
        return self

    def sign_in_with_sso(self, user: UserDTO):
        credentials = user
        with allure.step("Enter Credentials"):
            user = decode_base64(credentials.user_name)
            password = decode_base64(credentials.user_password)

            self.enter_user_name(user)
            self.click_next()
            self.click_push_notification()
            self.click_show_password()
            self.enter_password(password)
            self.click_verify()


        return self

    def is_login_successful(self):

        if self.element().is_present(locator=self._menu_profile_name,timeout=3):
            logger.info("User is logged!")
            return True
        else:
            logger.warning("User is not logged!")
            return False


