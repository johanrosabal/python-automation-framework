from core.ui.common.BasePage import BasePage
from core.ui.driver.DriverManager import DriverManager
from appium.webdriver.common.appiumby import AppiumBy as By
import time


class NotepadPage:

    application = "C:\\Windows\\System32\\notepad.exe"
    driver = None  # Esto se inicializará en el método get_instance

    # Locator
    __text_editor = (By.CLASS_NAME, "Edit")
    __menu_file = (By.CLASS_NAME, "Edit")

    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls.driver = DriverManager.windows_pc(cls.application)
            time.sleep(3)
            cls._instance = NotepadPage()  # Ahora crea una instancia de NotepadPage
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

    def close(self):
        if self.driver:
            self.driver.quit()
