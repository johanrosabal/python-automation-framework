from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.actions.Scroll import Scroll
from core.ui.actions.SendKeys import SendKeys
from core.ui.actions.Click import Click
from core.ui.actions.Element import Element

logger = setup_logger('DropdownAutocomplete')


class DropdownAutocomplete:

    def __init__(self, driver):
        """
        Initialize the DropdownAutocomplete instance.
        """
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._element = None
        self._locator_label = None
        self._locator = None
        self._label = None
        self._index = None

    def set_locator(self, locator: tuple, page='Page'):
        """
        Set the locator for the autocomplete input field and locate the element.

        This method waits for the element to be present on the page and logs the operation.

        :param locator: A tuple that contains the locator strategy and value (e.g., (By.ID, 'input-field-id')).
        :param page: The page name where the element is located, used for logging.
        :return: Returns self for method chaining.
        """
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        self._locator = locator
        return self

    def set_locator_by_label(self, index=1, label: str = None):
        """
        Set the locator for the autocomplete input field using the label

        This method waits for the element to be present on the page and logs the operation.

        :param index: Index value for autocomplete web element, default 1
        :param label: Label String to identify the Parent Container and find the Input Box
        :param page: The page name where the element is located, used for logging.
        :return: Returns self for method chaining.
        """
        # Root Locator String
        xpath = f"(//label[contains(text(), '{label}')])[{str(index)}]/..//input"
        locator = (By.XPATH, xpath, f"Label: {label}, Index: {index} [Label Locator]")
        # Dynamic Locator for Label value
        self._element = Element.wait_for_element(self._driver, locator)
        self._locator_label = True
        self._label = label
        self._index = index
        return self

    def by_text(self, text: str):

        if self._element:
            if self._locator_label:
                # Input Text Value
                SendKeys(self._driver).set_element(self._element).clear().set_text(text).pause(1)
                # Select value from Dropdown
                locator_root = f"(//label[contains(text(), '{self._label}')])[{str(self._index)}]"
                locator_select = (By.XPATH, f"{locator_root}/..//ul/li/span[contains(text(),\"{str(text)}\")]", f"Text {text} [Select]")
                # Click Element Text on Dropdown
                Click(self._driver).set_locator(locator_select, self._name).single_click().pause(1)
        return self

    def by_list_item(self, text: str):
        """Selects an option by its 'value' attribute."""
        if self._element:
            if self._locator_label:
                Click(self._driver).set_element(self._element).single_click()
                Click(self._driver).set_element(self._element).double_click()
                # Select value from Dropdown
                locator_root = f"(//label[text()='{self._label}'])[{str(self._index)}]"
                locator_select = (By.XPATH, f"{locator_root}/..//ul/li/span[contains(text(),\"{str(text)}\")]",
                                  f"Text {text} [Select]")
                # Click Element Text on Dropdown
                Click(self._driver).set_locator(locator_select, self._name).single_click()
        return self

    def by_list_item_contains(self, text: str):
        """Selects an option by its 'value' attribute."""
        if self._element:
            if self._locator_label:
                Click(self._driver).set_element(self._element).single_click()
                Click(self._driver).set_element(self._element).double_click()
                # Select value from Dropdown
                locator_root = f"(//label[contains(text(),'{self._label}')])[{str(self._index)}]"
                locator_select = (By.XPATH, f"{locator_root}/..//ul/li/span[contains(text(),\"{str(text)}\")]",
                                  f"Text {text} [Select]")
                Element.wait_for_element_present(self._driver, locator_select, 5)
                # Click Element Text on Dropdown
                Click(self._driver).set_locator(locator_select, self._name).single_click()
        return self



