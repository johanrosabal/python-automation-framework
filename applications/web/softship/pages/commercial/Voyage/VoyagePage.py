import allure
from selenium.webdriver.common.by import By

from applications.web.softship.common.SoftshipPage import SoftshipPage
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchAdvanceComponent import QuerySearchAdvanceComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('VoyagePage')


class VoyagePage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the VoyagePage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/Query/Index/VoyageAdvanced"
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root = (By.XPATH, "//table[contains(@id,'table')]", "Voyage Table")
        self._tbl_headers = None
        self._no_data_info_container = (By.XPATH, "//div[@class='no-data-info-inner-container']","Where is the data? [Div Container]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["commercial"]
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

    def click_new(self, pause: int = 1):
        self._buttons.click_new(pause)
        return self

    def click_delete(self, pause: int = 1):
        self._buttons.click_delete(pause)
        return self

    def click_create_new_voyage_from_template(self, pause: int = 1):
        self._buttons.click_create_new_voyage_from_template(pause)
        return self

    def click_create_new_voyage_from_selected_voyage(self, pause: int = 1):
        self._buttons.click_create_new_voyage_from_selected_voyage(pause)
        return self

    def click_calculate_cut_off(self, pause: int = 1):
        self._buttons.click_calculate_cut_off(pause)
        return self

    def _grid_table(self):
        return self.table_with_controls().set_locator(self._tbl_root, self._name)

    def check_all(self):
        self._grid_table().check_all_rows()
        return self

    def check_record(self, index: int = 1):
        self._grid_table().check_rows(index=index, column=2)

    def click_edit_icon(self, index: int = 1):
        self._grid_table().click_edit_icon(index)

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table().get_table_headers()
        return self._tbl_headers

    def get_cell_source(self, row):
        return self._grid_table().get_row_data_by_header(row, "Source", self.get_table_headers())

    def get_cell_publish_voyage(self, row):
        return self._grid_table().get_row_data_by_header(row, "Publish Voyage", self.get_table_headers())

    def get_cell_service(self, row):
        return self._grid_table().get_row_data_by_header(row, "Service", self.get_table_headers())

    def get_cell_vessel_code(self, row):
        return self._grid_table().get_row_data_by_header(row, "Vessel Code", self.get_table_headers())

    def get_cell_voyage_number(self, row):
        return self._grid_table().get_row_data_by_header(row, "Voyage Number", self.get_table_headers())

    def get_cell_status(self, row):
        return self._grid_table().get_row_data_by_header(row, "Status", self.get_table_headers())

    def get_cell_central_port(self, row):
        return self._grid_table().get_row_data_by_header(row, "Central Port", self.get_table_headers())

    def get_cell_central_date(self, row):
        return self._grid_table().get_row_data_by_header(row, "Central Date", self.get_table_headers())

    def get_cell_second_voyage_number(self, row):
        return self._grid_table().get_row_data_by_header(row, "Second Voyage Number", self.get_table_headers())

    def get_cell_vessel_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "Vessel Name", self.get_table_headers())

    def get_cell_voyage_machine_number(self, row):
        return self._grid_table().get_row_data_by_header(row, "Voyage Machine Number", self.get_table_headers())

    def get_cell_create_user(self, row):
        return self._grid_table().get_row_data_by_header(row, "Create User", self.get_table_headers())

    def get_cell_operator(self, row):
        return self._grid_table().get_row_data_by_header(row, "Operator", self.get_table_headers())

    def get_cell_financial_voyage_period(self, row):
        return self._grid_table().get_row_data_by_header(row, "Financial Voyage Period", self.get_table_headers())

    def get_cell_commercial_service(self, row):
        return self._grid_table().get_row_data_by_header(row, "Commercial Service", self.get_table_headers())

    def validate_data_results(self):
        data = self.element().wait(
            locator=self._no_data_info_container,
            timeout=3
        )
        if data is not None:
            if data.is_displayed():
                logger.info("No Data Results Displayed")
                return False
        return True

    def get_table_row(self, row):
        """
        Print a table data in the console.
        """
        # Extract Keys From Headers Dict
        # We need to process the Table Header to Get the Columns name and extract
        # all the 'keys' names and convert in to array
        headers = list(self.get_table_headers().keys())
        data = []

        source = self.get_cell_source(row) or "-"
        publish_voyage = self.get_cell_publish_voyage(row) or "-"
        service = self.get_cell_service(row) or "-"
        vessel_code = self.get_cell_vessel_code(row) or "-"
        voyage_number = self.get_cell_voyage_number(row) or "-"
        status = self.get_cell_status(row) or "-"
        central_port = self.get_cell_central_port(row) or "-"
        central_date = self.get_cell_central_date(row) or "-"
        second_voyage_number = self.get_cell_second_voyage_number(row) or "-"
        vessel_name = self.get_cell_vessel_name(row) or "-"
        voyage_machine_number = self.get_cell_voyage_machine_number(row) or "-"
        # create_user = self.get_cell_create_user(row) or "-"
        operator = self.get_cell_operator(row) or "-"
        financial_voyage_period = self.get_cell_financial_voyage_period(row) or "-"
        commercial_service = self.get_cell_commercial_service(row) or "-"

        data.append([
            source,
            service,
            vessel_code,
            voyage_number,
            status,
            central_port,
            central_date,
            second_voyage_number,
            vessel_name,
            voyage_machine_number,
            operator,
            financial_voyage_period,
            commercial_service,
            publish_voyage,
        ])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()

        return data[0]

    def click_previous(self):
        self._grid_table().click_previous()

    def click_next(self):
        self._grid_table().click_next()

    def select_pagination(self, number: int):
        self._grid_table().select_pagination(number)

    def select_page(self, number: int):
        self._grid_table().select_page(number)

    @allure.step("Query Search : field {field_name}, operator {field_operator}, value {field_value}")
    def query_search(self, field_name="", field_operator="", field_value=""):

        self.search_advance_filter().execute_query(
            field_name=field_name,
            field_operator=field_operator,
            field_value=field_value,
            press_enter=True
        )

        return self

    def queries_search(self, queries):
        self.search_advance_filter().execute_queries(queries)
        return self



