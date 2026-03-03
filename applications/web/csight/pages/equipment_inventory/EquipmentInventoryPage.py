from selenium.webdriver.common.by import By
from tabulate import tabulate

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.pages.equipment_inventory.searchs.SearchPanel import SearchPanel
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('EquipmentInventoryPage')


class EquipmentInventoryPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the EquipmentInventoryPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/equipmentinventory"
        # Base XPaths Strings
        self._xpath_item_container = "(//div[@class='booking-list-data-row'])"
        # Sub-Components
        self.search_panel = SearchPanel.get_instance()
        self.buttons = Buttons.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    # Pagination -------------------------------------------------------------------------------------------------------
    def click_refresh_icon(self):
        self.buttons.click_refresh_icon()
        return self

    def select_view_pages(self, number):
        self.buttons.select_view_pages(number)
        return self

    def click_previous_page(self):
        self.buttons.click_previous_page()
        return self

    def click_next_page(self):
        self.buttons.click_next_page()
        return self

    def click_sort_by_sublocation(self):
        self.buttons.click_sort_by("SUBLOCATION")
        return self

    def click_sort_by_size_type(self):
        self.buttons.click_sort_by("SIZE TYPE")
        return self

    def click_sort_by_full_empty(self):
        self.buttons.click_sort_by("FULL/EMPTY")
        return self

    # TABS ------------------------------------------------------------------------------------------------------------
    def click_tab_all_bookings(self):
        self.buttons.click_tab_button_with_label("Summary")
        return self

    def click_tab_pending(self):
        self.buttons.click_tab_button_with_label("Details")
        return self

    # ITEMS ------------------------------------------------------------------------------------------------------------
    def get_list_item_equipment_type(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Equipment Type']/..//label", f"Equipment Inventory Item [{index}]: Equipment Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_size_type(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Size / Type']/..//label", f"Equipment Inventory Item [{index}]: Size / Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_full_empty(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Full / Empty']/..//label", f"Equipment Inventory Item [{index}]: Full/Empty [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_number_of_equipments(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Number Of Equipments']/..//label", f"Equipment Inventory Item [{index}]: Number of Equipments [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_sublocation(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Sublocation']/..//label", f"Equipment Inventory Item [{index}]: Sublocation [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item_direction(self, index):
        locator = (By.XPATH, f"({self._xpath_item_container})[{str(index)}]//label[text()='Direction']/..//label", f"Equipment Inventory Item [{index}]: Direction [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_list_item(self, index):

        equipment_type = self.get_list_item_equipment_type(index) or "-"
        size_type = self.get_list_item_size_type(index) or "-"
        full_empty = self.get_list_item_full_empty(index) or "-"
        number_of_equipments = self.get_list_item_number_of_equipments(index) or "-"
        sublocation = self.get_list_item_sublocation(index) or "-"
        direction = self.get_list_item_direction(index) or "-"

        data = {
            "Equipment Type": equipment_type,
            "Size / Type": size_type,
            "Full / Empty": full_empty,
            "Number of Equipment": number_of_equipments,
            "Sublocation": sublocation,
            "Direction": direction
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data
