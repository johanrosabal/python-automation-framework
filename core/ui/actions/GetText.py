from core.config.logger_config import setup_logger
from core.ui.actions.Screeenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('GetText')


class GetText:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._text = None
        self._locator = None
        self._page = None

    def set_locator(self, locator: tuple, page='Page'):
        self._locator = locator
        self._page = page
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(self._page, self._name, locator))
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def by_text(self):
        if self._element:
            text = self._element.text
            logger.info("Getting Text ["+text+"]")
            return text
        else:
            logger.error("Unable to get text WebElement is None.")

    def by_attribute(self, attribute="value"):
        if self._element:
            try:
                return self._element.get_attribute(attribute)
            except Exception as e:
                logger.error(f"Exception occurred while getting attribute '{attribute}': {e}")
        else:
            logger.error("Unable to get text by attribute WebElement is None.")

    def trim(self):
        if self._element:
            return self._element.text.rstrip()
        else:
            logger.error("Unable to Trim Text WebElement is None.")

    def screenshot(self, name="screenshot"):
        Screenshot(self._driver).set_locator(self._locator, self._page).attach_to_allure(name)
        return self
