from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.actions.Click import Click
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.actions.SendKeys import SendKeys
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element

logger = setup_logger('DropdownAutocomplete')


class SearchAutocomplete:

    def __init__(self, driver):
        """
        Initialize the SearchDropdownAutocomplete instance.

        :param driver: Selenium WebDriver instance for interacting with the web application.
        """
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._btn_clear_list = (By.XPATH, "//button[@id='btnClearActiveCriteria']", "Clear List Button")

    def set_locator(self, locator: tuple, page='Page'):
        """
        Set the locator for the autocomplete input field and locate the element.

        This method waits for the element to be present on the page and logs the operation.

        :param locator: A tuple that contains the locator strategy and value (e.g., (By.ID, 'input-field-id')).
        :param page: The page name where the element is located, used for logging.
        :return: Returns self for method chaining.
        """
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def set_locator_by_attribute(self, attribute: str = "", value: str = "", page='Page'):
        """
        Use a locator for the input box using the attribute and value for the web element

        :param page:
        :param value:
        :param attribute:
        :return: Returns self for method chaining.
        """
        xpath = f"//input[@type='text' and contains(@{attribute},'{value}')]"
        locator = (By.XPATH, xpath, f"Page{page}, Dropdown Autocomplete by: Attribute: {attribute}, Value: {value})")
        self._element = Element.wait_for_element(self._driver, locator)
        return self

    def pause(self, seconds: int):
        """
        Pause the execution for a given number of seconds.

        :param seconds: Number of seconds to pause.
        :return: Returns self for method chaining.
        """
        BaseApp.pause(seconds)
        return self

    def clear(self):
        """
        Clear the text from the autocomplete input field.

        :return: Returns self for method chaining.
        """
        if self._element:
            self._element.clear()
        return self

    def click_clear_list(self):
        Click(self._driver).set_locator(self._btn_clear_list).single_click().screenshot(name="Clear List")
        return self

    def clear_search_item(self, text: str):
        parent_xpath = "//ul[@ui-sortable='tariff.actualCriteriaOptions']/li/div/"
        delete_xpath = "span[1]"
        text_xpath = "span[2]"

        list_container = (By.XPATH, f"{parent_xpath}{text_xpath}")
        list_buttons = (By.XPATH, f"{parent_xpath}{delete_xpath}")

        items = Element.wait_for_elements(self._driver, list_container)
        items_buttons = Element.wait_for_elements(self._driver, list_buttons)

        for index, item in enumerate(items):
            if item.text == text:
                logger.info("Search Option Found: " + item.text)
                btn_delete = items_buttons[index]
                ElementHighlighter(self._driver).set_element(btn_delete).highlight_temporarily()
                Click(self._driver).set_element(btn_delete).single_click().screenshot(name="clear_search_criteria")
                break  # Exit loop after selecting the item
        return self

    def check_compulsory_item(self, text: str):
        parent_xpath = "//ul[@ui-sortable='tariff.actualCriteriaOptions']/li/div/"
        text_xpath = "span[2]"
        checkbox_xpath = "input[@type='checkbox']"

        list_container = (By.XPATH, f"{parent_xpath}{text_xpath}")
        list_checkbox = (By.XPATH, f"{parent_xpath}{checkbox_xpath}")

        items = Element.wait_for_elements(self._driver, list_container)
        checkbox_items = Element.wait_for_elements(self._driver, list_checkbox)

        for index, item in enumerate(items):
            if item.text == text:
                logger.info("Search Option Found: " + item.text)
                checkbox = checkbox_items[index]
                ElementHighlighter(self._driver).set_element(checkbox).highlight_temporarily()
                Click(self._driver).set_element(checkbox).single_click().screenshot(name="check_compulsory")
                break  # Exit loop after selecting the item
        return self

    def by_text(self, text: str):
        """
        Type the provided text into the autocomplete input field and select the matching item from the dropdown.

        This method sends the text to the input field, waits for the dropdown options to appear,
        and selects the item that matches the provided text. The search for the option is done in the specified column.

        :param text: The text to type into the input field and search for in the dropdown.
        :return: None
        """
        if self._element:

            SendKeys(self._driver).set_element(self._element).clear().set_text(text).pause(1)
            parent_xpath = "//ul[@id='rightSortingList' and @ui-sortable='tariff.possibleCriteriaOptions']/li[contains(@class, 'list-group-item') and not(contains(@class, 'ng-hide'))]/div"
            # List Options

            modal_list_locator_text = (By.XPATH, f"{parent_xpath}/span")
            modal_list_locator_buttons = (By.XPATH, f"{parent_xpath}/button")

            items = Element.wait_for_elements(self._driver, modal_list_locator_text)
            buttons = Element.wait_for_elements(self._driver, modal_list_locator_buttons)

            for index, item in enumerate(items):
                if item.text == text:
                    logger.info("Search Option Found: " + item.text)
                    button = buttons[index]
                    ElementHighlighter(self._driver).set_element(button).highlight_temporarily()
                    Click(self._driver).set_element(button).single_click()
                    break  # Exit loop after selecting the item

            else:
                logger.error("Dropdown Option Not Found: " + text)

        return self
