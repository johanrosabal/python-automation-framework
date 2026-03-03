from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('PleaseConfirmYourDetailsPage')


class PleaseConfirmYourDetailsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the PleaseConfirmYourDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Roots
        self._modal = "//app-complete-delivery-confirmation-modal"
        self._table = f"{self._modal}//div[@id='complete-delivery-request-uploadedDocuments-list']//table"

        # Locators
        self._btn_confirm = (By.XPATH, f"{self._modal}//button/span[text()='Confirm']","Confirm [Confirm Your Details Button]")
        self._btn_cancel = (By.XPATH, f"{self._modal}//button/span[text()=' Cancel']", "Confirm [Confirm Your Details Button]")
        self._btn_ok = (By.XPATH, f"//app-shipment-completion-documents-popup//button/span[text()='Ok']", "Confirm [Confirm Your Details Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def is_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Confirm Your Details Modal")
        return self.element().is_present(locator=locator, timeout=5)

    def is_not_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Confirm Your Details Modal")
        return self.element().is_not_visible(locator=locator, timeout=5)

    def get_modal_subtitle_1(self):
        locator = (By.XPATH, f"({self._modal}//h2)[1]", "Sub-Title [Confirm Your Details Modal]")
        return self.get_text().set_locator(locator=locator).by_text()

    def click_modal_subtitle_1(self):
        locator = (By.XPATH, f"({self._modal}//h2)[1]", "Sub-Title [Confirm Your Details Modal]")
        return self.click().set_locator(locator).single_click()

    def get_modal_subtitle_2(self):
        locator = (By.XPATH, f"({self._modal}//h2)[2]", "Sub-Title [Confirm Your DetailsModal]")
        return self.get_text().set_locator(locator=locator).by_text()

    def click_modal_subtitle_2(self):
        locator = (By.XPATH, f"({self._modal}//h2)[2]", "Sub-Title [Confirm Your Details Modal]")
        return self.click().set_locator(locator).single_click()

    def click_confirm(self):
        self.click().set_locator(self._btn_confirm).highlight().single_click().pause(2)
        return self

    def click_ok(self):
        self.click().set_locator(self._btn_ok).highlight().single_click()
        return self

    def click_cancel(self):
        self.click().set_locator(self._btn_cancel).highlight().single_click()
        return self

    def get_table_file_name(self, row_index: int = 1):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{row_index}]/td[1]/div", f"File Name Row [{row_index}]")
        return self.get_text().set_locator(locator).by_text().strip()

    def get_table_document_type(self, row_index: int = 1):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{row_index}]/td[2]", f"Document Type Row [{row_index}]")
        return self.get_text().set_locator(locator).by_text().strip()

    def get_table_description(self, row_index: int = 1):
        locator = (By.XPATH, f"{self._table}/tbody/tr[{row_index}]/td[3]", f"Description Row [{row_index}]")
        return self.get_text().set_locator(locator).by_text().strip()
