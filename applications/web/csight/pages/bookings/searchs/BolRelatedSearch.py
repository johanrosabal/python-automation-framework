from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('BolRelatedSearch')


class BolRelatedSearch(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the BolRelatedSearch instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # String Base XPaths
        self._xpath_bol_source = "//label[contains(text(),'BOL Source')]/.."
        self._xpath_bol_prefix = "//label[contains(text(),'BOL Prefix')]/.."
        self._xpath_bol_created_by_category = "//label[contains(text(),'BOL Created By Category')]/.."
        self._xpath_bol_created_by_user = "//label[contains(text(),'BOL Created By User')]/.."
        self._xpath_bol_created_date_from = "//label[contains(text(),'BOL Created Date (From)')]/.."
        self._xpath_bol_created_date_to = "//label[contains(text(),'BOL Created Date (To)')]/.."
        self._xpath_itn_number = "//label[contains(text(),'ITN Number')]/.."
        self._xpath_itn_status = "//label[contains(text(),'ITN Status')]/.."
        self._xpath_ssf_status = "//label[contains(text(),'ISF Status')]/.."
        self._xpath_customer_bol_upload_date_from = "//label[contains(text(),'Customer BOL Upload Date From')]/.."
        self._xpath_customer_bol_upload_date_to = "//label[contains(text(),'Customer BOL Upload Date To')]/.."
        self._xpath_bol_status = "//label[contains(text(),'BOL Status')]/.."
        self._xpath_bol_pending_reason = "//label[contains(text(),'BOL Pending Reason')]/.."
        self._xpath_bol_assigned_to = "//label[contains(text(),'BOL Assigned To')]/.."
        self._xpath_bol_bill_of_lading = "//label[contains(text(),'Bill of Lading')]/.."
        self._xpath_bol_invoice = "//label[contains(text(),'BOL Invoiced')]/.."
        self._xpath_transshipment = "//label[contains(text(),'Transshipment')]/.."
        self._xpath_multiple_bol_identifier = "//label[contains(text(),'Multiple BOL Identifier')]/.."
        self._xpath_shipping_instructions_uploaded = "//label[contains(text(),'Shipping Instructions Uploaded')]/.."
        self._xpath_vehicle_cnc_mismatch = "//label[contains(text(),'Vehicle / CNC Mismatch')]/.."
        self._xpath_document_status = "//label[contains(text(),'Document Status')]/.."
        self._xpath_document_type = "//label[contains(text(),'Document Type')]/.."
        self._xpath_document_review = "//label[contains(text(),'Document Review')]/.."
        self._xpath_document_review_status = "//label[contains(text(),'Document Review Status')]/.."
        self._xpath_exemption_codes = "//label[contains(text(),'Exemption codes')]/.."

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
        self.toggle_accordion().set_locator_with_label('BOL Related').open()
        return self

    def close(self):
        self.toggle_accordion().set_locator_with_label('BOL Related').close()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_multiple_bol_source(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_source}//input[@type='text']/..",
                         f"Search: BOL Source [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_bol_source}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_option_list}\"]/..",
                         f"Search Checkbox List: BOL Source [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def enter_bol_prefix(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_bol_prefix}//input[@type='text']", f"Search: BOL Prefix [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def select_bol_created_by_category(self, option):
        locator_select = (By.XPATH, f"{self._xpath_bol_created_by_category}//select",
                          f"Search: BOL Created by Category [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_multiple_bol_created_by_user(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_created_by_user}//input[@type='text']/..",
                         f"Search: BOL Created By User [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_bol_created_by_user}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: BOL Created By User  [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def enter_bol_created_date_from(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_bol_created_date_from}//input[@type='text']", f"Search: BOL Created Date (From) [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def enter_bol_created_date_to(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_bol_created_date_to}//input[@type='text']", f"Search: BOL Created Date (To) [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def enter_itn_numbers(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_itn_number}//input[@type='text']", f"Search: ITN Number [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def select_multiple_itn_status(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_itn_status}//input[@type='text']/..",
                         f"Search: ITN Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_itn_status}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: ITN Status [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_isf_status(self, option):
        locator_select = (By.XPATH, f"{self._xpath_itn_status}//select", f"Search: ISF Status [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_customer_bol_upload_date_from(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_customer_bol_upload_date_from}//input[@type='text']", f"Search: Customer BOL Upload Date From [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def enter_customer_bol_upload_date_to(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_customer_bol_upload_date_to}//input[@type='text']", f"Search: Customer BOL Upload Date To [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def select_multiple_bol_status(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_status}//input[@type='text']/..",
                         f"Search: BOL Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_bol_status}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: BOL Status [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_bol_pending_reason(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_pending_reason}//input[@type='text']/..",
                         f"Search: BOL Pending Reason [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_bol_pending_reason}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..", f"Search Checkbox List: BOL Pending Reason [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_bol_assigned_to(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_assigned_to}//input[@type='text']/..",
                         f"Search: BOL Assigned To [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_bol_assigned_to}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..", f"Search Checkbox List: BOL Assigned To[{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_radio_bill_of_lading(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_bill_of_lading}//span[text()='Yes']", f"Search: Bill of Lading [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_bill_of_lading}//span[text()='No']", f"Search: Bill of Lading  [No][{value}][Input]")
            case _:
                logger.warning(f"Bill of Lading not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_bol_invoiced(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoice}//span[text()='Yes']",
                                f"Search: BOL Invoiced [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoice}//span[text()='No']", f"Search: BOL Invoiced [No][{value}][Input]")
            case _:
                logger.warning(f"BOL Invoice not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_bol_transshipment(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_transshipment}//span[text()='Yes']", f"Search: Transshipment [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_transshipment}//span[text()='No']", f"Search: Transshipment[No][{value}][Input]")
            case _:
                logger.warning(f"Transshipment not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_multiple_bol_identifier(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_multiple_bol_identifier}//span[text()='Yes']", f"Search: Multiple BOL Identifier [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_multiple_bol_identifier}//span[text()='No']", f"Search: Multiple BOL Identifier [No][{value}][Input]")
            case _:
                logger.warning(f"Multiple BOL Identifier  not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_shipping_instructions_uploaded(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_shipping_instructions_uploaded}//span[text()='Yes']", f"Search: Shipping Instructions Uploaded [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_shipping_instructions_uploaded}//span[text()='No']", f"Search: Shipping Instructions Uploaded [No][{value}][Input]")
            case _:
                logger.warning(f"Shipping Instructions Uploaded not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_vehicle_cnc_mismatch(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_vehicle_cnc_mismatch}//span[text()='Yes']", f"Search: Vehicle CNC Mismatch [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_vehicle_cnc_mismatch}//span[text()='No']", f"Search: Vehicle CNC Mismatch [No][{value}][Input]")
            case _:
                logger.warning(f"Vehicle CNC Mismatch not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_multiple_document_status(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_document_status}//input[@type='text']/..", f"Search: Document Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_document_status}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..", f"Search Checkbox List: Document Status [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_document_type(self, option):
        locator_select = (By.XPATH, f"{self._xpath_document_type}//select", f"Search: Document Type [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_document_review(self, option):
        locator_select = (By.XPATH, f"{self._xpath_document_review}//select", f"Search: Document Review [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_document_review_status(self, option):
        locator_select = (By.XPATH, f"{self._xpath_document_review_status}//select", f"Search: Document Review Status [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_multiple_exemption_codes(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_exemption_codes}//input[@type='text']/..", f"Search: Exemption codes [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_exemption_codes}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..", f"Search Checkbox List: Exemption codes [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_bol_prefix(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bol_prefix}//input[@type='text']", f"Clear: BOL Prefix [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bol_created_by_user(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bol_created_by_user}//input[@type='text']", f"Clear: BOL Created By User [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bol_created_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bol_created_date_from}//input[@type='text']", f"Clear: BOL Created Date From [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_by_bol_created_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bol_created_date_to}//input[@type='text']", f"Clear: BOL Created Date To [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_itn_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_itn_number}//input[@type='text']", f"Clear: ITN Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_customer_bol_upload_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_customer_bol_upload_date_from}//input[@type='text']", f"Clear: Customer BOL Upload Date From [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_customer_bol_upload_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_customer_bol_upload_date_to}//input[@type='text']", f"Clear: Customer BOL Upload Date To [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bol_assigned_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bol_assigned_to}//input[@type='text']", f"Clear: BOL Assigned To [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_document_status(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_document_status}//input[@type='text']", f"Clear: Document Status [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_bol_source(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_bol_source}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: BOL Source [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_bol_created_by_user(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_bol_created_by_user}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: BOL Created By User [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_itn_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_itn_status}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: ITN Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_bol_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_bol_status}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: BOL Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_bol_pending_reason(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_bol_pending_reason}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: BOL Pending Reason [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_bol_assigned_to(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_bol_assigned_to}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: BOL Assigned To [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_document_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_document_status}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Document Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_exemption_codes(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_exemption_codes}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Exemption codes [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
