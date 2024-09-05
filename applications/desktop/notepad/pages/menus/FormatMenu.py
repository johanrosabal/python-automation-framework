from applications.desktop.notepad.pages.menus.BaseMenu import BaseMenu
from core.desktop.actions.XPath import XPath


class FormatMenu(BaseMenu):
    def __init__(self, driver):
        super().__init__(driver)
        self._menu_name = "Format"
        self._word_wrap = XPath().contains("Word Wrap")
        self._font = XPath().contains("Font...")

    def word_wrap(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._word_wrap)

    def font(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._font)