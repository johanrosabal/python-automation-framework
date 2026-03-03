import allure
import re

from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('CommonElementsBookingPage')


class CommonElementsBookingsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/booking/main/general"
        self._module_url = None
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self.__lbl_booking_status = (By.XPATH, "//div[contains(@sshcustomizable, 'HeaderBookingStatus')]", "Booking Status")
        self.__lbl_operational_status = (By.XPATH, "//div[contains(@sshcustomizable, 'HeaderOperationalStatus')]//span", "")
        self.__lbl_auto_b_l_status = (By.XPATH, "//div[contains(@sshcustomizable, 'HeaderAutoBLStatus')]")
        self.__input_assignee = (By.XPATH, "//ssh-auto-complete[@field='Username']//input")
        self.__btn_assignee_toggle = (By.XPATH, "(//ssh-auto-complete[@field='Username']//span)[2]")
        self.__input_follow_up = (By.XPATH, "//ssh-date-time-picker[contains(@sshcustomizable, 'HeaderFollowUp')]")
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

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["booking"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def _update_relative_with_booking_number(self):
        """
        Detect and update the relative URL dynamically if a booking number is present.
        """
        current_url = self.driver.current_url
        logger.info(f"Current URL: {current_url}")
        # Use regex to extract the booking number from the URL
        match = re.search(r"/Booking/booking/(\d+)/main/cargo", current_url)
        if match:
            booking_number = match.group(1)
            logger.info(f"Detected booking number: {booking_number}")
            self.relative = f"/Booking/booking/{booking_number}/main/cargo"
            logger.info(f"Updated relative URL: {self.relative}")
        else:
            logger.warning("No booking number detected in the URL.")

    @allure.step("Validate presence of all locators on the page")
    def validate_information_status(self):
        """
        Validate that all specified locators are present on the page.
        """

        with allure.step("Validating booking status"):
            self.highlight_element().set_locator(self.__lbl_booking_status, self._name)
            assert "Pending" == self.get_text().set_locator(self.__lbl_booking_status).by_text()
        with allure.step("Validating operational status"):
            self.highlight_element().set_locator(self.__lbl_operational_status, self._name)
            assert "Not Assigned" == self.get_text().set_locator(self.__lbl_operational_status).by_text()
        with allure.step("Validating Auto B/L stats"):
            self.highlight_element().set_locator(self.__lbl_auto_b_l_status, self._name)
            assert "No Link" == self.get_text().set_locator(self.__lbl_auto_b_l_status).by_text()

    @allure.step("Validate presence of all locators on the page")
    def validate_header_booking_process(self):
        """
        Validate that all specified locators are present on the page.
        """

        with allure.step("Validating booking status"):
            self.highlight_element().set_locator(self.__lbl_booking_status, self._name)
            assert "Pending" == self.get_text().set_locator(self.__lbl_booking_status).by_text()
        with allure.step("Validating operational status"):
            self.highlight_element().set_locator(self.__lbl_operational_status, self._name)
            assert "Not Assigned" == self.get_text().set_locator(self.__lbl_operational_status).by_text()
        with allure.step("Validating Auto B/L stats"):
            self.highlight_element().set_locator(self.__lbl_auto_b_l_status, self._name)
            assert "No Link" == self.get_text().set_locator(self.__lbl_auto_b_l_status).by_text()

    @allure.step("Enter Assignee: {assignee}")
    def enter_assignee(self, assignee: str):
        self.send_keys().set_locator(self.__input_assignee, self._name).set_text(assignee)
        return self

    @allure.step("Enter follow up: {follow_up}")
    def enter_follow_up(self, follow_up: str):
        self.send_keys().set_locator(self.__input_follow_up, self._name).set_text(follow_up)
        return self

    @allure.step("Enter follow up: {follow_up}")
    def enter_follow_up(self, follow_up: str):
        self.send_keys().set_locator(self.__input_follow_up, self._name).set_text(follow_up)
        return self

    @allure.step("Enter from receipt: {from_receipt}")
    def validate_from_receipt(self, from_receipt: str):
        self.highlight_element().set_locator(self.__lbl_from, self._name)
        assert "Jacksonville, FL" == self.get_text().set_locator(self.__lbl_from).by_text()
        return self

    @allure.step("Enter to delivery: {to_delivery}")
    def validate_to_delivery(self, from_receipt: str):
        self.highlight_element().set_locator(self.__lbl_to, self._name)
        assert "San Juan, Puerto Rico" == self.get_text().set_locator(self.__lbl_to).by_text()
        return self

    @allure.step("Get text of FROM header")
    def get_text_from_header(self):
        return self.get_text().set_locator(self.__lbl_from).by_text()

    @allure.step("Get text of TO header")
    def get_text_to_header(self):
        return self.get_text().set_locator(self.__lbl_to).by_text()
