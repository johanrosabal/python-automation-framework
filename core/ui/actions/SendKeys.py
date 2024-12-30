from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.actions.Click import Click
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Screenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

# Logger setup for 'SendKeys' operations
logger = setup_logger('SendKeys')


class SendKeys:
    """
    The SendKeys class handles actions to send text and key inputs to web elements.

    Attributes:
        _name (str): Name of the class, used for logging.
        _driver (WebDriver): The WebDriver instance.
        _element (WebElement): The targeted element to interact with.
        _text (str): Text to send to the element.
        _clear (bool): Flag to indicate if the element should be cleared.
        _pause (int): Optional pause duration for actions.
        _special_characters (str): Holds special keys if needed.
        _locator (tuple): Locator used to find the element.
        _page (str): Page name for logging context.
    """

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._text = None
        self._clear = None
        self._pause = None
        self._special_characters = None
        self._locator = None
        self._page = None
        # Table Input Field
        self._locator_table = None

    def set_locator(self, locator: tuple, page='Page', explicit_wait=10):
        """
        Set the locator for the element, wait for it to become available, and log the result.

        Args:
            locator (tuple): Tuple with the locating strategy and value (e.g., By. ID, 'element_id').
            page (str): Name of the page to help with logging.
            explicit_wait (int): Time to wait for element visibility (default is 10 seconds).
        """
        self._locator = locator
        self._page = page
        # Wait for the element using Element class method, with specified timeout
        self._element = Element.wait_for_element(driver=self._driver, locator=locator, timeout=explicit_wait)
        # Log the action with page and element details
        logger.info(Element.log_console(self._page, self._name, locator))
        return self

    def set_element(self, element):
        self._element = element
        return self

    def set_locator_by_table(self, table_xpath):
        self._element = table_xpath
        self._locator_table = table_xpath
        return self

    def set_text(self, text: str):
        """Sets and sends the provided text to the element."""
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        if self._element:
            logger.info("Send Keys [" + text + "]")
            self._element.send_keys(str(text))
        else:
            logger.error("Unable to Send Text [" + text + "] element is None")
        return self

    def by_table_text(self,  row: int, text: str, column_index: list):
        """Sets and sends the provided text to the element."""
        parent_xpath = self._locator_table[1]

        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        if self._element:

            cell_xpath = f"/tbody/tr[{row}]/td[{column_index[0]}]"
            input_xpath = f"/tbody/tr[{row}]/td[{column_index[0]}]//input"

            # 01 Click on Cell to Activate the Input Field
            cell_locator = (By.XPATH, f"{parent_xpath}{cell_xpath}", f"Table Send Keys: Click Activate [{row}][{column_index[0]}]: Cell: {column_index}")
            Click(self._driver).set_locator(cell_locator).single_click()
            # 02 Click on Input Text Field
            input_text = (By.XPATH, f"{parent_xpath}{input_xpath}", f"Table Send Keys: Click Input '{column_index[1]}' [{row}][{column_index[0]}]: Select Text: {text}")
            Click(self._driver).set_locator(input_text).single_click()
            # 03 Send Text to Input Data
            SendKeys(self._driver).set_locator(input_text).clear().set_text(text).highlight()
        else:
            logger.error(f"Unable to Send Text to table {parent_xpath}[" + text + "] element is None")
        return self

    def set_text_by_character(self, text: str):
        """Sends text to the element character by character."""
        if not isinstance(text, str):
            raise TypeError("The argument should be a string text.")
        if self._element:
            logger.info(f"Sending text '{text}' by character.")
            for letter in text:
                logger.info(f"Sending character: '{letter}'")
                self._element.send_keys(letter)
        else:
            logger.error(f"Unable to send text by character '{text}': element is None.")
        return self

    def get_text(self):
        """Retrieves text from the element's value attribute."""
        if self._element:
            input_value = self._element.get_attribute('value')
            logger.info("Retrieved Element Value: " + input_value)
            return input_value

    def clear(self):
        """Clears the text from the element."""
        if self._element:
            logger.info("Clearing text from element.")
            self._element.click()
            self._element.clear()
        else:
            logger.error("Unable to clear element: element is None.")
        return self

    # Keyboard actions
    def press_return(self):
        """Presses the RETURN key on the element."""
        return self._press_key(Keys.RETURN, "RETURN")

    def press_enter(self):
        """Presses the ENTER key on the element."""
        return self._press_key(Keys.ENTER, "ENTER")

    def press_backspace(self):
        """Presses the BACKSPACE key on the element."""
        return self._press_key(Keys.BACKSPACE, "BACKSPACE")

    def press_tab(self):
        """Presses the TAB key on the element."""
        return self._press_key(Keys.TAB, "TAB")

    def press_escape(self):
        """Presses the ESCAPE key on the element."""
        return self._press_key(Keys.ESCAPE, "ESCAPE")

    def _press_key(self, key, key_name):
        """Helper method to press a specific key on the element."""
        if self._element:
            logger.info(f"Pressing [{key_name}] key.")
            self._element.send_keys(key)
        else:
            logger.error(f"Unable to press [{key_name}]: element is None.")
        return self

    def pause(self, seconds: int):
        """Pauses the execution for a given number of seconds."""
        BaseApp.pause(seconds)
        return self

    def screenshot(self, name="screenshot"):
        """Takes a screenshot of the checkbox and attaches it to the report."""
        if self._locator:
            Screenshot(self._driver).set_locator(self._locator, self._page).attach_to_allure(name)

        if self._element and self._locator is None:
            Screenshot(self._driver).set_element(self._element).attach_to_allure(name)
        return self

    def highlight(self, duration=1):
        ElementHighlighter(self._driver).set_locator(self._locator).highlight_temporarily(duration)
        return self
