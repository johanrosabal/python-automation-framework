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
        return self._driver.current_windows_handle

    def get_original_window(self):
        return self.original_window

    def select_tab(self, number: int):
        self._driver.switch_to.window(self.tabs[number])
        BaseApp.pause(1)

    def find_new_windows(self):
        for window_handle in self._driver.window_handles:
            if window_handle != self.original_window:
                self._driver.switch_to.window(window_handle)
                break

    def open_new_windows(self):
        # Open new windows using JavaScript
        self._driver.execute_script("window.open('');")
        # Handle the new windows
        self._driver.switch_to.new_window(self._driver.window_handles[-1])

    def close_tab(self):
        # Close the tab or window
        self._driver.close()
        # Switch back to the old tab or window
        self._driver.switch_to.window(self.original_window)