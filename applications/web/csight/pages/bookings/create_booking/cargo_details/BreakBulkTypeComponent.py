from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('BreakBulkTypeComponent')


class BreakBulkTypeComponent(BasePage):

    def __init__(self, driver):
        """
        Initialize the BreakBulkTypeComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Locator definitions

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def set_booking_data(self, data=None):
        """ Set Booking Data and share with all fill methods """
        self.booking_data = data
        return self

    def some_method(self):
        pass
