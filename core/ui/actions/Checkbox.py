from core.config.logger_config import setup_logger
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Screenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

# Logger setup for 'Checkbox' interactions
logger = setup_logger('Checkbox')


class Checkbox:
    """
    Checkbox class provides methods for handling checkbox elements in UI tests.

    Attributes:
        _name (str): The class name, used for logging.
        _driver (WebDriver): The WebDriver instance for browser interaction.
        _element (WebElement): The targeted checkbox element.
        _locator (tuple): Locator to find the checkbox element.
        _page (str): Name of the page, for logging purposes.
    """

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator = None
        self._page = None

    def set_locator(self, locator: tuple, page='Page', explicit_wait=10):
        """
        Set the locator for the element, wait for it to become available, and log the result.

        Args:
            locator (tuple): Tuple with the locating strategy and value (e.g., By.ID, 'element_id').
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

    def pause(self, seconds: int):
        """Pauses the execution for a given number of seconds."""
        BaseApp.pause(seconds)
        return self

    def is_displayed(self):
        """Checks if the checkbox element is displayed on the page."""
        if self._element:
            is_displayed = self._element.is_displayed()
            logger.info(f"Checkbox display status: {is_displayed}")
            return is_displayed
        else:
            logger.error("Cannot check display status: checkbox element is None.")
            return False

    def is_selected(self):
        """Checks if the checkbox element is currently selected."""
        if self._element:
            is_selected = self._element.is_selected()
            logger.info(f"Checkbox selected status: {is_selected}")
            return is_selected
        else:
            logger.error("Cannot check selected status: checkbox element is None.")
            return False

    def set_value(self, value: bool):
        """
        Sets the checkbox value based on the provided boolean.

        Args:
            value (bool): Desired checkbox state. `True` to select, `False` to deselect.
        """
        if self._element:
            selected = self._element.is_selected()
            if selected != value:
                self._element.click()
                logger.info(f"Checkbox set to {'selected' if value else 'deselected'}.")
            else:
                logger.info("Checkbox already in the desired state.")
        else:
            logger.error("Cannot set checkbox value: checkbox element is None.")
        return self

    def screenshot(self, name="screenshot"):
        """Takes a screenshot of the checkbox and attaches it to the report."""
        if self._locator:
            Screenshot(self._driver).set_locator(self._locator, self._page).attach_to_allure(name)
        if self._element:
            Screenshot(self._driver).set_element(self._element).attach_to_allure(name)
        return self

    def highlight(self, duration=1):
        ElementHighlighter(self._driver).set_locator(self._locator).highlight_temporarily(duration)
        return self
