import allure
from selenium.webdriver.common.by import By
from tabulate import tabulate

from core.config.logger_config import setup_logger
from core.ui.actions.Element import Element
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('QuerySearchAdvanceComponent')


class QuerySearchAdvanceComponent(BasePage):

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
            "//button/span[contains(@class,'pi pi-times')]",
            "[X] Close Search Button"
        )
        self.click().set_locator(_btn_close, self._name).single_click().pause(pause)
        return self

    def click_add_expression(self, index=1):
        btn_add_plus = (
            By.XPATH,
            "(//button/span[contains(@class,'pi-plus')])["+str(index)+"]/..",
            "[+] Add Search Button"
        )
        self.click().set_locator(btn_add_plus, self._name).highlight().single_click().pause(1)
        return self

    def click_remove_expression(self, index=1):
        btn_add_plus = (
            By.XPATH,
            "(//button/span[contains(@class,'pi-minus')])["+str(index)+"]/..",
            "[-] Add Search Button"
        )
        self.click().set_locator(btn_add_plus, self._name).highlight().single_click().pause(1)
        return self

    @allure.step("Click Toggle Search")
    def click_toggle_search(self, show=True):
        """
           Ensure the search button is in the desired state (shown or hidden).

           :param show: If True, ensures the search option is visible ('pi-angleup').
                        If False, ensures the search option is hidden ('pi-angle-down').
           """
        btn_select_search = (By.XPATH, "//div/span[contains(@class,'pi-angle')]/.", "Select Search Button")
        class_attribute = self.element().set_locator(btn_select_search, self._name).get_attribute("class")

        # Define the states based on the class attribute values
        is_hidden = "pi-angle-down" in class_attribute
        is_visible = "pi-angle-up" in class_attribute

        self.pause(2)

        # If we want the search option to be shown
        if show and is_hidden:
            self.click().set_locator(btn_select_search, self._name).single_click().highlight()
            logger.info("Show: Search Button")

        # If we want the search option to be hidden
        elif not show and is_visible:
            self.click().set_locator(btn_select_search, self._name).single_click().highlight()
            logger.info("Hide: Search Button")

        # (//div[contains(@class,'selection-bar')]/aqs-select-group/div)[1]

    def execute_query(self, index=1, field_name="", field_operator="", field_value="", press_enter=False):
        # Main Path Container For Search Expression
        main_xpath = f"(//div[contains(@class,'selection-bar')]/aqs-select-group/div)[{index}]"
        field_name_input_xpath = "//div[contains(@class,'p-overlay p-component')]//input"
        field_list_items_xpath = "//div[contains(@class,'p-overlay p-component')]//ul//li/span"

        container_index = 0
        if index > 1:
            container_index = 1

        # Field Name ------------------------------------------------------------------------------------------------- #
        field_name_open_xpath = f"/p-dropdown[{(1+container_index)}]"
        field_name_label = (By.XPATH, f"{main_xpath}{field_name_open_xpath}", "Field Name Label")
        field_name_input = (By.XPATH, f"{main_xpath}{field_name_open_xpath}{field_name_input_xpath}", "Field Name Dropdown")
        field_name_list_items = (By.XPATH, f"{main_xpath}{field_name_open_xpath}{field_list_items_xpath}", "Items Field Name Dropdown")

        self.click().set_locator(field_name_label, self._name).single_click()
        self.send_keys().set_locator(field_name_input, self._name).clear().set_text(field_name)

        # Use 'self.driver' from BaseApp because it's using a static method
        field_name_items = Element.wait_for_elements(self.driver, field_name_list_items, timeout=10)
        for item in field_name_items:
            if item.text == field_name:
                item.click()  # Click the matching item
                logger.info("[Field Name] Dropdown Option Found: " + item.text)
                break  # Exit loop after selecting the item

        # Operator Name ---------------------------------------------------------------------------------------------- #
        field_operator_open_xpath = f"/p-dropdown[{(2+container_index)}]"
        field_operator_label = (By.XPATH, f"{main_xpath}{field_operator_open_xpath}", "Field Name Label")
        field_operator_list_items = (By.XPATH, f"{main_xpath}{field_operator_open_xpath}{field_list_items_xpath}", "Items Field Operartor Dropdown")

        self.click().set_locator(field_operator_label, self._name).single_click()

        # Use 'self.driver' from BaseApp because it's using a static method
        field_operator_items = Element.wait_for_elements(self.driver, field_operator_list_items, timeout=10)
        for item in field_operator_items:
            if item.text == field_operator:
                item.click()  # Click the matching item
                logger.info("[Field Operator] Dropdown Option Found: " + item.text)
                break  # Exit loop after selecting the item

        # Value Name ---------------------------------------------------------------------------------------------- #
        field_value_input_xpath = "//input"
        field_value_input = (By.XPATH, f"({main_xpath}{field_value_input_xpath})[{(3+container_index)}]", "Field Value Input")

        self.send_keys().set_locator(field_value_input, self._name).clear().set_text(field_value)

        if press_enter:
            self.send_keys().set_locator(field_value_input, self._name).press_enter().press_tab().pause(1)

        self.pause(2)
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
