import allure
from selenium.webdriver.common.by import By

from applications.web.softship.common.SoftshipPage import SoftshipPage
from applications.web.softship.components.alert.AlertDialogBox import AlertDialogBox
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('PurchaseTariffCriteriaPage')


class PurchaseTariffCriteriaPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the PurchaseTariffCriteriaPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver

        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Query/Index/PurchaseTariffCriteria"
        self._module_url = None
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root_head = (By.XPATH, "//table[@class='ui-jqgrid-htable']", "Purchase Tariff Criteria Table")
        self._tbl_root_body = (By.XPATH, "//table[@id='queryScreenGrid']", "Purchase Tariff Criteria Table")
        self._tbl_headers = None
        # Alert
        self.alert = AlertDialogBox(self._driver)

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["finance"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def click_select(self, pause: int = 1):
        self._buttons.click_select(pause)
        return self

    def click_select_toggle(self, show=True, pause: int = 1):
        self._buttons.click_select_toggle(show=show, pause=pause)
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

    def click_confirmation_yes(self, pause: int = 1):
        self._buttons.click_confirm_yes(pause)
        return self

    def click_confirmation_no(self, pause: int = 1):
        self._buttons.click_confirm_no(pause)
        return self

    def click_export_excel(self, pause: int = 1):
        self._buttons.click_excel_export(pause)
        return self

    def click_customize_screen(self, pause: int = 1):
        self._buttons.click_customize_screen(pause)
        return self

    def click_sql_info(self, pause: int = 1):
        self._buttons.click_sql_info(pause)
        return self

    @allure.step("Query Search : field {field_name}, operator {field_operator}, value {field_value}")
    def query_search(self, field_name="", field_operator="", field_value=""):
        QuerySearchComponent(self._driver).execute_query(
            field_name=field_name,
            field_operator=field_operator,
            field_value=field_value,
            press_enter=True
        )
        return self

    def _grid_table_head(self):
        return self.table_with_controls().set_locator(self._tbl_root_head, self._name)

    def _grid_table_body(self):
        return self.table_with_controls().set_locator(self._tbl_root_body, self._name)

    def check_all(self):
        self._grid_table_head().check_all_rows()
        return self

    def check_record(self, index: int = 1):
        # Row 2 is the first Row Visible: index+1
        # Checkbox on this page is located on column 2
        self._grid_table_body().check_rows(index=(index+1), column=2)
        return self

    def check_multiple_records(self, multiple_list: list):
        if not multiple_list:
            logger.error(f"Multiple List Empty")
            raise ValueError("The list of criteria is empty.")

        for criteria in multiple_list:
            logger.info(f"Check Used Criteria: {criteria}")
            self.check_record(criteria)
        return self

    def click_edit_icon(self, index: int = 1):
        # Row 2 is the first Row Visible: index+1
        # Edit Icon on this page is located on column 4
        self._grid_table_body().click_edit_icon(index=(index+1))
        return self

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table_head().get_table_headers(old_table=True)
        return self._tbl_headers

    def get_cell_tariff_type(self, row):
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Type",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_no_of_matching_criteria(self, row):
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="No. of Matching Criteria",
            headers=self.get_table_headers(),
            old_table=True
        )

    def click_previous(self):
        self._grid_table_body().click_previous()
        return self

    def click_next(self):
        self._grid_table_body().click_next()
        return self

    def select_pagination(self, number: int):
        self._grid_table_body().select_pagination(number)
        return self

    def table_footer(self):
        return self._grid_table_body().table_footer()

    def print_row(self, row):
        """
        Print a table data in the console.
        """
        # Extract Keys From Headers Dict
        # We need to process the Table Header to Get the Columns name and extract
        # all the 'keys' names and convert in to array
        # First Row is Hidden : Plus 1 into Index Rows on Table
        row = row + 1
        headers = list(self.get_table_headers().keys())
        data = []

        tariff_type = self.get_cell_tariff_type(row) or "-"
        no_of_matching_criteria = self.get_cell_no_of_matching_criteria(row) or "-"

        data.append([tariff_type, no_of_matching_criteria])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return self

    def verify_search_results(self, row, tariff_type, matching_criteria):
        # First Row is Hidden : Plus 1 into Index Rows on Table
        row = row+1
        cell_tariff_type = self.get_cell_tariff_type(row)
        cell_matching_criteria = self.get_cell_no_of_matching_criteria(row)

        assert cell_tariff_type == tariff_type, f"[Error] Search Results Tariff Type: Expected text '{tariff_type}' but found '{cell_tariff_type}'"
        assert cell_matching_criteria == matching_criteria, f"[Error] Search Results Marching Criteria: Expected text '{matching_criteria}' but found '{cell_matching_criteria}'"
        return self

    @allure.step("Verify Data Deleted")
    def verify_data_deleted(self):
        toast_actual = self.alert.get_toast_detail()
        toast_expected = "Selected records were deleted successfully."
        self.screenshot().attach_to_allure("Verify Tariff Type Deleted", self._name)
        # Assert with a custom error message
        assert toast_actual == toast_expected, f"[Error] Delete Purchase Tariff Deleted: Expected text '{toast_expected}' but found '{toast_actual}'"
        return self

    def verify_table_footer(self, message):
        expected = message
        actual = self.table_footer()
        # Assert with a custom error message
        assert actual == expected, f"[Error] Verify Table Footer Message: Expected text '{expected}' but found '{actual}'"
        return self


