import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('HomeMenu')


class HomeMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Bookings/home"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__nav_home = (By.XPATH, "//span[@class='ng-binding ng-scope' and text()='Home']", "Home Menu Option")
        self.__nav_bookings = (By.XPATH, "//span[@class='ng-binding ng-scope' and text()='Bookings']", "Bookings Menu Option")
        self.__nav_system = (By.XPATH, "//span[@class='ng-binding ng-scope' and text()='System']", "System Menu Option")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["booking"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Home")
    def menu_home(self, pause: int = 0):
        self._load_page(self.__nav_home, pause)
        return self

    @allure.step("Menu Booking")
    def menu_bookings(self, pause: int = 0):
        self._load_page(self.__nav_bookings, pause)
        return self

    @allure.step("Menu System")
    def menu_system(self, pause: int = 0):
        self._load_page(self.__nav_system, pause)
        return self

    @allure.step("Click on Bookings menu")
    def click_menu_bookings(self, query_text: str, pause: int = 0):
        self.click().set_locator(self.__nav_bookings, self._name).single_click().pause(pause)
        return self

