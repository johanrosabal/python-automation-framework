import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.softship.common.SoftshipPage import SoftshipPage

logger = setup_logger('AlertDialogBox')


class AlertDialogBox(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the AlertDialogBox instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/web/index.php/auth/login"
        self._module_url = None
        # Locator definitions
        self._div_toast_summary = (By.XPATH, "//div[contains(@class, 'p-toast-summary')]", "Alert Toast Summary Text")
        self._div_toast_detail = (By.XPATH, "//div[contains(@class, 'p-toast-detail')] | //div[contains(@class,'alert')]//div/span[1]", "Alert Toast Detail Text")
        self._btn_toast_close = (By.XPATH, "//button[contains(@class, 'p-toast-icon-close')] | //div[contains(@class,'alert')]//button",
                                 "Alert Toast Close Button")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Toast: Summary Text")
    def get_toast_summary(self):
        return self.get_text().set_locator(self._div_toast_summary, self._name).by_text()

    @allure.step("Toast: Detail Text")
    def get_toast_detail(self):
        return self.get_text()\
            .set_locator(self._div_toast_detail, self._name)\
            .by_text()

    @allure.step("Toast: Close Button")
    def click_toast_close(self):
        self.click().set_locator(self._btn_toast_close, self._name).single_click()
