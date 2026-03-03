from selenium.webdriver.common.by import By
from tabulate import tabulate

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.cases.searchs.SearchPanel import SearchPanel
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CasesPage')


class CasesPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the CasesPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/web/index.php/auth/login"
        # Buttons Component Class
        self._buttons = Buttons.get_instance()
        # Locator definitions
        self._xpath_item_container = "//div[contains(@class,'caseslist-row')]"
        # Sub-Components
        self.search_panel = SearchPanel.get_instance()

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
        self._buttons.click_use_filters()
        return self

    def enter_search_the_list(self, text):
        self.enter_search_the_list(text)
        return self

    # HEADER  ----------------------------------------------------------------------------------------------------------
    def click_create_case(self):
        self._buttons.click_button_with_label("Create Case")
        return self

    # Pagination -------------------------------------------------------------------------------------------------------
    def click_refresh_icon(self):
        self._buttons.click_refresh_icon()
        return self

    def select_view_pages(self, number):
        self._buttons.select_view_pages(number)
        return self

    def click_previous_page(self):
        self._buttons.click_previous_page()
        return self

    def click_next_page(self):
        self._buttons.click_next_page()
        return self

    # TABS ------------------------------------------------------------------------------------------------------------
    def click_tab_all(self):
        self._buttons.click_tab_button_with_label("All")
        return self

    def click_tab_bl_revision(self):
        self._buttons.click_tab_button_with_label("BL Revision")
        return

    def click_tab_booking_request(self):
        self._buttons.click_tab_button_with_label("Booking Request")
        return self

    def click_tab_customer_inquiry(self):
        self._buttons.click_tab_button_with_label("Customer Inquiry")
        return

    def click_tab_managed_services_support(self):
        self._buttons.click_tab_button_with_label("Managed Services Support")
        return

    def click_tab_platform_automation(self):
        self._buttons.click_tab_button_with_label("Platform Automations")
        return

    def click_tab_pricing_inquiry_request(self):
        self._buttons.click_tab_button_with_label("Pricing Inquiry/Request")
        return

    def click_tab_service_support(self):
        self._buttons.click_tab_button_with_label("Service Support")
        return

    # ITEMS ------------------------------------------------------------------------------------------------------------
    def click_list_item_case_id(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//div[contains(@class, 'booking-id')]/span/a", f"Cases List Item [{index}]: Case Id [Text]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def get_list_item_case_id(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//div[contains(@class, 'booking-id')]/span/a", f"Cases List Item [{index}]: Case Id [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_case_status(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//div[contains(@class, 'booking-id')]/following-sibling::div", f"Cases List Item [{index}]: Case Status [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_case_owner(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//label[text()='Case Owner']/../div", f"Cases List Item [{index}]: Case Owner [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_case_origin(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//label[text()='Case Origin']/../div", f"Cases List Item [{index}]: Case Origin [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_account(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//label[text()='Account']/../div", f"Cases List Item [{index}]: Account [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_created_on(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//label[text()='Created On']/../div", f"Cases List Item [{index}]: Created On [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_customer_inquiry(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{index}]//label[text()='Customer Inquiry']/../div/a", f"Cases List Item [{index}]: Customer Inquiry [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item(self, index):

        case_id = self.get_list_item_case_id(index) or "-"
        case_status= self.get_list_item_case_status(index) or "-"
        case_owner = self.get_list_item_case_owner(index)  or "-"
        case_origin = self.get_list_item_case_origin(index) or "-"
        account = self.get_list_item_account(index) or "-"
        created_on = self.get_list_item_created_on(index)  or "-"
        customer_inquiry = self.get_list_item_customer_inquiry(index) or "-"

        data = {
            "Case ID": case_id,
            "Case Status:": case_status,
            "Case Owner": case_owner,
            "Case Origin": case_origin,
            "Account": account,
            "Created On": created_on,
            "Customer Inquiry": customer_inquiry
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data




