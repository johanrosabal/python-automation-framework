import allure
from selenium.webdriver.common.by import By
from tabulate import tabulate

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('QuerySearchComponent')


class QuerySearchComponent(BasePage):

    def __init__(self, driver):
        """
        Initialize the SearchComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Close Search Query")
    def click_close_search(self, pause=2):
        _btn_close = (
            By.XPATH,
            "//*[@id='btnClearSearch']",
            "[X] Close Search Button"
        )
        self.click().set_locator(_btn_close, self._name).single_click().pause(pause)
        return self

    def click_add_expression(self, index=1):
        btn_add_plus = (
            By.XPATH,
            "(//button/span[contains(@class,'fa fa-plus')])["+str(index)+"]/..",
            "[+] Add Search Button"
        )
        self.click().set_locator(btn_add_plus, self._name).highlight().single_click().pause(1)
        return self

    def click_remove_expression(self, index=1):
        btn_add_plus = (
            By.XPATH,
            "(//button/span[contains(@class,'fa fa-minus')])["+str(index)+"]/..",
            "[-] Add Search Button"
        )
        self.click().set_locator(btn_add_plus, self._name).highlight().single_click().pause(1)
        return self

    @allure.step("Click Toggle Search")
    def click_toggle_search(self, show=True):
        """
           Ensure the search button is in the desired state (shown or hidden).

           :param show: If True, ensures the search option is visible ('fa-caret-up').
                        If False, ensures the search option is hidden ('fa-caret-down').
           """
        btn_select_search = (By.XPATH, "//*[@id='btnSearch']/span[2]/..", "Select Search Button")  # Button locator
        class_attribute = self.element().set_locator(btn_select_search, self._name).get_attribute("class")

        # Define the states based on the class attribute values
        is_hidden = "fa fa-caret-down" in class_attribute
        is_visible = "fa fa-caret-up" in class_attribute

        # If we want the search option to be shown
        if show and is_hidden:
            self.click().set_locator(btn_select_search, self._name).single_click().highlight()
            logger.info("Show: Search Button")

        # If we want the search option to be hidden
        elif not show and is_visible:
            self.click().set_locator(btn_select_search, self._name).single_click().highlight()
            logger.info("Hide: Search Button")

    def execute_query(self, index=1, field_name="", field_operator="", field_value="", press_enter=False):
        # Main Path Container For Search Expression
        main_xpath = f"(//div[contains(@class,'query-search')]/div//span[@class='expression'])[{index}]"
        # Local Locators
        field_name_xpath = (By.XPATH, main_xpath + "/span[@class='field-name']/select", "Field Name Dropdown")
        field_operator_xpath = (By.XPATH, main_xpath + "/span[@class='operator']/select", "Field Operator Dropdown")
        field_value_xpath = (By.XPATH, main_xpath + "/span[@name='fieldValue']//input", "Field Value Dropdown")

        self.dropdown().set_locator(field_name_xpath, self._name).by_text(field_name)
        self.dropdown().set_locator(field_operator_xpath, self._name).by_text(field_operator)

        keywords = ["has value", "has no value"]
        if not any(word in field_operator for word in keywords):
            self.send_keys().set_locator(field_value_xpath, self._name).clear().set_text(field_value)

        if press_enter:
            self.send_keys().set_locator(field_value_xpath, self._name).press_enter().pause(1)

        self.pause(1)

        return self

    def execute_queries(self, queries):
        press_enter = False
        size = len(queries)

        # Press Toggle Button Before any query instruction
        self.click_toggle_search()

        for index, query in enumerate(queries, start=1):
            # Add a new expression if it's not the first query
            if index > 1:
                self.click_add_expression(index=index - 1)

            # If it's filling the last query item, press enter should be TRUE
            if index == size:
                press_enter = True

            # Execute the simple query
            self.execute_query(
                index=index,
                field_name=query["field_name"],
                field_operator=query["field_operator"],
                field_value=query["field_value"],
                press_enter=press_enter
            )

            table_data = [[q["field_name"], q["field_operator"], q["field_value"]] for q in queries]
            logger.info(tabulate(table_data, headers=["Field Name", "Operator", "Value"], tablefmt="grid"))

        return self
