from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
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
        self.relative = "Employees/s/cargoreleasetracking"
        # String Base XPaths
        self._xpath_equipment_id_vin_dock_receipt_no = "//label[contains(text(),'Equip ID / VIN / Dock receipt No.')]/.."
        self._xpath_booking_number = "//label[contains(text(),'Booking Number')]/.."
        self._xpath_bol_number = "//label[contains(text(),'BOL Number')]/.."
        self._xpath_release_location = "//label[contains(text(),'Release Location')]/.."
        self._xpath_customs_clearance_location = "//label[contains(text(),'Customs Clearance Location')]/.."
        self._xpath_voyage_number = "//label[contains(text(),'Voyage Number')]/.."
        self._xpath_place_of_delivery = "//label[contains(text(),'Place of Delivery')]/.."
        self._xpath_port_of_load = "//label[contains(text(),'Port Of Load')]/.."
        self._xpath_port_of_discharge = "//label[contains(text(),'Port Of Discharge')]/.."
        self._xpath_account_name = "//label[contains(text(),'Account Name')]/.."
        self._xpath_container_type = "//label[contains(text(),'Container Type')]/.."
        self._xpath_cargo_type = "//label[contains(text(),'Cargo Type')]/.."
        self._xpath_commodity = "//label[contains(text(),'Commodity')]/.."

        self._xpath_in_bond = "//label[contains(text(),'InBond')]/.."
        self._xpath_bol_cargo_released = "//label[contains(text(),'BOL Cargo Released')]/.."
        self._xpath_user_hold = "//label[contains(text(),'User Hold')]/.."
        self._xpath_credit_hold = "//label[contains(text(),'Credit Hold')]/.."
        self._xpath_agriculture_reg_hold = "//label[contains(text(),'Agriculture Reg. Hold')]/.."
        self._xpath_customs_hold = "//label[contains(text(),'Customs Hold')]/.."
        self._xpath_x_ray_hold = "//label[contains(text(),'X Ray Hold')]/.."
        self._xpath_fumigation_hold = "//label[contains(text(),'Fumigation Hold')]/.."
        self._xpath_delivery_instructions_received = "//label[contains(text(),'Delivery Instructions Received')]/.."
        self._xpath_cleared_for_release = "//label[contains(text(),'Cleared for Release')]/.."
        self._xpath_bol_surrendered = "//label[contains(text(),'BOL Surrendered')]/.."
        self._xpath_duties_paid = "//label[contains(text(),'Duties Paid')]/.."
        self._xpath_arrival_at_release_location = "//label[contains(text(),'Arrival at Release location')]/.."
        self._xpath_trucker_assigned = "//label[contains(text(),'Trucker Assigned')]/.."
        self._xpath_customs_cleared = "//label[contains(text(),'Customs Cleared')]/.."
        self._xpath_finance_cleared = "//label[contains(text(),'Finances Cleared')]/.."
        self._xpath_departed_release_location = "//label[contains(text(),'Departed Release Location')]/.."
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

    # Search Fields ----------------------------------------------------------------------------------------------------
    def enter_equipment_id_vin_dock_receipt_no(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_equipment_id_vin_dock_receipt_no}//input[@type='text']", f"Search: Equip ID / VIN / Dock receipt No. [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_booking_number(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_booking_number}//input[@type='text']/..", f"Search: Booking Number [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_booking_number}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Booking Number [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_bol_number(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_bol_number}//input[@type='text']/..", f"Search: BOL Number [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_bol_number}//ul[@role='listbox']//span[text()='{search}']", f"Search List: BOL Number [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_release_location(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_release_location}//input[@type='text']/..", f"Search: Release Location [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_release_location}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Release Location [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_customs_clearance_location(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_release_location}//input[@type='text']/..", f"Search: Customs Clearance Location [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_release_location}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Customs Clearance Location [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_voyage_number(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_voyage_number}//input[@type='text']/..", f"Search: Voyage Number [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_voyage_number}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Voyage Number [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_place_of_delivery(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_place_of_delivery}//input[@type='text']/..", f"Search: Place of Delivery [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_place_of_delivery}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Place of Delivery [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_port_of_load(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_port_of_load}//input[@type='text']/..", f"Search: Port Of Load [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_port_of_load}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Port Of Load [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_port_of_discharge(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_port_of_discharge}//input[@type='text']/..", f"Search: Port Of Discharge [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_port_of_discharge}//ul[@role='listbox']//span[text()='{search}']", f"Search List: Port Of Discharge [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

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

    def select_commodity(self, option):
        locator_select = (By.XPATH, f"{self._xpath_commodity}//select", f"Search: Commodity [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_radio_in_bod(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_in_bond}//span[text()='Yes']", f"Search: In Bond [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_in_bond}//span[text()='No']", f"Search: In Bond[No][{value}][Input]")
            case _:
                logger.warning(f"In Bond not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_bol_cargo_released(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_cargo_released}//span[text()='Yes']", f"Search: BOL Cargo Released [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_cargo_released}//span[text()='No']", f"Search: BOL Cargo Released [No][{value}][Input]")
            case _:
                logger.warning(f"BOL Cargo Released not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_user_hold(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_user_hold}//span[text()='Yes']", f"Search: User Hold [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_user_hold}//span[text()='No']", f"Search: User Hold [No][{value}][Input]")
            case _:
                logger.warning(f"User Hold not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_credit_hold(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_credit_hold}//span[text()='Yes']", f"Search: Credit Hold [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_credit_hold}//span[text()='No']", f"Search: Credit Hold [No][{value}][Input]")
            case _:
                logger.warning(f"Credit Hold not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_agriculture_reg_hold(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_agriculture_reg_hold}//span[text()='Yes']", f"Search: Agriculture Reg. Hold [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_agriculture_reg_hold}//span[text()='No']", f"Search: Agriculture Reg. Hold [No][{value}][Input]")
            case _:
                logger.warning(f"Agriculture Reg. Hold not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_customs_hold(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_customs_hold}//span[text()='Yes']", f"Search: Customs Hold [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_customs_hold}//span[text()='No']", f"Search: Customs Hold [No][{value}][Input]")
            case _:
                logger.warning(f"Customs Hold not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_x_ray_hold(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_x_ray_hold}//span[text()='Yes']", f"Search: X Ray Hold [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_x_ray_hold}//span[text()='No']", f"Search: X Ray Hold [No][{value}][Input]")
            case _:
                logger.warning(f"X Ray Hold not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_fumigation_hold(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_fumigation_hold}//span[text()='Yes']", f"Search: Fumigation Hold [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_fumigation_hold}//span[text()='No']", f"Search: Fumigation Hold [No][{value}][Input]")
            case _:
                logger.warning(f"Fumigation Hold not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_delivery_instructions_received(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_delivery_instructions_received}//span[text()='Yes']", f"Search: Delivery Instructions Received [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_delivery_instructions_received}//span[text()='No']", f"Search: Delivery Instructions Received [No][{value}][Input]")
            case _:
                logger.warning(f"Delivery Instructions Received not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_cleared_for_release(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_cleared_for_release}//span[text()='Yes']", f"Search: Cleared for Release [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_cleared_for_release}//span[text()='No']", f"Search: Cleared for Release [No][{value}][Input]")
            case _:
                logger.warning(f"Cleared for Release not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_bol_surrendered(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_bol_surrendered}//span[text()='Yes']", f"Search: BOL Surrendered [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_bol_surrendered}//span[text()='No']", f"Search: BOL Surrendered [No][{value}][Input]")
            case _:
                logger.warning(f"BOL Surrendered not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_duties_paid(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_duties_paid}//span[text()='Yes']", f"Search: Duties Paid [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_duties_paid}//span[text()='No']", f"Search: Duties Paid [No][{value}][Input]")
            case _:
                logger.warning(f"Duties Paid not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_arrival_at_release_location(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_arrival_at_release_location}//span[text()='Yes']", f"Search: Arrival at Release location [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_arrival_at_release_location}//span[text()='No']", f"Search: Arrival at Release location [No][{value}][Input]")
            case _:
                logger.warning(f"Arrival at Release location not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_trucker_assigned(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_trucker_assigned}//span[text()='Yes']", f"Search: Trucker Assigned [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_trucker_assigned}//span[text()='No']", f"Search: Trucker Assigned [No][{value}][Input]")
            case _:
                logger.warning(f"Trucker Assigned not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_customs_cleared(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_customs_cleared}//span[text()='Yes']", f"Search: Customs Cleared [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_customs_cleared}//span[text()='No']", f"Search: Customs Cleared  [No][{value}][Input]")
            case _:
                logger.warning(f"Customs Cleared not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_finance_cleared(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_finance_cleared}//span[text()='Yes']", f"Search: Finances Cleared [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_finance_cleared}//span[text()='No']", f"Search: Finances Cleared  [No][{value}][Input]")
            case _:
                logger.warning(f"Finances Cleared not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_departed_release_location(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_departed_release_location}//span[text()='Yes']", f"Search: Departed Release Location [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_departed_release_location}//span[text()='No']", f"Search: Departed Release Location [No][{value}][Input]")
            case _:
                logger.warning(f"Finances Cleared not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_equipment_id_vin_dock_receipt_no(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_id_vin_dock_receipt_no}//input[@type='text']", f"Clear: Equip ID / VIN / Dock receipt No. Clear [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_booking_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_booking_number}//input[@type='text']", f"Clear: Booking Number Clear [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_bol_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_bol_number}//input[@type='text']", f"Clear: BOL Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_release_location(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_release_location}//input[@type='text']", f"Clear: Release Location [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_customs_clearance_location(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_customs_clearance_location}//input[@type='text']", f"Clear: Customs Clearance Location [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_voyage_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_voyage_number}//input[@type='text']", f"Clear: Voyage Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_place_of_delivery(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_place_of_delivery}//input[@type='text']", f"Clear: Place of Delivery [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_port_of_load(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_port_of_load}//input[@type='text']", f"Clear: Port Of Load [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_port_of_discharge(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_port_of_discharge}//input[@type='text']", f"Clear: Port Of Discharge [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_account_name(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_account_name}//input[@type='text']", f"Clear: Account Name [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_container_type(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_container_type}//input[@type='text']", f"Clear: Container Type [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_cargo_type(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_cargo_type}//span[contains(@class,'pill')][text()='{search}']/..//button",
                        f"Pill: Cargo Type [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_commodity(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_commodity}//span[contains(@class,'pill')][text()='{search}']/..//button",
                        f"Pill: Commodity [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
