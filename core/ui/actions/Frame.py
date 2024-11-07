from core.config.logger_config import setup_logger
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Screenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('Frame')


class Frame:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
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

    def screenshot(self, name="screenshot"):
        Screenshot(self._driver).set_locator(self._locator, self._page).attach_to_allure(name)
        return self

    def highlight(self, duration=1):
        ElementHighlighter(self._driver).set_locator(self._locator).highlight_temporarily(duration)
        return self
