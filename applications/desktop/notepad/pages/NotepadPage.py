from core.ui.driver.DriverManager import DriverManager
from appium.webdriver.common.appiumby import AppiumBy as By
from core.config.config_loader import load_desktop_config
import time
from core.config.config_cmd import get_profile


def config_yaml():
    profile = get_profile() or "qa"
    # Load Profile Configurations
    return load_desktop_config(f"../config/{profile}_config.yaml")


class NotepadPage:
    driver = DriverManager.windows_pc(config_yaml().desktop.application)

    # Locator
    __text_editor = (By.CLASS_NAME, "Edit")
    __menu_file = (By.CLASS_NAME, "Edit")
    __dont_save_button = (By.NAME, "Don't Save")

    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = NotepadPage()
        return cls._instance

    def menu_edit(self):
        by, value = self.__menu_file
        if self.driver:
            self.driver.find_element(by, value).click()
        return self

    def edit_document(self, text: str):
        by, value = self.__text_editor
        if self.driver:
            self.driver.find_element(by, value).send_keys(text)
        return self

    def quit(self):
        if self.driver:
            self.driver.quit()

    def close(self):
        if self.driver:
            self.driver.close()
            time.sleep(1)
            try:
                # try to click "Don't Save" if dialog box appears
                self.driver.find_element(*self.__dont_save_button).click()
            except:
                pass
