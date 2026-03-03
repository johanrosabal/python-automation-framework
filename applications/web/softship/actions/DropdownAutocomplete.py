from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.actions.Click import Click
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.SendKeys import SendKeys
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('DropdownAutocomplete')


class DropdownAutocomplete:
    """
    A class to handle dropdown autocomplete interactions in a web application.

    This class provides methods to interact with a dropdown autocomplete input field,
    allowing the user to input text, clear the field, and select an option from the list of results.

    Attributes:
        driver: The Selenium WebDriver used to control the browser.
        _name: The name of the class, used for logging purposes.
        _element: The WebElement representing the autocomplete input field.
    """

    def __init__(self, driver):
        """
        Initialize the DropdownAutocomplete instance.

        :param driver: Selenium WebDriver instance for interacting with the web application.
        """
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator_label = False

        # Dropdown on tables
        self._locator_table = None

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
        return self

    def set_locator_by_label(self, label: str, page='Page'):
        """
        Set the locator for the autocomplete input field using the label

        This method waits for the element to be present on the page and logs the operation.

        :param label: Label String to identify the Parent Container and find the Input Box
        :param page: The page name where the element is located, used for logging.
        :return: Returns self for method chaining.
        """
        parent_xpath = f"(//label[text()='{label}']/..)"
        label_xpath = "/following-sibling::input"
        locator = (By.XPATH, f"{parent_xpath}{label_xpath}", f"Page{page}, Dropdown Autocomplete by label:{label}")
        self._element = Element.wait_for_element(self._driver, locator)
        self._locator_label = True
        return self

    def set_locator_by_label_span(self, label: str, root_xpath="", page='Page'):
        """
        Set the locator for the autocomplete input field using the label

        This method waits for the element to be present on the page and logs the operation.

        :param label: Label String to identify the Parent Container and find the Input Box
        :param page: The page name where the element is located, used for logging.
        :param root_xpath: Main Container XPATH
        :return: Returns self for method chaining.
        """
        # xpath = f"{root_xpath}//label/span[text()=\"{label}\"]/../../following-sibling::div//input"
        xpath = f"{root_xpath}//*[text()=\"{label}\"]/../../following-sibling::div//input"
        logger.info(f"Locator by Label Span: {xpath}")
        locator = (By.XPATH, xpath, f"Page{page}, Dropdown Autocomplete by label:{label}")
        self._element = Element.wait_for_element(self._driver, locator)
        self._locator_label = False
        return self

    def set_locator_by_label_span_2(self, label: str, root_xpath="", page='Page'):
        """
        Set the locator for the autocomplete input field using the label

        This method waits for the element to be present on the page and logs the operation.

        :param label: Label String to identify the Parent Container and find the Input Box
        :param page: The page name where the element is located, used for logging.
        :param root_xpath: Main Container XPATH
        :return: Returns self for method chaining.
        """
        xpath = f"{root_xpath}//label/span[text()=\"{label}\"]/../../..//input"
        logger.info(f"Locator by Label Span: {xpath}")
        locator = (By.XPATH, xpath, f"Page{page}, Dropdown Autocomplete by label:{label}")
        self._element = Element.wait_for_element(self._driver, locator)
        self._locator_label = False
        return self

    def set_locator_by_table(self, table_xpath):
        self._locator_table = table_xpath
        return self

    def pause(self, seconds: int):
        """
        Pause the execution for a given number of seconds.

        :param seconds: Number of seconds to pause.
        :return: Returns self for method chaining.
        """
        BaseApp.pause(seconds)
        return self

    def clear(self):
        """
        Clear the text from the autocomplete input field.

        :return: Returns self for method chaining.
        """
        if self._element:
            self._element.clear()
        return self

    def by_text(self, text: str, column: int):
        """
        Type the provided text into the autocomplete input field and select the matching item from the dropdown.

        This method sends the text to the input field, waits for the dropdown options to appear,
        and selects the item that matches the provided text. The search for the option is done in the specified column.

        :param text: The text to type into the input field and search for in the dropdown.
        :param column: The column number in the dropdown table where the text should be matched.
        :return: None
        """
        if self._element:

            SendKeys(self._driver).set_element(self._element).clear().set_text(text)

            # Locate the dropdown items based on the column number
            if self._locator_label:
                modal_list_locator = (By.XPATH, "//table[@class='matches-list']/tbody/tr/td[" + str(column) + "]/span")
            else:
                modal_list_locator = (By.XPATH, "//div[contains(@class,autocomplete-panel)]//table[@role='table']/tbody/tr/td["+str(column)+"]/span")

            items = Element.wait_for_elements(self._driver, modal_list_locator)

            for item in items:
                if item.text == text:
                    ElementHighlighter(self._driver).set_element(item).highlight_temporarily()
                    logger.info("Dropdown Option Found: " + item.text)
                    Click(self._driver).set_element(item).single_click()
                    break  # Exit loop after selecting the item
                else:
                    logger.error("Dropdown Option Not Found: " + text)
        return self

    def by_table_text(self, row: int, text: str, column_index: list, column_list_match: int):

        parent_xpath = self._locator_table[1]
        cell_xpath = f"/tbody/tr[{row}]/td[{column_index[0]}]"
        input_xpath = f"/tbody/tr[{row}]/td[{column_index[0]}]//input"
        match_list = f"/tbody/tr[{row}]/td[{column_index[0]}]//div[@class='auto-completer-popup ng-scope']//table[@class='matches-list']/tbody/tr/td[{column_list_match}]/span"

        # 01 Click on Cell to Activate the Input Field
        cell_locator = (By.XPATH, f"{parent_xpath}{cell_xpath}", f"Table Dropdown: Click Activate [{row}][{column_index}]: Cell: {column_index}")
        Click(self._driver).set_locator(cell_locator).single_click()
        # 02 Click on Input Text Field
        input_text = (By.XPATH, f"{parent_xpath}{input_xpath}", f"Table Dropdown: Click Input '{column_index[1]}' [{row}][{column_index[0]}]: Select Text: {text}")
        Click(self._driver).set_locator(input_text).single_click()
        # 03 Send Text to Input Data Dropdown
        SendKeys(self._driver).set_locator(input_text).clear().set_text(text).highlight()
        # In case the Text is Empty or ""
        if text != "":
            # 04 Looping Match List
            locator_match = (By.XPATH, f"{parent_xpath}{match_list}", f"Match List {column_index[1]}: Column{column_list_match}")
            items = Element.wait_for_elements(self._driver, locator_match)

            for item in items:
                if item.text == text:
                    ElementHighlighter(self._driver).set_element(item).highlight_temporarily()
                    logger.info("Dropdown Option Found: " + item.text)
                    Click(self._driver).set_element(item).single_click()
                    break  # Exit loop after selecting the item
                else:
                    logger.error("Dropdown Option Not Found: " + text)

        return self
