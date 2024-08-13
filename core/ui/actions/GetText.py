from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('GetText')


class GetText:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._text = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def by_text(self):
        if self._element:
            return self._element.text
        else:
            logger.error("No text value found.")

    def by_attribute(self, attribute="value"):
        if self._element:
            return self._element.get_attribute(attribute)
        else:
            logger.error("No attribute value found.")

    def trim(self):
        if self._element:
            return self._element.text.rstrip()
        else:
            logger.error("No attribute value found.")