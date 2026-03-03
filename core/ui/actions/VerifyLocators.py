from selenium.webdriver.remote.webdriver import WebDriver
from core.config.logger_config import setup_logger
from core.ui.actions.Element import Element

logger = setup_logger('VerifyLocators')


class VerifyLocators:
    def __init__(self, driver: WebDriver):
        """
        Initialize the VerifyLocators with the WebDriver instance.
        """
        self._driver = driver

    def verify_page_locators(self, locators: list):
        """
        Verify that all provided locators are present on the page.

        Args:
            locators (list): List of tuples containing (By, value, description)

        Returns:
            list: List of descriptions of missing elements (empty list if all found)
        """
        missing_elements = []

        for locator in locators:
            by, value, description = locator
            try:
                Element.wait_for_element(driver=self._driver, locator=(by, value), timeout=10)
                logger.info(f"✅ Found element: {description}")
            except Exception as e:
                logger.error(f"❌ Missing element: {description} | Locator: ({by}, {value})")
                missing_elements.append(description)

        return missing_elements
