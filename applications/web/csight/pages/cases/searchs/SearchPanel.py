from selenium.webdriver.common.by import By
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
        self.relative = "Employees/s/cases"
        # String Base XPaths
        self._xpath_status = "//label[contains(text(),'Status')]/.."
        self._xpath_case_owner = "//label[contains(text(),'Case Owner')]/.."
        self._xpath_case_origin = "//label[contains(text(),'Case Origin')]/.."
        self._xpath_account = "//label[contains(text(),'Account')]/.."
        self._xpath_created_between = "//label[contains(text(),'Created Between')]/.."
        self._xpath_bol_bkg_numbers = "//label[contains(text(),'BOL/BKG Number(s)')]/.."
        self._xpath_voyage = "//label[contains(text(),'Voyage')]/.."
        self._xpath_shipper = "//label[contains(text(),'Shipper')]/.."
        self._xpath_consignee = "//label[contains(text(),'Consignee')]/.."
        self._xpath_created_by = "//label[contains(text(),'Created By')]/.."
        self._xpath_subject = "//label[contains(text(),'Subject')]/.."
        self._xpath_description = "//label[contains(text(),'Description')]/.."
        self._xpath_customer_reference_number = "//label[contains(text(),'Customer Reference #')]/.."
        self._xpath_bol_number = "//label[contains(text(),'BOL Number')]/.."

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

    def some_method(self):
        pass
