import allure
from applications.web.softship.components.alert.AlertDialogBox import AlertDialogBox
from applications.web.softship.common.SoftshipPage import SoftshipPage
from applications.web.softship.components.buttons.Buttons import Buttons
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('PurchaseTariffCriteriaFormPage')


class PurchaseTariffCriteriaFormPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the PurchaseTariffCriteriaFormPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Details?taskHandlerId=PurchaseTariffCriteria"
        self._module_url = None
        # Locator definitions
        # Headers Buttons
        self._buttons = Buttons(self._driver)
        # Alert
        self.alert = AlertDialogBox(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["finance"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def click_save(self, pause: int = 0):
        self._buttons.click_save(pause=pause)
        return self

    def click_save_and_close(self, pause: int = 2):
        self._buttons.click_save_and_close(pause=pause)
        return self

    def click_close(self, pause: int = 2):
        self._buttons.click_close(pause=pause)
        return self

    def click_sql_info(self, pause: int = 2):
        self._buttons.click_sql_info(pause=pause)
        return self

    def click_customize_screen(self, pause: int = 2):
        self._buttons.click_customize_screen(pause=pause)
        return self

    @allure.step("Select Tariff Type Input Form: {tariff_type}")
    def select_tariff_type(self, tariff_type: str):
        self.dropdown_autocomplete().set_locator_by_label("Tariff Type").by_text(text=tariff_type, column=1)
        return self

    @allure.step("Enter Rate Category Assignment Form: {rate_category_assignment}")
    def select_rate_category_assignment(self, rate_category_assignment: str):
        self.dropdown_autocomplete().set_locator_by_label("Rate Category Assignment").by_text(
            text=rate_category_assignment, column=2)
        return self

    @allure.step("Search Available Criteria Input Form: {available_criteria}")
    def search_rate_available_criteria(self, available_criteria: str):
        self.search_autocomplete() \
            .set_locator_by_attribute(attribute="ng-model", value="tariff.searchKeyword") \
            .clear() \
            .by_text(text=available_criteria)
        return self

    @allure.step("Search Available Criteria List Input Form: {available_criteria_list}")
    def search_rate_available_criteria_list(self, available_criteria_list: list):
        """
            Iterates through a list of available criteria and performs the search operation for each.
            :param available_criteria_list: List of criteria to search for
            :return: Self (for chaining)
            """
        if not available_criteria_list:
            logger.error(f"Searching criteria List Empty")
            raise ValueError("The list of criteria is empty.")

        for criteria in available_criteria_list:
            logger.info(f"Searching criteria: {criteria}")
            self.search_rate_available_criteria(criteria)
        return self

    @allure.step("Checkbox Used Criteria: {used_criteria}")
    def check_used_criteria(self, used_criteria: str):
        self.search_autocomplete().check_compulsory_item(used_criteria)
        return self

    @allure.step("Checkbox Used Criteria List: {used_criteria_list}")
    def check_used_criteria_list(self, used_criteria_list: list):
        if not used_criteria_list:
            logger.error(f"Searching criteria List Empty")
            raise ValueError("The list of criteria is empty.")

        for criteria in used_criteria_list:
            logger.info(f"Check Used Criteria: {criteria}")
            self.check_used_criteria(criteria)
        return self

    @allure.step("Clear Used Criteria: {used_criteria}")
    def clear_used_criteria(self, used_criteria: str):
        self.search_autocomplete().clear_search_item(used_criteria)
        return self

    @allure.step("Clear List")
    def clear_list_used_criteria(self):
        self.search_autocomplete().click_clear_list()
        return self

    @allure.step("Verify Data Saved")
    def verify_saved_data(self):
        toast_actual = self.alert.get_toast_detail()
        toast_expected = "Data has been saved."
        self.screenshot().attach_to_allure("Verify Tariff Type", self._name)
        # Assert with a custom error message
        assert toast_actual == toast_expected, f"Error: Expected text '{toast_expected}' but found '{toast_actual}'"
        return self

