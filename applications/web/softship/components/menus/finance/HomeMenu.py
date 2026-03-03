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
        self.relative = "/Home/Index"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__nav_home = (
            By.XPATH,
            "//span[@class='ng-binding ng-scope' and text()='Home']",
            "Home Menu Option")
        self.__nav_cost_controlling = (
            By.XPATH,
            "//span[@class='ng-binding ng-scope' and text()='Cost / Controlling']",
            "Home Cost / Controlling Menu Option")
        self.__nav_voucher = (
            By.XPATH,
            "//span[@class='ng-binding ng-scope' and text()='Voucher']",
            "Voucher Menu Option")
        self.__nav_sales_invoicing = (
            By.XPATH,
            "//span[@class='ng-binding ng-scope' and text()='Sales Invoicing']",
            "Sales Invoicing Menu Option")
        self.__nav_system = (
            By.XPATH,
            "//span[@class='ng-binding ng-scope' and text()='System']",
            "System Menu Option")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["finance"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Home")
    def menu_home(self, pause: int = 0):
        self._load_page(self.__nav_home, pause)
        return self

    @allure.step("Menu Cost/Controlling")
    def menu_cost_controlling(self, pause: int = 0):
        self._load_page(self.__nav_cost_controlling, pause)
        return self

    @allure.step("Menu Voucher")
    def menu_voucher(self, pause: int = 0):
        self._load_page(self.__nav_voucher, pause)
        return self

    @allure.step("Menu Sales Invoicing")
    def menu_sales_invoicing(self, pause: int = 0):
        self._load_page(self.__nav_sales_invoicing, pause)
        return self

    @allure.step("Menu System")
    def menu_system(self, pause: int = 0):
        self._load_page(self.__nav_system, pause)
        return self
