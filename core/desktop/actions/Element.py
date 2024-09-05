from core.config.logger_config import setup_logger
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = setup_logger('Element')


class Element:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator: tuple, timeout=10):
        # Extract only first two values of the tuple
        __locator = locator[:2]
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(__locator)
            )
            return element
        except TimeoutException:
            logger.info(f"Element with locator {locator} was not found within {timeout} seconds.")
            return None
