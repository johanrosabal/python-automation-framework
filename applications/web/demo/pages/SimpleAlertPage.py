from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SimpleAlertPage')


class SimpleAlertPage(BasePage):
    base_url = "https://www.w3schools.com"

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative_alert = "/js/tryit.asp?filename=tryjs_alert"
        self.relative_prompt = "/js/tryit.asp?filename=tryjs_prompt"
        # Locator definitions
        self._frame_content = (By.XPATH, "//iframe[@id='iframeResult']", "Frame Content")
        self._btn_try_it = (By.XPATH, "//button[@onclick='myFunction()']", "Try it Button")
        self._txt_demo = (By.ID,"demo","Demo Text")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = SimpleAlertPage(BaseApp.get_driver())
            cls.name = __class__.__name__
        return cls._instance

    def load_alert_page(self):
        self.go(self.base_url, self.relative_alert)
        return self

    def load_prompt_page(self):
        self.go(self.base_url, self.relative_prompt)
        return self

    def click_try_it(self):
        # Switch to IFrame
        self.frame().set_locator(self._frame_content, self.name).switch_to().pause(2)

        (self.click_element()
         .set_locator(self._btn_try_it, self.name)
         .single_click()
         .pause(3))
        return self

    def get_alert_text(self):
        return self.alert().get_text()

    def get_demo_text(self):
        return self.get_text().set_locator(self._txt_demo,self.name).by_text()

    def click_alert_accept(self):
        self.alert().simple_accept()
        return self

    def click_prompt_accept(self):
        self.alert().confirm_accept()
        return self

    def click_prompt_cancel(self):
        self.alert().confirm_cancel()
        return self

    def enter_prompt_text(self, text: str):
        self.alert().send_keys(text)
        return self

    def verify_alert_text(self, text: str):
        actual = self.get_alert_text()
        AssertCollector.assert_equal_message(text, actual, "Alert text match.")
        return self

    def verify_demo_text(self, text: str):
        actual = self.get_demo_text()
        AssertCollector.assert_equal_message(text, actual, "Alert Demo text match.")
