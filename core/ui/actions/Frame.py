from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('Click')


class Frame:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def switch_to(self):
        if self._driver:
            self._driver.switch_to.frame(self._element)
        else:
            logger.error("Unable to Switch to Element WebDriver is None.")

        return self

    def switch_to_default(self):
        if self._driver:
            logger.info("Switch to Default Content")
            self._driver.switch_to.default_content()
        else:
            logger.error("Unable to Switch to Element WebDriver is None.")
        return self
