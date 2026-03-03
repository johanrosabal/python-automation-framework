import allure

from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('RebookingQueryPage')


class RebookingQueryPage(SoftshipPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/Query/Index/RebookingLegBasis"
        self._module_url = None
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root = (By.XPATH, "//table[contains(@id,'table')]", "Rebooking Table")
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

    def get_cell_service(self, row):
        return self._grid_table().get_row_data_by_header(row, "Service", self.get_table_headers(), True)

    def get_cell_vessel(self, row):
        return self._grid_table().get_row_data_by_header(row, "Vessel", self.get_table_headers(), True)

    def get_cell_voyage(self, row):
        return self._grid_table().get_row_data_by_header(row, "Voyage", self.get_table_headers(), True)

    def get_cell_agency(self, row):
        return self._grid_table().get_row_data_by_header(row, "Agency", self.get_table_headers(), True)

    def get_cell_booking_no(self, row):
        return self._grid_table().get_row_data_by_header(row, "Booking No.", self.get_table_headers(), True)

    def get_cell_booking_status(self, row):
        return self._grid_table().get_row_data_by_header(row, "Booking_Status", self.get_table_headers(), True)

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
        service = self.get_cell_service(row) or "-"
        vessel = self.get_cell_vessel(row) or "-"
        voyage = self.get_cell_voyage(row) or "-"
        agency = self.get_cell_agency(row) or "-"
        booking_no = self.get_cell_booking_no(row) or "-"
        booking_status = self.get_cell_booking_status(row) or "-"

        data.append([booking_ref, service, vessel, voyage, agency, booking_no, booking_status])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
