from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SearchPanel')


class SearchPanel(BasePage):

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
        self.relative = "Employees/s/equipmentinventory"
        # String Base XPaths
        self._xpath_country = "//label[contains(text(),'Country')]/.."
        self._xpath_sublocation_type = "//label[contains(text(),'Sublocation Type')]/.."
        self._xpath_sublocation = "(//label[text()='Sublocation']/..)[1]"
        self._xpath_next_location = "//label[contains(text(),'Next Location')]/.."
        self._xpath_full_empty = "//label[contains(text(),'Full / Empty')]/.."
        self._xpath_inventory_status = "//label[contains(text(),'Inventory Status')]/.."
        self._xpath_latest_movement = "//label[contains(text(),'Latest Movement')]/.."
        self._xpath_equipment_size_type = "//label[contains(text(),'Equipment Size / Type')]/.."
        self._xpath_equipment_ownership = "//label[contains(text(),'Equipment Ownership')]/.."
        self._xpath_direction = "//label[contains(text(),'Direction')]/.."
        self._xpath_assigned = "//label[contains(text(),'Assigned')]/.."
        self._xpath_attached_container = "//label[contains(text(),'Attached Container')]/.."
        self._xpath_attached_chassis = "//label[contains(text(),'Attached Chassis')]/.."
        self._xpath_attached_genset_nose_mounted = "//label[contains(text(),'Attached Genset Nose-Mounted')]/.."
        self._xpath_attached_genset_underslung = "//label[contains(text(),'Attached Genset Underslung')]/.."
        self._xpath_special_status = "//label[contains(text(),'Special Status')]/.."
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
    def enter_country(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_country}//input[@type='text']", f"Search: Country [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_sublocation_type(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_sublocation_type}//div[contains(@class,'_click')]//button", f"Search: Sublocation Type [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_sublocation_type}//div[@role='listbox']//span[text()='{search}']", f"Search List: Sublocation Type [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_sublocation(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_sublocation}//input[@type='text']", f"Search: Sublocation [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Enter Text
        self.send_keys().set_locator(locator_input).set_text(search_text)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_sublocation}//div[@role='listbox']//span[contains(@class, '-checkbox')]/label/span[text()='{search_option_list}']",
                         f"Search Checkbox List: Sublocation [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_next_location(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_next_location}//input[@type='text']", f"Search: Next Location [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Enter Text
        self.send_keys().set_locator(locator_input).set_text(search_text)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_next_location}//div[@role='listbox']//span[contains(@class, '-checkbox')]/label/span[text()='{search_option_list}']",
                         f"Search Checkbox List: Location [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_full_empty(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_full_empty}//div[contains(@class,'_click')]//button", f"Search: Full / Empty [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_full_empty}//div[@role='listbox']//span[text()='{search}']", f"Search List: Full / Empty [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_inventory_status(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_inventory_status}//input[@type='text']", f"Search: Inventory Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Enter Text
        self.send_keys().set_locator(locator_input).set_text(search_text)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_next_location}//div[@role='listbox']//span[contains(@class, '-checkbox')]/label/span[text()='{search_option_list}']",
                         f"Search Checkbox List: Inventory Status [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_latest_movement(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_latest_movement}//input[@type='text']", f"Search: Latest Movement [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Enter Text
        self.send_keys().set_locator(locator_input).set_text(search_text)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_latest_movement}//div[@role='listbox']//span[contains(@class, '-checkbox')]/label/span[text()='{search_option_list}']",
                         f"Search Checkbox List: Latest Movement [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_equipment_size_type(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_equipment_size_type}//input[@type='text']", f"Search: Equipment Size / Type [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Enter Text
        self.send_keys().set_locator(locator_input).set_text(search_text)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_equipment_size_type}//div[@role='listbox']//span[contains(@class, '-checkbox')]/label/span[text()='{search_option_list}']",
                         f"Search Checkbox List: Equipment Size / Type [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_equipment_ownership(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_equipment_ownership}//div[contains(@class,'_click')]//button", f"Search: Equipment Ownership [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_equipment_ownership}//div[@role='listbox']//span[text()='{search}']", f"Search List: Equipment Ownership [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_direction(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_direction}//div[contains(@class,'_click')]//button", f"Search: Direction [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_direction}//div[@role='listbox']//span[text()='{search}']", f"Search List: Direction [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_assigned(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_assigned}//div[contains(@class,'_click')]//button", f"Search: Assigned [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_assigned}//div[@role='listbox']//span[text()='{search}']", f"Search List: Assigned [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return

    def select_attached_container(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_attached_container}//div[contains(@class,'_click')]//button", f"Search: Attached Container [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_attached_container}//div[@role='listbox']//span[text()='{search}']", f"Search List: Attached Container [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_attached_chassis(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_attached_chassis}//div[contains(@class,'_click')]//button", f"Search: Attached Chassis [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_attached_chassis}//div[@role='listbox']//span[text()='{search}']", f"Search List: Attached Chassis [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_attached_genset_nose_mounted(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_attached_genset_nose_mounted}//div[contains(@class,'_click')]//button", f"Search: Attached Genset Nose-Mounted [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_attached_genset_nose_mounted}//div[@role='listbox']//span[text()='{search}']", f"Search List: Attached Genset Nose-Mounted [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_attached_genset_underslung(self, search, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_attached_genset_underslung}//div[contains(@class,'_click')]//button", f"Search: Attached Genset Underslung [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH, f"{self._xpath_attached_genset_underslung}//div[@role='listbox']//span[text()='{search}']", f"Search List: Attached Genset Underslung [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_special_status(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_special_status}//input[@type='text']", f"Search: Special Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Enter Text
        self.send_keys().set_locator(locator_input).set_text(search_text)
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_special_status}//div[@role='listbox']//span[contains(@class, '-checkbox')]/label/span[text()='{search_option_list}']",
                         f"Search Checkbox List: Special Status [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_country(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_country}//input[@type='text']", f"Clear: Country [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_sublocation(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_sublocation}//input[@type='text']", f"Clear: Sublocation [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_next_location(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_next_location}//input[@type='text']", f"Clear: Next location [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_latest_movement(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_latest_movement}//input[@type='text']", f"Clear: Latest Movement [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_equipment_size_type(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_equipment_size_type}//input[@type='text']", f"Clear: Equipment Type Size [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_special_status(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_special_status}//input[@type='text']", f"Clear: Special Status [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_sublocation(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_sublocation}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Sublocation [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return

    def pill_remove_next_location(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_next_location}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Next Location [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return

    def pill_remove_inventory_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_inventory_status}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Inventory Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return

    def pill_remove_latest_movement(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_latest_movement}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Latest Movement [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return

    def pill_remove_equipment_size_type(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_equipment_size_type}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Equipment Size Type [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)

    def pill_remove_special_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_equipment_size_type}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Special Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
