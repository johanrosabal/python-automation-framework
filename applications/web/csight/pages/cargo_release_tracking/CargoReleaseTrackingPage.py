from selenium.webdriver.common.by import By
from tabulate import tabulate

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.cargo_release_tracking.searchs.SearchPanel import SearchPanel
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
logger = setup_logger('CargoReleaseTrackingPage')


class CargoReleaseTrackingPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the CargoReleaseTrackingPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/cargoreleasetracking"
        # Base XPaths Strings
        self._xpath_item_container = "//c-cc_-cargo-release-tracking-list-data-item/div"

        # Sub-Components
        self.search_panel = SearchPanel.get_instance()
        self.buttons = Buttons.get_instance()

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

    # Filters & Search -------------------------------------------------------------------------------------------------
    def click_use_filters(self):
        self.buttons.click_use_filters()
        return self

    # Pagination -------------------------------------------------------------------------------------------------------
    def click_refresh_icon(self):
        self.buttons.click_refresh_icon()
        return self

    def select_view_pages(self, number):
        self.buttons.select_view_pages(number)
        return self

    def click_previous_page(self):
        self.buttons.click_previous_page()
        return self

    def click_next_page(self):
        self.buttons.click_next_page()
        return self

    # HEADER  ----------------------------------------------------------------------------------------------------------
    def get_item_list_dock_receipt_no(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='DOCK RECEIPT NO.']/..//span", f"[{index}]: Cargo Release Tracking Item [{index}]: DOCK RECEIPT NO. [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_bol_number(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='BOL NUMBER']/../div", f"[{index}]: Cargo Release Tracking Item [{index}]: BOL NUMBER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_customs_clearance_location(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='CUSTOMS CLEARANCE LOCATION']/../div", f"[{index}]: Cargo Release Tracking Item [{index}]: CUSTOMS CLEARANCE LOCATION [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_release_location(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='RELEASE LOCATION']/../div", f"[{index}]: Cargo Release Tracking Item [{index}]: RELEASE LOCATION [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_bol_surrendered(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='BOL SURRENDERED']/../div", f"[{index}]: Cargo Release Tracking Item [{index}]: BOL SURRENDERED [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_arrived_at_release_location(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='ARRIVED AT RELEASE LOCATION']/../div/span/span", f"[{index}]: Cargo Release Tracking Item [{index}]: ARRIVED AT RELEASE LOCATION [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_release_type(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='RELEASE TYPE']/../div/span/div", f"[{index}]: Cargo Release Tracking Item [{index}]: RELEASE TYPE [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_bol_cargo_release(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[1]//label[text()='BOL CARGO RELEASED']/../div/span/div", f"[{index}]: Cargo Release Tracking Item [{index}]: BOL CARGO RELEASED [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_item_list_invoice_label(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[2]/div/div", f"[{index}]: Cargo Release Tracking Item [{index}]: INVOICE LABEL [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def click_item_list_view_details(self, index):
        locator_button = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[3]/span//button", f"[{index}]: Cargo Release Tracking Item [{index}]: Dropdown Menu Options [...] [button]")
        locator_menu_item = (By.XPATH, f"({self._xpath_item_container})[{index}]/div[3]/span//a[@role='menuitem']/span[text()='VIEW DETAILS']", f"[{index}]: Cargo Release Tracking Item [{index}]: DETAILS Menu Item [button]")
        # Display Menu Item Options
        self.click().set_locator(locator_button).single_click()
        # Click 'View Details Option'
        self.click().set_locator(locator_menu_item).single_click()
        return self

    def get_list_item(self, index):

        dock_receipt_no = self.get_item_list_dock_receipt_no(index) or "-"
        bol_number = self.get_item_list_bol_number(index) or "-"
        customs_clearance_location = self.get_item_list_customs_clearance_location(index) or "-"
        release_location = self.get_item_list_release_location(index) or "-"
        bol_surrendered = self.get_item_list_bol_surrendered(index) or "-"
        arrived_at_release_location = self.get_item_list_arrived_at_release_location(index) or "-"
        release_type = self.get_item_list_release_type(index) or "-"
        bol_cargo_release = self.get_item_list_bol_cargo_release(index) or "-"
        invoice_label = self.get_item_list_invoice_label(index) or "-"

        data = {
            "DOCK RECEIPT NO.": dock_receipt_no,
            "BOL NUMBER": bol_number,
            "CUSTOMS CLEARANCE LOCATION": customs_clearance_location,
            "RELEASE LOCATION": release_location,
            "BOL SURRENDERED": bol_surrendered,
            "ARRIVED AT RELEASE LOCATION": arrived_at_release_location,
            "RELEASE TYPE": release_type,
            "BOL CARGO RELEASED": bol_cargo_release,
            "INVOICE LABEL": invoice_label
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data



