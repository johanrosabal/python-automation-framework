from selenium.webdriver.common.by import By

from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.data import UserDTO

logger = setup_logger('DashboardPage')


class DashboardPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/login"
        # Locator definitions
        self._page_content = (By.ID, "dashboard-layout", "Main Page: Dashboard")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = DashboardPage(BaseApp.get_driver())
            cls.name = __class__.__name__
        return cls._instance


    def is_displayed(self):
        return self.element().set_locator(self._page_content).is_visible()