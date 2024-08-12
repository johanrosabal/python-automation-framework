from core.config.logger_config import setup_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = setup_logger('Element')


class Element:

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
            print(f"Element with locator {locator} was not found within {timeout} seconds.")
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
