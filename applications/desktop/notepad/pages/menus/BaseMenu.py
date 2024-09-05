import time

from appium.webdriver.common.appiumby import AppiumBy as By

from core.desktop.actions.Element import Element


class BaseMenu:
    def __init__(self, driver):
        self._driver = driver

    def _open_menu(self, menu_name):
        menu = self._driver.find_element(By.NAME, menu_name)
        menu.click()
        time.sleep(1)

    def _select_menu_option(self, option_name):
        option = Element(self._driver).wait_for_element(option_name)
        option.click()
        time.sleep(1)
