from selenium.webdriver.support.select import Select
from core.config.logger_config import setup_logger
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Screenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

# Logger setup for Dropdown interactions
logger = setup_logger('Dropdown')


class Dropdown:
    """
    Dropdown class provides methods for interacting with dropdown menu elements in UI tests.

    Attributes:
        _name (str): The class name, used for logging.
        _driver (WebDriver): The WebDriver instance for browser interaction.
        _element (WebElement): The targeted dropdown element.
        _locator (tuple): Locator to find the dropdown element.
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

    def pause(self, seconds: int):
        """Pauses execution for a specified number of seconds."""
        BaseApp.pause(seconds)
        return self

    def by_value(self, value: str):
        """Selects an option by its 'value' attribute."""
        if self._element:
            Select(self._element).select_by_value(value)
            logger.info(f"Dropdown option selected by value: {value}")
        else:
            logger.error("Cannot select dropdown option by value: dropdown element is None.")
        return self

    def by_index(self, index: int):
        """Selects an option by its index."""
        if self._element:
            Select(self._element).select_by_index(index)
            logger.info(f"Dropdown option selected by index: {index}")
        else:
            logger.error("Cannot select dropdown option by index: dropdown element is None.")
        return self

    def by_text(self, text: str):
        """Selects an option by its visible text."""
        if self._element:
            Select(self._element).select_by_visible_text(text)
            logger.info(f"Dropdown option selected by text: {text}")
        else:
            logger.error("Cannot select dropdown option by text: dropdown element is None.")
        return self

    def by_text_contains(self, search_text: str):
        """Selects an option that contains specific text."""
        if self._element:
            for option in Select(self._element).options:
                if search_text in option.text:
                    option.click()
                    logger.info(f"Dropdown option containing '{search_text}' selected: {option.text}")
                    return self
            logger.error(f"Dropdown option containing '{search_text}' not found.")
        else:
            logger.error("Cannot find dropdown options: dropdown element is None.")
        return self

    def deselect_all(self):
        """Deselects all selected options if the dropdown supports multiple selections."""
        if self._element:
            Select(self._element).deselect_all()
            logger.info("All dropdown options deselected.")
        else:
            logger.error("Cannot deselect options: dropdown element is None.")
        return self

    def screenshot(self, name="screenshot"):
        """Takes a screenshot of the dropdown and attaches it to the report."""
        Screenshot(self._driver).set_locator(self._locator, self._page).attach_to_allure(name)
        return self

    def highlight(self, duration=1):
        ElementHighlighter(self._driver).set_locator(self._locator).highlight_temporarily(duration)
        return self
