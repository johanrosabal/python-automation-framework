import allure
from selenium.webdriver.common.by import By

from applications.web.softship.common.SoftshipPage import SoftshipPage
from applications.web.softship.components.menus.booking.BookingMenu import BookingMenu
from applications.web.softship.components.menus.commercial.CommercialMenu import CommercialMenu
from applications.web.softship.components.menus.configuration.ConfigurationMenu import ConfigurationMenu
from applications.web.softship.components.menus.contract.ContractMenu import ContractMenu
from applications.web.softship.components.menus.finance.FinanceMenu import FinanceMenu
from applications.web.softship.components.menus.master_data.MasterDataMenu import MasterDataMenu

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('SoftshipMenu')


class SoftshipMenu(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the SoftshipMenu instance.
        """
        super().__init__(driver)
        self._driver = driver
        self.app_commercial = CommercialMenu(self._driver)
        self.app_configuration = ConfigurationMenu(self._driver)
        self.app_contract = ContractMenu(self._driver)
        self.app_finance = FinanceMenu(self._driver)
        self.app_master_data = MasterDataMenu(self._driver)
        self.app_bookings = BookingMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Link Logout")
    def logout(self, pause: int = 3):
        locator = (By.ID, "btnLogout", "Logout User")
        self.click().set_locator(locator, self._name).single_click().pause(pause)
        return self
