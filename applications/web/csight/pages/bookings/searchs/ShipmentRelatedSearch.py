from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('ShipmentRelatedSearch')


class ShipmentRelatedSearch(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the ShipmentRelatedSearch instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # String Base XPaths
        self._xpath_booking_sources = "//label[contains(text(),'Booking Sources')]/.."
        self._xpath_shipment_id_number = "//label[contains(text(),'Shipment Id Number')]/.."
        self._xpath_booked_date_from = "//label[contains(text(),'Booked Date(From)')]/.."
        self._xpath_booked_date_to = "//label[contains(text(),'Booked Date(To)')]/.."
        self._xpath_booking_created_category = "//label[contains(text(),'Booking Created Category')]/.."
        self._xpath_booking_created_by_user = "//label[contains(text(),'Booking Created By User')]/.."
        self._xpath_booking_assigned_to_user = "//label[text()='Booking Assigned to User']/.."
        self._xpath_booking_rolled = "//label[text()='Booking Rolled]/.."
        self._xpath_roll_over_reason = "//label[contains(text(),'Roll Over Reason')]/.."
        self._xpath_booking_status = "//label[contains(text(),'Booking Status')]/.."
        self._xpath_cancel_reason = "//label[contains(text(),'Cancel Reason')]/.."
        self._xpath_eei_required = "//label[text()='EEI Required']/.."
        self._xpath_shipment_type = "//label[text()='Shipment Type']/.."
        self._xpath_reference_numbers = "//label[contains(text(),'Reference Numbers')]/.."
        self._xpath_load_list_status = "//label[contains(text(),'Load List Status')]/.."
        self._xpath_payment_terms = "//label[contains(text(),'Payment Terms')]/.."

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
        self.toggle_accordion().set_locator_with_label('Shipment Related').open()
        return self

    def close(self):
        self.toggle_accordion().set_locator_with_label('Shipment Related').close()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_booking_sources(self, option):
        locator_select = (By.XPATH, f"{self._xpath_booking_sources}//select",
                          f"Search: Booking Sources [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def enter_shipment_id_number(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_shipment_id_number}//input[@type='text']", f"Search: Shipment Id Number [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def enter_booked_date_from(self, date: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_booked_date_from}//input[@type='text']",
                         f"Search: Booked Date(From) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def enter_booked_date_to(self, date: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_booked_date_to}//input[@type='text']",
                         f"Search: Booked Date(To) [{date}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(date).pause(pause)
        return self

    def select_booking_created_category(self, option):
        locator_select = (By.XPATH, f"{self._xpath_booking_created_category}//select",
                          f"Search: Booking Created Category [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_booking_created_by_user(self, search: str, pause=1):
        locator_input = (By.XPATH, f"{self._xpath_booking_created_by_user}//input[@type='search']",
                         f"Search: Booking Created By User [{search}][Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        locator_list = (By.XPATH, f"//div[@id='lookup']//span[text()='{search}']",
                        f"Search: Booking Created By User [{search}][Select]")
        self.click().set_locator(locator_list).single_click()
        return self

    def select_booking_assigned_by_user(self, search: str, pause=1):
        locator_input = (By.XPATH, f"{self._xpath_booking_assigned_to_user}//input[@type='search']",
                         f"Search: Booking Assigned to User [{search}][Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        locator_list = (By.XPATH, f"//div[@id='lookup']//span[text()='{search}']",
                        f"Search: Booking Assigned to User [{search}][Select]")
        self.click().set_locator(locator_list).single_click()
        return self

    def select_radio_booked_in_rolled(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_booking_rolled}//span[text()='Yes']", f"Search: Booking Rolled [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_booking_rolled}//span[text()='No']", f"Search: Booking Rolled [No][{value}][Input]")
            case _:
                logger.warning(f"In Bond Indicator not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_multiple_roll_over_reason(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_roll_over_reason}//input[@type='text']/..",
                         f"Search: Container Type [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_roll_over_reason}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_option_list}\"]/..",
                         f"Search Checkbox List: Roll Over Reason [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_cancel_reason(self, search_text, search_option_list, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_cancel_reason}//input[@type='text']/..",
                         f"Search: Cancel Reason [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_roll_over_reason}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_option_list}\"]/..",
                         f"Search Checkbox List: Cancel Reason [{search_option_list}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_roll_booking_status(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_booking_status}//input[@type='text']/..",
                         f"Search: Booking Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_booking_status}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: Booking Status [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_radio_eei_required(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_eei_required}//span[text()='Yes']", f"Search: EEI Required[Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_eei_required}//span[text()='No']", f"Search: EEI Required [No][{value}][Input]")
            case _:
                logger.warning(f"EEI Required not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_shipment_type(self, value):
        locator_item = None

        match value:
            case "FCL":
                locator_item = (By.XPATH, f"{self._xpath_shipment_type}//span[text()='Yes']", f"Search: Shipment Type [Yes][{value}][Input]")
            case "LCL":
                locator_item = (By.XPATH, f"{self._xpath_shipment_type}", f"Search: Shipment Type [No][{value}][Input]")
            case _:
                logger.warning(f"Shipment Type Assigned not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def enter_reference_numbers(self, search: str, pause=1):
        # First Enter Text on Search Input
        locator_input = (By.XPATH, f"{self._xpath_reference_numbers}//input[@type='text']", f"Search: Reference Numbers [{search}] [Input]")
        self.send_keys().set_locator(locator_input, self._name).set_text(search).pause(pause)
        return self

    def select_multiple_load_list_status(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_load_list_status}//input[@type='text']/..",
                         f"Search: Load List Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_load_list_status}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: Load List Status[{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_payment_terms(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_payment_terms}//input[@type='text']/..",
                         f"Search: Load List Status [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_payment_terms}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: Load List Status[{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    # Search Clear Icon ------------------------------------------------------------------------------------------------
    def clear_vin_shipment_id(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_shipment_id_number}//input[@type='text']", f"Clear: VIN / Shipment Id Number [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_booked_date_from(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_booked_date_from}//input[@type='text']", f"Clear: Booked Date(From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_booked_date_to(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_booked_date_to}//input[@type='text']", f"Clear: Booked Date(From) [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_booking_created_by_user(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_booking_created_by_user}//input[@type='text']", f"Clear: Booking Created By User [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_booking_assigned_by_user(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_booking_assigned_to_user}//input[@type='text']", f"Clear: Booking Assigned to User [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_roll_over_reason(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_roll_over_reason}//input[@type='text']", f"Clear: Roll Over Reason [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    def clear_reference_numbers(self, pause=0):
        locator_input = (By.XPATH, f"{self._xpath_reference_numbers}//input[@type='text']", f"Clear: Reference Numbers [Icon]")
        self.send_keys().set_locator(locator_input).clear().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_roll_over_reason(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_roll_over_reason}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Roll Over Reason [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_booking_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_booking_status}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Booking Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_cancel_reason(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_cancel_reason}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Cancel Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_load_list_status(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_load_list_status}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Load List Status [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
