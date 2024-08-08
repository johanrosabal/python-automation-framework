from selenium.webdriver import Keys

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('SendKeys')


class SendKeys:

    def __init__(self, driver):
        self.__driver = driver
        self.__element = None
        self.__text = None
        self.__clear = None
        self.__pause = None
        self.__special_characters = None

    def set_locator(self, locator: tuple):
        by, value = locator
        self.__element = self.__driver.find_element(by, value)
        return self

    def set_text(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        self.__element.send_keys(text)
        return self

    def set_text_by_character(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        letters = list(text)
        for letter in letters:
            self.__element.send_keys(letter)

        return self

    def get_text(self):
        if self.__element:
            input_value = self.__element.get_attribute('value')
            logger.info(" Send Keys: Get Element Value: " + input_value)
            return input_value

    def clear(self):
        logger.info(" Send Keys: Press [RETURN] Keyboard Button")
        if self.__element:
            self.__element.click()
            self.__element.clear()

    def press_return(self):
        logger.info(" Send Keys: Press [RETURN] Keyboard Button")
        if self.__element:
            self.__element.send_keys(Keys.RETURN)

    def press_enter(self):
        logger.info(" Send Keys: Press [ENTER] Keyboard Button")
        if self.__element:
            self.__element.send_keys(Keys.ENTER)

    def press_backspace(self):
        logger.info(" Send Keys: Press [BACKSPACE] Keyboard Button")
        if self.__element:
            self.__element.send_keys(Keys.BACKSPACE)

    def press_tab(self):
        logger.info(" Send Keys: Press [TAB] Keyboard Button")
        if self.__element:
            self.__element.send_keys(Keys.TAB)

    def press_escape(self):
        logger.info(" Send Keys: Press [ESCAPE] Keyboard Button")
        if self.__element:
            self.__element.send_keys(Keys.ESCAPE)

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self
