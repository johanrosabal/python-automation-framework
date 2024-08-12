from selenium.webdriver import Keys
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('SendKeys')


class SendKeys:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._text = None
        self._clear = None
        self._pause = None
        self._special_characters = None

    def set_locator(self,locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def set_text(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        self._element.send_keys(text)
        return self

    def set_text_by_character(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        letters = list(text)
        for letter in letters:
            self._element.send_keys(letter)

        return self

    def get_text(self):
        if self._element:
            input_value = self._element.get_attribute('value')
            logger.info(" Send Keys: Get Element Value: " + input_value)
            return input_value

    def clear(self):
        logger.info(" Send Keys: Press [RETURN] Keyboard Button")
        if self._element:
            self._element.click()
            self._element.clear()

    def press_return(self):
        logger.info(" Send Keys: Press [RETURN] Keyboard Button")
        if self._element:
            self._element.send_keys(Keys.RETURN)

    def press_enter(self):
        logger.info(" Send Keys: Press [ENTER] Keyboard Button")
        if self._element:
            self._element.send_keys(Keys.ENTER)

    def press_backspace(self):
        logger.info(" Send Keys: Press [BACKSPACE] Keyboard Button")
        if self._element:
            self._element.send_keys(Keys.BACKSPACE)

    def press_tab(self):
        logger.info(" Send Keys: Press [TAB] Keyboard Button")
        if self._element:
            self._element.send_keys(Keys.TAB)

    def press_escape(self):
        logger.info(" Send Keys: Press [ESCAPE] Keyboard Button")
        if self._element:
            self._element.send_keys(Keys.ESCAPE)

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self
