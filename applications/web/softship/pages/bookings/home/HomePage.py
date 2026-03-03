import allure

from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By
from applications.web.softship.components.menus.booking.HomeMenu import HomeMenu

from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('HomePage')


class HomePage(SoftshipPage):

    menu = HomeMenu.menu_home()

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/home"
        self._module_url = None
        # Name
        self.name = self.__class__.__name__
        # Locator definitions
        self._lbl_welcome_message = (By.XPATH, "//span[@class='welcome-text']")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["booking"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def is_home_successful(self):
        url = BaseApp.get_base_url() + self.relative
        AssertCollector.assert_equal_message(
            url,
            self.navigation().get_current_url(),
            "Home page not load.",
            self._name,
            self.method_name()
        )
        logger.info("Successful Home page.")
        return self

    # TODO Checkout this
    def click_on_home(self):
        # self.menu.app
        pass

