from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from selenium.webdriver.common.action_chains import ActionChains

logger = setup_logger('Click')


class Click:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def single_click(self):
        if self._element:
            logger.info("Single Click")
            self._element.click()
        else:
            logger.error("Unable to Click Element WebElement is None.")
        return self

    def double_click(self):
        if self._element:
            logger.info("Double Click")
            actions = ActionChains(self._driver)
            actions.double_click(self._element).perform()
        else:
            logger.error("Unable to Double Click Element WebElement is None.")
        return self

    def click_and_hold(self):
        if self._element:
            logger.info("Click and Hold")
            actions = ActionChains(self._driver)
            actions.click_and_hold(self._element).perform()
        else:
            logger.error("Unable to Click and Hold Element WebElement is None.")
        return self

    def context_click(self):
        if self._element:
            logger.info("Context Click")
            actions = ActionChains(self._driver)
            actions.context_click(self._element).perform()
        else:
            logger.error("Unable to Context Click WebElement is None.")
        return self

    def mouse_over(self):
        if self._element:
            logger.info("Mouse Over")
            actions = ActionChains(self._driver)
            actions.move_to_element(self._element).perform()
        else:
            logger.error("Unable to Context Click WebElement is None.")
        return self
