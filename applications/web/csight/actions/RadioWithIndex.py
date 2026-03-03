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
logger = setup_logger('RadioWithIndex')


class RadioWithIndex:
    """
    The SendKeys class handles actions to send text and key inputs to web elements.
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
        self._xpath = f"(//legend[text()='{str(label)}'])[{str(index)}]/../.."
        self._label = label
        self._index = index
        self._explicit_wait = explicit_wait
        self._locator_label = True
        return self

    def set_yes(self):
        if self._locator_label:
            locator = (By.XPATH, f"{self._xpath}//input[@value='YES']/..//label", f"Label: {self._label}, Index: {self._index} [Label Locator]")
            # Dynamic Locator for Label value
            self._element = Element.wait_for_element(driver=self._driver, locator=locator, timeout=self._explicit_wait)
            Scroll(self._driver).set_element(self._element).to_element(pixels=-100)
            Click(self._driver).set_element(self._element).single_click()
        return self

    def set_no(self):
        if self._locator_label:
            locator = (By.XPATH, f"{self._xpath}//input[@value='NO']/..//label", f"Label: {self._label}, Index: {self._index} [Label Locator]")
            # Dynamic Locator for Label value
            self._element = Element.wait_for_element(driver=self._driver, locator=locator, timeout=self._explicit_wait)
            Scroll(self._driver).set_element(self._element).to_element(pixels=-100)
            Click(self._driver).set_element(self._element).single_click()
        return self


