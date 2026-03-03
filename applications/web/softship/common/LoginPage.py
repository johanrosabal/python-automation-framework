import allure
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from applications.web.softship.config.sub_application import SubApplication, Agencies
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('LoginPage')


class LoginPage(SoftshipPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._relative = "/public/login"
        self._module_url = None
        # Locator definitions
        self._input_user_name = (By.XPATH, "//input[@name='loginName']", "Input Username")
        self._input_password = (By.NAME, "loginPassword", "Input Password")
        self._btn_login = (By.ID, "loginButton", "Login Button")
        self._select_agency = (By.XPATH, "//select[@id='selectAgency']", "Agency Dropdown")
        self._btn_select_agency = (By.XPATH, "//button[@id='btnSelectAgency']", "Agency Button")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Login Master Data Page")
    def login_master_data(self, user):
        self._module_url = BaseApp.get_modules()["master_data"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="")
        return self

    @allure.step("Login Finance Page")
    def login_finance(self, user):
        self._module_url = BaseApp.get_modules()["finance"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="")
        return self

    @allure.step("Login Contract Page")
    def login_contract(self, user):
        self._module_url = BaseApp.get_modules()["contracts"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="home")
        return self

    @allure.step("Login Commercial Page")
    def login_commercial(self, user):
        self._module_url = BaseApp.get_modules()["commercial"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="")
        return self

    @allure.step("Login Configuration Page")
    def login_configuration(self, user):
        self._module_url = BaseApp.get_modules()["configuration"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="")
        return self

    @allure.step("Login Booking Page")
    def login_booking(self, user):
        self._module_url = BaseApp.get_modules()["booking"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="home")
        return self

    @allure.step("Login Booking Page")
    def login_sof(self, user):
        self._module_url = BaseApp.get_modules()["sof"]
        self.navigation().go(self._module_url, self._relative)
        self.login_user_with_agency(user=user, agency=Agencies.CROWLEY_HQ.value, relative="")
        return self

    def login_user(self, user: UserDTO):
        with allure.step("Enter Credentials"):
            self.enter_user_name(user.user_name)
            self.enter_password(user.user_password)
            self.click_login()
            return self

    def login_user_with_agency(self, user: UserDTO, agency: str, relative = ""):
        with allure.step("Enter Credentials and select agency"):
            # Enter Credentials and Sign In
            self.enter_user_name(user.user_name)
            self.enter_password(user.user_password)
            self.click_login()
            # Checkout Agency Elements and Select Agency
            self.verify_agency_is_visible()
            self.select_agency(agency)
            self.click_agency()
            # Checkout Login Success
            self.is_login_successful(relative)
            return self

    @allure.step("Enter username: {username}")
    def enter_user_name(self, username: str):
        (self.send_keys()
         .set_locator(self._input_user_name, self._name)
         .set_text(username)
         )

        return self

    @allure.step("Enter password: {password}")
    def enter_password(self, password: str):
        self.send_keys() \
            .set_locator(self._input_password, self._name) \
            .set_text(password) \
            .screenshot(name="Entering Password")
        return self

    @allure.step("Click on Login Button")
    def click_login(self):
        self.click() \
            .set_locator(self._btn_login, self._name) \
            .single_click()
        return self

    @allure.step("Select agency:{agency} ")
    def select_agency(self, agency: str):
        self.dropdown() \
            .set_locator(self._select_agency, self._name) \
            .by_text_contains(search_text=agency) \
            .screenshot(name="Agency Selected")
        return self

    @allure.step("Click Agency Button")
    def click_agency(self):
        (
            self.click()
            .set_locator(self._btn_select_agency, self._name)
            .single_click()
            .pause(4)
        )
        return self

    def verify_title(self, title: str):
        AssertCollector.assert_equal_message(
            title,
            self.navigation().get_title(),
            "Login Page Title Match.",
            self._name,
            self.method_name()
        )

    def is_login_successful(self, relative=""):
        home_relative = self._relative.replace("public/login", relative)
        url = self._module_url + home_relative
        AssertCollector.assert_equal_message(
            url,
            self.navigation().get_current_url(),
            "Login user failed.",
            self._name,
            self.method_name()
        )
        logger.info("Successful login..")

    def verify_agency_is_visible(self):

        AssertCollector.assert_equal_message(
            True,
            self.element().set_locator(self._select_agency, self._name).is_visible(),
            "Agency Select Options not visible.",
            self._name,
            self.method_name()
        )
