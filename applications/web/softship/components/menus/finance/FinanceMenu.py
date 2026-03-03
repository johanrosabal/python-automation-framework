from applications.web.softship.components.menus.finance.HomeMenu import HomeMenu
from applications.web.softship.components.menus.finance.CostControllingMenu import CostControllingMenu
from applications.web.softship.components.menus.finance.VoucherMenu import VoucherMenu
from applications.web.softship.components.menus.finance.SalesInvoicingMenu import SalesInvoicingMenu

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('FinanceMenu')


class FinanceMenu:

    def __init__(self, driver):
        self._driver = driver
        self.menu_home = HomeMenu(self._driver)
        self.menu_cost_controlling = CostControllingMenu(self._driver)
        self.menu_voucher = VoucherMenu(self._driver)
        self.menu_sales_invoice = SalesInvoicingMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
        return cls._instance
