from applications.web.softship.components.menus.commercial.HomeMenu import HomeMenu
from applications.web.softship.components.menus.commercial.QuoteRateMenu import QuoteRateMenu
from applications.web.softship.components.menus.commercial.VoyageMenu import VoyageMenu

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('CommercialMenu')


class CommercialMenu:

    def __init__(self, driver):
        self._driver = driver
        self.menu_home = HomeMenu(self._driver)
        self.menu_voyage = VoyageMenu(self._driver)
        self.menu_quote_rate = QuoteRateMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
        return cls._instance
