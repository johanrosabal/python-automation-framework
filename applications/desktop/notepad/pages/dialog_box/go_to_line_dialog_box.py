from appium.webdriver.common.appiumby import AppiumBy as By
from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
from core.desktop.actions.XPath import XPath
logger = setup_logger('GoToLineDialogBox')


class GoToLineDialogBox:

    def __init__(self, driver):
        self._driver = driver
        self._input_go_to_line = XPath().automation_id("258")
        self._btn_go_to = (By.NAME, "Go To")
        self._btn_cancel = (By.NAME, "Cancel")

    def enter_line_number(self, text: str = 1):
        logger.info(f"Go to line: '{text}'")
        element = Element(self._driver).wait_for_element(self._input_go_to_line)
        element.clear()
        element.send_keys(text)
        return self

    def click_go_to(self):
        logger.info(f"Go to Button")
        Element(self._driver).wait_for_element(self._btn_go_to).click()
        return self

    def click_cancel(self):
        logger.info(f"Cancel Button")
        Element(self._driver).wait_for_element(self._btn_cancel).click()
        return self

