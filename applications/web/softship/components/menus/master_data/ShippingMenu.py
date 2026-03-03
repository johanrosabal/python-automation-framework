import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ShippingMenu')


class ShippingMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Shipping Manu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=6"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_car_model = (By.XPATH, "//a[text()='Car Model']", "Car Model Link")
        self.__link_commodity = (By.XPATH, "//a[text()='Commodity']", "Commodity Link")
        self.__link_kind_of_package = (By.XPATH, "//a[text()='Kind of Package']", "Kind of Package Link")
        self.__link_bunker_type = (By.XPATH, "//a[text()='Bunker Type'] ", "Bunker Type Link")
        self.__link_shipowner = (By.XPATH, "//a[text()='Shipowner']", "Shipowner Link")
        self.__link_vessel = (By.XPATH, "//a[text()='Vessel']", "Vessel Link")
        self.__link_voyage_template = (By.XPATH, "//a[text()='Voyage Template']", "Voyage Template Link")
        self.__link_service = (By.XPATH, "//a[text()='Service']", "Service Link")
        self.__link_shipment_condition = (By.XPATH, "//a[text()='Shipment Condition']", "Shipment Condition Link")
        self.__link_transport_means = (By.XPATH, "//a[text()='Transport Means']", "Transport Means Link")

    @allure.step("Load Shipping Page")
    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Link Car Model")
    def link_car_model(self, pause: int = 0):
        self._load_page(self.__link_car_model, pause)
        return self

    @allure.step("Link Commodity")
    def link_commodity(self, pause: int = 0):
        self._load_page(self.__link_commodity, pause)
        return self

    @allure.step("Link Kind of Package")
    def link_kind_of_package(self, pause: int = 0):
        self._load_page(self.__link_kind_of_package, pause)
        return self

    @allure.step("Link Bunker Type")
    def link_bunker_type(self, pause: int = 0):
        self._load_page(self.__link_bunker_type, pause)
        return self

    @allure.step("Link Shipowner")
    def link_shipowner(self, pause: int = 0):
        self._load_page(self.__link_shipowner, pause)
        return self

    @allure.step("Link Vessel")
    def link_vessel(self, pause: int = 0):
        self._load_page(self.__link_vessel, pause)
        return self

    @allure.step("Link Voyage Template")
    def link_voyage_template(self, pause: int = 0):
        self._load_page(self.__link_voyage_template, pause)
        return self

    @allure.step("Link Service")
    def link_service(self, pause: int = 0):
        self._load_page(self.__link_service, pause)
        return self

    @allure.step("Link Shipment Condition")
    def link_shipment_condition(self, pause: int = 0):
        self._load_page(self.__link_shipment_condition, pause)
        return self

    @allure.step("Link Transport Means")
    def link_transport_means(self, pause: int = 0):
        self._load_page(self.__link_transport_means, pause)
        return self
