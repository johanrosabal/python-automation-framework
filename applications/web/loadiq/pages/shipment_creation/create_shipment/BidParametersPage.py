from selenium.webdriver.common.by import By
from pathlib import Path
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('BidParametersPage')


class BidParametersPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the BidParameters instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/create"
        # Locator definitions
        self._form = "(//div[contains(@class,'additional-info')])"
        self._input_book_it_row_rate = (By.XPATH, f"{self._form}//label[contains(text(),'Book it Now Rate')]/..//input", "Book It Now Rate [Input Box]")
        self._input_bid_expiration_date = (By.XPATH, f"{self._form}//label[contains(text(),'Bid Expiration Date')]/..//input", "Bid Expiration Date")
        self._button_data_picker = (By.XPATH, f"{self._form}//button[contains(@class,'daterangepicker-action')]", "Data Picker Button")
        self._button_today_day = (By.XPATH, f"{self._form}//td[contains(@class,'start-date')]", "Today Day on Calendar [Date Picker]")

        self._input_hours = (By.XPATH, f"{self._form}//div[contains(@class, 'timepickercontrol')]//input[contains(@aria-label,'Hours')]", "Hours [Input Box]")
        self._input_minutes = (By.XPATH, f"{self._form}//div[contains(@class, 'timepickercontrol')]//input[contains(@aria-label,'Minutes')]", "Hours [Input Box]")
        #CHANGE FOR LOGIB-3445
        #self._button_indicator = (By.XPATH, f"({self._form}//div[contains(@class, 'timepickercontrol')]//button)[5]", "Indicator [Button]")

        self._button_upload = (By.XPATH, f"{self._form}//div[@class='uploadButton']/button", "Upload [Button]")
        self._button_collapse_documents = (By.XPATH, f"{self._form}//a[@aria-controls='tblAttachments']", "Collapse [Button]")

        self._table = "//div[@id='bolAttachments']//table"

        self._button_cancel = (By.XPATH, f"{self._form}//button/span[text()='Cancel']", "Cancel [Button]")
        self._button_save_for_later = (By.XPATH, f"{self._form}//button/span[text()='Save For Later']", "Save For Later [Button]")
        self._button_save_and_submit = (By.XPATH, f"{self._form}//button/span[text()='Save & Submit']", "Save & Submit [Button]")

        # Upload Files Modal
        self._upload_modal = (By.XPATH,"//div[contains(@class,'uploaddoc p-0')]","Upload Modal")
        self._button_add_file = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//a[contains(text(),'Add File +')]", "Add File + [Modal Add File]")
        self._input_add_file = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//input[@type='file']", "File Input Path + [Modal Add File]")
        self._button_close_modal = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//button[@aria-label='Close dialog']", "X Close [Modal Add File]")
        self._button_cancel_modal = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//button/span[text()='Cancel']", "Cancel [Modal Add File]")
        self._button_upload_file_modal = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//button/span[text()='Upload File']", "Upload File [Modal Add File]")
        self._input_description_modal = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//input[@placeholder='Description']", "Description [Modal Add File]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = BidParametersPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def _enter_book_it_now_rate(self, value):
        self.send_keys().set_locator(self._input_book_it_row_rate, self._name).set_text(value)
        return self

    def _enter_bid_expiration_date(self, value):

        self.send_keys().set_locator(self._input_bid_expiration_date, self._name).set_text(value)
        # This is important to Enable the "Continue & Submit" Button
        self.click().set_locator(self._button_data_picker, self._name).single_click().pause(1)
        self.click().set_locator(self._button_today_day, self._name).highlight().single_click().pause(1)

        return self

    def _enter_time(self, hours: str, minutes: str):

        self.send_keys().set_locator(self._input_hours, self._name).clear().set_text(str(hours))
        self.send_keys().set_locator(self._input_minutes, self._name).clear().set_text(str(minutes))

        # CHANGE FOR LOGIB-3445
        '''
        # Gets Current Button Text Indicator
        current_indicator = self.get_text().set_locator(self._button_indicator, self._name).by_text().strip()

        # Compares Indicator Text
        if current_indicator != indicator:
            # Change Button State
            self.click().set_locator(self._button_indicator, self._name).single_click()
            # Verify Indicator State Change
            updated_indicator = self.get_text().set_locator(self._button_indicator).by_text().strip()
            assert updated_indicator == indicator, f"Expected Indicator should be {indicator}, but found {updated_indicator}"
        else:
            logger.info(f"Open Time Indicator state is correct {indicator}")
        '''

    def enter_bid_parameters(self, book_it_now_rate, bid_expiration_date, hours, minutes):
        self._enter_book_it_now_rate(book_it_now_rate)
        self._enter_bid_expiration_date(bid_expiration_date)
        self._enter_time(hours, minutes)
        return self

    def _get_table_cell_date(self, index: int):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{str(index)}]/td[1]", f"Date [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_document_type(self, index: int):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{str(index)}]/td[2]", f"Document Type [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_description(self, index: int):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{str(index)}]/td[3]", f"Description [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_file_name(self, index: int):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{str(index)}]/td[4]", f"File Name [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_table_cell_file_type(self, index: int):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{str(index)}]/td[5]", f"File Type [Table Cell Row {index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_document_item(self, index:int):
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

    def click_cancel(self):
        self.click().set_locator(self._button_cancel, self._name).single_click()
        return self

    def click_save_for_later(self):
        self.click().set_locator(self._button_save_for_later, self._name).single_click()
        return self

    def click_save_and_submit(self):
        self.click().set_locator(self._button_save_and_submit, self._name).single_click().pause(2)
        return self

    def click_add_file(self, file_name: str, description: str):

        # Wait For Modal Should be visible
        self.element().wait_for_element(self.driver, self._upload_modal)

        # Display Temporarily Input Chosen File
        self.element().set_css_property(self._input_add_file, "display: block;")

        # Send Path File
        # self.click().set_locator(self._button_add_file, self._name).single_click().pause(2) # Avoid to Click the "Add File" to not display the dialog box for search the file
        self.upload_file().set_locator(self._input_add_file, self._name).set_file_name(file_name).upload().pause(1)

        # Hidden Temporarily Input Chosen File
        self.element().set_css_property(self._input_add_file, "display: none;")

        # Add some Description to the upload File
        self.send_keys().set_locator(self._input_description_modal, self._name).clear().set_text(description)

        # Click to Upload Current File
        self.click().set_locator(self._button_upload_file_modal, self._name).single_click().pause(2)

