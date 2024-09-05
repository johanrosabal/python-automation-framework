from applications.desktop.notepad.pages.menus.BaseMenu import BaseMenu
from core.desktop.actions.XPath import XPath

class ViewMenu(BaseMenu):
    def __init__(self, driver):
        super().__init__(driver)
        self._menu_name = "View"
        self._zoom = XPath().contains("Zoom")
        self._status_bar = XPath().contains("Status Bar")

    def zoom(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._zoom)

    def status_bar(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._status_bar)
