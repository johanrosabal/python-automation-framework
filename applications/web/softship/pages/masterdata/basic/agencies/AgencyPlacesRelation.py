import allure
from selenium.webdriver.common.by import By
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.common.SoftshipPage import SoftshipPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('AgencyPlacesRelation')


class AgencyPlacesRelation(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the AgencyPlacesRelation instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/Query/Index/AgencyPlacesRelation"
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root_head = (By.XPATH, "//table[@class='ui-jqgrid-htable']", "Agency Table")
        self._tbl_root_body = (By.XPATH, "//table[@id='queryScreenGrid']", "Agency Table")
        self._tbl_headers = None

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def _grid_table_head(self):
        return self.table_with_controls().set_locator(self._tbl_root_head, self._name)

    def _grid_table_body(self):
        return self.table_with_controls().set_locator(self._tbl_root_body, self._name)

    def click_select(self, pause: int = 3):
        self._buttons.click_select(pause)
        return self

    def click_select_toggle(self, pause: int = 1):
        self._buttons.click_select_toggle(pause)
        return self

    def click_edit(self, pause=1):
        self._buttons.click_edit()
        return self

    def click_new(self, pause: int = 1):
        self._buttons.click_new(pause)
        return self

    def click_copy(self, pause: int = 1):
        self._buttons.click_copy(pause)
        return self

    def click_delete(self, pause: int = 1):
        self._buttons.click_delete(pause)
        return self

    def click_save(self, pause: int = 1):
        self._buttons.click_save(pause)
        return self

    def click_cancel(self, pause: int = 1):
        self._buttons.click_cancel(pause)
        return self

    def click_export_excel(self, pause: int = 1):
        self._buttons.click_excel_export(pause)
        return self

    def click_customize_size(self, pause: int = 1):
        self._buttons.click_customize_screen(pause)
        return self

    def click_sql_info(self, pause: int = 1):
        self._buttons.click_sql_info(pause)
        return self

    def check_all(self):
        self._grid_table_head().check_all_rows()
        return self

    def check_record(self, index: int = 2):
        self._grid_table_body().check_rows(index=index, column=2)

    def click_edit_icon(self, index: int = 2):
        self._grid_table_body().click_edit_icon(index)

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table_head().get_table_headers()
        return self._tbl_headers

    def get_cell_agency(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Agency", self.get_table_headers())

    def get_cell_location(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Location", self.get_table_headers())

    def get_cell_function(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Function", self.get_table_headers())

    def get_cell_description(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Description", self.get_table_headers())

    def get_cell_free_text(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Free Text", self.get_table_headers())

    def get_cell_type(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Type", self.get_table_headers())

    def get_cell_zip_code(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Zip Code", self.get_table_headers())

    def get_cell_country(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Country", self.get_table_headers())

    def print_row(self, row):
        """
        Print a table data in the console.
        """
        # Extract Keys From Headers Dict
        # We need to process the Table Header to Get the Columns name and extract
        # all the 'keys' names and convert in to array
        headers = list(self.get_table_headers().keys())
        data = []

        agency = self.get_cell_agency(row) or "-"
        location = self.get_cell_location(row) or "-"
        function = self.get_cell_function(row) or "-"
        description = self.get_cell_description(row) or "-"
        free_text = self.get_cell_free_text(row) or "-"
        type_ = self.get_cell_type(row) or "-"
        zip_code = self.get_cell_zip_code(row) or "-"
        country = self.get_cell_country(row) or "-"

        data.append([agency, location, function, description, free_text, type_, zip_code, country])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()

    def click_previous(self):
        self._grid_table_body().click_previous()

    def click_next(self):
        self._grid_table_body().click_next()

    def select_pagination(self, number: int):
        self._grid_table_body().select_pagination(number)
