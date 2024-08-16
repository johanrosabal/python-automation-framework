from core.config.logger_config import setup_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = setup_logger('Element')


class Element:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def is_visible(self):
        self._element.is_displayed()

    def is_enabled(self):
        self._element.is_enabled()

    def is_selected(self):
        self._element.is_selected()

    def get_tag_name(self):
        return self._element.tag_name

    def get_position(self):
        return self._element.rect

    def get_css_property(self, css_property):
        return self._element.value_of_css_property(css_property)

    def get_text(self):
        return self._element.text

    def get_attribute(self,value="value"):
        return self._element.get_attribute(value)

    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        # Extract only first two values of the tuple
        __locator = locator[:2]
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(__locator)
            )
            return element
        except TimeoutException:
            logger.info(f"Element with locator {locator} was not found within {timeout} seconds.")
            return None

    @staticmethod
    def log_console(page: str, event: str, locator: tuple):

        if len(locator) == 3:
            by, value, message = locator
            optional = " | " + message
        else:
            by, value = locator
            optional = ""

        return "Page: " + page + " | Event: [" + event + "] | Web Element By: [" + by + "] | Locator value: [" + value + "]" + optional
