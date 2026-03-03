from selenium.webdriver.common.by import By
from tabulate import tabulate

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.bookings.searchs.SearchPanel import SearchPanel
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('BookingsPage')


class BookingsPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the BookingsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # Locator definitions
        self._xpath_item_container = "//div[contains(@class,'booking-list-data-row')]"
        # Sub-Components
        self.search_panel = SearchPanel.get_instance()
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

    # HEADER  ----------------------------------------------------------------------------------------------------------
    def click_update_operational_routes(self):
        self.buttons.click_button_with_label("Update Operational Route")
        return self

    def click_book_shipment(self):
        self.buttons.click_button_with_label("Book Shipment")
        return self

    # Filters & Search -------------------------------------------------------------------------------------------------
    def click_use_filters(self):
        self.buttons.click_use_filters()
        return self

    def enter_search_the_list(self, text):
        self.enter_search_the_list(text)
        return self

    # Pagination -------------------------------------------------------------------------------------------------------
    def click_refresh_icon(self):
        self.buttons.click_refresh_icon()
        return self

    def select_view_pages(self, number):
        self.buttons.select_view_pages(number)
        return self

    def click_previous_page(self):
        self.buttons.click_previous_page()
        return self

    def click_next_page(self):
        self.buttons.click_next_page()
        return self

    # TABS ------------------------------------------------------------------------------------------------------------

    def click_tab_all_bookings(self):
        self.buttons.click_tab_button_with_label("All Bookings")
        return self

    def click_tab_pending(self):
        self.buttons.click_tab_button_with_label("Pending")
        return self

    def click_tab_request_initiated(self):
        self.buttons.click_tab_button_with_label("Request Initiated")
        return self

    def click_tab_active(self):
        self.buttons.click_tab_button_with_label("Active")
        return self

    def click_tab_incomplete(self):
        self.buttons.click_tab_button_with_label("Incomplete")
        return self

    def click_tab_cancel(self):
        self.buttons.click_tab_button_with_label("Cancel")
        return self

    def click_tab_submission_failed(self):
        self.buttons.click_tab_button_with_label("Submission Failed")
        return self

    def click_tab_pending_hazardous(self):
        self.buttons.click_tab_button_with_label("Pending Hazardous")
        return self

    # ITEMS ------------------------------------------------------------------------------------------------------------
    def get_list_item_booking_source(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-source')]", f"Booking List Item [{index}]: Booking Source [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_id(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-id')]/span/a", f"Booking List Item [{index}]: Booking ID [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_status(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-status')]", f"Booking List Item [{index}]: Booking Status [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_pending_reason(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-status')]//span[@class='slds-assistive-text'][2]", f"Booking List Item [{index}]: Booking Pending Reason [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_load_type(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'load-type')]", f"Booking List Item [{index}]: Booking Load Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_account_name(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[1]/div[1]/div[2]/div[1]/span", f"Booking List Item [{index}]: Booking Account Name [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_contract_number(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[1]/div[1]/div[2]/div[2]/span", f"Booking List Item [{index}]: Booking Contract No. [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_origin_location(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[2]/div/div[1]/div[1]", f"Booking List Item [{index}]: Booking Origin Location [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_origin_location_type(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[2]/div/div[1]/div[2]/span", f"Booking List Item [{index}]: Booking Origin Location Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_vessel(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[2]/div/div[2]/div/span", f"Booking List Item [{index}]: Booking Vessel [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_number_stops(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[2]/div/div[2]/div[2]", f"Booking List Item [{index}]: Booking Number of Stops [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_destination_location(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[2]/div/div[3]/div[1]", f"Booking List Item [{index}]: Booking Destination Location [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_destination_location_type(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[2]/div/div[3]/div[2]/span", f"Booking List Item [{index}]: Booking Destination Location Type[Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_booked_date(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[3]/div[1]/strong", f"Booking List Item [{index}]: Booked Date[Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_current_sail_date(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[3]/div[2]/strong", f"Booking List Item [{index}]: Current Sail Date [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_discharge_date(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[3]/div[3]/strong", f"Booking List Item [{index}]: Discharge Date [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_assigned_to(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[3]/div[4]/strong", f"Booking List Item [{index}]: Assigned To [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_document_upload_date(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/div[3]/div[5]/strong", f"Booking List Item [{index}]: Document Upload Date [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def click_list_item_menu(self, index, option):
        locator_button = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/following-sibling::div[1]//button", f"Booking List Item [{index}]: Menu [Text]")
        locator_option = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-grid-cont')]/following-sibling::div[1]//ul/li//span[text()='{option}']", f"Booking List Item [{index}]: Option Menu [{option}][Text]")
        self.click().set_locator(locator_button, self._name).single_click()
        self.send_keys().set_locator(locator_option, self._name).set_text()
        return self

    def get_list_item(self, index):

        booking_source = self.get_list_item_booking_source(index) or "-"
        booking_id = self.get_list_item_booking_id(index) or "-"
        booking_status = self.get_list_item_booking_status(index) or "-"
        booking_pending_reason = self.get_list_item_booking_pending_reason(index) or "-"
        booking_load_type = self.get_list_item_booking_load_type(index) or "-"
        booking_account_name = self.get_list_item_booking_account_name(index) or "-"
        booking_contract_number = self.get_list_item_booking_contract_number(index) or "-"
        booking_origin_location = self.get_list_item_booking_origin_location(index) or "-"
        booking_origin_location_type = self.get_list_item_booking_origin_location_type(index) or "-"
        booking_vessel = self.get_list_item_booking_vessel(index) or "-"
        booking_number_stops = self.get_list_item_booking_number_stops(index) or "-"
        booking_destination_location = self.get_list_item_booking_destination_location(index) or "-"
        booking_destination_location_type = self.get_list_item_booking_destination_location_type(index) or "-"
        booking_booked_date = self.get_list_item_booking_booked_date(index) or "-"
        current_sail_date = self.get_list_item_current_sail_date(index) or "-"
        discharge_date = self.get_list_item_discharge_date(index) or "-"
        assigned_to = self.get_list_item_assigned_to(index) or "-"
        document_upload_date = self.get_list_item_document_upload_date(index) or "-"

        # Create a Dictionary
        data = {
            "Booking Source": booking_source,
            "Booking ID": booking_id,
            "Booking Status": booking_status,
            "Pending Reason": booking_pending_reason,
            "Load Type": booking_load_type,
            "Account Name": booking_account_name,
            "Contract Number": booking_contract_number,
            "Origin Location": booking_origin_location,
            "Origin Location Type": booking_origin_location_type,
            "Vessel": booking_vessel,
            "Number of Stops": booking_number_stops,
            "Destination Location": booking_destination_location,
            "Destination Location Type": booking_destination_location_type,
            "Booked Date": booking_booked_date,
            "Current Sail Date": current_sail_date,
            "Discharge Date": discharge_date,
            "Assigned To": assigned_to,
            "Document Upload Date": document_upload_date,
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data
