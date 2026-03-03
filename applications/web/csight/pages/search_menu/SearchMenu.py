from selenium.webdriver.common.by import By

from applications.web.csight.components.loadings.Loadings import Loadings
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SearchMenu')


class SearchMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the SearchMenu instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/"
        # Locator definitions
        self._input_search = (By.XPATH, "//div[@data-region-name='headerPanel']//input", "Input Search on Menu Header")
        self._input_search_options = (By.XPATH, "//div[@data-region-name='headerPanel']//select", "Input Search Options on Menu Header")

        # Sub-Components
        self.loadings = Loadings.get_instance()

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

    def select_search_option(self, option):
        self.element().set_locator(self._input_search_options, self._name).is_visible()
        self.dropdown().set_locator(self._input_search_options, self._name).by_text(option)
        return self

    def enter_search_criteria(self, criteria):
        self.element().set_locator(self._input_search, self._name).is_visible()
        # With this load the list on UI and ReCalculate the Desired Value
        lastDigit = criteria[-1]
        self.send_keys().set_locator(self._input_search, self._name)\
            .set_text(criteria)\
            .press_backspace()\
            .pause(1)\
            .set_text(lastDigit)\
            .pause(2)

        str_xpath = f"//li[@data-bookingid='{criteria}']"
        locator = (By.XPATH, str_xpath, f"Selection From List {criteria}")
        self.element().set_locator(locator).is_visible()
        self.click().set_locator(locator).highlight(duration=2).single_click()
        return self

    def search_booking(self, booking_number):
        self.select_search_option("Bookings")
        self.enter_search_criteria(booking_number)

        self.loadings.is_not_visible_loading_icon()
        self.loadings.is_not_visible_spinner()
        return self




