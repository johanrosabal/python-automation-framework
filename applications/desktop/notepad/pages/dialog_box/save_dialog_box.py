from appium.webdriver.common.appiumby import AppiumBy as By
from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
from core.desktop.actions.XPath import XPath

logger = setup_logger('SaveDialogBox')


class SaveDialogBox:

    def __init__(self, driver):
        self._driver = driver
        self._input_file_name = XPath().automation_id("1001")
        self._btn_save = (By.NAME, "Save")
        self._btn_dont_save = (By.NAME, "Don't Save")
        self._btn_cancel = (By.NAME, "Cancel")

    def enter_file_name(self, file_name: str):
        Element(self._driver).wait_for_element(self._input_file_name).send_keys(file_name)
        return self

    def click_save(self):
        logger.info("Click 'Save' Button")
        Element(self._driver).wait_for_element(self._btn_save).click()
        return self

    def click_dont_save(self):
        logger.info("Click 'Don't Save' Button")
        Element(self._driver).wait_for_element(self._btn_dont_save).click()
        return self

    def click_cancel(self):
        logger.info("Click 'Cancel' Button")
        Element(self._driver).wait_for_element(self._btn_cancel).click()
        return self

