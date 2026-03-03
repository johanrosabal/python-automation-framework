from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('HazmatDetailsTab')


class HazmatDetailsTab(BasePage):

    def __init__(self, driver):
        """
        Initialize the HazmatDetailsTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/web/index.php/auth/login"
        # Locator definitions
        self._locator_1 = (By.NAME, "...", "Input Locator_1")
        self._locator_2 = (By.NAME, "...", "Input Locator_2")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = HazmatDetailsTab(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def some_method(self):
        pass
