from enum import Enum

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('DestinationInformationPage')


class DestinationInformationPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the OriginInformationPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/create"
        # Locator definitions
        self._form = "(//div[contains(@class,'destination-info')])"
        # Locators for Location ----------------------------------------------------------------------------------------
        self._input_location_name = (
            By.XPATH, f"{self._form}//label[contains(text(),'Location Name')]/following-sibling::input",
            "Location Name [Input Text]")
        self._input_location_address = (
            By.XPATH, f"{self._form}//label[contains(text(),'Location Address')]/following-sibling::input",
            "Location Address [Input Text]")
        self._input_location_address_line_2 = (
            By.XPATH, f"{self._form}//label[contains(text(),'Address Line 2')]/following-sibling::input",
            "Location Address Line 2 [Input Text]")

        # Locators for Contact -----------------------------------------------------------------------------------------
        self._input_contact_name = (
            By.XPATH, f"{self._form}//label[contains(text(),'Contact Name')]/following-sibling::input",
            "Contact Name [Input Text]")
        self._input_contact_phone = (
            By.XPATH, f"{self._form}//label[contains(text(),'Phone')]/following-sibling::input", "Phone [Input Text]")
        self._input_contact_email = (
            By.XPATH, f"{self._form}//label[contains(text(),'Email')]/following-sibling::input", "Email [Input Text]")

        # Pick Up Appointment ------------------------------------------------------------------------------------------
        self._radio_first_come = (By.XPATH, f"{self._form}//span[contains(text(),'Select Option')]/following-sibling::ul//label/span[contains(text(),'First Come, First Serve')]", "First Come, First Serve [Radio Option]")
        self._radio_pre_scheduled = (By.XPATH, f"{self._form}//span[contains(text(),'Select Option')]/following-sibling::ul//label/span[contains(text(),'Pre-Scheduled')]", "First Come, First Serve [Radio Option]")
        self._radio_first_call_for_appointment = (By.XPATH, f"{self._form}//span[contains(text(),'Select Option')]/following-sibling::ul//label/span[contains(text(),'Call for Appointment')]", "First Come, First Serve [Radio Option]")
        self._input_early_pickup_date = (By.XPATH, "//input[@name='earlyDeliveryDate']", "From Day [Pickup Days Input Box]")  # Only Visible when First Come is Selected
        self._input_late_pickup_date = (By.XPATH, "//input[@name='lateDeliveryDate']", "To Day [Pickup Days Input Box]")  # These are visible on the 3 Radio Options

        # Select Time --------------------------------------------------------------------------------------------------
        # Open Time
        self._input_open_time_hours = (By.XPATH, f"{self._form}//span[contains(text(),'Open Time')]/..//input[@aria-label='Hours']", "Open Time Hours [Input Box]")
        self._input_open_time_minutes = (By.XPATH, f"{self._form}//span[contains(text(),'Open Time')]/..//input[@aria-label='Minutes']", "Open Time Minutes [Input Box]")
        # CHANGE FOR LOGIB-3445
        #self._button_open_time_indicator = (By.XPATH, f"({self._form}//span[contains(text(),'Open Time')]/..//button)[5]", "Open Time AM/PM [Toggle Button]")

        # Close Time
        self._input_close_time_hours = (By.XPATH, f"{self._form}//span[contains(text(),'Close Time')]/..//input[@aria-label='Hours']", "Open Time Hours [Input Box]")
        self._input_close_time_minutes = (By.XPATH, f"{self._form}//span[contains(text(),'Close Time')]/..//input[@aria-label='Minutes']", "Open Time Minutes [Input Box]")
        # CHANGE FOR LOGIB-3445
        #self._button_close_time_indicator = (By.XPATH, f"({self._form}//span[contains(text(),'Close Time')]/..//button)[5]", "Close Time AM/PM [Toggle Button]")

        # Time : Pre-Scheduled
        self._input_time_hours = (By.XPATH, f"{self._form}//input[@aria-label='Hours']", "Time Hours [Input Box]")
        self._input_time_minutes = (By.XPATH, f"{self._form}//input[@aria-label='Minutes']", "Time Minutes [Input Box]")
        #CHANGE FOR LOGIB-3445
        #self._button_time_indicator = (By.XPATH, f"({self._form}//span[contains(text(),'Select Specific Time')]/following-sibling::div//button)[5]", "Close Time AM/PM [Toggle Button]")

        # Open Time Controls
        self._button_open_hours_up = (By.XPATH, f"({self._form}//span[contains(text(),'Open Time')]/..//button)[1]", "Open Time Hours Up Arrow [Button]")
        self._button_open_hours_down = (By.XPATH, f"({self._form}//span[contains(text(),'Open Time')]/..//button)[2]", "Open Time Hours Down Arrow [Button]")
        self._button_open_minutes_up = (By.XPATH, f"({self._form}//span[contains(text(),'Open Time')]/..//button)[3]", "Open Time Minutes Up Arrow [Button]")
        self._button_open_minutes_down = (By.XPATH, f"({self._form}//span[contains(text(),'Open Time')]/..//button)[4]", "Open Time Minutes Down Arrow [Button]")

        # Close Time Controls
        self._button_close_hours_up = (By.XPATH, f"({self._form}//span[contains(text(),'Close Time')]/..//button)[1]", "Close Time Hours Up Arrow [Button]")
        self._button_close_hours_down = (By.XPATH, f"({self._form}//span[contains(text(),'Close Time')]/..//button)[2]", "Close Time Hours Down Arrow [Button]")
        self._button_close_minutes_up = (By.XPATH, f"({self._form}//span[contains(text(),'Close Time')]/..//button)[3]", "Close Time Minutes Up Arrow [Button]")
        self._button_close_minutes_down = (By.XPATH, f"({self._form}//span[contains(text(),'Close Time')]/..//button)[4]", "Close Time Minutes Down Arrow [Button]")

        # Point of Contact
        self._checkbox_use_current_point_of_contact_label = (By.XPATH, "(//span[contains(text(),'Point of Contact')]/..//span)[2]","Use current point of contact [Label]")  # Only Visible on Call for Appointment
        self._input_first_and_last_name = (By.NAME, "destPickupContactName","Contact name [Input Box]")
        self._input_phone = (By.NAME,  "destPickupContactPhone", "Phone [Input Box]")
        self._input_email = (By.NAME, "destPickupContactEmail", "Email [Input Box]")

        # Locator definitions
        self._button_cancel = (By.XPATH, f"{self._form}//button/span[text()='Cancel']", "Cancel [Button]")
        self._button_save_for_later = (By.XPATH, f"{self._form}//button/span[text()='Save For Later']", "Save For Later [Button]")
        self._button_save_and_continue = (By.XPATH, f"{self._form}//button/span[text()='Save & Continue']", "Save & Continue [Button]")

        #Expedite
        self._checkbox_expedite_destination = (By.XPATH, f"{self._form}//*[@id='mat-checkbox-1-input']")
        self._get_text_expedite =  (By.XPATH, f"{self._form}//*[@id='mat-checkbox-1']/label/span[2]")



    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = DestinationInformationPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    # Location Name ----------------------------------------------------------------------------------------------------
    def _enter_location_name(self, text: str):
        self.send_keys().set_locator(self._input_location_name, self._name).clear().set_text(text)
        return self

    def _select_autocomplete_location_name_by_index(self, index: int):
        locator = (By.XPATH, f"({self._form}//*[contains(@class,'dropdown-menu')]//button)[{str(index)}]", "Location Option Index [Dropdown Locations Autocomplete]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _select_autocomplete_location_name_by_location(self, text: str):
        locator = (By.XPATH, f"({self._form}//*[contains(@class,'dropdown-menu')]//button)/div/div[1]/span[contains(text(),'{text}')]", "Location Option Location Name [Dropdown Locations Autocomplete]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _select_autocomplete_location_name_by_address(self, text: str):
        locator = (By.XPATH, f"({self._form}//*[contains(@class,'dropdown-menu')]//button)/div/div[2]/span[contains(text(),'{text}')]", "Location Option Location Address [Dropdown Locations Autocomplete]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _select_autocomplete_location_name_by_contact_email(self, text: str):
        locator = (By.XPATH, f"({self._form}//*[contains(@class,'dropdown-menu')]//button)/div/div[2]/span/span[6][contains(text(), '{text}')]", "Location Option Location Contact Email [Dropdown Locations Autocomplete]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    # Location Address -------------------------------------------------------------------------------------------------
    def _enter_location_address(self, text: str):
        self.send_keys().set_locator(self._input_location_address, self._name).clear().set_text(text)
        return self

    def _select_autocomplete_location_by_address_name(self, text: str):
        locator = (By.XPATH, f"({self._form}//label[contains(text(),'Location Address')]/..//button)[1]//span[contains(text(),'{text}')]", "Location Option Location Address Name [Dropdown Locations Autocomplete]")
        self.click().set_locator(locator, self._name).single_click().pause()
        return self

    def _select_autocomplete_location_by_address_index(self, index: int):
        locator = (By.XPATH, f"({self._form}//label[contains(text(),'Location Address')]/..//button)[{index}]//span", "Location Option Location Address Index [Dropdown Locations Autocomplete]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_address_line_2(self, text: str):
        self.send_keys().set_locator(self._input_location_address_line_2, self._name).set_text_by_character(text)
        return self

    def enter_destination_location(self, name, location, address, address_line_2):
        # Location Name
        self._enter_location_name(name)
        self._select_autocomplete_location_name_by_location(location)
        # Location Address
        #self._enter_location_address(address)
        #self._select_autocomplete_location_by_address_name(address)
        # Address Line 2
        self._enter_address_line_2(address_line_2)
        return self

    # Contact ----------------------------------------------------------------------------------------------------------
    def _enter_contact_name(self, text: str):
        self.send_keys().set_locator(self._input_contact_name, self._name).clear().set_text(text)
        return self

    def _enter_contact_phone(self, text: str):
        self.send_keys().set_locator(self._input_contact_phone, self._name).clear().set_text(text)
        return self

    def _enter_contact_email(self, text: str):
        self.send_keys().set_locator(self._input_contact_email, self._name).clear().set_text(text)
        return self

    def enter_contact(self, name, phone, email):
        self._enter_contact_name(name)
        self._enter_contact_phone(phone)
        self._enter_contact_email(email)
        return self

    # PickUp Appointment -----------------------------------------------------------------------------------------------
    # Select Option - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _click_first_come_first_serve(self):
        self.scroll().set_locator(self._radio_first_come).to_element(600)
        self.click().set_locator(self._radio_first_come, self._name).highlight().single_click()
        return self

    def _click_pre_scheduled(self):
        self.scroll().set_locator(self._radio_pre_scheduled).to_element(600)
        self.click().set_locator(self._radio_pre_scheduled, self._name).highlight().single_click()
        return self

    def _click_call_for_appointment(self):
        self.scroll().set_locator(self._radio_first_call_for_appointment).to_element(600)
        self.click().set_locator(self._radio_first_call_for_appointment, self._name).highlight().single_click()
        return self

    # PickUp Days - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    '''
    Inputs Visibility Depends on Select Option Radio Buttons:
    --------------------------------------------------------------------
    First Come, First Serve: From Days + To Day | Select Time Open + Close
    Pre-Scheduled: To Day | Select Time HH : MM
    Call for Appointment: To Day | Hide Time Options | Use Contact Point
    '''

    def _enter_pickup_day_from_day(self, text):
        self.send_keys().set_locator(self._input_early_pickup_date, self._name).clear().set_text(text)
        return self

    def _enter_pickup_day_to_day(self, text):
        self.send_keys().set_locator(self._input_late_pickup_date, self._name).clear().set_text(text)
        return self

    # Select Time  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _enter_open_time(self, hours: str, minutes: str):

        self.send_keys().set_locator(self._input_open_time_hours, self._name).clear().set_text(str(hours))
        self.send_keys().set_locator(self._input_open_time_minutes, self._name).clear().set_text(str(minutes)).set_text(Keys.TAB)

        '''# CHANGE FOR LOGIB-3445
        # Gets Current Button Text Indicator
        current_indicator = self.get_text().set_locator(self._button_open_time_indicator).by_text().strip()
        
        # Compares Indicator Text
        if current_indicator != indicator:
            # Change Button State
            self.click().set_locator(self._button_open_time_indicator, self._name).single_click()
            # Verify Indicator State Change
            updated_indicator = self.get_text().set_locator(self._button_open_time_indicator).by_text().strip()
            assert updated_indicator == indicator, f"Expected Indicator should be {indicator}, but found {updated_indicator}"
        else:
            logger.info(f"Open Time Indicator state is correct {indicator}")
            
            '''

    def _enter_close_time(self, hours: str, minutes: str):

        self.send_keys().set_locator(self._input_close_time_hours, self._name).clear().set_text(str(hours))
        self.send_keys().set_locator(self._input_close_time_minutes, self._name).clear().set_text(str(minutes)).set_text(Keys.TAB)

        '''# CHANGE FOR LOGIB-3445
        # Gets Current Button Text Indicator
        current_indicator = self.get_text().set_locator(self._button_close_time_indicator).by_text().strip()

        # Compares Indicator Text
        if current_indicator != indicator:
            # Change Button State
            self.click().set_locator(self._button_close_time_indicator, self._name).single_click()
            # Verify Indicator State Change
            updated_indicator = self.get_text().set_locator(self._button_close_time_indicator).by_text().strip()
            assert updated_indicator == indicator, f"Expected Indicator should be {indicator}, but found {updated_indicator}"
        else:
            logger.info(f"Close Time Indicator state is correct {indicator}")
        '''
    def _enter_time(self, hours: str, minutes: str, ):
        self.send_keys().set_locator(self._input_time_hours, self._name).clear().set_text(str(hours))
        self.send_keys().set_locator(self._input_time_minutes, self._name).clear().set_text(str(minutes)).set_text(Keys.TAB)

        '''# CHANGE FOR LOGIB-3445
        # Gets Current Button Text Indicator
        current_indicator = self.get_text().set_locator(self._button_time_indicator).by_text().strip()

        # Compares Indicator Text
        if current_indicator != indicator:
            # Change Button State
            self.click().set_locator(self._button_time_indicator, self._name).single_click()
            # Verify Indicator State Change
            updated_indicator = self.get_text().set_locator(self._button_time_indicator).by_text().strip()
            assert updated_indicator == indicator, f"Expected Indicator should be {indicator}, but found {updated_indicator}"
        else:
            logger.info(f"Close Time Indicator state is correct {indicator}")
            
        '''

    def _click_checkbox_use_current_point_of_contact(self, value: bool):
        # Verify CheckBox Current Value
        self.scroll().set_locator(self._checkbox_use_current_point_of_contact_label).to_element(pixels=600)
        element_value = self.driver.find_element(By.XPATH, "//span[contains(text(),'Point of Contact')]/..//input").get_attribute("ng-reflect-model")
        if bool(element_value) != value:
            self.click().set_locator(self._checkbox_use_current_point_of_contact_label, self._name).single_click()

        return self

    def enter_point_contact(self, name, phone, email):
        self.send_keys().set_locator(self._input_first_and_last_name, self._name).clear().set_text(name)
        self.send_keys().set_locator(self._input_phone, self._name).clear().set_text(phone)
        self.send_keys().set_locator(self._input_email, self._name).clear().set_text(email)
        return self

    def enter_pickup_appointment_first_come_first_serve(self,
                                                        from_day: str, to_day: str,
                                                        open_hours: str, open_minutes: str,
                                                        close_hours: str, close_minutes: str):
        # Click Radio Button
        self._click_first_come_first_serve()
        # Enter Days Range
        self._enter_pickup_day_from_day(from_day)
        self._enter_pickup_day_to_day(to_day)
        # Select Time
        self._enter_open_time(open_hours, open_minutes)
        self._enter_close_time(close_hours, close_minutes)
        return self

    def enter_pickup_appointment_pre_scheduled(self, from_day: str, hours: str, minutes: str):
        # Click Radio Button
        self._click_pre_scheduled()
        # Enter Day
        self._enter_pickup_day_to_day(from_day)
        # Select Time
        self._enter_time(hours, minutes)
        return self

    def enter_pickup_appointment_call_for_appointment(self, to_day: str, point_of_contact: bool):
        # Click Radio Button
        self._click_call_for_appointment()
        # Enter Day
        self._enter_pickup_day_to_day(to_day)
        # Select Time
        self._click_checkbox_use_current_point_of_contact(point_of_contact)
        return self

    def click_cancel(self):
        self.click().set_locator(self._button_cancel, self._name).single_click()
        return self

    def click_save_for_later(self):
        self.click().set_locator(self._button_save_for_later, self._name).single_click().pause(2)
        return self

    def click_save_and_continue(self):
        self.click().set_locator(self._button_save_and_continue, self._name).single_click().pause()
        return self

    def check_expedite(self):
        self.click().set_locator(self._checkbox_expedite_destination, self._name).single_click()
        return self.get_expedite_element()

    def get_expedite_element(self):
        try:
            element = self.driver.find_element(By.ID, "mat-checkbox-1-input")
            return element
        except NoSuchElementException:
            return None





