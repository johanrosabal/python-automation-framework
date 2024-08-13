from selenium.webdriver.support.select import Select

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('Dropdown')


class Dropdown:

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

    def by_value(self, value: str):
        if self._element:
            select = Select(self._element)
            select.select_by_value(value)
        return self

    def by_index(self, index: int):
        if self._element:
            select = Select(self._element)
            select.select_by_index(index)
        return self

    def by_text(self, text: str):
        if self._element:
            select = Select(self._element)
            select.select_by_visible_text(text)
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
        return self
