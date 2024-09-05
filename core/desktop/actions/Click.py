from core.config.logger_config import setup_logger
from core.desktop.actions.Element import Element
from selenium.webdriver import ActionChains

logger = setup_logger('Click')


class Click:

    def __init__(self, driver):
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple):
        self._element = Element(self._driver).wait_for_element(locator)
        return self

    def single_click(self):
        if self._element:
            logger.info("Single Click")
            self._element.click()
        else:
            logger.error("Unable to Click Element is None.")
        return self

    def double_click(self):
        if self._element:
            logger.info("Double Click")
            actions = ActionChains(self._driver)
            actions.double_click(self._element).perform()
        else:
            logger.error("Unable to Click Element is None.")
        return self

    def click_and_hold(self):
        if self._element:
            logger.info("Click and Hold")
            actions = ActionChains(self._driver)
            actions.click_and_hold(self._element).perform()
        else:
            logger.error("Unable to Click and Hold Element is None.")
        return self

    def context_click(self):
        if self._element:
            logger.info("Right Click")
            actions = ActionChains(self._driver)
            actions.context_click(self._element).perform()
        else:
            logger.error("Unable to Context Click Element WebElement is None.")
        return self

    def click_with_coordinates(self, x_offset, y_offset):
        if self._element:
            logger.info("Right Click")
            actions = ActionChains(self._driver)
            actions.move_to_element_with_offset(self._element, x_offset, y_offset).click().perform()
        else:
            logger.error("Unable to Click with Coordinates Element WebElement is None.")
        return self
