from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter
from core.asserts.AssertCollector import AssertCollector

logger = setup_logger('BidDetailsPage')


class BidDetailsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the BidDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/load-details"
        # Locator definitions
        self._text_tracking_number = (By.XPATH, "//load-address-header-with-action//span[contains(@class,'d-block')]/span", "Tracking Number [Local Details]")
        self._text_address_detail = (By.XPATH, "//load-address-header-with-action//span[contains(@class,'fw-medium')]", "Address Detail [Local Details]")
        self._button_extend_bid = (By.XPATH, "//load-address-header-with-action//button[@id='dropdownMenuButton']", "Extend Bid [Button]")
        self._button_close_bid = (By.XPATH, "//load-address-header-with-action//span[contains(text(),'Close Bid')]", "Extend Bid [Button]")
        self._text_pick_up_date = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Pick Up Date')]/following-sibling::span", "Pick Up Date [Text]")
        self._text_bids_received = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Bids Received')]/following-sibling::span", "Bids Received [Text]")
        self._text_book_now = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Book Now')]/following-sibling::span", "Book Now [Text]")
        self._text_low = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Low')]/following-sibling::span", "Low [Text]")
        self._text_median = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Median')]/following-sibling::span", "Median [Text]")
        self._text_high = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'High')]/following-sibling::span", "High [Text]")
        self._text_equipment = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Equipment')]/following-sibling::span", "Equipment [Text]")
        self._text_offers_ending_soon = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Offers Ending Soon')]/following-sibling::span", "Offers Ending Soon [Text]")
        self._text_bid_status = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//label[contains(text(),'Bid Status')]/following-sibling::span", "Bid Status [Text]")
        self._button_documents = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[1]/div//span[contains(text(),'Documents')]/..", "Documents [Button]")
        self._button_assign_a_carrier = (By.XPATH, "//app-load-details//button[.//span[contains(normalize-space(), 'Assign a Carrier')]]")
        self._table_carrier = "(//div[contains(@class,'loadboard-card')])[2]//table"
        self._table_documents = "(//div[contains(@class,'loadboard-card')])[3]//table"
        self._button_upload = (By.XPATH, "(//div[contains(@class,'loadboard-card')])[3]//span[contains(text(),'Upload')]/..", "Upload [Button]")
        self._upload_documents = (By.XPATH, "//*[@id='bolAttachments']/div[2]/div[1]/div/button","Upload docuemnts [Button]")

        #Customer portal: Modal Assign Load to Carrier
        self._input_search_carrier = (By.XPATH, "//div[contains(@class,'modal-dialog')]//input[@placeholder='Search by Name, MC#, DOT#, SCAC Code']","Search by name[Input]")
        self._input_carrier_rate = (By.XPATH, "//div[contains(@class,'modal-dialog')]//input[@placeholder='Enter Rate']","Enter Rate[Input]")
        self._button_assign_load = (By.XPATH, "//div[contains(@class,'modal-dialog')]//button/span[contains(text(),'Assign Load')]","Assign load [Button]")
        self._button_cancel_load = (By.XPATH, "//div[contains(@class,'modal-dialog')]//button/span[contains(text(),'Cancel')]","Assign cancel [Button]")
        self._button_close_modal = (By.XPATH, "//div[contains(@class,'modal-dialog')]//button[contains(@class,'btn-close')]","Assign close [Button]")



    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = BidDetailsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def get_shipment_tracker_number(self):
        return self.get_text().set_locator(self._text_tracking_number, self._name).by_text().replace("#", "").strip()

    def get_local_address_details(self):
        return self.get_text().set_locator(self._text_address_detail, self._name).by_text()

    def click_extend_bid(self, minutes: int):
        # Click 'Extend Bid' Dropdown Menu
        self.click().set_locator(self._button_extend_bid, self._name).single_click().pause(1)
        # Select an Option: '30 Minutes', '60 Minutes', '90 Minutes', '120 Minutes'
        locator_menu = (By.XPATH, f"//div[contains(@class,'dropdown-menu')]/a[contains(text(),'{minutes}')]", f" {minutes} Minutes [Dropdown]")
        self.click().set_locator(locator_menu, self._name).single_click()
        return self

    def _get_book_load_pick_up_date(self):
        return self.get_text().set_locator(self._text_pick_up_date, self._name).by_text()

    def _get_book_load_bids_received(self):
        return self.get_text().set_locator(self._text_bids_received, self._name).by_text()

    def _get_book_load_book_now(self):
        return self.get_text().set_locator(self._text_book_now, self._name).by_text()

    def _get_book_load_low(self):
        return self.get_text().set_locator(self._text_low, self._name).by_text()

    def _get_book_load_median(self):
        return self.get_text().set_locator(self._text_median, self._name).by_text()

    def _get_book_load_high(self):
        return self.get_text().set_locator(self._text_high, self._name).by_text()

    def _get_book_load_equipment(self):
        return self.get_text().set_locator(self._text_equipment, self._name).by_text()

    def _get_book_load_offers_ending_soon(self):
        return self.get_text().set_locator(self._text_offers_ending_soon, self._name).by_text()

    def _get_book_load_bid_status(self):
        return self.get_text().set_locator(self._text_bid_status, self._name).by_text()

    def get_book_load(self):
        data = []

        pick_up_date = self._get_book_load_pick_up_date() or "-"
        bids_received = self._get_book_load_bids_received()
        book_now = self._get_book_load_low()
        median = self._get_book_load_median()
        high = self._get_book_load_high()
        equipment = self._get_book_load_equipment()
        offers_ending_soon = self._get_book_load_offers_ending_soon()
        bid_status = self._get_book_load_bid_status()

        headers = ["Pick Up Date", "Bids Received", "Book Now", "Low", "Median", "High", "Equipment", "Offers Ending Soon", "Bid Status"]

        data.append([pick_up_date, bids_received, book_now, median, high, equipment, offers_ending_soon,bid_status])
        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return data[0]

    def click_documents(self):
        self.click().set_locator(self._button_documents, self._name).single_click()
        return self

    def click_close_bid(self):
        self.click().set_locator(self._button_close_bid, self._name).single_click()
        return self

    def click_assign_a_carrier(self):
        self.click().set_locator(self._button_assign_a_carrier, self._name).single_click()
        return self

    def _get_table_cell_date(self, index: int):
        locator = (By.XPATH, f"{self._table_documents}/tbody/tr[{str(index)}]/td[1]", f"Date [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_document_type(self, index: int):
        locator = (By.XPATH, f"{self._table_documents}/tbody/tr[{str(index)}]/td[2]", f"Document Type [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_description(self, index: int):
        locator = (By.XPATH, f"{self._table_documents}/tbody/tr[{str(index)}]/td[3]", f"Description [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_file_name(self, index: int):
        locator = (By.XPATH, f"{self._table_documents}/tbody/tr[{str(index)}]/td[4]", f"File Name [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_file_type(self, index: int):
        locator = (By.XPATH, f"{self._table_documents}/tbody/tr[{str(index)}]/td[5]", f"File Type [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_document_item(self, index: int):
        data = []

        date = self._get_table_cell_date(index) or "-"
        document_type = self._get_table_cell_document_type(index) or "-"
        description = self._get_table_cell_description(index) or "-"
        file_name = self._get_table_cell_file_name(index) or "-"
        file_type = self._get_table_cell_file_type(index) or "-"

        headers = [
            "Date", "Document Type", "Description", "File Name", "File Type"
        ]

        data.append([date, document_type, description, file_name, file_type])

        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return data

    def click_upload(self):
        self.click().set_locator(self._button_upload, self._name).single_click()
        return self

    # Modal Assign Load to Carrier ------------------------------------------------------------------------------------
    def _enter_search_carrier(self, text):
        self.send_keys().set_locator(self._input_search_carrier, self._name).set_text(text)
        return self

    def _enter_rate(self, text):
        self.send_keys().set_locator(self._input_carrier_rate, self._name).set_text(text)
        return self

    def enter_load_to_carrier(self, search_carrier, rate):
        self._enter_search_carrier(search_carrier)
        self._enter_rate(rate)
        return self

    def click_assign_load(self):
        self.click().set_locator(self._button_assign_load, self._name).single_click().pause(1)
        return self
    def is_assign_load_visible(self):
        return self.element().set_locator(self._button_assign_load,self._name).is_enabled()

    def click_cancel_load(self):
        self.click().set_locator(self._button_cancel_load, self._name).single_click().pause(1)
        return self

    def click_close_modal(self):
        self.click().set_locator(self._button_close_modal, self._name).single_click().pause(1)
        return self
