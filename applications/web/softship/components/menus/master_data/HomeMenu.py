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
        self.__nav_home = (By.XPATH, "//span[@class='menu-title ng-binding' and text()='Home']", "Home Menu Option")
        self.__nav_basic = (By.XPATH, "//span[@class='menu-title ng-binding' and text()='BASIC']", "BASIC Menu Option")
        self.__nav_edi = (By.XPATH, "//span[@class='menu-title ng-binding' and text()='EDI']", "EDI Menu Option")
        self.__nav_equipment = (
            By.XPATH, "//span[@class='menu-title ng-binding' and text()='EQUIPMENT']", "EQUIPMENT Menu Option")
        self.__nav_financial = (
            By.XPATH, "//span[@class='menu-title ng-binding' and text()='FINANCIAL']", "FINANCIAL Menu Option")
        self.__nav_geographic = (
            By.XPATH, "//span[@class='menu-title ng-binding' and text()='GEOGRAPHIC']", "GEOGRAPHIC Menu Option")
        self.__nav_shipping = (
            By.XPATH, "//span[@class='menu-title ng-binding' and text()='SHIPPING']", "SHIPPING Menu Option")
        self.__nav_system = (
            By.XPATH, "//span[@class='menu-title ng-binding' and text()='System']", "System Menu Option")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Home")
    def menu_home(self, pause: int = 0):
        self._load_page(self.__nav_home, pause)
        return self

    @allure.step("Menu Basic")
    def menu_basic(self, pause: int = 0):
        self._load_page(self.__nav_basic, pause)
        return self

    @allure.step("Menu Edi")
    def menu_edi(self, pause: int = 0):
        self._load_page(self.__nav_edi, pause)
        return self

    @allure.step("Menu Equipment")
    def menu_equipment(self, pause: int = 0):
        self._load_page(self.__nav_equipment, pause)
        return self

    @allure.step("Menu Financial")
    def menu_financial(self, pause: int = 0):
        self._load_page(self.__nav_financial, pause)
        return self

    @allure.step("Menu Geographic")
    def menu_geographic(self, pause: int = 0):
        self._load_page(self.__nav_geographic, pause)
        return self

    @allure.step("Menu Shipping")
    def menu_shipping(self, pause: int = 0):
        self._load_page(self.__nav_shipping, pause)
        return self

    @allure.step("Menu System")
    def menu_system(self, pause: int = 0):
        self._load_page(self.__nav_system, pause)
        return self
