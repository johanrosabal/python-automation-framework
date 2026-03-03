import allure
from selenium.webdriver.common.by import By

from applications.web.csight.pages.login.SignInSSOPage import SignInSSOPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.data.UserDTO import UserDTO
from core.utils.encryptation_utils import decode_base64

logger = setup_logger('LoginPage')


class LoginPage(CSightBasePage):

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
        self.relative = "Employees/s/login/"
        self.sign_code = None
        # Locator definitions
        self._input_user_name = (By.XPATH, "//input[@name='Username']", "Username [Input]")
        self._input_password = (By.XPATH, "//input[@name='Password']", "Password [Input]")
        self._btn_sign_in = (By.XPATH, "//div[@class='login-form-buttons']/button", "Sign In with Logistics Account [Button]")
        self._btn_single_sign_on = (By.XPATH, "(//div[contains(@class,'crowley-emp-login')]//button)[2]", "Sign In Single Sign in with Crowley Credentials [Button]")
        self._btn_sign_in_customer_portal = (By.XPATH, "(//div[contains(@class,'crowley-emp-login')]//button)[1]", "Sign In Customer Portal[Button]")
        self._menu_profile_name = (By.XPATH, "//span[contains(@class,'forceSocialPhoto')] | //div[contains(@class,'user-name')]", "Menu Profile [is visible]")
        # Sub-Components
        self.signInSSO = SignInSSOPage.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.maximize_window()
        self.navigation().go(base_url, self.relative)
        return self

    def load_salesforce(self):
        base_url = "https://crowley2--uat.sandbox.lightning.force.com"
        logger.info("LOAD PAGE SALES FORCE: " + base_url + self.relative)
        self.maximize_window()
        self.navigation().go(base_url, "/lightning/page/home")
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
            .screenshot(name="C-Sight_Login_Entering_Password")
        return self

    @allure.step("Click on SIGN IN Button")
    def click_sign_in(self):
        self.click() \
            .set_locator(self._btn_sign_in, self._name) \
            .single_click()
        return self

    def login_user(self, user: UserDTO):
        credentials = user
        with allure.step("Enter Credentials"):
            user = decode_base64(credentials.user_name)
            password = decode_base64(credentials.user_password)

            self.enter_user_name(user)
            self.enter_password(password)
            self.click_sign_in()
            self.element().wait(locator=self._menu_profile_name)
            return self

    def extract_sign_code(self):
        url = self.navigation().get_current_url()
        logger.info(f"Current URL: {url}")

        parts = url.split("/")  # Split the  URL by "/"
        try:
            index = parts.index("salesforce")  # found the position of "salesforce" string in the URL
            self.sign_code = parts[index + 1]  # it takes the next value, where the code is
            logger.info(f"Sign Code: {self.sign_code}")
        except (ValueError, IndexError):
            logger.warning("No sign code found in the URL.")

        return self.sign_code

    @allure.step("Sign In | Single Sign On")
    def click_sign_in_single_sign_on(self, pause=2):
        self.click().set_locator(self._btn_single_sign_on, self._name).single_click().pause(pause)
        return self.signInSSO

    def is_login_successful(self):

        if self.element().is_present(locator=self._menu_profile_name,timeout=3):
            logger.info("User is logged!")
            return True
        else:
            logger.warning("User is not logged!")
            return False



