from applications.web.softship.components.menus.master_data.BasicMenu import BasicMenu
from applications.web.softship.components.menus.master_data.EdiMenu import EdiMenu
from applications.web.softship.components.menus.master_data.EquipmentMenu import EquipmentMenu
from applications.web.softship.components.menus.master_data.FinancialMenu import FinancialMenu
from applications.web.softship.components.menus.master_data.GeographicMenu import GeographicMenu
from applications.web.softship.components.menus.master_data.HomeMenu import HomeMenu
from applications.web.softship.components.menus.master_data.ShippingMenu import ShippingMenu
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('MenuMasterData')


class MasterDataMenu:

    def __init__(self, driver):
        self._driver = driver
        self.menu_home = HomeMenu(self._driver)
        self.menu_basic = BasicMenu(self._driver)
        self.menu_edi = EdiMenu(self._driver)
        self.menu_equipment = EquipmentMenu(self._driver)
        self.menu_financial = FinancialMenu(self._driver)
        self.menu_geographic = GeographicMenu(self._driver)
        self.menu_shipping = ShippingMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
        return cls._instance
