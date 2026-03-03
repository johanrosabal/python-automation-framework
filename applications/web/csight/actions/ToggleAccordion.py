from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.actions.Click import Click
from core.ui.actions.Element import Element

logger = setup_logger('ToggleAccordion')


class ToggleAccordion:

    """
    The ToggleAccordion class handles to Expand or Collapse a Content by Click and Button Element, Identify with the Label Text
    """

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._xpath = None
        self._label = None
        self._explicit_wait = 0
        self._locator = None
        self._current_state = False

    def set_locator_with_label(self, label: str = None, explicit_wait=10):
        """
        Set the locator for the autocomplete input field using the label

        This method waits for the element to be present on the page and logs the operation.

        :param label: Label String to identify the Parent Container and find the Input Box
        :param explicit_wait: Wait Explicit Time after send text to the element
        :return: Returns self for method chaining.
        """
        # Root Locator String
        self._xpath = f"//span[text()='{label}']/.."
        self._label = label
        self._explicit_wait = explicit_wait

        # Set Element
        locator = (By.XPATH, self._xpath, f"Toggle Accordion with label: {self._label} [Button]")

        self._element = Element.wait_for_element(self._driver, locator)

        if self._element:
            self._current_state = bool(self._element.get_attribute("aria-expanded"))

        return self

    def open(self):

        if not self._current_state:
            Click(self._driver).set_element(self._element).single_click()
        return self

    def close(self):
        if self._current_state:
            Click(self._driver).set_element(self._element).single_click()
        return selfs