from appium.webdriver.common.appiumby import AppiumBy as By
from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
from core.desktop.actions.XPath import XPath
logger = setup_logger('ReplaceDialogBox')


class ReplaceDialogBox:

    def __init__(self, driver):
        self._driver = driver
        self._input_find_what = XPath().automation_id("1152")
        self._input_replace_with = XPath().automation_id("1153")
        self._btn_find_next = (By.NAME, "Find Next")
        self._btn_replace = XPath().automation_id("1024")
        self._btn_replace_all = (By.NAME, "Replace All")
        self._btn_cancel = (By.NAME, "Cancel")
        self._checkbox_match_case = (By.NAME, "Match case")
        self._checkbox_wrap_around = (By.NAME, "Wrap around")

    def find_what(self, text: str):
        logger.info(f"Find What: '{text}'")
        element = Element(self._driver).wait_for_element(self._input_find_what)
        element.clear()
        element.send_keys(text)
        return self

    def replace_with(self, text: str):
        logger.info(f"Replace with: '{text}'")
        element = Element(self._driver).wait_for_element(self._input_replace_with)
        element.clear()
        element.send_keys(text)
        return self

    def click_find_next(self):
        logger.info(f"Find Next Button")
        Element(self._driver).wait_for_element(self._btn_find_next).click()
        return self

    def click_replace(self):
        logger.info(f"Replace Button")
        element = Element(self._driver).wait_for_element(self._btn_replace)
        element.click()
        return self

    def click_replace_all(self):
        logger.info(f"Replace All Button")
        Element(self._driver).wait_for_element(self._btn_replace_all).click()
        return self

    def click_cancel(self):
        logger.info(f"Cancel Button")
        Element(self._driver).wait_for_element(self._btn_cancel).click()
        return self

    def click_match_case(self):
        logger.info(f"Match Case CheckBox")
        Element(self._driver).wait_for_element(self._checkbox_match_case).click()
        return self

    def click_wrap_around(self):
        logger.info(f"Wrap Around CheckBox")
        Element(self._driver).wait_for_element(self._checkbox_wrap_around).click()
        return self
