from selenium.webdriver.common.by import By
from tabulate import tabulate

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.accounts.searchs.SearchPanel import SearchPanel
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('AccountsPage')


class AccountsPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the AccountsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/accounts"

        # Locator definitions
        self._xpath_item_container = "//div[contains(@class,'row-data-repeat')]"

        # Sub-Components
        self.buttons = Buttons.get_instance()
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
        self.buttons.click_use_filters()
        return self

    def enter_search_the_list(self, text):
        self.enter_search_the_list(text)
        return self

    def select_sort_by(self, sort_by: str):
        self.buttons.select_sort_by(sort_by)
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

    # ITEMS ------------------------------------------------------------------------------------------------------------
    def click_list_item_account_name(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Account Name']/following-sibling::a", f"Accounts Item [{index}]: Account Name [Click]")
        return self.click().set_locator(locator, self._name).single_click()

    def get_list_item_account_name(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Account Name']/following-sibling::a", f"Accounts Item [{index}]: Account Name [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_customer_status(self, index):
        locator_full_text = (By.XPATH,
                             f"({self._xpath_item_container})[{str(index)}]//label[text()='Customer Status']/..",
                             f"Accounts [{index}]: Customer Status [Full Container Text]")

        locator_label_text = (By.XPATH,
                              f"({self._xpath_item_container})[{str(index)}]//label[text()='Customer Status']",
                              f"Accounts [{index}]: Customer Status [Label Text]")

        full_text = self.get_text().set_locator(locator_full_text).by_text()
        label_text = self.get_text().set_locator(locator_label_text).by_text()

        active_text = full_text.replace(label_text, "").strip()
        return active_text

    def get_list_item_cvif_id(self, index):
        locator_full_text = (By.XPATH,
                             f"({self._xpath_item_container})[{str(index)}]//label[text()='CVIF Id']/..",
                             f"Accounts [{index}]: CVIF Id [Full Container Text]")

        locator_label_text = (By.XPATH,
                              f"({self._xpath_item_container})[{str(index)}]//label[text()='CVIF Id']",
                              f"Accounts [{index}]: CVIF Id [Label Text]")

        full_text = self.get_text().set_locator(locator_full_text).by_text()
        label_text = self.get_text().set_locator(locator_label_text).by_text()

        active_text = full_text.replace(label_text, "").strip()
        return active_text

    def click_list_item_parent_account(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Parent Account']/..//a", f"Accounts Item [{index}]: Parent Account [Click]")
        return self.click().set_locator(locator, self._name).single_click()

    def get_list_item_parent_account(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Parent Account']/..//a", f"Accounts Item [{index}]: Parent Account [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_parent_cvif_id(self, index):
        locator_full_text = (By.XPATH,
                             f"({self._xpath_item_container})[{str(index)}]//label[text()='Parent CVIF Id']/..",
                             f"Accounts [{index}]: Parent CVIF Id [Full Container Text]")

        locator_label_text = (By.XPATH,
                              f"({self._xpath_item_container})[{str(index)}]//label[text()='Parent CVIF Id']",
                              f"Accounts [{index}]: Parent CVIF Id [Label Text]")

        full_text = self.get_text().set_locator(locator_full_text).by_text()
        label_text = self.get_text().set_locator(locator_label_text).by_text()

        active_text = full_text.replace(label_text, "").strip()
        return active_text

    def get_list_item_account_owner(self, index):
        locator_full_text = (By.XPATH,
                             f"({self._xpath_item_container})[{str(index)}]//label[text()='Account Owner']/..",
                             f"Accounts [{index}]: Account Owner [Full Container Text]")

        locator_label_text = (By.XPATH,
                              f"({self._xpath_item_container})[{str(index)}]//label[text()='Account Owner']",
                              f"Accounts [{index}]: Account Owner [Label Text]")

        full_text = self.get_text().set_locator(locator_full_text).by_text()
        label_text = self.get_text().set_locator(locator_label_text).by_text()

        active_text = full_text.replace(label_text, "").strip()
        return active_text

    def get_list_item_sales_rep_region(self, index):
        locator_full_text = (By.XPATH,
                             f"({self._xpath_item_container})[{str(index)}]//label[text()='Sales Rep Region']/..",
                             f"Accounts [{index}]: Sales Rep Region [Full Container Text]")

        locator_label_text = (By.XPATH,
                              f"({self._xpath_item_container})[{str(index)}]//label[text()='Sales Rep Region']",
                              f"Accounts [{index}]: Sales Rep Region [Label Text]")

        full_text = self.get_text().set_locator(locator_full_text).by_text()
        label_text = self.get_text().set_locator(locator_label_text).by_text()

        active_text = full_text.replace(label_text, "").strip()
        return active_text

    def get_list_item_type(self, index):
        locator_full_text = (By.XPATH,
                             f"({self._xpath_item_container})[{str(index)}]//label[text()='Type']/..",
                             f"Accounts [{index}]: Type [Full Container Text]")

        locator_label_text = (By.XPATH,
                              f"({self._xpath_item_container})[{str(index)}]//label[text()='Type']",
                              f"Accounts [{index}]: Type [Label Text]")

        full_text = self.get_text().set_locator(locator_full_text).by_text()
        label_text = self.get_text().set_locator(locator_label_text).by_text()

        active_text = full_text.replace(label_text, "").strip()
        return active_text

    def get_list_item(self, index):
        account_name = self.get_list_item_account_name(index)
        customer_status = self.get_list_item_customer_status(index)
        cvif_id = self.get_list_item_cvif_id(index)
        parent_account = self.get_list_item_parent_account(index)
        parent_cvif_id = self.get_list_item_parent_cvif_id(index)
        account_owner = self.get_list_item_account_owner(index)
        sales_rep_region = self.get_list_item_sales_rep_region(index)
        type_ = self.get_list_item_type(index)

        data = {
            "Account Name": account_name,
            "Customer Status": customer_status,
            "CVIF Id": cvif_id,
            "Parent Account": parent_account,
            "Parent CVIF Id": parent_cvif_id,
            "Account Owner": account_owner,
            "Sales Rep Region": sales_rep_region,
            "Type": type_
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data
