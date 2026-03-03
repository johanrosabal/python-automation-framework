from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.ui.actions.Element import Element
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = setup_logger('UserManagementPage')


class UserManagementPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the User Management Page instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/user-manage"

        # Locator definitions
        ## Search Bar
        self._input_search_bar = (By.XPATH,  "//input[@ng-reflect-message='Search by First name, Last nam']", "Search bar [Dropdown]")
        self._btn_search = (By.XPATH, "//button[@ng-reflect-message='Search']", "Search [Button]")
        self._lbl_total_records = (By.XPATH, "//span[contains(@class, 'search-result' )]", "Total of Records [Label]")



        self._btn_cancel = (By.XPATH, "//button[@type='reset']", "Cancel [Button]")
        self._btn_create_account = (By.XPATH, "//button[@type='submit']", "Create Account [Button]")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = UserManagementPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load Page")
    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def _enter_search_criteria(self, search_criteria: str):
        self.send_keys().set_locator(self._input_search_bar, self._name).pause(5).set_text(search_criteria)
        return self

    def _click_search(self):
        self.click().set_locator( self._btn_search, self._name).pause(5).single_click()
        return self

    @allure.step("Search User")
    def search_user(self, search_criteria: str):
        self._enter_search_criteria(search_criteria)
        self._click_search().pause(3)
        return self

    def get_table_headers(self):
        """
        Gets the text from all table headers to use as dictionary keys.

        :return: A list of strings with the header names.
        """
        header_elements = self.driver.find_elements(By.XPATH, "//table/thead//th/a")
        # We exclude the 'Profile' header as it contains no data, only a button.
        headers = [header.text for header in header_elements if header.text and header.text != 'Profile']
        return headers

    def get_user_data_as_dict(self, account_name):
        """
        Finds a user row by their Account Name, extracts all data, and returns it as a dictionary.

        :param account_name: The unique Account Name to find the user row.
        :return: A dictionary where keys are column headers and values are the cell data for that user.
                 Returns an empty dictionary if the user is not found.
        """
        try:
            # 1. Get the list of headers to use as keys.
            headers = self.get_table_headers()

            # 2. Locate the specific row for the given account_name.
            user_row_xpath = f"//tbody/tr[td[contains(., '{account_name}')]]"
            row = self.driver.find_element(By.XPATH, user_row_xpath)

            # 3. Get all data cells from that specific row.
            cells = row.find_elements(By.XPATH, "./td")

            # 4. Extract text from each cell, ignoring the 'Profile' column which has the button.
            cell_texts = [cell.text for cell in cells if cell.text and cell.text != 'View']

            # 5. Combine headers and cell texts into a dictionary.
            user_data = dict(zip(headers, cell_texts))

            return user_data

        except Exception:
            print(f"User with Account Name '{account_name}' not found in the table.")
            return {}

