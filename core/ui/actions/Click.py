from core.config.logger_config import setup_logger
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Screenshot import Screenshot
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from selenium.webdriver.common.action_chains import ActionChains

# Initialize logger specifically for the Click class
logger = setup_logger('Click')


class Click:

    # Initialize the Click class with WebDriver and set up default values
    def __init__(self, driver):
        # Store the class name, driver instance, and initialize placeholders
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
        """
        Pause the execution for a specified number of seconds.

        Args:
            seconds (int): Duration of the pause.
        """
        BaseApp.pause(seconds)
        return self

    def single_click(self):
        """
        Perform a single click action on the element if it is available.
        """
        if self._element:
            logger.info("Single Click")
            self._element.click()
        else:
            logger.error("Unable to Click: Element WebElement is None.")
        return self

    def double_click(self):
        """
        Perform a double-click action on the element if it is available.
        """
        if self._element:
            logger.info("Double Click")
            actions = ActionChains(self._driver)
            actions.double_click(self._element).perform()
        else:
            logger.error("Unable to Double Click: Element WebElement is None.")
        return self

    def click_and_hold(self):
        """
        Click and hold the element if it is available.
        """
        if self._element:
            logger.info("Click and Hold")
            actions = ActionChains(self._driver)
            actions.click_and_hold(self._element).perform()
        else:
            logger.error("Unable to Click and Hold: Element WebElement is None.")
        return self

    def context_click(self):
        """
        Perform a right-click (context click) on the element if it is available.
        """
        if self._element:
            logger.info("Context Click")
            actions = ActionChains(self._driver)
            actions.context_click(self._element).perform()
        else:
            logger.error("Unable to Context Click: WebElement is None.")
        return self

    def drag_and_drop(self, draggable, droppable):
        """
        Drag an element (draggable) and drop it onto another element (droppable).

        Args:
            draggable: The WebElement to drag.
            droppable: The WebElement where draggable will be dropped.
        """
        if draggable is not None and droppable is not None:
            logger.info("Drag and Drop")
            actions = ActionChains(self._driver)
            actions.drag_and_drop(draggable, droppable).perform()
        else:
            logger.error("Unable to Drag and Drop: WebElement is None.")
        return self

    def mouse_over(self):
        """
        Move the mouse over the element if it is available.
        """
        if self._element:
            logger.info("Mouse Over")
            actions = ActionChains(self._driver)
            actions.move_to_element(self._element).perform()
        else:
            logger.error("Unable to Mouse Over: WebElement is None.")
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
