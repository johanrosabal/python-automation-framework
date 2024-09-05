import time

from applications.desktop.notepad.pages.menus.BaseMenu import BaseMenu
from appium.webdriver.common.appiumby import AppiumBy as By
from core.desktop.actions.XPath import XPath


class FileMenu(BaseMenu):
    def __init__(self, driver):
        super().__init__(driver)
        self._menu_name = "File"
        self._new = XPath().contains("New")
        self._new_window = XPath().contains("New Window")
        self._open = XPath().contains("Open...")
        self._save = (By.NAME, "Save	Ctrl+S")
        self._save_as = XPath().contains("Save As...")
        self._page_setup = XPath().contains("Page Setup...")
        self._print = XPath().contains("Print...")
        self._exit = XPath().contains("Exit")

    def new(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._new)

    def new_windows(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._new_window)

    def open(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._open)

    def save(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._save)

    def save_as(self):
        self._open_menu(self._menu_name)
        time.sleep(1)
        self._select_menu_option(self._save_as)

    def page_setup(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._page_setup)

    def print(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._print)

    def exit(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._exit)
