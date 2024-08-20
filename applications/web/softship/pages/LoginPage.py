from applications.web.softship.pages.MasterDataPage import MasterDataPage
from selenium.webdriver.common.by import By

from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('LoginPage')


class LoginPage(MasterDataPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/MasterData/public/login"
        # Locator definitions
        self._input_user_name = (By.XPATH, "//input[@name='loginName']", "Input Username")
        self._input_password = (By.NAME, "loginPassword", "Input Password")
        self._btn_login = (By.ID, "loginButton", "Login Button")
        self._select_agency = (By.XPATH, "//select[@id='selectAgency']", "Agency Dropdown")
        self._btn_select_agency = (By.XPATH, "//button[@id='btnSelectAgency']", "Agency Button")

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

    def login_user(self, user: UserDTO):
        self.set_user_name(user.user_name)
        self.set_password(user.user_password)
        self.click_login()
        self.click_agency()
        return self

    def login_user_with_agency(self, user: UserDTO, agency: str):
        self.set_user_name(user.user_name)
        self.set_password(user.user_password)
        self.click_login()
        self.select_agency(agency)
        self.click_agency()
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
        (self.click()
         .set_locator(self._btn_login, self.name)
         .single_click())
        return self

    def select_agency(self, text: str):
        ((self.dropdown()
          .set_locator(self._select_agency, self.name))
         .by_text_contains(text))
        return self

    def click_agency(self):
        (self.click()
         .set_locator(self._btn_select_agency, self.name)
         .single_click())
        return self

    def verify_title(self, title: str):
        AssertCollector.assert_equal_message(
            title,
            self.navigation().get_title(),
            "Login Page Title Match.",
            self.name,
            self.method_name()
        )
