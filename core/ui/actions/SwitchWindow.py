from core.config.logger_config import setup_logger
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List

from core.ui.common.BaseApp import BaseApp

logger = setup_logger('SwitchWindow')


class SwitchWindow:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self.tabs = driver.window_handles
        self.original_window = driver.current_windows_handle
        self.tab = 0

    def get_current_window(self):
        if self._driver:
            return self._driver.current_windows_handle
        else:
            logger.error("Unable to Show Current Window WebDriver is None.")

    def get_original_window(self):
        tab = self.original_window
        logger.info("Original Windows: "+str(tab))
        return tab

    def select_tab(self, number: int):
        if self._driver:
            self._driver.switch_to.window(self.tabs[number])
            BaseApp.pause(1)
        else:
            logger.error("Unable to Select Tab WebDriver is None.")

    def find_new_windows(self):
        if self._driver:
            for window_handle in self._driver.window_handles:
                if window_handle != self.original_window:
                    self._driver.switch_to.window(window_handle)
                    break
        else:
            logger.error("Unable to Find New Tab WebDriver is None.")

    def open_new_windows(self):
        if self._driver:
            # Open new windows using JavaScript
            self._driver.execute_script("window.open('');")
            # Handle the new windows
            self._driver.switch_to.new_window(self._driver.window_handles[-1])
        else:
            logger.error("Unable to Open Tab Windows WebDriver is None.")

    def close_tab(self):
        if self._driver:
            logger.error("Closing Tab Windows.")
            # Close the tab or window
            self._driver.close()
            # Switch back to the old tab or window
            self._driver.switch_to.window(self.original_window)
        else:
            logger.error("Unable to close Tab Windows WebDriver is None.")
