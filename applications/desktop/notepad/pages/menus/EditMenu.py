from applications.desktop.notepad.pages.menus.BaseMenu import BaseMenu
from core.desktop.actions.XPath import XPath


class EditMenu(BaseMenu):
    def __init__(self, driver):
        super().__init__(driver)
        self._menu_name = "Edit"
        self._undo = XPath().contains("Undo")
        self._cut = XPath().contains("Cut")
        self._copy = XPath().contains("Copy")
        self._paste = XPath().contains("Paste")
        self._delete = XPath().contains("Delete")
        self._find = XPath().contains("Find...")
        self._find_next = XPath().contains("Find Next")
        self._find_previous = XPath().contains("Find Previous")
        self._replace = XPath().contains("Replace...")
        self._go_to = XPath().contains("Go To...")
        self._select_all = XPath().contains("Select All")
        self._time_date = XPath().contains("Time/Date")

    def undo(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._undo)

    def cut(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._cut)

    def copy(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._copy)

    def paste(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._paste)

    def delete(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._delete)

    def find(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._find)

    def find_next(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._find_next)

    def find_previous(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._find_previous)

    def replace(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._replace)

    def go_to(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._go_to)

    def select_all(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._select_all)

    def time_date(self):
        self._open_menu(self._menu_name)
        self._select_menu_option(self._time_date)
