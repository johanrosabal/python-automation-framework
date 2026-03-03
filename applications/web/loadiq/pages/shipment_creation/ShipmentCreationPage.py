from enum import Enum

from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('ShipmentCreationPage')


class ShipmentCreationPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the ShipmentCreationPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/draftlist"
        # Locator definitions
        self._no_load = (By.XPATH, '//h5[contains(text(),"Sorry, we couldn\'t find any results.")]', "[Sorry, we couldn't find any results.]")
        self._input_search_by = (By.XPATH, "//input[@type='text' and contains(@mattooltip,'Search by')]", "Search by [Input Box]")
        self._button_search = (By.XPATH, "//button[@mattooltip='Search']", "Search [Button]")
        self._button_create_shipment = (By.XPATH, "//button/span/span[contains(text(),'Create Shipment')]", "Create Shipment [Button]")
        self._text_total_number_of_draft = (By.XPATH, "//span[contains(@class,'search-result')]", "Total Number of draft shipments")
        self._select_sort_dropdown = (By.XPATH, "//select[@name='sortingField']", "Sort By [Dropdown]")
        self._order_asc_desc = (By.XPATH, "//select[@name='sortingField']/following-sibling::span[1]", "Order Ascending | Descending [Button]")
        #Feedback
        self._button_feedback = (By.XPATH, "//*[@id='mybutton']/button")
        self._input_feedback_comment = (By.XPATH, "//app-feedback-form//form//div[3]/div[2]")
        self._button_submit = (By.XPATH, "//button[@data-cy='feedbacksubmit']")
        self._button_cancel = (By.XPATH, "//button[@data-cy='feedbackclose']")



    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = ShipmentCreationPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def no_load_results(self):
        try:
            element = self.element().wait(self._no_load, 2)
            return element is not None
        except Exception as e:
            logger.error(f"{e.msg}")
            return False

    def enter_search_by(self, text: str):
        self.send_keys().set_locator(self._input_search_by, self._name).set_text(text)
        return self

    def click_search(self):
        self.click().set_locator(self._button_search, self._name).single_click().pause(3)
        return self

    def enter_feedback_comment(self, text: str):
        self.send_keys().set_locator(self._input_feedback_comment, self._name).set_text(text)
        return self

    def click_feedback_button(self):
        self.click().set_locator(self._button_feedback, self._name).single_click().pause(3)
        return self

    def click_feedback_button_submit(self):
        self.click().set_locator(self._button_submit, self._name).single_click().pause(3)
        return self

    def click_feedback_button_cancel(self):
        self.click().set_locator(self._button_cancel, self._name).single_click().pause(3)
        return self

    def search_by(self, text):
        self.enter_search_by(text)
        self.click_search()
        return self

    def search_clear(self):
        self.send_keys().set_locator(self._input_search_by, self._name).clear()

    def click_create_shipment(self):
        self.click().set_locator(self._button_create_shipment, self._name).highlight().single_click()
        return self

    def get_total_draft_shipments(self):
        return self.get_text().set_locator(self._text_total_number_of_draft, self._name).by_text()

    def select_sort_by(self, sort_options):
        # Validate Enum Argument
        if not isinstance(sort_options, Enum):
            raise ValueError("Invalid account type. Must be an Enum member.")

        self.dropdown().set_locator(self._select_sort_dropdown, self._name).by_text(sort_options.value).pause(2)
        return self

    def click_order(self):
        self.click().set_locator(self._order_asc_desc, self._name).single_click()

    def get_shipment_tracker_number(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Shipment Number')]/following-sibling::span[1])[{str(index)}]", "Shipment Number")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def get_address_origin(self, index: int):
        origin = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'origin')]/span)[{str(index)}]", "Address Origin")
        if self.element().is_present(origin):
            return self.get_text().set_locator(origin, self._name).by_text()
        else:
            return "-"

    def get_address_origin_tooltip(self, index: int):
        origin = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'origin')]/span)[{str(index)}]", "Address Origin")

        if self.element().is_present(origin):
            self.click().set_locator(origin, self._name).mouse_over()

            xpath_1 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'origin')]/div/div/span[1])[{str(index)}]", "Tool Tip Origin Line 1")
            xpath_2 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'origin')]/div/div/span[2])[{str(index)}]", "Tool Tip Origin Line 2")
            xpath_3 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'origin')]/div/div/span[3])[{str(index)}]", "Tool Tip Origin Line 3")
            xpath_4 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'origin')]/div/div/span[4])[{str(index)}]", "Tool Tip Origin Line4 ")

            tooltip = {
                "line_1": self.get_text().set_locator(xpath_1, self._name).by_text(),
                "line_2": self.get_text().set_locator(xpath_2, self._name).by_text(),
                "line_3": self.get_text().set_locator(xpath_3, self._name).by_text(),
                "line_4": self.get_text().set_locator(xpath_4, self._name).by_text(),
            }

            return tooltip
        else:
            return "-"

    def get_address_destination(self, index: int):
        destination = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'dest')]/span)[{str(index)}]", "Address Destination")
        if self.element().is_present(destination):
            return self.get_text().set_locator(destination, self._name).by_text()
        else:
            return "-"

    def get_address_destination_tooltip(self, index: int):
        destination = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'dest')]/span)[{str(index)}]", "Address Destination")

        if self.element().is_present(destination):
            self.click().set_locator(destination, self._name).mouse_over()
            xpath_1 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'dest')]/div/div/span[1])[{str(index)}]", "Tool Tip Destination Line 1")
            xpath_2 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'dest')]/div/div/span[2])[{str(index)}]", "Tool Tip Destination Line 2")
            xpath_3 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'dest')]/div/div/span[3])[{str(index)}]", "Tool Tip Destination Line 3")
            xpath_4 = (By.XPATH, f"(//div[contains(@class,'address')]/a[contains(@class,'dest')]/div/div/span[4])[{str(index)}]", "Tool Tip Destination Line 4")

            tooltip = {
                "line_1": self.get_text().set_locator(xpath_1, self._name).by_text(),
                "line_2": self.get_text().set_locator(xpath_2, self._name).by_text(),
                "line_3": self.get_text().set_locator(xpath_3, self._name).by_text(),
                "line_4": self.get_text().set_locator(xpath_4, self._name).by_text(),
            }

            return tooltip
        else:
            return "-"

    def get_request_equipment(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Requested Equipment')]/following-sibling::span[1])[{str(index)}]", "Requested Equipment")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_created_by(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Created By')]/following-sibling::span[1])[{str(index)}]", "Created By")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_created_date(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Created Date')]/following-sibling::span[1])[{str(index)}]", "Created Date")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_modified_date(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Modified Date')]/following-sibling::span[1])[{str(index)}]", "Modified Date")
        return self.get_text().set_locator(locator, self._name).by_text()

    def click_action_edit(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Actions')]/following-sibling::i[1])[{str(index)}]", "Edit [Action]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_action_copy(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Actions')]/following-sibling::i[2])[{str(index)}]", "Copy [Action]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_action_delete(self, index: int):
        locator = (By.XPATH, f"(//label[contains(text(),'Actions')]/following-sibling::i[3])[{str(index)}]", "Delete [Action]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def get_shipment_item(self, index: int):

        data = []
        tooltip1 = self.get_address_origin_tooltip(index)
        tooltip1 = ", ".join(tooltip1.values()) or "-"

        tooltip2 = self.get_address_destination_tooltip(index)
        tooltip2 = ", ".join(tooltip2.values()) or "-"

        shipment_number = self.get_shipment_tracker_number(index) or "-"
        address_origin = self.get_address_origin(index) or "-"
        address_origin_tooltip = tooltip1 or "-"
        address_destination = self.get_address_destination(index) or "-"
        address_destination_tooltip = tooltip2 or "-"
        requested_equipment = self.get_request_equipment(index) or "-"
        created_by = self.get_created_by(index) or "-"
        created_date = self.get_created_date(index) or "-"
        modified_date = self.get_modified_date(index) or "-"

        headers = [
            "Shipment Number",
            "Address Origin",
            "Address Origin Tooltip",
            "Address Destination",
            "Address Destination Tooltip",
            "Requested Equipment",
            "Created By",
            "Created Date",
            "Modified Date"
        ]

        data.append([
            shipment_number,
            address_origin,
            address_origin_tooltip,
            address_destination,
            address_destination_tooltip,
            requested_equipment,
            created_by,
            created_date,
            modified_date
        ])

        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return data[0]


class SortOptions(Enum):
    SHIPMENT_NUMBER = "Shipment Number"
    MODE = "Mode"
    ORIGIN = "Origin"
    DESTINATION = "Destination"
    REQUESTED_EQUIPMENT = "Requested Equipment"
    CREATED_BY = "Created By"
    CREATED_DATE = "Created Date"
    MODIFIED_DATE = "Modified Date"






