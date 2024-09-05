from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
from selenium.webdriver import Keys
from selenium.webdriver import ActionChains

logger = setup_logger('SendKeys')


class SendKeys:

    def __init__(self, driver):
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple):
        self._element = Element(self._driver).wait_for_element(locator)
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

    def set_text_with_action_chain(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        if self._element:
            logger.info("Send Keys ["+text+"]")
            actions = ActionChains(self._driver)
            actions.send_keys_to_element(self._element, text).perform()
        else:
            logger.error("Unable to Send Text with Action Chain [" + text + "] element is None")
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

    def set_value(self, text: str):
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        if self._element:
            logger.info("Send Keys Set Value ["+text+"]")
            self._element.set_value(text)
        else:
            logger.error("Unable to Set Value [" + text + "] element is None")
        return self

    def clear(self):
        if self._element:
            logger.info("Press [CLEAR] Keyboard Button.")
            self._element.click()
            self._element.clear()
        else:
            logger.error("Unable to Clear Element Web Element is None.")

    def paste_clipboard_text(self):
        if self._element:
            logger.info("Paste Clipboard Text.")
            self._element.send_keys(Keys.CONTROL, 'v')
        else:
            logger.error("Unable to Paste Text Element Web Element is None.")

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