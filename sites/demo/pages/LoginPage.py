from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('LoginPage')


class LoginPage(BasePage):

    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    page = None

    # Locator
    __input_user_name = (By.NAME, "username")
    __input_password = (By.NAME, "password")
    __button_login = (By.XPATH, "//button[contains(@class,'login-button')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoginPage(BaseApp.get_driver())
        return cls._instance

    def load_page(self):
        self.go(self.url)
        self.pause(5)
        return self

    def set_user_name(self, username: str):
        (self.send_keys()
         .set_locator(self.__input_user_name)
         .set_text(username)
         )
        return self

    def set_password(self, password: str):
        (self.send_keys()
         .set_locator(self.__input_password)
         .set_text(password)
         )
        return self

    def click_login(self):
        self.click_element().set_locator(self.__button_login).single_click()
        self.pause(5)
        return self

    # def login_user(self):
    #     self.set_user_name()
    #     self.set_password()
    #     self.click_login()