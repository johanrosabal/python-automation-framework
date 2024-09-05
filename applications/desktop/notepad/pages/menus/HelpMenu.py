from applications.desktop.notepad.pages.menus.BaseMenu import BaseMenu
from core.desktop.actions.XPath import XPath


class HelpMenu(BaseMenu):
    def __init__(self, driver):
        super().__init__(driver)
        self._menu_name = "Help"
        self._view_help = XPath().contains("View Help")
        self._about_notepad = XPath().contains("About Notepad")

    def view_help(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._view_help)

    def about_notepad(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._about_notepad)
