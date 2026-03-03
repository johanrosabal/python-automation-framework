from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ConfirmationDialogModal')


class ConfirmationDialogModal(BasePage):

    def __init__(self, driver):
        """
        Initialize the ConfirmationDialogModal instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/web/index.php/auth/login"
        # Root
        self._modal = "//app-confirmation-dialog"
        # Locator definitions
        self._btn_my_payments = (By.XPATH, f"{self._modal}//button/span[text()='My Payments']", "My Payments [Button]")
        self._btn_my_loads = (By.XPATH, f"{self._modal}//button/span[text()='My Payments']", "My Payments [Button]")
        self._btn_close = (By.XPATH, f"{self._modal}//button[contains(@class,'close')]", "Close [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def is_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Confirmation Modal")
        return self.element().is_present(locator=locator, timeout=5)

    def is_not_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Confirmation Modal")
        return self.element().is_not_visible(locator=locator, timeout=5)

    def get_title(self):
        locator = (By.XPATH, f"{self._modal}//h4", "Title")
        return self.get_text().set_locator(locator=locator).by_text()

    def get_confirmation_description(self):
        locator = (By.XPATH, f"{self._modal}//h4/../span", "Title")
        return self.get_text().set_locator(locator=locator).by_text()

    def click_my_payments(self):
        self.element().is_present(locator=self._btn_my_payments, timeout=5)
        self.click().set_locator(self._btn_my_payments).single_click()
        return self

    def click_my_loads(self):
        self.element().is_present(locator=self._btn_my_loads, timeout=5)
        self.click().set_locator(self._btn_my_loads).single_click()
        return self

    def click_close(self):
        self.element().is_present(locator=self._btn_close, timeout=5)
        self.click().set_locator(self._btn_close).single_click()
        return self
