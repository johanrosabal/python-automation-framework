from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('UploadFilesModal')


class UploadFilesModal(BasePage):

    def __init__(self, driver):
        """
        Initialize the UploadFilesModal instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._modal = "//div[contains(@class,'mdc-dialog__container')]//upload-documents"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def is_upload_files_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Upload Files Modal")
        return self.element().is_present(locator=locator, timeout=5)

    def is_upload_files_not_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Upload Files Modal")
        return self.element().is_not_visible(locator=locator, timeout=5)

    def get_modal_title(self):
        locator = (By.XPATH, f"{self._modal}//h4", "Title [Upload Files Modal]")
        return self.get_text().set_locator(locator=locator).by_text()

    def click_add_file(self, file_name: str, description: str):
        # locator = (By.XPATH, f"{self._modal}//a[text()='Add File +']", "Submit [Complete Delivery Modal Button]")
        # self.click().set_locator(locator).highlight().single_click()
        input_add_file = (By.XPATH, f"{self._modal}//input[@type='file']", "Input Add File")
        input_description_modal = (By.XPATH, f"{self._modal}//input[@type='text'][@placeholder='Description']","Description Add File")

        # Wait For Modal Should be visible
        self.is_upload_files_visible()

        # Display Temporarily Input Chosen File
        self.element().set_css_property(input_add_file, "display: block;")

        # Send Path File
        self.upload_file().set_locator(input_add_file, self._name).set_file_name(file_name).upload().pause(1)

        # Hidden Temporarily Input Chosen File
        self.element().set_css_property(input_add_file, "display: none;")

        # Add some Description to the upload File
        self.send_keys().set_locator(input_description_modal, self._name).clear().set_text(description)

        return self

    def click_upload_file(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='Upload File']", "Submit [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def click_cancel(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()='Cancel']", "Cancel [Complete Delivery Modal Button]")
        self.click().set_locator(locator).highlight().single_click()
        return self
