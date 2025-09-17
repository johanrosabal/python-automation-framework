from core.config.logger_config import setup_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from core.ui.common.BaseApp import BaseApp

# Initialize logger specifically for the Element class
logger = setup_logger('Element')


class Element:

    # Initialize the Element class with WebDriver and set up default values
    def __init__(self, driver):
        # Store the class name, driver instance, and initialize placeholder for the element
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator = None
        self._xpath = None

    def set_locator(self, locator: tuple, page='Page'):
        """
        Set the locator for the target element, wait for it to become available, and log the result.

        Args:
            locator (tuple): Tuple with the locating strategy and value (e.g., By. ID, 'element_id').
            page (str): Name of the page for logging purposes.
        """
        self._locator = locator
        self._xpath = locator[1]
        # Wait for the element to be visible, and store the WebElement if found
        self._element = Element.wait_for_element(self._driver, locator)
        # Log the action with page and element details
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def set_element(self, element):
        self._element = element
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

    def is_not_visible(self,locator, timeout=5):
        try:
            # Extract only the first two values of the locator tuple: the locating strategy and locator string.
            __locator = locator[:2]
            # Wait for the element to be invisible
            element = WebDriverWait(self._driver, timeout).until(
                ec.invisibility_of_element_located(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not invisible within the specified timeout
            logger.error(f"Element with locator {locator} was not invisible within {timeout} seconds.")
            return None

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

    def is_present(self, locator,  timeout=5):

        try:
            __locator = locator[:2]
            # Wait for the element to be visible
            WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(__locator)
            )
            return True
        except NoSuchElementException:
            logger.warning("Element not Present.")
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {locator}")
        except Exception as e:
            logger.warning(f"Unexpected error: {e}")

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

    def set_css_property(self, locator, style):
        __by = locator[0]
        __locator = locator[1]
        element = self._driver.find_element(__by, __locator)
        self._driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)
        return self

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

    def get_list_text(self):
        """
        Retrieve a list of text content from <span> elements inside <li> items.

        Returns:
            list[str]: The list of text content from the <span> elements.
        """
        if self._element is not None:

            span_items = self._element.find_elements(By.XPATH, self._xpath)
            items_text = [item.text for item in span_items]
            return items_text
        return []

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

    def wait(self, locator, timeout=15):
        __locator = locator[:2]
        try:
            # Wait for the element to be visible
            WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(__locator)
            )
            # Wait for the element to be clickable
            element = WebDriverWait(self._driver, timeout).until(
                ec.element_to_be_clickable(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not found within the specified timeout
            logger.error(f"Element with locator {__locator} was not visible or clickable within {timeout} seconds.")
            return None

    @staticmethod
    def wait_for_page_load(driver, timeout=15):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @staticmethod
    def wait_for_element(driver, locator, timeout=15):
        """
        Wait for an element to become visible and clickable within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the element, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            WebElement: The WebElement if it becomes visible and clickable within the timeout, else None.
        """

        # Extract only the first two values of the locator tuple: the locating strategy and locator string.
        __locator = locator[:2]

        try:
            # Wait for the element to be visible
            WebDriverWait(driver, timeout).until(
                ec.visibility_of_element_located(__locator)
            )
            # Wait for the element to be clickable
            element = WebDriverWait(driver, timeout).until(
                ec.element_to_be_clickable(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not found within the specified timeout
            logger.error(f"Element with locator {locator} was not visible or clickable within {timeout} seconds.")
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
                ec.visibility_of_all_elements_located(__locator)
            )
            return element
        except TimeoutException:
            # Log an error if elements are not found within the specified timeout
            logger.error(f"Elements with locator {locator} were not found within {timeout} seconds.")
            return None

    @staticmethod
    def wait_for_element_present(driver, locator, timeout=15):
        """
        Wait for an element to become present within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the element, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            WebElement: The WebElement if it becomes present within the timeout, else None.
        """

        # Extract only the first two values of the locator tuple: the locating strategy and locator string.
        __locator = locator[:2]

        try:
            # Wait for the element to be present
            element = WebDriverWait(driver, timeout).until(
                ec.presence_of_element_located(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not present within the specified timeout
            logger.error(f"Element with locator {locator} was not present within {timeout} seconds.")
            return None

    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=15):
        """
        Wait for an element to become clickable within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the element, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            WebElement: The WebElement if it becomes clickable within the timeout, else None.
        """

        # Extract only the first two values of the locator tuple: the locating strategy and locator string.
        __locator = locator[:2]

        try:
            # Wait for the element to be clickable
            element = WebDriverWait(driver, timeout).until(
                ec.element_to_be_clickable(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not found within the specified timeout
            logger.error(f"Element with locator {locator} was not clickable within {timeout} seconds.")
            return None

    @staticmethod
    def wait_for_element_invisible(driver, locator, timeout=15):
        """
        Wait for an element to become invisible within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the element, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            WebElement: The WebElement if it becomes invisible within the timeout, else None.
        """

        # Extract only the first two values of the locator tuple: the locating strategy and locator string.
        __locator = locator[:2]

        try:
            # Wait for the element to be invisible
            element = WebDriverWait(driver, timeout).until(
                ec.invisibility_of_element_located(__locator)
            )
            return element

        except TimeoutException:
            # Log an error if the element is not invisible within the specified timeout
            logger.error(f"Element with locator {locator} was not invisible within {timeout} seconds.")
            return None

    @staticmethod
    def wait_for_text_to_be_present(driver, locator, text, timeout=15):
        """
        Wait for an element to contain text within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            locator (tuple): The locator used to find the element, typically in the form (By.ID, "element_id").
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            bool: True if the text is present within the timeout, else False.
        """

        # Extract only the first two values of the locator tuple: the locating strategy and locator string.
        __locator = locator[:2]

        try:
            # Wait for the text is present in element
            return WebDriverWait(driver, timeout).until(
                ec.text_to_be_present_in_element(__locator, text)
            )

        except TimeoutException:
            # Log an error if the text is not display in the element within the specified timeout
            logger.error(f"Element with locator {locator} did not contain text {text} within {timeout} seconds.")
            return False

    @staticmethod
    def wait_for_alert(driver, timeout=15):
        """
        Wait for an alert present and visible within a given timeout.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            timeout (int): Maximum time to wait for the element in seconds (default is 15 seconds).

        Returns:
            Alert: The alert if it becomes present within the timeout, else None.
        """


        try:
            # Wait for the alert to be present
            element = WebDriverWait(driver, timeout).until(
                ec.alert_is_present()
            )
            return element

        except TimeoutException:
            # Log an error if the alert is not found within the specified timeout
            logger.error(f"The alert is not present")
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

    def pause(self, seconds: int = 2):
        """
        Pause the execution for a specified number of seconds.

        Args:
            seconds (int): Duration of the pause.
        """
        BaseApp.pause(seconds)
        return self
