import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CostControllingMenu')


class CostControllingMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=1"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_purchase_tariffs = (By.XPATH, "//a[text()='Purchase Tariffs']", "Purchase Tariffs Link")
        self.__link_purchase_tariffs_extended = (By.XPATH, "//a[text()='Purchase Tariffs']", "Purchase Tariffs Extended Link")
        self.__link_cost_templates = (By.XPATH, "//a[text()='Cost Templates']", "Cost Templates Link")
        self.__link_create_port_calculation_vouchers = (By.XPATH, "//a[text()='Create Port Cost Vouchers']", "Create Port Cost Vouchers Link")
        self.__link_port_cost_calculation_header = (By.XPATH, "//a[text()='Port Cost Calculation Header']", "Port Cost Calculation Header Link")
        self.__link_port_cost_code_overview = (By.XPATH, "//a[text()='Cost Code Overview']", "Port Cost Calculation Header Link")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["finance"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Purchase Tariffs")
    def link_purchase_tariffs(self, pause: int = 0):
        self._load_page(self.__link_purchase_tariffs, pause)
        return self

    @allure.step("Menu Purchase Tariffs Extend")
    def link_purchase_tariffs_extended(self, pause: int = 0):
        self._load_page(self.__link_purchase_tariffs_extended, pause)
        return self

    @allure.step("Menu Cost Templates Extend")
    def link_cost_templates(self, pause: int = 0):
        self._load_page(self.__link_cost_templates, pause)
        return self

    @allure.step("Menu Create Port Cost Vouchers")
    def link_create_port_calculation_vouchers(self, pause: int = 0):
        self._load_page(self.__link_create_port_calculation_vouchers, pause)
        return self

    @allure.step("Menu Port Cost Calculation Header")
    def link_port_cost_calculation_header(self, pause: int = 0):
        self._load_page(self.__link_port_cost_calculation_header, pause)
        return self

    @allure.step("Menu Cost Code Overview")
    def link_port_cost_code_overview(self, pause: int = 0):
        self._load_page(self.__link_port_cost_code_overview, pause)
        return self
