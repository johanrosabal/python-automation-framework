import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('GeographicMenu')


class GeographicMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Geographic Manu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=5"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_country = (By.XPATH, "//a[text()='Country']", "Country Link")
        self.__link_holidays = (By.XPATH, "//a[text()='Holidays']", "Holidays Link")
        self.__link_location = (By.XPATH, "//a[text()='Location']", "Location Link")
        self.__link_location_hub_assignment = (By.XPATH, "//a[text()='Location Hub Assignment']",
                                               "Location Hub Assignment Link")
        self.__link_province = (By.XPATH, "//a[text()='Province']", "Province Link")
        self.__link_sublocation = (By.XPATH, "//a[text()='Sublocation']", "Sublocation Link")
        self.__link_ZIP_code = (By.XPATH, "//a[text()='ZIP Code']", "ZIP Code Link")
        self.__link_truck_route_segments = (By.XPATH, "//a[text()='Truck Route Segments']", "Truck Route Segments Link")
        self.__link_route_exclusion_rules = (By.XPATH, "//a[text()='Route Exclusion Rules']",
                                             "Route Exclusion Rules Link")
        self.__link_sublocation_cutoff_rules = (By.XPATH, "//a[text()='Sublocation Cutoff Rules']",
                                                "Sublocation Cutoff Rules Link")
        self.__link_default_equipment_locations = (By.XPATH, "//a[text()='Default Equipment Locations']",
                                                   "Default Equipment Locations Link")

    @allure.step("Load Geographic Page")
    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Link Country")
    def link_country(self, pause: int = 0):
        self._load_page(self.__link_country, pause)
        return self

    @allure.step("Link Holidays")
    def link_holidays(self, pause: int = 0):
        self._load_page(self.__link_holidays, pause)
        return self

    @allure.step("Link Location")
    def link_location(self, pause: int = 0):
        self._load_page(self.__link_location, pause)
        return self

    @allure.step("Link Location Hub Assignment")
    def link_location_hub_assignment(self, pause: int = 0):
        self._load_page(self.__link_location_hub_assignment, pause)
        return self

    @allure.step("Link Province")
    def link_province(self, pause: int = 0):
        self._load_page(self.__link_province, pause)
        return self

    @allure.step("Link Sublocation")
    def link_sublocation(self, pause: int = 0):
        self._load_page(self.__link_sublocation, pause)
        return self

    @allure.step("Link ZIP Code")
    def link_zip_code(self, pause: int = 0):
        self._load_page(self.__link_ZIP_code, pause)
        return self

    @allure.step("Link Truck Route Segments")
    def link_truck_route_segments(self, pause: int = 0):
        self._load_page(self.__link_truck_route_segments, pause)
        return self

    @allure.step("Link Route Exclusion Rules")
    def link_route_exclusion_rules(self, pause: int = 0):
        self._load_page(self.__link_route_exclusion_rules, pause)
        return self

    @allure.step("Link Sublocation Cutoff Rules")
    def link_sublocation_cutoff_rules(self, pause: int = 0):
        self._load_page(self.__link_sublocation_cutoff_rules, pause)
        return self

    @allure.step("Link Default Equipment Locations")
    def link_default_equipment_locations(self, pause: int = 0):
        self._load_page(self.__link_default_equipment_locations, pause)
        return self
