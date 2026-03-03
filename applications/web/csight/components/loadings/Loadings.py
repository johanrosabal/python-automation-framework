from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('Loadings')


class Loadings(BasePage):

    def __init__(self, driver):
        """
        Initialize the Loadings instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__

        # Locator definitions
        self._spinner = (By.XPATH, "//div[contains(@class,'spinner_container')]", "Getting booking data [Spinner Loading]")
        self._spinner_medium = (By.XPATH,"//div[contains(@class,'spinner_medium')]","Getting Spinner Medium [Spinner Loading]")
        self._loading_con = (By.XPATH, "//div[contains(@class,'loadingCon')]", "Loading Gif Animation")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def is_not_visible_spinner(self):
        is_visible = self.element().is_not_visible(self._spinner, timeout=10)
        logger.info(f"IS SPINNER VISIBLE? {is_visible}")
        return self

    def is_not_visible_spinner_medium(self):
        is_visible = self.element().is_not_visible(self._spinner_medium, timeout=5)
        logger.info(f"IS SPINNER MEDIUM VISIBLE? {is_visible}")
        return self

    def is_not_visible_loading_icon(self):
        is_visible = self.element().is_not_visible(self._loading_con, timeout=5)
        logger.info(f"IS NOT LOADING ICON VISIBLE? {is_visible}")
        return self

    def wait_until_loading_not_present(self):
        self.is_not_visible_spinner()
        self.is_not_visible_loading_icon()
        return self
