from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('Radio')


class Radio:

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

    def is_displayed(self):
        value = False
        if self._element:
            value = self._element.is_displayed()
            logger.info("Radio button displayed value ["+value+"]")
        else:
            logger.error("Unable to Display Value Radio WebElement is None.")
        return value

    def is_selected(self):
        value = False
        if self._element:
            value = self._element.is_selected()
            logger.info("Radio button selected value [" + value + "]")
        else:
            logger.error("Unable to Selected Value Radio WebElement is None.")
        return value

    def set_value(self, value: bool):

        if self._element:

            selected = self._element.is_selected()
            if not selected and value:
                self._element.click()
            else:
                if selected and not value:
                    self._element.click()
        else:
            logger.error("Unable to Select Radio WebElement is None.")

        return self
