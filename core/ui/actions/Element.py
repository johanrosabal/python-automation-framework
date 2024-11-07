from core.config.logger_config import setup_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize logger specifically for the Element class
logger = setup_logger('Element')


class Element:

    # Initialize the Element class with WebDriver and set up default values
    def __init__(self, driver):
        # Store the class name, driver instance, and initialize placeholder for the element
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple, page='Page'):
        """
        Set the locator for the target element, wait for it to become available, and log the result.

        Args:
            locator (tuple): Tuple with the locating strategy and value (e.g., By.ID, 'element_id').
            page (str): Name of the page for logging purposes.
        """
        # Wait for the element to be visible, and store the WebElement if found
        self._element = Element.wait_for_element(self._driver, locator)
        # Log the action with page and element details
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def is_visible(self):
        """
        Check if the element is visible.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        if self._element is not None:
            self._element.is_displayed()
            return True
        return False

    def is_enabled(self):
        """
        Check if the element is enabled.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        if self._element is not None:
            self._element.is_enabled()
            return True
        return False

    def is_selected(self):
        """
        Check if the element is selected.

        Returns:
            bool: True if the element is selected, False otherwise.
        """
        if self._element is not None:
            self._element.is_selected()
            return True
        return False

    def get_tag_name(self):
        """
        Retrieve the tag name of the element.

        Returns:
            str: The tag name of the element.
        """
        if self._element is not None:
            return self._element.tag_name

    def get_position(self):
        """
        Retrieve the position and size of the element.

        Returns:
            dict: The position and size of the element as a dictionary.
        """
        if self._element is not None:
            return self._element.rect

    def get_css_property(self, css_property):
        """
        Retrieve the value of a specific CSS property of the element.

        Args:
            css_property (str): The CSS property to retrieve.

        Returns:
            str: The value of the CSS property.
        """
        if self._element is not None:
            return self._element.value_of_css_property(css_property)

    def get_text(self):
        """
        Retrieve the text content of the element.

        Returns:
            str: The text content of the element.
        """
        if self._element is not None:
            return self._element.text

    def get_attribute(self, value="value"):
        """
        Retrieve the value of a specified attribute of the element.

        Args:
            value (str): The attribute name to retrieve (default is "value").

        Returns:
            str: The attribute value.
        """
        if self._element is not None:
            return self._element.get_attribute(value)

    @staticmethod
    def wait_for_element(driver, locator, timeout=15):
        """
        Wait for an element to become visible within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the element, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            WebElement: The WebElement if it becomes visible within the timeout, else None.
        """

        # Extract only the first two values of the locator tuple: the locating strategy and locator string.
        __locator = locator[:2]

        try:
            # Wait until the element specified by __locator is visible within the timeout period, then return it
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not found within the specified timeout
            logger.error(f"Element with locator {locator} was not found within {timeout} seconds.")
            return None

    @staticmethod
    def wait_for_elements(driver, locator, timeout=15):
        """
        Wait for all elements matching the locator to become visible within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the elements, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for elements in seconds (default is 15 seconds).

        Returns:
            list[WebElement]: A list of WebElements if they become visible within the timeout, else None.
        """
        # Extract only the first two values of the tuple, the locating strategy and locator string
        __locator = locator[:2]
        try:
            # Wait until all elements matching __locator are visible within the timeout period, then return them
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_all_elements_located(__locator)
            )
            return element
        except TimeoutException:
            # Log an error if elements are not found within the specified timeout
            logger.error(f"Elements with locator {locator} were not found within {timeout} seconds.")
            return None

    @staticmethod
    def log_console(page: str, event: str, locator: tuple):
        """
        Generate a log message with page, event, and locator details for easy identification.

        Args:
            page (str): The name of the page where the event is occurring.
            event (str): The event name, usually the action being performed.
            locator (tuple): The locator tuple, typically (By, value, optional_message).

        Returns:
            str: A formatted log message.
        """

        # Determine if there is an optional message in the locator tuple
        if len(locator) == 3:
            by, value, message = locator
            optional = " | " + message
        else:
            by, value = locator
            optional = ""

        # Format and return the log message
        return "Page: " + page + " | Event: [" + event + "] | Web Element By: [" + by + "] | Locator value: [" + value + "]" + optional
