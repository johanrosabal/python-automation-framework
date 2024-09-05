from appium.webdriver.common.appiumby import AppiumBy as By
from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
from core.desktop.actions.XPath import XPath

logger = setup_logger('FindDialogBox')


class FindDialogBox:

    def __init__(self, driver):
        self._driver = driver
        self._input_find_what = XPath().automation_id("1152")
        self._btn_find_next = (By.NAME, "Find Next")
        self._btn_cancel = (By.NAME, "Cancel")
        self._radio_up = (By.NAME, "Up")
        self._radio_down = (By.NAME, "Down")
        self._checkbox_match_case = (By.NAME, "Match case")
        self._checkbox_wrap_around = (By.NAME, "Wrap around")

    def find_what(self, text: str):
        logger.info(f"Find What: '{text}'")
        element = Element(self._driver).wait_for_element(self._input_find_what)
        element.clear()
        element.send_keys(text)
        return self

    def click_find_next(self):
        logger.info(f"Find Next Button")
        Element(self._driver).wait_for_element(self._btn_find_next).click()
        return self

    def click_cancel(self):
        logger.info(f"Cancel Button")
        Element(self._driver).wait_for_element(self._btn_cancel).click()
        return self

    def click_up(self):
        logger.info(f"Up Button")
        Element(self._driver).wait_for_element(self._radio_up).click()
        return self

    def click_down(self):
        logger.info(f"Down Button")
        Element(self._driver).wait_for_element(self._radio_down).click()
        return self

    def click_match_case(self):
        logger.info(f"Match Case CheckBox")
        Element(self._driver).wait_for_element(self._checkbox_match_case).click()
        return self

    def click_wrap_around(self):
        logger.info(f"Wrap Around CheckBox")
        Element(self._driver).wait_for_element(self._checkbox_wrap_around).click()
        return self
