import time

from core.config.logger_config import setup_logger
from core.ui.actions.Element import Element

# Initialize logger specifically for the Element class
logger = setup_logger('Element')


class ElementHighlighter:

    def __init__(self, driver):
        # Store the driver instance, and initialize placeholder for the element
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator = None
        self._page = None

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

    def highlight_element(self, color: str = "red", border_width: str = "3px"):
        """
       Highlights the specified WebElement with a colored border.
       :param color: The color of the highlight border, e.g., "red" or "blue".
       :param border_width: The width of the border, e.g., "3px".
       """
        if self._element:
            js = f"arguments[0].style.border='{border_width} solid {color}'"
            self._driver.execute_script(js, self._element)

    def highlight_remove(self):
        """
        Removes the highlight from the specified WebElement.
        """
        if self._element:
            self._driver.execute_script("arguments[0].style.border=''", self._element)

    def highlight_temporarily(self, duration: int = 0.5, color: str = "red", border_width: str = "3px"):
        """
        Highlights the specified WebElement for a few seconds, then removes the highlight.
        :param duration: Duration to keep the highlight in seconds.
        :param color: The color of the highlight border.
        :param border_width: The width of the border.
        """
        self.highlight_element(color=color, border_width=border_width)
        time.sleep(duration)
        self.highlight_remove()
