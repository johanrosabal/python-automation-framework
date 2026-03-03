from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('FeedbackForm')


class FeedbackForm(BasePage):

    def __init__(self, driver):
        """
        Initialize the FeedbackForm instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/load-board"
        # Locator definitions
        self._btn_my_button = (By.XPATH, "//div[@id='mybutton']/button", "My Button [Button]")
        self._input_username = (By.XPATH, "//label[text()='Username']/..//input", "Username [Input]")
        self._input_comment = (By.XPATH, "//label[text()='Comment']/..//div[@class='note-editing-area']//textarea", "Comment [Input]")
        self._input_editable_div = (By.XPATH, "//label[text()='Comment']/..//div[@class='note-editable']", "Comment Editable Area")
        self._btn_submit = (By.XPATH, "//button[@data-cy='feedbacksubmit']", "Submit [Button]")
        self._btn_cancel = (By.XPATH, "//button[@data-cy='feedbackclose']", "Cancel [Button]")
        self._btn_close = (By.XPATH, "//span[@class='closebtn']", "Close [Close Modal Form]")
        self._modal_form = (By.XPATH, "//div[contains(@class,'feebackformshow')]", "Modal Form [Modal]")

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
        return self.element().set_locator(self._modal_form, self._name).is_visible()

    def is_not_visible(self):
        return self.element().is_not_visible(locator=self._modal_form, timeout=10)

    def enter_username(self, text: str = None):
        self.send_keys().set_locator(self._input_username, self._name).set_text(text)
        return self

    def enter_comments(self, text: str = None):
        self.element().is_present(locator=self._input_editable_div, timeout=10)
        self.send_keys().set_locator(self._input_editable_div, self._name).set_text(text)
        self.screenshot().attach_to_allure(name="Feedback Form Comment Entered")
        return self

    def click_feedback_form(self):
        self.click().set_locator(self._btn_my_button, self._name).single_click()
        return self

    def click_submit(self):
        self.click().set_locator(self._btn_submit, self._name).single_click()
        self.is_not_visible()
        return self

    def click_cancel(self):
        self.click().set_locator(self._btn_cancel, self._name).single_click()
        return self

