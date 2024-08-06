from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
logger = setup_logger('SendKeys')


class Click:

    def __init__(self, driver):
        self.__driver = driver
        self.__element = None

    def set_locator(self, locator: tuple):
        by, value = locator
        self.__element = self.__driver.find_element(by, value)
        return self

    def single_click(self):
        if self.__element:
            self.__element.click()
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self
