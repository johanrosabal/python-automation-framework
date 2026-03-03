import allure

from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('ContainerQueryPage')


class ContainerQueryPage(SoftshipPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/Booking/Query/Index/BookingAdvancedContainer"
        self._module_url = None
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root = (By.XPATH, "//table[contains(@id,'table')]", "Container Table")
        self._tbl_head = (By.XPATH, "p-datatable-thead", "Header Table")
        self._tbl_headers = None

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["booking"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def click_select(self, pause: int = 1):
        self._buttons.click_select(pause)
        return self

    def click_select_toggle(self, show=True, pause: int = 1):
        self._buttons.click_select_toggle(show=show, pause=pause)
        return self

    def click_export_excel(self, pause: int = 1):
        self._buttons.click_excel_export(pause)
        return self

    def click_multi_update(self, pause: int = 1):
        self._buttons.click_multi_update(pause)
        return self

    def click_create_events(self, pause: int = 1):
        self._buttons.click_create_events(pause)
        return self

    def click_manage_doc_bookings(self, pause: int = 1):
        self._buttons.click_manage_doc_only_bookings(pause)
        return self

    def click_copy_booking(self, pause: int = 1):
        self._buttons.click_copy_booking(pause)
        return self

    @allure.step("Query Search : field {field_name}, operator {field_operator}, value {field_value}")
    def query_search(self, field_name="", field_operator="", field_value=""):
        QuerySearchComponent(self._driver).execute_query(
            field_name=field_name,
            field_operator=field_operator,
            field_value=field_value,
            press_enter=True
        )

    def _grid_table(self):
        return self.table_with_controls().set_locator(self._tbl_root, self._name)

    def check_all(self):
        self._grid_table().check_all_rows()
        return self

    def check_record(self, index: int = 2):
        self._grid_table().check_rows(index=index, column=2)

    def click_edit_icon(self, index: int = 2):
        self._grid_table().click_edit_icon(index)

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table().get_table_headers(old_table=False)
        return self._tbl_headers

    def get_cell_booking_ref(self, row):
        return self._grid_table().get_row_data_by_header(row, "Booking Ref.", self.get_table_headers(), True)

    def get_cell_container_no(self, row):
        return self._grid_table().get_row_data_by_header(row, "Container No.", self.get_table_headers(), True)

    def get_cell_container_type(self, row):
        return self._grid_table().get_row_data_by_header(row, "Container Type", self.get_table_headers(), True)

    def get_cell_commodity_code(self, row):
        return self._grid_table().get_row_data_by_header(row, "Commodity Code", self.get_table_headers(), True)

    def get_cell_customer_id(self, row):
        return self._grid_table().get_row_data_by_header(row, "Customer ID", self.get_table_headers(), True)

    def get_cell_vessel(self, row):
        return self._grid_table().get_row_data_by_header(row, "Vessel", self.get_table_headers(), True)

    def get_cell_voyage(self, row):
        return self._grid_table().get_row_data_by_header(row, "Voyage", self.get_table_headers(), True)

    def click_previous(self):
        self._grid_table().click_previous()

    def click_next(self):
        self._grid_table().click_next()

    def select_pagination(self, number: int):
        self._grid_table().select_pagination(number)

    def print_row(self, row):

        headers = list(self.get_table_headers().keys())
        data = []

        booking_ref = self.get_cell_booking_ref(row) or "-"
        container_no = self.get_cell_container_no(row) or "-"
        container_type = self.get_cell_container_type(row) or "-"
        commodity_code = self.get_cell_commodity_code(row) or "-"
        customer_id = self.get_cell_customer_id(row) or "-"
        vessel = self.get_cell_vessel(row) or "-"
        voyage = self.get_cell_voyage(row) or "-"

        data.append([booking_ref, container_no, container_type,
                     commodity_code, customer_id, vessel, voyage])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
