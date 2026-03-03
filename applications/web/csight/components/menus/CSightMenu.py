from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CSightMenu')


class CSightMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the CSightMenu instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Base XPATH Containers
        self._xpath_base_menu = "//div[@class='header']"
        # Locator definitions
        self._menu_accounts = (By.XPATH, f"{self._xpath_base_menu}//ul/li/a[text()='Accounts']", "Menu: Accounts [Menu]")
        self._menu_bill_of_lading = (By.XPATH, f"{self._xpath_base_menu}//ul/li/a[text()='Bills of Lading']", "Menu: Bills of Lading [Menu]")
        self._menu_bookings = (By.XPATH, f"{self._xpath_base_menu}//ul/li/a[text()='Bookings']", "Menu: Bookings [Menu]")
        self._menu_cargo_not_in_container_shipping = (By.XPATH, f"{self._xpath_base_menu}//ul/li/a[text()='Cargo Not In Container Shipping']", "Menu: Cargo Not In Container Shipping [Menu]")
        self._menu_cargo_release_tracking = (By.XPATH, "{self._xpath_base_menu}//ul/li/a[text()='Cargo Release Tracking']", "Menu: Cargo Release Tracking [Menu]")
        self._menu_cases = (By.XPATH, f"{self._xpath_base_menu}//ul/li/a[text()='Cases']", "Menu: Cases [Menu]")
        self._menu_ideas = (By.XPATH, f"{self._xpath_base_menu}//ul/li/a[text()='Ideas']", "Menu: Ideas [Menu]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def click_menu_accounts(self):
        self.click().set_locator(self._menu_accounts, self._name).single_click()
        return self

    def click_menu_bill_of_lading(self):
        self.click().set_locator(self._menu_bill_of_lading, self._name).single_click()
        return self

    def click_menu_bookings(self):
        self.click().set_locator(self._menu_bookings, self._name).single_click()
        return self

    def click_menu_cargo_not_in_container_shipping(self):
        self.click().set_locator(self._menu_cargo_not_in_container_shipping, self._name).single_click()
        return self

    def click_menu_cargo_release_tracking(self):
        self.click().set_locator(self._menu_cargo_release_tracking, self._name).single_click()
        return self

    def click_menu_cases(self):
        self.click().set_locator(self._menu_cases, self._name).single_click()
        return self

    def click_menu_ideas(self):
        self.click().set_locator(self._menu_ideas, self._name).single_click()
        return self

    def _click_sub_menu_more(self, option):
        menu_more = (By.XPATH, f"{self._xpath_base_menu}//ul/li[@class='-more']/button", "Menu: More [Dropdown Menu]")
        self.click().set_locator(menu_more, self._name).single_click()
        sub_menu_locator = (By.XPATH, f"{self._xpath_base_menu}//ul/li[@class='-more']/ul/li/a[text()='{option}']", f"More Menu Options: [{option}]")
        self.click().set_locator(sub_menu_locator, self._name).single_click()
        return self

    def click_menu_empty_reposition_bookings(self):
        self._click_sub_menu_more("Empty Reposition Bookings")
        return self

    def click_menu_equipment_events(self):
        self._click_sub_menu_more("Equipment Events")
        return self

    def click_menu_equipment_inventory(self):
        self._click_sub_menu_more("Equipment Inventory")
        return self

    def click_menu_event_correction(self):
        self._click_sub_menu_more("Event Correction")
        return self

    def click_menu_invoice_configuration(self):
        self._click_sub_menu_more("Invoice Configuration")
        return self

    def click_menu_invoice_tracking(self):
        self._click_sub_menu_more("Invoice Tracking")
        return self

