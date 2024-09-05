from appium.webdriver.common.appiumby import AppiumBy as By
from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element

logger = setup_logger('AboutNotepadDialogBox')


class AboutNotepadDialogBox:

    def __init__(self, driver):
        self._driver = driver
        self._btn_ok = (By.NAME, "OK")

    def click_ok(self):
        logger.info("Click 'Ok' Button")
        Element(self._driver).wait_for_element(self._btn_ok).click()
