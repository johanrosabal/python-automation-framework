# (//legend[text()='Hazardous Booking'])[1]/../..//input[@value='NO']
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
logger = setup_logger('CheckboxWithIndex')


class CheckboxWithIndex:

    """
    The CheckboxWithIndex class handles actions to with Check Elements in a List Container
    """

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator_label = None
        self._xpath = None
        self._label = None
        self._index = None
        self._explicit_wait = 0
        self._locator = None

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
        self._xpath = f"(//label[text()='{str(label)}'] | //label/span[text()='{str(label)}'])[{str(index)}]/../.."
        self._label = label
        self._index = index
        self._explicit_wait = explicit_wait
        self._locator_label = True
        return self

    def click(self):
        # Click Checkbox According to Index Value and Label Locator
        locator = (By.XPATH, f"{self._xpath}//span[contains(@part,'indicator')]", f"Checkbox with index[{self._index}]: label: {self._label}")
        if Element(self._driver).set_locator(locator).is_enabled():
            Click(self._driver).set_locator(locator, self._name).single_click()
        else:
            logger.warning(f"Element is not enable to be clickable: {locator[:2]}")
        return self

    def with_text(self, text):
        new_xpath = str(self._xpath).replace('/../..', '')
        locator = (By.XPATH, f"{new_xpath}/following::input[@part='input'][1]", f"Checkbox and Input Text with index[{self._index}]: label{self._label}")
        SendKeys(self._driver).set_locator(locator, self._name).set_text(text)
        return self
    