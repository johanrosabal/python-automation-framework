from selenium.webdriver.common.by import By
from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.components.loadings.Loadings import Loadings
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp


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
        self.relative = "Employees/s/billsoflading"
        # String Base XPaths
        self._xpath_accounts = "//label[contains(text(),'Account')]/.."
        self._xpath_booking_number = "//label[contains(text(),'Booking Number')]/.."
        self._xpath_port_of_load = "//label[contains(text(),'Port of Load')]/.."
        self._xpath_discharge_port = "//label[contains(text(),'Discharge Port')]/.."
        self._xpath_destination = "//label[contains(text(),'Destination')]/.."
        self._xpath_direction = "//label[contains(text(),'Direction')]/.."
        self._xpath_voyage_prefix = "//label[contains(text(),'Voyage Prefix')]/.."
        self._xpath_voyage_number = "//label[contains(text(),'Voyage Number')]/.."
        self._xpath_equipment_number = "//label[contains(text(),'Equipment Number')]/.."
        self._xpath_bill_of_lading_prefix = "//label[contains(text(),'Bill of Lading Prefix')]/.."
        self._xpath_current_sail_date_from = "//label[contains(text(),'Current Sail Date (From)')]/.."
        self._xpath_current_sail_date_to = "//label[contains(text(),'Current Sail Date (To)')]/.."
        self._xpath_shipper = "//label[contains(text(),'Shipper')]/.."
        self._xpath_consignee = "//label[contains(text(),'Consignee')]/.."
        self._xpath_bill_created_date_from = "//label[contains(text(),'Bill Created Date (From)')]/.."
        self._xpath_bill_created_date_to = "//label[contains(text(),'Bill Created Date (To)')]/.."
        self._xpath_customer_sent_date_from = "//label[contains(text(),'Customer Sent Date (From)')]/.."
        self._xpath_customer_sent_date_to = "//label[contains(text(),'Customer Sent Date (To)')]/.."
        self._xpath_equipment_receive_date_from = "//label[contains(text(),'Equipment Receive Date (From)')]/.."
        self._xpath_equipment_receive_date_to = "//label[contains(text(),'Equipment Receive Date (To)')]/.."
        self._xpath_bol_creation = "//label[contains(text(),'BOL Creation')]/.."
        self._xpath_created_by = "//label[contains(text(),'Created By')]/.."
        self._xpath_assigned_to = "//label[contains(text(),'Assigned To')]/.."
        self._xpath_status = "//label[contains(text(),'Status')]/.."
        self._xpath_cargo_type = "//label[contains(text(),'Cargo Type')]/.."
        self._xpath_equipment_type = "//label[contains(text(),'Equipment Type')]/.."
        self._xpath_bol_source = "//label[contains(text(),'BOL Source')]/.."
        self._xpath_isf_status = "//label[contains(text(),'ISF Status')]/.."
        self._xpath_cargo_received = "//label[contains(text(),'Cargo Received')]/.."
        self._xpath_hazardous = "//label[contains(text(),'Hazardous')]/.."
        self._xpath_in_bond_indicator = "//label[contains(text(),'In Bond Indicator')]/.."
        self._xpath_bol_invoiced = "//label[contains(text(),'BOL Invoiced')]/.."
        self._xpath_multiple_bill_identifier = "//label[contains(text(),'Multiple Bill Identifier')]/.."
        self._xpath_final_imo_received = "//label[contains(text(),'Final IMO Received')]/.."
        self._xpath_payment_terms = "//label[contains(text(),'Payment Terms')]/.."
        self._xpath_customer_reference_id = "//label[contains(text(),'Customer Reference ID')]/.."

        # Sub-Components
        self.buttons = Buttons.get_instance()
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

    # LOADING COMPONENT ------------------------------------------------------------------------------------------------
    def is_not_visible_spinner(self):
        self.loadings.is_not_visible_spinner()
        return self

    # BUTTONS  ---------------------------------------------------------------------------------------------------------
    def click_apply(self):
        self.buttons.click_apply()
        return self

    def click_clear_all(self):
        self.buttons.click_clear_all()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_multiple_account(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_accounts}//input[@type='text']/..",
                         f"Search: Account [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_accounts}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Account [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_booking_number(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_accounts}//input[@type='text']/..",
                         f"Search: Booking Number [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_accounts}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Booking Number [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_port_of_load(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_port_of_load}//input[@type='text']/..",
                         f"Search: Port of Load [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_port_of_load}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Port of Load [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_discharge_port(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_discharge_port}//input[@type='text']/..",
                         f"Search: Discharge Port [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_discharge_port}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Discharge Port [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_destination(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_destination}//input[@type='text']/..",
                         f"Search: Destination [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_discharge_port}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Destination [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_radio_direction(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_direction}//span[text()='Yes']", f"Search: Direction [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_direction}//span[text()='No']", f"Search: Direction [No][{value}][Input]")
            case _:
                logger.warning(f"Direction not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_multiple_voyage_prefix(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_voyage_prefix}//input[@type='text']/..",
                         f"Search: Voyage Prefix [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_voyage_prefix}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Voyage Prefix  [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_voyage_number(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_voyage_number}//input[@type='text']/..",
                         f"Search: Voyage Number [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_voyage_number}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Voyage Number [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_equipment_number(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_equipment_number}//input[@type='text']/..",
                         f"Search: Equipment Number [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_equipment_number}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Equipment Number [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def enter_bill_of_lading_prefix(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_bill_of_lading_prefix}//input[@type='text']", f"Search: Bill of Lading Prefix [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_current_sail_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_from}//input[@type='text']", f"Search: Current Sail Date (From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_current_sail_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_to}//input[@type='text']", f"Search: Current Sail Date (To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_multiple_shipper(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_shipper}//input[@type='text']/..",
                         f"Search: Shipper [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_shipper}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Shipper [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_consignee(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_consignee}//input[@type='text']/..", f"Search: Consignee [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_consignee}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Consignee [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def enter_current_bill_created_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_bill_created_date_from}//input[@type='text']", f"Search: Bill Created Date (From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_current_bill_created_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_bill_created_date_to}//input[@type='text']", f"Search: Bill Created Date (To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_customer_sent_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_customer_sent_date_from}//input[@type='text']", f"Search: Customer Sent Date (From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_customer_sent_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_customer_sent_date_to}//input[@type='text']", f"Search: Customer Sent Date (To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_equipment_receive_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_from}//input[@type='text']", f"Search: Equipment Receive Date (From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_equipment_receive_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_to}//input[@type='text']", f"Search: Equipment Receive Date (To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_bol_creation(self, option):
        locator_select = (By.XPATH, f"{self._xpath_bol_creation}//select", f"Search: BOL Creation [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_multiple_creation_by(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_created_by}//input[@type='text']/..", f"Search: Creation By [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_created_by}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Creation By [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_assign_to(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_assigned_to}//input[@type='text']/..", f"Search: Assigned To [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_assigned_to}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Assigned To [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_status(self, option):
        locator_select = (By.XPATH, f"{self._xpath_status}//select", f"Search: Status [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_multiple_cargo_type(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_cargo_type}//input[@type='text']/..", f"Search: Cargo Type [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_cargo_type}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Cargo Type [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_equipment_type(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_equipment_type}//input[@type='text']/..", f"Search: Equipment Type [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_equipment_type}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Equipment Type [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_bol_source(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_source}//input[@type='text']/..", f"Search: BOL Source [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_bol_source}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: BOL Source [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_isf_status(self, option):
        locator_select = (By.XPATH, f"{self._xpath_isf_status}//select", f"Search: ISF Status [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_radio_cargo_received(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_cargo_received}//span[text()='Yes']", f"Search: Cargo Received [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_cargo_received}//span[text()='No']", f"Search: Cargo Received [No][{value}][Input]")
            case _:
                logger.warning(f"Cargo Received not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_hazardous(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_hazardous}//span[text()='Yes']", f"Search: Hazardous [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_hazardous}//span[text()='No']", f"Search: Hazardous [No][{value}][Input]")
            case _:
                logger.warning(f"Hazardous not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_in_bond_indicator(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_in_bond_indicator}//span[text()='Yes']", f"Search: In Bond Indicator [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_in_bond_indicator}//span[text()='No']", f"Search: In Bond Indicator [No][{value}][Input]")
            case _:
                logger.warning(f"In Bond Indicator not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_bol_invoiced(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoiced}//span[text()='Yes']", f"Search: BOL Invoiced [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoiced}//span[text()='No']", f"Search: BOL Invoiced [No][{value}][Input]")
            case _:
                logger.warning(f"BOL Invoiced not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_multiple_bill_identifier(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoiced}//span[text()='Yes']", f"Search: Multiple Bill Identifier [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoiced}//span[text()='No']", f"Search: Multiple Bill Identifier [No][{value}][Input]")
            case _:
                logger.warning(f"Multiple Bill Identifier not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_final_imo_received(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoiced}//span[text()='Yes']", f"Search: Final IMO Received [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_invoiced}//span[text()='No']", f"Search: Final IMO Received [No][{value}][Input]")
            case _:
                logger.warning(f"Final IMO Received not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_payment_terms(self, option):
        locator_select = (By.XPATH, f"{self._xpath_payment_terms}//select", f"Search: Payment Terms [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_customer_reference_id(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_customer_reference_id}//input[@type='text']", f"Search: Customer Reference ID [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_account(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_accounts}//input[@type='text']", f"Clear: Account [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_booking_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_booking_number}//input[@type='text']", f"Clear: Booking Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_port_of_load(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_port_of_load}//input[@type='text']", f"Clear: Port of Load [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_discharge_port(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_discharge_port}//input[@type='text']", f"Clear: Discharge Port [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_destination(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_destination}//input[@type='text']", f"Clear: Destination [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_voyage_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_voyage_number}//input[@type='text']", f"Clear: Voyage Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_equipment_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_number}//input[@type='text']", f"Clear: Equipment Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bill_of_lading_prefix(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bill_of_lading_prefix}//input[@type='text']", f"Clear: Bill of Lading Prefix [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_current_sail_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_from}//input[@type='text']", f"Clear: Current Sail Date (From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_current_sail_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_from}//input[@type='text']", f"Clear: Current Sail Date (To) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_shipper(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_shipper}//input[@type='text']", f"Clear: Shipper [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_consignee(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_consignee}//input[@type='text']", f"Clear: Consignee [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bill_created_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bill_created_date_from}//input[@type='text']", f"Clear: Bill Created Date (From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bill_created_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bill_created_date_to}//input[@type='text']", f"Clear: Bill Created Date (To) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_customer_sent_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_customer_sent_date_from}//input[@type='text']", f"Clear: Customer Sent Date (From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_customer_sent_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_customer_sent_date_to}//input[@type='text']", f"Clear: Customer Sent Date (To) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_equipment_receive_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_from}//input[@type='text']", f"Clear: Equipment Receive Date (From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_equipment_receive_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_from}//input[@type='text']", f"Clear: Equipment Receive Date (To) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_created_by(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_created_by}//input[@type='text']", f"Clear: Created By [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_assigned_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_assigned_to}//input[@type='text']", f"Clear: Assigned To [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_customer_reference_id(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_customer_reference_id}//input[@type='text']", f"Clear:Customer Reference ID [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_account(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_accounts}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Account [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_booking_number(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_booking_number}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Booking Number [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_port_of_load(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_port_of_load}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Port of Load [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_discharge_port(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_discharge_port}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Discharge Port [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_destination(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_destination}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Destination [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_voyage_prefix(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_voyage_prefix}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Voyage Prefix [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_voyage_number(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_voyage_number}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Voyage Number [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_equipment_number(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_equipment_number}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Equipment Number [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_shipper(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_shipper}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Shipper [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_consignee(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_consignee}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Consignee [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_created_by(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_created_by}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Created By [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_created_assigned_to(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_assigned_to}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Assigned To [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_cargo_type(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_assigned_to}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Cargo Type [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_equipment_type(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_equipment_type}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Equipment Type [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_bol_source(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_bol_source}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: BOL Source [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
