from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
logger = setup_logger('GetText')


class GetText:

    def __init__(self, driver):
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple):
        self._element = Element(self._driver).wait_for_element(locator)
        return self

    def by_text(self):
        if self._element:
            text = self._element.text
            logger.info("Getting Text ["+text+"]")
            return text
        else:
            logger.error("Unable to get Text Element is None.")
