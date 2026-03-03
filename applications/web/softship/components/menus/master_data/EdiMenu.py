import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('EdiMenu')


class EdiMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the EDI Manu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=2"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_edi = (By.XPATH, "//a[text()='EDI']", "EDI Link")

    @allure.step("Load Edit Page")
    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Link Agency")
    def link_edi(self, pause: int = 0):
        self._load_page(self.__link_edi, pause)
        return self
