from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.bookings.searchs.BolRelatedSearch import BolRelatedSearch
from applications.web.csight.pages.bookings.searchs.EquipmentsCommoditiesSearch import EquipmentsCommoditiesSearch
from applications.web.csight.pages.bookings.searchs.HazardousSearch import HazardousSearch
from applications.web.csight.pages.bookings.searchs.PartiesSearch import PartiesSearch
from applications.web.csight.pages.bookings.searchs.RoutesTransportationSearch import RoutesTransportationSearch
from applications.web.csight.pages.bookings.searchs.ShipmentRelatedSearch import ShipmentRelatedSearch
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SearchPanel')


class SearchPanel(BasePage):

    def __init__(self, driver):
        """
        Initialize the SearchPanel instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # Locator definitions
        self.panel_parties = PartiesSearch.get_instance()
        self.panel_routes_transportation = RoutesTransportationSearch.get_instance()
        self.panel_equipment_commodities = EquipmentsCommoditiesSearch.get_instance()
        self.panel_shipment_related = ShipmentRelatedSearch.get_instance()
        self.panel_bol_related = BolRelatedSearch.get_instance()
        self.panel_hazardous = HazardousSearch.get_instance()
        # Buttons Component Class
        self._buttons = Buttons.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    # BUTTONS  ---------------------------------------------------------------------------------------------------------
    def click_apply(self):
        self._buttons.click_apply()
        return self

    def click_clear_all(self):
        self._buttons.click_clear_all()
        return self
