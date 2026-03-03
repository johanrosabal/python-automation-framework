from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('DocumentsDetailsTab')


class DocumentsDetailsTab(BasePage):

    def __init__(self, driver):
        """
        Initialize the DocumentsDetailsTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/bookingDetail?id={ID}"
        # Locator definitions
        self._div_document_item = "//div[@role='tabpanel']/div[contains(@class,'booking-list-data-row')]"

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

    def get_document_name(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[2]/div[2]", f"Document Name [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_document_type(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[3]/div/div", f"Document Type [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_customer_doc_send_date_time(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[4]/div/div", f"Customer Doc Send Date/Time [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_freighted(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[5]/div/div", f"Freighted [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_show_excluded_charges(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[6]/div/div", f"Show Excluded Charges [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_account_name(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[7]/div/div", f"Account Name [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_customer_contact_name(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[8]/div/div", f"Customer Contact Name [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_customer_contact_email(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[9]/div/div", f"Customer Contact Email [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_original_bol_complete(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[10]/div/div", f"Original Bol Complete [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_uploaded_downloaded_on(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[11]/div/div", f"Uploaded/Downloaded On [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_uploaded_downloaded_by(self, index):
        locator = (By.XPATH, f"({self._div_document_item})[{index}]/div[12]/div/div", f"Uploaded/Downloaded By [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()
