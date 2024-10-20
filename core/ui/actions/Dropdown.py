from selenium.webdriver.support.select import Select

from core.config.logger_config import setup_logger
from core.ui.actions.Screeenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('Dropdown')


class Dropdown:

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

    def by_value(self, value: str):
        if self._element:
            select = Select(self._element)
            select.select_by_value(value)
        else:
            logger.error("Unable to Find Dropdown Option by Value WebElement is None.")
        return self

    def by_index(self, index: int):
        if self._element:
            select = Select(self._element)
            select.select_by_index(index)
        else:
            logger.error("Unable to Find Dropdown Option by Index WebElement is None.")
        return self

    def by_text(self, text: str):
        if self._element:
            select = Select(self._element)
            select.select_by_visible_text(text)
        else:
            logger.error("Unable to Find Dropdown Option by Text WebElement is None.")
        return self

    def by_text_contains(self, search_text: str):
        if self._element:
            options = Select(self._element).options
            for option in options:
                if search_text in option.text:
                    option.click()
                    logger.info("Dropdown Option Found: "+option.text)
                    break
            else:
                logger.error("Dropdown Option Not Found: "+search_text)
        return self

    def deselect_all(self):
        if self._element:
            select = Select(self._element)
            select.deselect_all()
        else:
            logger.error("Unable to Find Dropdown Deselect WebElement is None.")
        return self

    def screenshot(self, name="screenshot"):
        Screenshot(self._driver).set_locator(self._locator, self._page).attach_to_allure(name)
        return self
