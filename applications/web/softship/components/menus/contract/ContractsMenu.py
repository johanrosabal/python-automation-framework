import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ContractsMenu')


class ContractsMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/contracts/home?page_index=0"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__nav_advance_search = (By.XPATH, "//a[text()='Advanced Search']", "Advanced Search Link")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["contracts"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Advanced Search")
    def link_advance_search(self, pause: int = 0):
        self._load_page(self.__nav_advance_search, pause)
        return self

