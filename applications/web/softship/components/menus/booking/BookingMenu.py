from applications.web.softship.components.menus.booking.HomeMenu import HomeMenu
from applications.web.softship.components.menus.booking.HomeMenu import HomeMenu
import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('BookingMenu')


class BookingMenu:

    def __init__(self, driver):
        self._driver = driver
        self.menu_home = HomeMenu(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
        return cls._instance
