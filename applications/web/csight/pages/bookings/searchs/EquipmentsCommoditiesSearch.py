from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('EquipmentsCommoditiesSearch')


class EquipmentsCommoditiesSearch(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the EquipmentsCommoditiesSearch instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # String Base XPaths
        self._xpath_container_type = "//label[contains(text(),'Container Type')]/.."
        self._xpath_cargo_type = "//label[contains(text(),'Cargo Type')]/.."
        self._xpath_vin_serial_number = "//label[contains(text(),'VIN / Serial Number')]/.."
        self._xpath_commodity = "//label[contains(text(),'Commodity')]/.."
        self._xpath_equipment_number = "//label[contains(text(),'Equipment Number')]/.."
        self._xpath_equipment_receive_date_from = "//label[contains(text(),'Equipment Receive Date (From)')]/.."
        self._xpath_equipment_receive_date_to = "//label[contains(text(),'Equipment Receive Date (To)')]/.."
        self._xpath_in_bond_indicator = "//label[text()='In Bond Indicator']/.."
        self._xpath_cargo_received = "//label[text()='Cargo Received']/.."
        self._xpath_seal_number = "//label[text()='Equipment Assigned']/.."
        self._xpath_equipment_assigned = "//label[text()='Equipment Assigned']/.."
        self._xpath_shipper_owned = "//label[text()='Shipper Owned']/.."

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
        self.toggle_accordion().set_locator_with_label('Equipments / Commodities').open()
        return self

    def close(self):
        self.toggle_accordion().set_locator_with_label('Equipments / Commodities').close()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_multiple_container_type(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_container_type}//input[@type='text']/..",
                         f"Search: Container Type [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_container_type}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search}\"]/..",
                         f"Search Checkbox List: Container Type [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_cargo_type(self, option):
        locator_select = (By.XPATH, f"{self._xpath_cargo_type}//select",
                          f"Search: Cargo Type [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_vin_serial_number(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_vin_serial_number}//input[@type='text']", f"Search: VIN / Serial Number [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def select_commodity(self, option):
        locator_select = (By.XPATH, f"{self._xpath_commodity}//select",
                          f"Search: Commodity [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
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

    def enter_equipment_receive_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_from}//input[@type='text']",
                         f"Search: Equipment Receive Date (From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_equipment_receive_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_to}//input[@type='text']",
                         f"Search: Equipment Receive Date (To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
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

    def select_radio_seal_number(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_seal_number}//span[text()='Yes']", f"Search: Seal Number [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_seal_number}//span[text()='No']", f"Search: Seal Number [No][{value}][Input]")
            case _:
                logger.warning(f"Seal Number not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_equipment_assigned(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_equipment_assigned}//span[text()='Yes']", f"Search: Equipment Assigned [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_equipment_assigned}//span[text()='No']", f"Search: Equipment Assigned [No][{value}][Input]")
            case _:
                logger.warning(f"Equipment Assigned not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_shipped_owned(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_shipper_owned}//span[text()='Yes']", f"Search: Shipper Owned [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_shipper_owned}//span[text()='No']", f"Search: Shipper Owned [No][{value}][Input]")
            case _:
                logger.warning(f"Equipment Assigned not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_vin_number_serial_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_vin_serial_number}//input[@type='text']", f"Clear: VIN / Serial Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_equipment_receive_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_from}//input[@type='text']", f"Clear: Equipment Receive Date (From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_equipment_receive_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_receive_date_to}//input[@type='text']", f"Clear: Equipment Receive Date (To) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_container_type(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_container_type}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Container Type [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
