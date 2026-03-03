import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('EquipmentMenu')


class EquipmentMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Equipment Manu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=3"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_component_warranty = (By.XPATH, "//a[text()='Component Warranty']", "Component Warranty Link")
        self.__link_define_equipment_status = (By.XPATH, "//a[text()='Define Equipment Status']",
                                               "Define Equipment Status Link")
        self.__link_define_movements = (By.XPATH, "//a[text()='Define Movements']", "Define Movements Link")
        self.__link_define_cis_criteria = (By.XPATH, "//a[text()='Define CIS Criteria']", "Define CIS Criteria Link")
        self.__link_define_disposition_code = (
            By.XPATH, "//a[text()='Define Disposition Code']", "Define Disposition Code Link")
        self.__link_equipment_owner = (By.XPATH, "//a[text()='Equipment Owner']", "Equipment Owner Link")
        self.__link_equipment_series = (By.XPATH, "//a[text()='Equipment Series']", "Equipment Series Link")
        self.__link_container = (By.XPATH, "//a[text()='Container']", "Container Link")
        self.__link_container_type = (By.XPATH, "//a[text()='Container Type']", "Container Type Link")
        self.__link_components = (By.XPATH, "//a[text()='Components']", "Components Link")
        self.__link_damage_locations = (By.XPATH, "//a[text()='Damage Locations']", "Damage Locations Link")
        self.__link_damage_type = (By.XPATH, "//a[text()='Damage Type']", "Damage Type Link")
        self.__link_repair_code = (By.XPATH, "//a[text()='Repair Code']", "Repair Code Link")
        self.__link_repair_material = (By.XPATH, "//a[text()='Repair Material']", "Repair Material Link")
        self.__link_repair_status = (By.XPATH, "//a[text()='Repair Status']", "Repair Status Link")
        self.__link_survey_contract = (By.XPATH, "//a[text()='Survey Contract']", "Survey Contract Link")
        self.__link_surveyor = (By.XPATH, "//a[text()='Surveyor']", "Surveyor Link")

    @allure.step("Load Equipment Page")
    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Link Component Warranty")
    def link_component_warranty(self, pause: int = 0):
        self._load_page(self.__link_component_warranty, pause)
        return self

    @allure.step("Link Define Equipment Status")
    def link_define_equipment_status(self, pause: int = 0):
        self._load_page(self.__link_define_equipment_status, pause)
        return self

    @allure.step("Link Define Movements")
    def link_define_movements(self, pause: int = 0):
        self._load_page(self.__link_define_movements, pause)
        return self

    @allure.step("Link Define CIS Criteria")
    def link_define_cis_criteria(self, pause: int = 0):
        self._load_page(self.__link_define_cis_criteria, pause)
        return self

    @allure.step("Link Define Disposition Code")
    def link_define_disposition_code(self, pause: int = 0):
        self._load_page(self.__link_define_disposition_code, pause)
        return self

    @allure.step("Link Equipment Owner")
    def link_equipment_owner(self, pause: int = 0):
        self._load_page(self.__link_equipment_owner, pause)
        return self

    @allure.step("Link Equipment Series")
    def link_equipment_series(self, pause: int = 0):
        self._load_page(self.__link_equipment_series, pause)
        return self

    @allure.step("Link Container")
    def link_container(self, pause: int = 0):
        self._load_page(self.__link_container, pause)
        return self

    @allure.step("Link Container Type")
    def link_container_type(self, pause: int = 0):
        self._load_page(self.__link_container_type, pause)
        return self

    @allure.step("Link Components")
    def link_components(self, pause: int = 0):
        self._load_page(self.__link_components, pause)
        return self

    @allure.step("Link Damage Locations")
    def link_damage_locations(self, pause: int = 0):
        self._load_page(self.__link_damage_locations, pause)
        return self

    @allure.step("Link Damage Type")
    def link_damage_type(self, pause: int = 0):
        self._load_page(self.__link_damage_type, pause)
        return self

    @allure.step("Link Repair Code")
    def link_repair_code(self, pause: int = 0):
        self._load_page(self.__link_repair_code, pause)
        return self

    @allure.step("Link Repair Material")
    def link_repair_material(self, pause: int = 0):
        self._load_page(self.__link_repair_material, pause)
        return self

    @allure.step("Link Repair Status")
    def link_repair_status(self, pause: int = 0):
        self._load_page(self.__link_repair_status, pause)
        return self

    @allure.step("Link Survey Contract")
    def link_survey_contract(self, pause: int = 0):
        self._load_page(self.__link_survey_contract, pause)
        return self

    @allure.step("Link Surveyor")
    def link_surveyor(self, pause: int = 0):
        self._load_page(self.__link_surveyor, pause)
        return self
