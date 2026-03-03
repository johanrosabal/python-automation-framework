import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('VoucherMenu')


class VoucherMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=2"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_voucher_normal = (By.XPATH, "//a[text()='Voucher Normal']", "Voucher Normal Link")
        self.__link_voucher_detail = (By.XPATH, "//a[text()='Voucher Detail']", "Voucher Detail Link")
        self.__link_incoming_invoices = (By.XPATH, "//a[text()='Incoming Invoices']", "Incoming Invoices Link")
        self.__link_balance_account = (By.XPATH, "//a[text()='Balance Account']", "Balance AccountLink")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["finance"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Voucher Normal")
    def link_voucher_normal(self, pause: int = 0):
        self._load_page(self.__link_voucher_normal, pause)
        return self

    @allure.step("Menu Voucher Detail")
    def link_voucher_detail(self, pause: int = 0):
        self._load_page(self.__link_voucher_detail, pause)
        return self

    @allure.step("Menu Incoming Invoices")
    def link_incoming_invoices(self, pause: int = 0):
        self._load_page(self.__link_incoming_invoices, pause)
        return self

    @allure.step("Menu Balance Account")
    def link_balance_account(self, pause: int = 0):
        self._load_page(self.__link_balance_account, pause)
        return self
