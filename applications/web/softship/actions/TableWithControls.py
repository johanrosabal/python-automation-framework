from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from core.config.logger_config import setup_logger
from core.ui.actions.Element import Element
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.Table import Table
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('TableWithControls')


class TableWithControls(Table):

    def __init__(self, driver):
        """
        Initialize the DropdownAutocomplete instance.

        :param driver: Selenium WebDriver instance for interacting with the web application.
        """
        super().__init__(driver)
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def check_all_rows(self):
        """
        Get all table data as a list of cell data.
        """
        checkbox = self._element.find_element(By.XPATH,
                                              "thead/tr/th[2]//div[contains(@class,'checkbox')] | //table[@class='ui-jqgrid-htable']/thead/tr/th[2]//input")
        if checkbox and checkbox.is_displayed():
            ElementHighlighter(self._driver).set_element(checkbox).highlight_temporarily(1)
            checkbox.click()

    def click_edit_icon(self, index: int = 1, column: int = 4):
        """
        Get click on edit icon
        """
        root = self._locator[1]
        xpath = f"{root}/tbody/tr[{str(index)}]/td[{str(column)}]//a"
        edit_icon_locator = (By.XPATH, xpath, f"Table Edit Icon: Row {index}, Column {column}")
        icon = Element(self._driver).wait(edit_icon_locator)

        # icon = self._element.find_element(By.XPATH, f"tbody/tr[{index}]/td[{column}]//a")
        if icon and icon.is_displayed():
            ElementHighlighter(self._driver).set_element(icon).highlight_temporarily(1)
            icon.click()

    def click_previous(self):
        button = self._driver.find_element(By.XPATH,
                                           "//button[contains(@class,'paginator-prev')] | //td[@id='prev_queryScreenGrid-footer']")
        if button and button.is_displayed() and button.is_enabled():
            ElementHighlighter(self._driver).set_element(button).highlight_temporarily(1)
            button.click()
            BaseApp.pause(1)

    def click_next(self):
        button = self._driver.find_element(By.XPATH,
                                           "//button[contains(@class,'paginator-next')] | //td[@id='next_queryScreenGrid-footer']")
        if button and button.is_displayed() and button.is_enabled():
            ElementHighlighter(self._driver).set_element(button).highlight_temporarily(1)
            button.click()
            BaseApp.pause(1)

    def select_pagination(self, number: int = 200):

        try:
            old_select = WebDriverWait(self._driver, 2).until(
                ec.presence_of_element_located((By.XPATH, "//select[@class='ui-pg-selbox']"))
            )
        except TimeoutException:
            old_select = None

        if old_select:
            Select(old_select).select_by_visible_text(str(number))
            logger.info(f"Pagination: {number}")
            BaseApp.pause(1)
        else:
            # Locators
            label_ = (
                By.XPATH, "//div[contains(@class,'paginator')]/div[@class='p-dropdown-trigger']",
                "Pagination: Dropdown Label")
            list_ = (By.XPATH, "//ul[@role='listbox']//li", "Pagination: List Options")

            # Getting Dropdown Label
            dropdown_label = Element.wait_for_element(driver=self._driver, locator=label_)
            if dropdown_label and dropdown_label.is_displayed() and dropdown_label.is_enabled():
                dropdown_label.click()

                # Reading Dropdown Options
                items = Element.wait_for_elements(driver=self._driver, locator=list_)

                # Looping Option to match number
                for item in items:
                    if item.text == str(number):
                        item.click()  # Click the matching item
                        logger.info("Dropdown Option Found: " + item.text)
                        break  # Exit loop after selecting the item

    def select_page(self, number: int = 1):
        page = (By.XPATH,
                f"//span[contains(@class,'paginator-pages')]/button[text()=' {number} ']",
                f"Pagination: Page Number{number}")

        page_button = Element.wait_for_element(driver=self._driver, locator=page)
        if page_button and page_button.is_displayed() and page_button.is_enabled():
            page_button.click()

    def table_footer(self):
        footer = (By.XPATH, "//td[@id='queryScreenGrid-footer_right']/div | //div[contains(@class,'no-data-info')]/h4", "Table Footer")
        footer_text = Element.wait_for_element(driver=self._driver, locator=footer)
        if footer_text and footer_text.is_displayed() and footer_text.is_enabled():
            return footer_text.text
