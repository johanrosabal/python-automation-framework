from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('SendKeys')


class Click:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self,locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def single_click(self):
        if self._element:
            self._element.click()
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self
