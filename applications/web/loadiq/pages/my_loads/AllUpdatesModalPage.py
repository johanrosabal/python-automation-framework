from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('AllUpdatesModalPage')


class AllUpdatesModalPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the AllUpdatesModalPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._modal = "//h4[text()='All Updates']/../../.."

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def click_close(self):
        locator = (By.XPATH, f"", "Close Modal All Updates")
        self.click().set_locator(locator).single_click()
        return self

    def get_all_updates_stop(self, index: int = 1):
        locator = (By.XPATH, f"(//h4[text()='All Updates']/../../..//ul/li/div[2])[{index}]", f"All Updates Stop [{index}]")
        return self.get_text().set_locator(locator).by_text().replace("\n", " - ")
