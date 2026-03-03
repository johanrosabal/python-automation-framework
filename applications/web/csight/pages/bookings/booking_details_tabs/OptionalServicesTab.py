from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('OptionalServicesTab')


class OptionalServicesTab(BasePage):

    def __init__(self, driver):
        """
        Initialize the OptionalServicesTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/bookingDetail?id={ID}"
        # Locator definitions
        self._txt_optional_service = "//div[contains(@class,'BookingDetailsOptionalServices')]/div/div/div/span"

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

    def get_cargo_marine(self):
        locator = (By.XPATH, f"{self._txt_optional_service}[contains(text(),'MARINE CARGO INSURANCE')]/../span[2]", f"Get Cargo Details Option [MARINE CARGO INSURANCE]")
        return self.get_text().set_locator(locator).by_text()
