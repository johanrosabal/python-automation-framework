from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('DownloadsPage')


class DownloadsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the DownloadsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/FileDownload.html"
        # Locator definitions
        self._button_download = (By.XPATH, "//a[@type='button']", "Download [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = DownloadsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def go_to(self, url):
        self.navigation().go_to_url(url)

    def click_download(self):
        self.click().set_locator(self._button_download, self._name).single_click()
        return self
