from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.actions.Click import Click
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Scroll import Scroll
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.SendKeys import SendKeys
from core.ui.actions.Element import Element

# Logger setup for 'SendKeys' operations
logger = setup_logger('SendKeysWithIndex')


class SendKeysWithIndex:
    """
    The SendKeys class handles actions to send text and key inputs to web elements.

    Attributes:
        _name (str): Name of the class, used for logging.
        _driver (WebDriver): The WebDriver instance.
        _element (WebElement): The targeted element to interact with.
        _text (str): Text to send to the element.
        _clear (bool): Flag to indicate if the element should be cleared.
        _pause (int): Optional pause duration for actions.
    """

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._text = None
        self._clear = None
        self._pause = None
        # self._special_characters = None
        self._locator_label = None
        self._locator = None
        # self._page = None
        # self._page = None

    def set_locator(self, index=1, label: str = None, explicit_wait=10):
        """
        Set the locator for the autocomplete input field using the label

        This method waits for the element to be present on the page and logs the operation.

        :param index: Index value for autocomplete web element, default 1
        :param label: Label String to identify the Parent Container and find the Input Box
        :param explicit_wait: Wait Explicit Time after send text to the element
        :return: Returns self for method chaining.
        """
        # Root Locator String
        xpath = f"(//label[contains(text(),'{label}')])[{str(index)}]/..//input"
        locator = (By.XPATH, xpath, f"Label: {label}, Index: {index} [Label Locator]")
        self._locator = locator
        # Dynamic Locator for Label value
        self._element = Element.wait_for_element(driver=self._driver, locator=locator, timeout=explicit_wait)
        self._locator_label = True
        return self

    def clear(self):
        """Clears the text from the element."""
        if self._element:
            logger.info("Clearing text from element.")
            self._element.click()
            self._element.clear()
        else:
            logger.error("Unable to clear element: element is None.")
        return self

    def pause(self, seconds: int):
        """Pauses the execution for a given number of seconds."""
        BaseApp.pause(seconds)
        return self

    def highlight(self, duration=1):
        if self._element:
            ElementHighlighter(self._driver).set_locator(self._locator).highlight_temporarily(duration)
        return self

    def by_text(self, text: str):

        if self._element:
            if self._locator_label:
                # Input Text Value
                Scroll(self._driver).set_element(self._element).to_element(pixels=-100)
                SendKeys(self._driver).set_element(self._element).set_text(text)
                # Select value from Dropdown
        return self


