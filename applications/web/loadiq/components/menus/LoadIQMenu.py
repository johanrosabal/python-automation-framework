import allure
from selenium.webdriver.common.by import By

from applications.web.loadiq.components.menus.carrier_portal.CarrierPortalMenu import CarrierPortalMenu
from applications.web.loadiq.components.menus.customer_portal.CustomerPortalMenu import CustomerPortalMenu
from applications.web.loadiq.components.menus.operations_portal.OperationsPortalMenu import OperationsPortalMenu
from applications.web.loadiq.components.menus.support_portal.SupportPortalMenu import SupportPortalMenu
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('LoadIQMenu')


class LoadIQMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the LoadIQMenu instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        self.customer_portal = CustomerPortalMenu(self._driver)
        self.carrier_portal = CarrierPortalMenu(self._driver)
        self.operations_portal = OperationsPortalMenu(self._driver)
        self.support_portal = SupportPortalMenu(self._driver)


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoadIQMenu(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Link Logout")
    def logout(self, pause: int = 1):
        username = (By.XPATH, "//span[contains(@class,'iq-username')]", "Username [Profile]")
        logout = (By.XPATH,"//a[@class='dropdown-item' and text()=' Log Out']", "Logout [Link]")
        self.click().set_locator(username, self._name).single_click().pause(pause)
        self.click().set_locator(logout, self._name).single_click().pause(pause)
        return self
