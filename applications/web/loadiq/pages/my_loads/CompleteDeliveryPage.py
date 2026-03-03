from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CompleteDeliveryPage')


class CompleteDeliveryPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the CompleteDeliveryPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._modal = "//div[contains(@class,'mat-mdc-dialog-panel')]"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def is_complete_delivery_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Complete Delivery Modal")
        return self.element().is_present(locator=locator, timeout=5)

    def is_complete_delivery_not_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Complete Delivery Modal")
        return self.element().is_not_visible(locator=locator, timeout=5)

    def get_modal_title(self):
        locator = (By.XPATH, f"{self._modal}//h4", "Title [Complete Delivery Modal]")
        return self.get_text().set_locator(locator=locator).by_text()

    def get_modal_subtitle_1(self):
        locator = (By.XPATH, f"({self._modal}//h2)[1]", "Sub-Title [Complete Delivery Modal]")
        return self.get_text().set_locator(locator=locator).by_text()

    def click_modal_subtitle_1(self):
        locator = (By.XPATH, f"({self._modal}//h2)[1]", "Sub-Title [Complete Delivery Modal]")
        return self.click().set_locator(locator).single_click()

    def get_modal_subtitle_2(self):
        locator = (By.XPATH, f"({self._modal}//h2)[2]", "Sub-Title [Complete Delivery Modal]")
        return self.get_text().set_locator(locator=locator).by_text()

    def click_modal_subtitle_2(self):
        locator = (By.XPATH, f"({self._modal}//h2)[2]", "Sub-Title [Complete Delivery Modal]")
        return self.click().set_locator(locator).single_click()

    def click_yes(self):
        locator = (By.XPATH, f"{self._modal}/button/span[text()='Yes']", "Yes [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def click_no(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='No']", "No [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def click_upload_file(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='Upload File']", "Upload File [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def click_add_more_files(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='Add More Files']", "Submit [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def click_submit(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='Submit']", "Submit [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def click_cancel(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='Cancel']", "Cancel [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def get_error_message(self):
        locator = (By.XPATH, f"{self._modal}//div[contains(@class,'errorMessage')]/p")
        return self.get_text().set_locator(locator).by_text()

    def get_table_file_name(self, row_index: int = 1):
        locator = (By.XPATH, f"//complete-delivery-uploaded-document-list//table/tbody/tr[{row_index}]/td[1]/div", f"File Name Row [{row_index}]")
        return self.get_text().set_locator(locator).by_text().strip()

    def get_table_document_type(self, row_index: int = 1):
        locator = (By.XPATH, f"//complete-delivery-uploaded-document-list//table/tbody/tr[{row_index}]/td[2]", f"Document Type Row [{row_index}]")
        return self.get_text().set_locator(locator).by_text().strip()

    def get_table_description(self, row_index: int = 1):
        locator = (By.XPATH, f"//complete-delivery-uploaded-document-list//table/tbody/tr[{row_index}]/td[3]", f"Description Row [{row_index}]")
        return self.get_text().set_locator(locator).by_text().strip()

    def click_table_remove_file(self, row_index: int = 1):
        locator = (By.XPATH, f"//complete-delivery-uploaded-document-list//table/tbody/tr[{row_index}]/td[4]//a", f"Remove File Row [{row_index}]")
        self.click().set_locator(locator).single_click()
        return self


