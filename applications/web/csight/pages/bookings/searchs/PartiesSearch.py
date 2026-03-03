from selenium.webdriver.common.by import By
from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('PartiesSearch')


class PartiesSearch(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the PartiesSearch instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # String Base XPaths
        self._xpath_accounts = "//label[contains(text(),'Account')]/.."
        self._xpath_vertical_item = "//span[contains(@class,'listbox_vertical')]"
        self._xpath_contract_number = "//label[contains(text(),'Contract Number')]/.."
        self._xpath_shipper = "//label[contains(text(),'Shipper')]/.."
        self._xpath_consignee = "//label[contains(text(),'Consignee')]/.."

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

    # HIDE/SHOW PANEL --------------------------------------------------------------------------------------------------
    def open(self):
        self.toggle_accordion().set_locator_with_label('Parties').open()
        return self

    def close(self):
        self.toggle_accordion().set_locator_with_label('Parties').close()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_multiple_account(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_accounts}/label[contains(text(),'Account')]/..//input[@type='text']", f"Search: Account [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_vertical_item}//span[text()='{search}']/..", f"Search Checkbox List: Account [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def enter_contract_number(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_contract_number}//input[@type='text']", f"Search: Contract Number [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        # TODO: CSIGH: Search List Box not displayed after enter Contract Number, Verify this functionality with the TEAM MEMBERS
        # locator_check = (By.XPATH, f"{self._xpath_vertical_item}//span[text()='{search}']/..", f"Search Checkbox List: Contract Number [{search}] [Input]")
        # Click Option Checkbox Displayed
        # self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list
        # self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def enter_shipper(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_shipper}//input[@type='text']", f"Search: Shipper [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_vertical_item}//span[text()='{search}']/..", f"Search Checkbox List: Shipper [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def enter_consignee(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_consignee}//input[@type='text']", f"Search: Consignee [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)

        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_vertical_item}//span[text()='{search}']/..", f"Search Checkbox List: Consignee [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    # Search Clear Icon ----------------------------------------------------------------------------------------------------
    def clear_account(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_accounts}//i[@class='clear-field']", f"Clear: Account [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def clear_contract_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_contract_number}//i[@class='clear-field']", f"Clear: Contract Number [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def clear_shipper(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_shipper}//i[@class='clear-field']", f"Clear: Shipper [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def clear_consignee(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_consignee}//i[@class='clear-field']", f"Clear: Consignee [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    # Remove Pills Criteria ----------------------------------------------------------------------------------------------------
    def pill_remove_account(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_accounts}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Account [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_contract_number(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_contract_number}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Contract Number [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_shipper(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_shipper}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Shipper [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_consignee(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_consignee}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Consignee [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
