from selenium.webdriver.common.by import By
from tabulate import tabulate

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.bill_of_landings.searchs.SearchPanel import SearchPanel
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('BillOfLandingPage')


class BillOfLandingPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the BillOfLandingPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/billsoflading"
        # Buttons Component Class

        # Locator definitions
        self._xpath_item_container = "//div[contains(@class,'row-data-repeat')]"
        # Sub-Components
        self.buttons = Buttons.get_instance()
        self.search_panel = SearchPanel.get_instance()

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
    def click_create_shipping_instructions(self):
        self.buttons.click_button_with_label("CREATE SHIPPING INSTRUCTIONS")
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
    def click_tab_all(self):
        self.buttons.click_tab_button_with_label("ALL")
        return self

    def click_tab_in_process(self):
        self.buttons.click_tab_button_with_label("IN PROCESS")
        return self

    def click_tab_doc_received(self):
        self.buttons.click_tab_button_with_label("DOC RECEIVED")
        return self

    def click_tab_pending(self):
        self.buttons.click_tab_button_with_label("PENDING")
        return self

    def click_tab_bol_for_review(self):
        self.buttons.click_tab_button_with_label("BOL FOR REVIEW")
        return self

    def click_tab_rework(self):
        self.buttons.click_tab_button_with_label("REWORK")
        return self

    def click_tab_void(self):
        self.buttons.click_tab_button_with_label("VOID")
        return self

    def click_tab_bol_complete(self):
        self.buttons.click_tab_button_with_label("BOL COMPLETE")
        return self

    def click_tab_export_bill_released(self):
        self.buttons.click_tab_button_with_label("EXPORT BILL RELEASED")
        return self

    def click_tab_ready_for_pre_manifest(self):
        self.buttons.click_tab_button_with_label("READY FOR PRE-MANIFEST")
        return self

    def click_tab_pre_manifest_complete(self):
        self.buttons.click_tab_button_with_label("PRE-MANIFEST COMPLETE")
        return self

    def click_tab_ready_for_reconciliation(self):
        self.buttons.click_tab_button_with_label("READY FOR RECONCILIATION")
        return self

    def click_tab_vessel_closed(self):
        self.buttons.click_tab_button_with_label("VESSEL CLOSED")
        return self

    def click_tab_manifest_submitted(self):
        self.buttons.click_tab_button_with_label("MANIFEST SUBMITTED")
        return self

    def click_tab_more(self):
        self.buttons.click_tab_more()
        return self

    # ITEMS ------------------------------------------------------------------------------------------------------------
    def click_list_item_booking_id(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-id')]//a", f"Bill of ladings Item [{index}]: Booking Id [Click]")
        return self.click().set_locator(locator, self._name).single_click()

    def get_list_item_booking_id(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-id')]//a", f"Bill of ladings Item [{index}]: Booking Id [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_status(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'booking-status')]", f"Bill of ladings Item [{index}]: Booking Status [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def click_list_item_bol_equipment_icon(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]//button[1]", f"Bill of ladings Item [{index}]: Bol Equipment Icon [Click]")
        return self.click().set_locator(locator, self._name).single_click()

    def get_list_item_rate_basis(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[1]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: RATE BASIS [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_booking_number(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[2]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: BOOKING NUMBER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_account(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[3]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: ACCOUNT [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_voyage_number(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[4]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: VOYAGE NUMBER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_port_of_load(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[5]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: PORT OF LOAD [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_current_sail_date(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[6]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: CURRENT SAIL DATE [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_created_by(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[7]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: CREATED BY [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_assigned_to(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[{str(index)}]//div[contains(@class,'bol-equipment-icons')]/following-sibling::div[7]/div[2]//span)[1]", f"Bill of ladings Item [{index}]: ASSIGNED TO [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_equipment_numbers(self, index):
        locator = (By.XPATH, f"(({self._xpath_item_container})[5]//div[contains(@class,'equipment-numbers-row')]//span)[2]", f"Bill of ladings Item [{index}]: Equipment Number(s) [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item(self, index):

        booking_id = self.get_list_item_booking_id(index) or "-"
        booking_status = self.get_list_item_booking_status(index) or "-"
        rate_basis = self.get_list_item_rate_basis(index) or "-"
        booking_number = self.get_list_item_booking_number(index) or "-"
        account = self.get_list_item_account(index) or "-"
        voyage_number = self.get_list_item_voyage_number(index) or "-"
        port_of_load = self.get_list_item_port_of_load(index) or "-"
        current_sail_date = self.get_list_item_current_sail_date(index) or "-"
        create_by = self.get_list_item_created_by(index) or "-"
        assigned_to = self.get_list_item_assigned_to(index) or "-"
        equipment_numbers = self.get_list_item_equipment_numbers(index) or "-"

        data = {
            "Booking ID": booking_id,
            "Booking Status": booking_status,
            "RATE BASIS": rate_basis,
            "ACCOUNT": account,
            "BOOKING NUMBER": booking_number,
            "VOYAGE NUMBER": voyage_number,
            "PORT OF LOAD": port_of_load,
            "CURRENT SAIL DATE": current_sail_date,
            "CREATED BY": create_by,
            "ASSIGNED TO": assigned_to,
            "EQUIPMENT NUMBERS": equipment_numbers,
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data
