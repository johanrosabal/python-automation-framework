from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('SearchPanel')


class SearchPanel(CSightBasePage):

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
        self.relative = "Employees/s/accounts"
        # String Base XPaths
        self._xpath_account_name = "//label[contains(text(),'Account')]/.."
        self._xpath_customer_status = "//label[contains(text(),'Account')]/.."
        self._xpath_cvif_id = "//label[contains(text(),'Account')]/.."
        self._xpath_parent_account = "//label[contains(text(),'Account')]/.."
        self._xpath_parent_cvif_id = "//label[contains(text(),'Account')]/.."
        self._xpath_account_owner = "//label[contains(text(),'Account')]/.."
        self._xpath_sales_rep_region = "//label[contains(text(),'Account')]/.."
        self._xpath_type = "//label[contains(text(),'Account')]/.."
        # Sub-Components
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

    # BUTTONS  ---------------------------------------------------------------------------------------------------------
    def click_apply(self):
        self.buttons.click_apply()
        return self

    def click_clear_all(self):
        self.buttons.click_clear_all()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_account_name(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_account_name}//input[@type='text']/..", f"Search: Account Name [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_account_name}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Account Name [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_customer_status(self, option):
        locator_select = (By.XPATH, f"{self._xpath_customer_status}//select", f"Search: Customer Status [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_cvif_id(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_cvif_id}//input[@type='text']", f"Search: CVIF ID [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_parent_account(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_parent_account}//input[@type='text']/..", f"Search: Parent Account [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_parent_account}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Parent Account [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def enter_parent_cvif_id(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_parent_cvif_id}//input[@type='text']", f"Search: Parent CVIF ID [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_account_owner(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_account_owner}//input[@type='text']/..", f"Search: Account Owner [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_account_owner}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Account Owner [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_sales_rep_region(self, option):
        locator_select = (By.XPATH, f"{self._xpath_sales_rep_region}//select", f"Search: Sales Rep Region [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_type(self, option):
        locator_select = (By.XPATH, f"{self._xpath_type}//select", f"Search: Type [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_account_name(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_account_name}//input[@type='text']", f"Clear: Account Name [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_cvif_id(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_cvif_id}//input[@type='text']", f"Clear: CVIF ID [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_parent_account(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_parent_account}//input[@type='text']", f"Clear: Parent Account [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_parent_cvif_id(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_parent_cvif_id}//input[@type='text']", f"Clear: Parent CVIF ID [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_account_owner(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_account_owner}//input[@type='text']", f"Clear: Account Owner [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self
