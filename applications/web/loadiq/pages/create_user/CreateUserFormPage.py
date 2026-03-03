from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.ui.actions.Element import Element
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = setup_logger('CreateUserFormPage')


class CreateUserFormPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the Create User Form Page instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/add-user"

        # Locator definitions
        ## Account Information
        self._dropdown_account_type = (By.XPATH,  "//*[@ng-reflect-name='accountType']", "Account Type [Dropdown]")
        self._input_tms = (By.XPATH, "//input[@ng-reflect-name='tradingPartnerNumber']", "TMS [Input Form]")
        self._input_account = (By.XPATH, "//input[@ng-reflect-name='carrierName']", "Account [Input Form]")

        ## Point of Contact
        self._input_first_name = (By.XPATH, "//input[@ng-reflect-name='firstname']", "First Name [Input Form]")
        self._input_last_name = (By.XPATH, "//input[@ng-reflect-name='lastname']", "Last Name [Input Form]")
        self._input_email = (By.XPATH, "//input[@ng-reflect-name='email']", "Email [Input Form]")
        self._dropdown_role = (By.XPATH, "//*[@ng-reflect-name='role']", "Role [Input Form]")

        self._btn_cancel = (By.XPATH, "//button[@type='reset']", "Cancel [Button]")
        self._btn_create_account = (By.XPATH, "//button[@type='submit']", "Create Account [Button]")

        self.txt_alert_message = (By.XPATH, "//span[@class='mat-simple-snack-bar-content']", "Alert Message [Text]")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = CreateUserFormPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load Page")
    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def _select_account_type(self, account_type):
        self.click().set_locator(self._dropdown_account_type).single_click()
        locator = (By.XPATH, f'//span[@class="mat-option-text" and contains(text(),"{account_type}")]', "Select Dropdown")

        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_tms(self, tms: str):
        self.send_keys().set_locator(self._input_tms, self._name).set_text(tms)
        return self

    def _enter_account(self, account: str):
        self.send_keys().set_locator(self._input_account, self._name).set_text(account)
        return self

    def _enter_first_name(self, first_name: str):
        self.send_keys().set_locator(self._input_first_name, self._name).set_text(first_name)
        return self

    def _enter_last_name(self, last_name: str):
        self.send_keys().set_locator(self._input_last_name, self._name).set_text(last_name)
        return self

    def _enter_email(self, email: str):
        self.send_keys().set_locator(self._input_email, self._name).set_text(email)
        return self

    @allure.step("Enter Account and Point Contact Information")
    def _select_role(self, role):
        self.click().set_locator(self._dropdown_role).single_click()
        locator = (By.XPATH, f'//span[@class="mat-option-text" and contains(text(),"{role}")]', "Select Dropdown")

        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Click on the Cancel Button")
    def click_cancel(self):
        self.click().set_locator(self._btn_cancel, self._name).single_click()
        return self

    @allure.step("Click on the Create Account Button")
    def click_create_account(self):
        self.click().set_locator(self._btn_create_account, self._name).single_click()
        return self

    @allure.step("Verify all locators are present on the Create User Form Page")
    def verify_all_locators_present(self):
        locators = [
            self._dropdown_account_type,
            self._input_tms,
            self._input_account,
            self._input_first_name,
            self._input_last_name,
            self._input_email,
            self._dropdown_role,
            self._btn_cancel,
            self._btn_create_account
        ]
        return self.verify_locators().verify_page_locators(locators)

    def get_alert_text(self):
        return self.get_text().set_locator(self.txt_alert_message, self._name).by_text()

    def enter_account_information(self, account_type, tms, account, first_name, last_name, email, role):
        self._select_account_type(account_type)
        self._enter_tms(tms)
        self._enter_account(account)
        self._enter_first_name(first_name)
        self._enter_last_name(last_name)
        self._enter_email(email)
        self._select_role(role)
