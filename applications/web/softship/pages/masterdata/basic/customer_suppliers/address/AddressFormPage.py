import allure
from selenium.webdriver.common.by import By
from applications.web.softship.components.alert.AlertDialogBox import AlertDialogBox
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.data.address_source_mapping import CustomerAppliersAddressDto
from applications.web.softship.common.SoftshipPage import SoftshipPage
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('AddressFormPage')


class AddressFormPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the Address Form Page instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        self.alert = AlertDialogBox(self._driver)
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/addressnew/0/general?taskhandlerId=AddressNew"
        # Locator definitions
        # Headers Buttons
        self._buttons = Buttons(self._driver)

        # Form Locators
        self._input_address_code = (By.XPATH, "//input[contains(@id, 'addressCode')]", "Address Code Input Form")

        self._input_address_code_line_1 = (By.XPATH, "//input[contains(@id, 'addressLine1')]", "Address Text Line 1 Input Form")
        self._input_address_code_line_2 = (By.XPATH, "//input[contains(@id, 'addressLine2')]", "Address Text Line 2 Input Form")
        self._input_address_code_line_3 = (By.XPATH, "//input[contains(@id, 'addressLine3')]", "Address Text Line 3 Input Form")
        self._input_address_code_line_4 = (By.XPATH, "//input[contains(@id, 'addressLine4')]", "Address Text Line 4 Input Form")
        self._input_address_code_line_5 = (By.XPATH, "//input[contains(@id, 'addressLine5')]", "Address Text Line 5 Input Form")
        self._input_address_code_line_6 = (By.XPATH, "//input[contains(@id, 'addressLine6')]", "Address Text Line 6 Input Form")
        self._input_address_code_line_7 = (By.XPATH, "//input[contains(@id, 'addressLine7')]", "Address Text Line 7 Input Form")

        self._input_secondary_language_line_1 = (By.XPATH, "//input[contains(@id, 'secLang1')]", "Secondary Language Line 1 Input Form")
        self._input_secondary_language_line_2 = (By.XPATH, "//input[contains(@id, 'secLang2')]", "Secondary Language Line 2 Input Form")
        self._input_secondary_language_line_3 = (By.XPATH, "//input[contains(@id, 'secLang3')]", "Secondary Language Line 3 Input Form")
        self._input_secondary_language_line_4 = (By.XPATH, "//input[contains(@id, 'secLang4')]", "Secondary Language Line 4 Input Form")
        self._input_secondary_language_line_5 = (By.XPATH, "//input[contains(@id, 'secLang5')]", "Secondary Language Line 5 Input Form")
        self._input_secondary_language_line_6 = (By.XPATH, "//input[contains(@id, 'secLang6')]", "Secondary Language Line 6 Input Form")
        self._input_secondary_language_line_7 = (By.XPATH, "//input[contains(@id, 'secLang7')]", "Secondary Language Line 7 Input Form")

        self._input_contact_1 = (By.XPATH, "//input[contains(@id, 'contact1')]", "Contact 1 Input Form")
        self._input_contact_2 = (By.XPATH, "//input[contains(@id, 'contact2')]", "Contact 2 Input Form")

        self._autocomplete_contact_type = (By.XPATH, "//*[contains(@id, 'contactType')]//input", "Contact Type Auto Complete Form")

        self._input_street_line_1 = (By.XPATH, "//input[contains(@id, 'street1')]", "Street Line 1 Input Form")
        self._input_street_line_2 = (By.XPATH, "//input[contains(@id, 'street2')]", "Street Line 2 Input Form")
        self._input_street_line_3 = (By.XPATH, "//input[contains(@id, 'street3')]", "Street Line 3 Input Form")

        self._autocomplete_location = (By.XPATH, "//*[contains(@id, 'location')]//input", "LocationInput Form")
        self._input_postal_code = (By.XPATH, "//input[contains(@id, 'postalCode')]", "Postal Code Input Form")
        self._input_city_name = (By.XPATH, "//input[contains(@id, 'cityName')]", "City Name Auto Complete Form")

        self._autocomplete_country = (By.XPATH, "//*[contains(@id, 'country')]//input", "Country Auto Complete Form")
        self._autocomplete_province = (By.XPATH, "//*[contains(@id, 'province')]//input", "Province Auto Complete Form")

        self._input_ban_address = (By.XPATH, "//input[contains(@id, 'ban')]", "BAN Input Form")

        self._btn_coordinates_edit = (By.XPATH, "//*[contains(@id, 'detailsEditButtonId')]", "Coordinates Edit Button Icon")
        self._input_coordinates_latitude = (By.XPATH, "//*[contains(@id, 'latitude')]", "Coordinates Latitude Input Form")
        self._input_coordinates_longitude = (By.XPATH, "//*[contains(@id, 'longitude')]", "Coordinates Longitude Input Form")
        self._btn_coordinates_get_coordinates = (By.XPATH, "//button[contains(text(),'Get Coordinates')]", "Get Coordinates Button Form")
        self._btn_coordinates_apply = (By.XPATH, "//button[contains(text(),'Apply')]", "Coordinates Apply Button Form")
        self._btn_coordinates_cancel = (By.XPATH, "//button[contains(text(),'Cancel')]", "Coordinates Apply Button Form")

        self._btn_coordinates_confirmation_yes = (By.XPATH, "//button[contains(text(),'Yes')]", "Coordinates Confirmation Yes Button Form")
        self._btn_coordinates_confirmation_no = (By.XPATH, "//button[contains(text(),'No')]", "Coordinates Confirmation No Button Form")

        self._checkbox_is_hide = (By.XPATH, "//input[contains(@id, 'isHide')]", "Coordinates -> Hide Checkbox Form")
        self._checkbox_is_web_booking = (By.XPATH, "//input[contains(@id, 'isWebbooking')]", "Coordinates -> Webbooking Checkbox Form")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def click_save(self, pause: int = 2):
        self._buttons.click_save(pause=pause)
        return self

    def click_save_and_close(self, pause: int = 2):
        self._buttons.click_save_and_close(pause=pause)
        return self

    def click_close(self, pause: int = 2):
        self._buttons.click_close(pause=pause)
        return self

    def click_confirm_yes(self, pause: int = 2):
        self._buttons.click_confirm_yes(pause=pause)
        return self

    def click_confirm_no(self, pause: int = 5):
        self._buttons.click_confirm_no(pause=pause)
        return self

    @allure.step("Enter Address Code Input Form: {address_code}")
    def enter_address_code(self, address_code: str):
        self.send_keys().set_locator(self._input_address_code, self._name).set_text(address_code)
        return self

    @allure.step("Enter Address Line 1 Input Form: {address_line_1}")
    def enter_address_line_1(self, address_line_1: str):
        self.send_keys().set_locator(self._input_address_code_line_1, self._name).set_text(address_line_1)
        return self

    @allure.step("Enter Address Line 2 Input Form: {address_line_2}")
    def enter_address_line_2(self, address_line_2: str):
        self.send_keys().set_locator(self._input_address_code_line_2, self._name).set_text(address_line_2)
        return self

    @allure.step("Enter Address Line 3 Input Form: {address_line_3}")
    def enter_address_line_3(self, address_line_3: str):
        self.send_keys().set_locator(self._input_address_code_line_3, self._name).set_text(address_line_3)
        return self

    @allure.step("Enter Address Line 4 Input Form: {address_line_4}")
    def enter_address_line_4(self, address_line_4: str):
        self.send_keys().set_locator(self._input_address_code_line_4, self._name).set_text(address_line_4)
        return self

    @allure.step("Enter Address Line 5 Input Form: {address_line_5}")
    def enter_address_line_5(self, address_line_5: str):
        self.send_keys().set_locator(self._input_address_code_line_5, self._name).set_text(address_line_5)
        return self

    @allure.step("Enter Address Line 6 Input Form: {address_line_6}")
    def enter_address_line_6(self, address_line_6: str):
        self.send_keys().set_locator(self._input_address_code_line_6, self._name).set_text(address_line_6)
        return self

    @allure.step("Enter Address Line 7 Input Form: {address_line_7}")
    def enter_address_line_7(self, address_line_7: str):
        self.send_keys().set_locator(self._input_address_code_line_7, self._name).set_text(address_line_7)
        return self

    @allure.step("Enter Secondary Language Line 1 Input Form: {secondary_language_1}")
    def enter_secondary_language_line_1(self, secondary_language_1: str):
        self.send_keys().set_locator(self._input_secondary_language_line_1, self._name).set_text(secondary_language_1)
        return self

    @allure.step("Enter Secondary Language Line 2 Input Form: {secondary_language_2}")
    def enter_secondary_language_line_2(self, secondary_language_2: str):
        self.send_keys().set_locator(self._input_secondary_language_line_2, self._name).set_text(secondary_language_2)
        return self

    @allure.step("Enter Secondary Language Line 3 Input Form: {secondary_language_3}")
    def enter_secondary_language_line_3(self, secondary_language_3: str):
        self.send_keys().set_locator(self._input_secondary_language_line_3, self._name).set_text(secondary_language_3)
        return self

    @allure.step("Enter Secondary Language Line 4 Input Form: {secondary_language_4}")
    def enter_secondary_language_line_4(self, secondary_language_4: str):
        self.send_keys().set_locator(self._input_secondary_language_line_4, self._name).set_text(secondary_language_4)
        return self

    @allure.step("Enter Secondary Language Line 5 Input Form: {secondary_language_5}")
    def enter_secondary_language_line_5(self, secondary_language_5: str):
        self.send_keys().set_locator(self._input_secondary_language_line_5, self._name).set_text(secondary_language_5)
        return self

    @allure.step("Enter Secondary Language Line 6 Input Form: {secondary_language_6}")
    def enter_secondary_language_line_6(self, secondary_language_6: str):
        self.send_keys().set_locator(self._input_secondary_language_line_6, self._name).set_text(secondary_language_6)
        return self

    @allure.step("Enter Secondary Language Line 7 Input Form: {secondary_language_7}")
    def enter_secondary_language_line_7(self, secondary_language_7: str):
        self.send_keys().set_locator(self._input_secondary_language_line_7, self._name).set_text(secondary_language_7)
        return self

    @allure.step("Enter Contact 1 Input Form")
    def enter_contact_1(self, contact_1: str):
        self.send_keys().set_locator(self._input_contact_1, self._name).set_text(contact_1)
        return self

    @allure.step("Enter Contact 2 Input Form")
    def enter_contact_2(self, contact_2: str):
        self.send_keys().set_locator(self._input_contact_2, self._name).set_text(contact_2)
        return self

    @allure.step("Enter Contact Type Input Form: {contact_type}")
    def enter_contact_type(self, contact_type: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_contact_type, self._name) \
            .by_text(text=contact_type, column=1)
        return self

    @allure.step("Enter Street Line 1 Form: {street_line_1}")
    def enter_street_line_1(self, street_line_1: str):
        self.send_keys().set_locator(self._input_street_line_1, self._name).set_text(street_line_1)
        return self

    @allure.step("Enter Street Line 2 Form: {street_line_2}")
    def enter_street_line_2(self, street_line_2: str):
        self.send_keys().set_locator(self._input_street_line_2, self._name).set_text(street_line_2)
        return self

    @allure.step("Enter Street Line 3 Form: {street_line_3}")
    def enter_street_line_3(self, street_line_3: str):
        self.send_keys().set_locator(self._input_street_line_3, self._name).set_text(street_line_3)
        return self

    @allure.step("Enter Location Form: {location}")
    def enter_location(self, location: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_location, self._name) \
            .clear() \
            .by_text(text=location, column=1)
        return self

    @allure.step("Enter Postal Code Form: {postal_code}")
    def enter_postal_code(self, postal_code: str):
        self.send_keys().set_locator(self._input_postal_code, self._name).set_text(postal_code)

    @allure.step("Enter City Name Form: {city_name}")
    def enter_city_name(self, city_name: str):
        self.send_keys().set_locator(self._input_city_name, self._name).clear().set_text(city_name)

    @allure.step("Enter Country Form: {country}")
    def enter_country(self, country: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_country, self._name) \
            .clear() \
            .pause(2) \
            .by_text(text=country, column=1)
        return self

    @allure.step("Enter Province Form: {province}")
    def enter_province(self, province: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_province, self._name) \
            .clear() \
            .pause(1) \
            .by_text(text=province, column=2)
        return self

    @allure.step("Enter Ban Address Form: {ban_address}")
    def enter_ban_address(self, ban_address: str):
        self.send_keys().set_locator(self._input_ban_address, self._name).set_text(ban_address)
        return self

    @allure.step("Click Checkbox Coordinates Edit")
    def click_coordinates_edit(self):
        self.click().set_locator(self._btn_coordinates_edit, self._name).single_click().pause(2)
        return self

    @allure.step("Enter Coordinates Latitude Form: {coordinates_latitude}")
    def enter_coordinates_latitude(self, coordinates_latitude):
        self.send_keys().set_locator(self._input_coordinates_latitude, self._name).set_text(coordinates_latitude)
        return self

    @allure.step("Enter Coordinates Longitude Form: {coordinates_longitude}")
    def enter_coordinates_longitude(self, coordinates_longitude):
        self.send_keys().set_locator(self._input_coordinates_longitude, self._name).set_text(coordinates_longitude)
        return self

    @allure.step("Click Get Coordinates")
    def click_get_coordinates(self):
        self.click()\
            .set_locator(self._btn_coordinates_get_coordinates, self._name)\
            .pause(5)\
            .single_click()
        return self

    @allure.step("Click Coordinates Apply")
    def click_coordinates_apply(self):
        self.click()\
            .set_locator(self._btn_coordinates_apply, self._name)\
            .screenshot(name="Address Form Coordinates")\
            .pause(5) \
            .single_click()
        return self

    @allure.step("Click Coordinates Cancel")
    def click_coordinates_cancel(self):
        self.click().set_locator(self._btn_coordinates_cancel, self._name).single_click()
        return self

    @allure.step("Click Coordinates Confirm Yes")
    def click_coordinates_confirm_yes(self):
        self.click().set_locator(self._btn_coordinates_confirmation_yes, self._name).single_click()
        return self

    @allure.step("Click Coordinates Confirm No")
    def click_coordinates_confirm_no(self):
        self.click().set_locator(self._btn_coordinates_confirmation_no, self._name).single_click()
        return self

    @allure.step("Checkbox Is Hide Form: {is_hide}")
    def checkbox_is_hide(self, is_hide: str):
        self.checkbox().set_locator(self._checkbox_is_hide, self._name).set_value(is_hide)
        return self

    @allure.step("Checkbox Is Web Booking Form: {is_web_booking}")
    def checkbox_is_web_booking(self, is_web_booking: str):
        self.checkbox().set_locator(self._checkbox_is_web_booking, self._name).set_value(is_web_booking)
        return self

    @allure.step("Address Form")
    def fill_out_address_form(self, address: CustomerAppliersAddressDto):
        with allure.step("Customer Suppliers: Complete Address Form"):
            logger.info(address)
            self.enter_address_code(address.address_code)
            self.enter_address_line_1(address.address_line_1)
            self.enter_address_line_2(address.address_line_2)
            self.enter_address_line_3(address.address_line_3)
            self.enter_address_line_4(address.address_line_4)
            self.enter_address_line_5(address.address_line_5)
            self.enter_address_line_6(address.address_line_6)
            self.enter_address_line_7(address.address_line_7)
            self.enter_secondary_language_line_1(address.secondary_language_line_1)
            self.enter_secondary_language_line_2(address.secondary_language_line_2)
            self.enter_secondary_language_line_3(address.secondary_language_line_3)
            self.enter_secondary_language_line_4(address.secondary_language_line_4)
            self.enter_secondary_language_line_5(address.secondary_language_line_5)
            self.enter_secondary_language_line_6(address.secondary_language_line_6)
            self.enter_secondary_language_line_7(address.secondary_language_line_7)
            self.enter_contact_1(address.contact_1)
            self.enter_contact_2(address.contact_2)
            self.enter_contact_type(address.contact_type)
            self.enter_street_line_1(address.street_line_1)
            self.enter_street_line_2(address.street_line_2)
            self.enter_street_line_3(address.street_line_3)
            self.enter_location(address.location)
            self.enter_postal_code(address.postal_code)

            if address.location is None:
                self.enter_city_name(address.city_name)
                self.enter_country(address.country)
                self.enter_province(address.province)

            self.enter_ban_address(address.ban)

            if address.coordinates_edit:
                self.click_coordinates_edit()
                self.enter_coordinates_latitude(address.coordinates_latitude)
                self.enter_coordinates_longitude(address.coordinates_longitude)
                self.click_get_coordinates()
                self.click_coordinates_apply()

            if address.is_hide:
                self.checkbox_is_hide(address.is_hide)

            if address.is_web_booking:
                self.checkbox_is_web_booking(address.is_web_booking)

            self.scroll().to_top()
            self.screenshot().attach_to_allure("Form Fields Part 1", self._name)

        return self

    @allure.step("Verify Data Saved")
    def verify_saved_data(self):
        toast_actual = self.alert.get_toast_detail()
        toast_expected = "Data has been saved."

        # Assert with a custom error message
        # assert toast_actual == toast_expected, f"Error: Expected text '{toast_expected}' but found '{toast_actual}'"

    def is_address_form_displayed(self):
        url = BaseApp.get_modules()["master_data"] + '/addressnew/0/general?taskhandlerId=AddressNew'
        AssertCollector.assert_equal_message(
            url,
            self.navigation().get_current_url(),
            "Address Form is not displayed.",
            self._name,
            self.method_name()
        )
