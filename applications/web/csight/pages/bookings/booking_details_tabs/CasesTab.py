from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CasesTab')


class CasesTab(BasePage):

    def __init__(self, driver):
        """
        Initialize the CasesTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/bookingDetail?id={ID}"
        # Locator definitions
        self._div_cases = "//div[contains(@class,'caseslist-row')]/div"

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

    def get_case_number(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[1]/div[contains(@class, 'booking-id')]//a")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

    def get_case_status(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[1]/div[contains(@class, 'booking-status')]")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

    def get_case_owner(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[2]/div")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

    def get_case_parent(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[3]/div//a")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

    def get_case_origin(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[4]/div")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

    def get_case_account(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[5]/div//a")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

    def get_case_created_on(self, index):
        locator = (By.XPATH, f"({self._div_cases})[{index}]/div[6]/div")
        return self.get_text().set_locator(locator, self._name).highlight().by_text()

