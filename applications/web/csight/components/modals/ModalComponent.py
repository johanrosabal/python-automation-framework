from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.components.loadings.Loadings import Loadings
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ModalComponent')


class ModalComponent(BasePage):

    def __init__(self, driver):
        """
        Initialize the ModalComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/web/index.php/auth/login"
        # Locator definitions
        self._locator_1 = (By.NAME, "...", "Input Locator_1")
        # Modal
        self._modal = (By.XPATH, "//section[@aria-modal='true'] | //div[contains(@class, 'modal__content') or contains(@class, 'modalContent')]", "Modal Displayed [Modal]")
        self._modal_close = (By.XPATH,"//section[@aria-modal='true']//i[contains(@class,'close-dlg')]", "[Close Modal]")
        self._modal_content = "//div[contains(@class, 'modal__content') or contains(@class, 'modalContent')]"
        # Sub-Components
        self.buttons = Buttons.get_instance()
        self.loadings = Loadings.get_instance()

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

    def is_visible(self):
        return self.element().set_locator(self._modal).is_visible()

    def get_title_contains(self ):
        locator = (By.XPATH, "//section[@aria-modal='true']//h5", "Title h5 Message [Popup]")
        return self.get_text().set_locator(locator).by_text()

    def click_close(self):
        self.click().set_locator(self._modal_close).single_click()
        return self

    def get_booking_number(self):
        xpath = f"{self._modal_content}/div//span[contains(text(),'Booking Number')]/..//span/b"
        locator = (By.XPATH,xpath, "Booking Number [Modal]")
        return self.get_text().set_locator(locator).by_text().replace("\"","")

    def get_booking_status(self):
        xpath = f"{self._modal_content}/div//span[contains(text(),'Booking Status')]/..//span/b"
        locator = (By.XPATH,xpath, "Booking Status [Modal]")
        return self.get_text().set_locator(locator).by_text()

    def get_booking_reason(self):
        xpath = f"{self._modal_content}/div//span[contains(text(),'Reason')]/..//span[2]/b/span"
        locator = (By.XPATH, xpath, "Booking Reason [Modal]")
        return  self.get_text().set_locator(locator).by_text()

    def get_booking_reason_text(self):
        xpath = f"{self._modal_content}/div//span[contains(text(),'Reason')]/..//p"
        locator = (By.XPATH,xpath, "Booking Reason Text [Modal - Paragraph]")
        return self.get_text().set_locator(locator).by_text()

    def get_modal_title(self):
        xpath = f"{self._modal_content}/div[2]/div/h5"
        locator = (By.XPATH, xpath, "Modal Title Text [Modal - Title]")
        return self.get_text().set_locator(locator).by_text()

    def get_modal_event_number(self):
        xpath = f"{self._modal_content}/div[2]/div[2]//a"
        locator = (By.XPATH, xpath, "Modal Event Number Text [Event Number]")
        return self.get_text().set_locator(locator).by_text()

    def click_modal_event_number(self):
        xpath = f"{self._modal_content}/div[2]/div[2]//a"
        locator = (By.XPATH, xpath, "Modal Event Number Text [Event Number]")
        self.element().set_locator(locator).is_visible()
        self.click().set_locator(locator).single_click()
        self.loadings.is_not_visible_spinner()
        return self

    def get_modal_message(self):
        xpath = f"{self._modal_content}/div/p"
        locator = (By.XPATH, xpath, "Modal Paragraph Text [Modal - Paragraph]")
        return self.get_text().set_locator(locator).by_text()

    def click_proceed(self):
        self.buttons.click_proceed()
        return self

    def click_ok(self):
        self.buttons.click_ok()
        return self

    def click_remove(self):
        self.buttons.click_remove()
        return self

    def click_go_event_list(self):
        self.buttons.click_go_to_event_list()
        return self

    def click_create_new_at_this_location(self):
        self.buttons.click_create_new_at_this_location()
        return self

    def click_create_new(self):
        self.buttons.click_create_new()
        return self


