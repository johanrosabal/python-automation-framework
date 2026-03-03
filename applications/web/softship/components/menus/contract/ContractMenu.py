from applications.web.softship.components.menus.contract.HomeMenu import HomeMenu
from applications.web.softship.components.menus.contract.ContractsMenu import ContractsMenu


from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('ContractMenu')


class ContractMenu:

    def __init__(self, driver):
        self._driver = driver
        self.menu_home = HomeMenu(self._driver)
        self.menu_contracts = ContractsMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
        return cls._instance
