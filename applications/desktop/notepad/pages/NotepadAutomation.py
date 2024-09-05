from applications.desktop.notepad.pages.dialog_box.go_to_line_dialog_box import GoToLineDialogBox
from core.desktop.common.BaseApp import BaseApp
from core.ui.driver.DriverManager import DriverManager
from appium.webdriver.common.appiumby import AppiumBy as By

from applications.desktop.notepad.pages.menus.EditMenu import EditMenu
from applications.desktop.notepad.pages.menus.FileMenu import FileMenu
from applications.desktop.notepad.pages.menus.FormatMenu import FormatMenu
from applications.desktop.notepad.pages.menus.HelpMenu import HelpMenu
from applications.desktop.notepad.pages.menus.ViewMenu import ViewMenu

from applications.desktop.notepad.pages.dialog_box.about_notepad_dialog_box import AboutNotepadDialogBox
from applications.desktop.notepad.pages.dialog_box.find_dialog_box import FindDialogBox
from applications.desktop.notepad.pages.dialog_box.replace_dialog_box import ReplaceDialogBox
from applications.desktop.notepad.pages.dialog_box.save_dialog_box import SaveDialogBox

from core.config.config_loader import load_desktop_config
from core.config.config_cmd import get_profile


# Load Profile Configurations
def config_yaml():
    profile = get_profile() or "qa"
    return load_desktop_config(f"../config/{profile}_config.yaml")


class NotepadAutomation(BaseApp):

    def __init__(self):
        self._driver = DriverManager.windows_pc(config_yaml().desktop.application)
        super().__init__(self._driver)

        # Menu NavigationOptions
        self.file_menu = FileMenu(self._driver)
        self.edit_menu = EditMenu(self._driver)
        self.format_menu = FormatMenu(self._driver)
        self.view_menu = ViewMenu(self._driver)
        self.help_menu = HelpMenu(self._driver)

        # Application Dialog Boxes
        self.save_dialog_box = SaveDialogBox(self._driver)
        self.about_dialog_box = AboutNotepadDialogBox(self._driver)
        self.find_dialog_box = FindDialogBox(self._driver)
        self.replace_dialog_box = ReplaceDialogBox(self._driver)
        self.go_to_line_dialog_box = GoToLineDialogBox(self._driver)

        # Application Elements
        self.__text_area = (By.CLASS_NAME, "Edit")

    def write_new_line_text(self, text: str):
        self.send_keys()\
            .set_locator(self.__text_area)\
            .set_text(text)\
            .press_enter()
        return self

    def write_text(self, text: str):
        self.send_keys()\
            .set_locator(self.__text_area)\
            .set_text(text)
        return self

    def save_as_file(self, filepath):
        self.file_menu.save_as()
        self.save_dialog_box.enter_file_name(filepath).click_save()
        return self

    def close_without_saving(self):
        self._driver.close()
        self.save_dialog_box.click_dont_save()
        return self

    def verify_text(self, text, message):
        assert self.get_text().set_locator(self.__text_area).by_text() == text, message
        return self

