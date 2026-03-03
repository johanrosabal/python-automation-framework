from applications.web.softship.components.menus.configuration.HomeMenu import HomeMenu
from applications.web.softship.components.menus.configuration.SecurityMenu import SecurityMenu
from applications.web.softship.components.menus.configuration.UtilitiesMenu import UtilitiesMenu


from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('ConfigurationMenu')


class ConfigurationMenu:

    def __init__(self, driver):
        self._driver = driver
        self.menu_home = HomeMenu(self._driver)
        self.menu_security = SecurityMenu(self._driver)
        self.menu_utilities = UtilitiesMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
        return cls._instance
