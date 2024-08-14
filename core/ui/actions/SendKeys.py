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

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def set_text(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        if self._element:
            logger.info("Send Keys ["+text+"]")
            self._element.send_keys(text)
        else:
            logger.error("Unable to Send Text [" + text + "] element is None")
        return self

    def set_text_by_character(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        letters = list(text)
        if self._element:
            logger.info("Send Keys [" + text + "] by Character.")
            for letter in letters:
                logger.info("Send Keys Letter [" + letter + "].")
                self._element.send_keys(letter)
        else:
            logger.error("Unable to Send Text By Character [" + text + "] element is None.")
        return self

    def get_text(self):
        if self._element:
            input_value = self._element.get_attribute('value')
            logger.info("Get Element Value: " + input_value)
            return input_value

    def clear(self):
        if self._element:
            logger.info("Press [RETURN] Keyboard Button.")
            self._element.click()
            self._element.clear()
        else:
            logger.error("Unable to Clear Element Web Element is None.")

    def press_return(self):
        if self._element:
            logger.info("Press [RETURN] Keyboard Button.")
            self._element.send_keys(Keys.RETURN)
        else:
            logger.error("Unable to Press [RETURN] element is None.")

    def press_enter(self):
        if self._element:
            logger.info("Press [ENTER] Keyboard Button.")
            self._element.send_keys(Keys.ENTER)
        else:
            logger.error("Unable to Press [ENTER] element is None.")

    def press_backspace(self):
        if self._element:
            logger.info("Press [BACKSPACE] Keyboard Button.")
            self._element.send_keys(Keys.BACKSPACE)
        else:
            logger.error("Unable to Press [BACKSPACE] element is None.")

    def press_tab(self):
        if self._element:
            logger.info("Press [TAB] Keyboard Button.")
            self._element.send_keys(Keys.TAB)
        else:
            logger.error("Unable to Press [TAB] element is None.")

    def press_escape(self):
        if self._element:
            logger.info("Press [ESCAPE] Keyboard Button")
            self._element.send_keys(Keys.ESCAPE)
        else:
            logger.error("Unable to Press [ESCAPE] element is None.")

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self
