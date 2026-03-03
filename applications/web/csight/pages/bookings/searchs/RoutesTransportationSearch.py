from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('RoutesTransportationSearch')


class RoutesTransportationSearch(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the RoutesTransportationSearch instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # String Base XPaths
        self._xpath_voyage_prefix = "//label[contains(text(),'Voyage Prefix')]/.."
        self._xpath_voyage_number = "//label[contains(text(),'Voyage Number')]/.."
        self._xpath_current_sail_date_from = "//label[contains(text(),'Current Sail Date (From)')]/.."
        self._xpath_current_sail_date_to = "//label[contains(text(),'Current Sail Date (To)')]/.."
        self._xpath_origin_movement_type = "//label[contains(text(),'Origin Movement Type')]/.."
        self._xpath_destination_movement_type = "//label[contains(text(),'Destination Movement Type')]/.."
        self._xpath_origin = "//label[text()='Origin']/.."
        self._xpath_port_of_loading = "//label[contains(text(),'Port of Loading')]/.."
        self._xpath_transportation_mode_origin = "//label[contains(text(),'Transportation Mode Origin')]/.."
        self._xpath_port_of_discharge = "//label[contains(text(),'Port of Discharge')]/.."
        self._xpath_final_destination = "//label[contains(text(),'Final Destination')]/.."
        self._xpath_transportation_mode_destination = "//label[contains(text(),'Transportation Mode Destination')]/.."
        self._xpath_direction = "//label[text()='Direction']/.."

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
        self.toggle_accordion().set_locator_with_label('Routes / Transportation').open()
        return self

    def close(self):
        self.toggle_accordion().set_locator_with_label('Routes / Transportation').close()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_multiple_voyage_prefix(self, search: str, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_voyage_prefix}//input[@type='text']/..",
                         f"Search: Voyage Prefix [{search}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_voyage_prefix}//span[contains(@class,'checkbox')]//span/label/span[text()='{search}']/..",
                         f"Search Checkbox List: Voyage Prefix [{search}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def enter_voyage_number(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_voyage_number}//input[@type='text']",
                         f"Search: Voyage Number [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def enter_current_sail_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_from}//input[@type='text']",
                         f"Search: Current Sail Date (From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_current_sail_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input: Format Date 'Apr 17, 2025'
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_to}//input[@type='text']",
                         f"Search: Current Sail Date (To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_origin_movement_type(self, option):
        locator_select = (By.XPATH, f"{self._xpath_origin_movement_type}//select",
                          f"Search: Origin Movement Type [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_destination_movement_type(self, option):
        locator_select = (By.XPATH, f"{self._xpath_destination_movement_type}//select",
                          f"Search: Destination Movement Type [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_origin(self, search: str, pause=1):
        locator_input = (By.XPATH, f"{self._xpath_origin }//input[@type='search']",
                         f"Search: Origin [{search}][Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        locator_list = (By.XPATH, f"//div[@id='lookup']//span[@class='location-name'][text()='{search}']",
                        f"Search: Origin [{search}][Select]")
        self.click().set_locator(locator_list).single_click()
        return self

    def enter_port_of_loading(self, location_name: str = "", location_code: str = "", pause=1):
        # Use a 'Location Name' or 'Location Code'
        search = None
        locator_item = None
        xpath = f"{self._xpath_port_of_loading}//input[@type='search']"

        if location_name is not "":
            search = location_name
            locator_item = (By.XPATH, f"//div[@id='lookup']//span[@class='location-name'][contains(text(),'{search}')]",
                            f"Search: Port of Loading [{search}][Select]")

        if location_code is not "":
            search = location_code
            locator_item = (By.XPATH, f"//div[@id='lookup']//span[@class='location-code'][contains(text(),'{search}')]",
                            f"Search: Port of Loading [{search}][Select]")

        if search is not None and locator_item is not None:
            # Enter Search Criteria
            locator_input = (By.XPATH, xpath, f"Search: Port of Loading [{search}][Input]")
            self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
            # Click on Item Type with Search Text
            self.click().set_locator(locator_item).single_click()

        return self

    def select_transportation_mode_origin(self, option):
        locator_select = (By.XPATH, f"{self._xpath_transportation_mode_origin}//select",
                          f"Search: Transportation Mode Origin [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_port_of_discharge(self, location_name: str = "", location_code: str = "", pause=1):
        # Use a 'Location Name' or 'Location Code'
        search = None
        locator_item = None
        xpath = f"{self._xpath_port_of_discharge}//input[@type='search']"

        if location_name is not "":
            search = location_name
            locator_item = (By.XPATH, f"//div[@id='lookup']//span[@class='location-name'][contains(text(),'{search}')]",
                            f"Search: Port of Discharge [{search}][Select]")

        if location_code is not "":
            search = location_code
            locator_item = (By.XPATH, f"//div[@id='lookup']//span[@class='location-code'][contains(text(),'{search}')]",
                            f"Search: Port of Discharge [{search}][Select]")

        if search is not None and locator_item is not None:
            # Enter Search Criteria
            locator_input = (By.XPATH, xpath, f"Search: Port of Loading [{search}][Input]")
            self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
            # Click on Item Type with Search Text
            self.click().set_locator(locator_item).single_click()

        return self

    def enter_final_destination(self, search: str, pause=1):
        locator_input = (By.XPATH, f"{self._xpath_final_destination}//input[@type='search']",
                         f"Search: Final Destination [{search}][Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        locator_list = (By.XPATH, f"//div[@id='lookup']//span[@class='location-name'][text()='{search}']",
                        f"Search: Final Destination [{search}][Select]")
        self.click().set_locator(locator_list).single_click()
        return self

    def select_transportation_mode_destination(self, option):
        locator_select = (By.XPATH, f"{self._xpath_transportation_mode_destination}//select",
                          f"Search: Transportation Mode Destination [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_radio_direction(self, direction_type):
        locator_item = None

        match direction_type:
            case "N":
                locator_item = (By.XPATH, f"{self._xpath_direction}//span[text()='N']", f"Search: Direction [N][{direction_type}][Input]")
            case "S":
                locator_item = (By.XPATH, f"{self._xpath_direction}//span[text()='S']", f"Search: Direction [S][{direction_type}][Input]")
            case _:
                logger.warning(f"Direction Type not found [{direction_type}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_voyage_number(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_voyage_number}//input[@type='text']", f"Clear: Voyage Number  Clear [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_current_sail_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_from}//input[@type='text']", f"Clear: Current Sail Date (From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_current_sail_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_current_sail_date_to}//input[@type='text']", f"Clear: Current Sail Date (To) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_origin(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_origin}//i[@class='clear-field']", f"Clear: Origin [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def clear_port_of_loading(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_port_of_loading}//i[@class='clear-field']", f"Clear: Port of Loading [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def clear_port_of_discharge(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_port_of_discharge}//i[@class='clear-field']", f"Clear: Port of Discharge [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    def clear_final_destination(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_final_destination}//i[@class='clear-field']", f"Clear: Final Destination [Icon]")
        self.click().set_locator(locator_input).single_click().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_voyage_prefix(self, search, pause=0):
        locator_pill = (By.XPATH, f"{self._xpath_voyage_prefix}//span[contains(@class,'pill')]//span[text()='{search}']/..//button", f"Pill: Voyage Prefix [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
