import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('QuoteRateMenu')


class QuoteRateMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Quotation/Home/QuotationHome"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_advance_search = (By.XPATH, "//a[text()='Advanced Search']", "Link Advanced Search")
        self.__btn_create = (By.XPATH, "//a[text()='Create']", "Create Button")
        self.__btn_find = (By.XPATH, "//button[text()='Find']", "Find Button")
        self.__input_searching_for = (By.XPATH, "//input[@placeholder='What are you searching for?']", "Searching For Input Box")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["commercial"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Update Voyage")
    def menu_advance_search(self, pause: int = 0):
        self._load_page(self.__link_advance_search, pause)
        return self

    @allure.step("Click Create Button")
    def click_create(self, pause: int = 0):
        self._load_page(self.__btn_create, pause)
        return self

    @allure.step("Enter searching for")
    def enter_searching_for(self, search: str, pause: int = 0):
        self.send_keys().set_locator(self.__input_searching_for, self._name).set_text(search)
        self.click().set_locator(self.__btn_find, self._name).single_click().pause(pause)
        return self

    @allure.step("Link My Queries")
    def menu_my_queries(self, query_text: str, pause: int = 0):
        locator = (By.XPATH, f"//a[text()='{query_text}']", "Link My Queries:{query_text}")
        self._load_page(locator, pause)
        return self
