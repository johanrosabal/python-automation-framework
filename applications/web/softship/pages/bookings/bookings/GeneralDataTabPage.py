import allure
import re

from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from applications.web.softship.pages.bookings.bookings.CommonElementsBookingsPage import CommonElementsBookingsPage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('generalDataTabPage')


class GeneralDataTabPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        self.commons_bookings_elements = CommonElementsBookingsPage(driver)
        super().__init__(driver)
        # Relative URL
        self.relative = "/booking/main/general"
        self._module_url = None
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self.__input_from_receipt_term = (By.XPATH, "//span[contains(text(), 'Receipt Term *')]/following::input[contains(@class, 'p-autocomplete-input')][1]", "From Receipt Term [Input]")
        self.__input_from_location = (By.XPATH, "//span[contains(text(), 'Location *')]/following::input[contains(@class, 'p-autocomplete-input')][1]", "From Location [Input]")
        self.__input_from_receipt_type = (By.XPATH, "//span[contains(text(), 'Receipt Type')]/following::input[contains(@class, 'p-autocomplete-input')][1]", "From Receipt Type [Input]")
        self.__input_to_delivery_term = (By.XPATH, "//span[contains(text(), 'Delivery Term *')]/following::input[contains(@class, 'p-autocomplete-input')][1]", "To Delivery Term [Input]")
        self.__input_to_location = (By.XPATH, "//span[contains(text(), 'Location')]/following::input[contains(@class, 'p-autocomplete-input')][8]", "To Location [Input]")
        self.__input_to_delivery_type = (By.XPATH, "//span[contains(text(), 'Delivery Type')]/following::input[contains(@class, 'p-autocomplete-input')][1]","From Delivery Type [Input]")
        self.__btn_follow_up_toggle = (By.XPATH, "(//ssh-date-time-picker[contains(@sshcustomizable, 'HeaderFollowUp')]//span)[2]")
        self.__lbl_from = (By.XPATH,"//ssh-labeled-field[@for='headerFrom']//div[@sshcustomizable]")
        self.__lbl_to = (By.XPATH, "//ssh-labeled-field[@for='headerTo']//div[@sshcustomizable]")
        self.__lbl_max_transship = (By.XPATH, "//ssh-labeled-field[@for='headerMaxTrans']//div[@sshcustomizable]")
        self.__lbl_customer = (By.XPATH, "//ssh-labeled-field[@for='headerCustomer']//div[@sshcustomizable]")
        self.__lbl_contact = (By.XPATH, "//ssh-labeled-field[@for='headerContact']//div[@sshcustomizable]")
        self.__lbl_agency = (By.XPATH, "//ssh-labeled-field[@for='headerAgency']//div[@sshcustomizable]")
        self.__lbl_currency = (By.XPATH, "//ssh-labeled-field[@for='headerCurrency']//div[@sshcustomizable]")
        self.__lbl_contract = (By.XPATH, "//ssh-labeled-field[@for='headerContract']//div[@sshcustomizable]")
        self.__lbl_iny_booking_no = (By.XPATH, "//ssh-labeled-field[@for='headerIntBookingNo']//div[@sshcustomizable]")
        self.__nav_bookings = (By.XPATH, "//span[@class='ng-binding ng-scope' and text()='Bookings']", "Bookings Menu Option")
        self.__nav_system = (By.XPATH, "//span[@class='ng-binding ng-scope' and text()='System']", "System Menu Option")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Enter from receipt term: {from_receipt_term}")
    def enter_from_receipt_term(self, from_receipt_term: str):
        self.send_keys().set_locator(self.__input_from_receipt_term, self._name).set_text(from_receipt_term).press_tab().pause(1)
        return self

    @allure.step("Enter from location: {from_location}")
    def enter_from_location(self, from_location: str):
        self.send_keys().set_locator(self.__input_from_location, self._name).set_text(from_location).press_tab().pause(1)
        return self

    @allure.step("Enter from receipt type: {from_receipt_type}")
    def enter_from_receipt_type(self, from_receipt_type: str):
        self.send_keys().set_locator(self.__input_from_receipt_type, self._name).set_text(from_receipt_type).press_tab().pause(1)
        return self

    @allure.step("Enter from delivery term: {to_delivery_term}")
    def enter_to_delivery_term(self, to_delivery_term: str):
        self.send_keys().set_locator(self.__input_to_delivery_term, self._name).set_text(to_delivery_term).press_tab().pause(1)
        return self

    @allure.step("Enter from location: {to_location}")
    def enter_to_location(self, to_location: str):
        self.send_keys().set_locator(self.__input_to_location, self._name).set_text(to_location).press_tab().pause(1)
        return self

    @allure.step("Enter to delivery type: {to_delivery_type}")
    def enter_to_delivery_type(self, to_delivery_type: str):
        self.send_keys().set_locator(self.__input_to_delivery_type, self._name).set_text(to_delivery_type).press_tab().pause(1)
        return self

    @allure.step("Validate General tab")
    def validate_general_tab_elements(self, from_receipt_term: str, from_location_zip: str, from_location_name: str, to_delivery_term: str, to_location_zip:str, to_location_name: str):
        """
        Validate that all specified locators are present on the page.
        """
        with allure.step("Enter from receipt term: {from_receipt_term}"):
            self.enter_from_receipt_term(from_receipt_term)
        with allure.step("Enter and validate 'FROM' location on header section"):
            self.enter_from_location(from_location_zip)
            assert from_location_name == self.commons_bookings_elements.get_text_from_header()
        with allure.step("Enter to delivery term: {to_delivery_term}"):
            self.enter_to_delivery_term(to_delivery_term)
        with allure.step("Enter and validate 'TO' location on header section"):
            self.enter_to_location(to_location_zip)
            assert to_location_name == self.commons_bookings_elements.get_text_to_header()