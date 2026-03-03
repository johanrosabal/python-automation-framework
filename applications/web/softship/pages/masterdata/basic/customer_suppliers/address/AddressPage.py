import allure

from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('AddressPage')


class AddressPage(SoftshipPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Relative URL
        self.relative = "/Query/Index/AddressNew"
        self._module_url = None
        # Name
        self._name = self.__class__.__name__
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

    def click_select(self, pause: int = 1):
        self._buttons.click_select(pause)
        return self

    def click_select_toggle(self, show=True, pause: int = 1):
        self._buttons.click_select_toggle(show=show, pause=pause)
        return self

    def click_delete(self, pause: int = 1):
        self._buttons.click_delete(pause)
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

    def click_new(self, pause: int = 1):
        self._buttons.click_new(pause)
        return self

    def click_copy(self, pause: int = 1):
        self._buttons.click_copy(pause)
        return self

    @allure.step("Query Search : field {field_name}, operator {field_operator}, value {field_value}")
    def query_search(self, field_name="", field_operator="", field_value=""):
        QuerySearchComponent(self._driver).execute_query(
            field_name=field_name,
            field_operator=field_operator,
            field_value=field_value,
            press_enter=True
        )

    def _grid_table_head(self):
        return self.table_with_controls().set_locator(self._tbl_root_head, self._name)

    def _grid_table_body(self):
        return self.table_with_controls().set_locator(self._tbl_root_body, self._name)

    def check_all(self):
        self._grid_table_head().check_all_rows()
        return self

    def check_record(self, index: int = 2):
        self._grid_table_body().check_rows(index=index, column=2)

    def click_edit_icon(self, index: int = 2):
        self._grid_table_body().click_edit_icon(index)

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table_head().get_table_headers(old_table=True)
        return self._tbl_headers

    def get_cell_address_code(self, row):
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Address Code",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_customer_address_type(self, row):
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Customer Address Type",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_customer_id(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Customer ID", self.get_table_headers(), True)

    def get_cell_customer_match_code(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Customer Match Code", self.get_table_headers(), True)

    def get_cell_customer_name(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Customer Name", self.get_table_headers(), True)

    def get_cell_address_line_1(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 1", self.get_table_headers(), True)

    def get_cell_address_line_2(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 2", self.get_table_headers(), True)

    def get_cell_address_line_3(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 3", self.get_table_headers(), True)

    def get_cell_address_line_4(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 4", self.get_table_headers(), True)

    def get_cell_address_line_5(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 5", self.get_table_headers(), True)

    def get_cell_address_line_6(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 6", self.get_table_headers(), True)

    def get_cell_address_line_7(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Address Line 7", self.get_table_headers(), True)

    def get_cell_secondary_language_1(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 1", self.get_table_headers(), True)

    def get_cell_secondary_language_2(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 2", self.get_table_headers(), True)

    def get_cell_secondary_language_3(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 3", self.get_table_headers(), True)

    def get_cell_secondary_language_4(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 4", self.get_table_headers(), True)

    def get_cell_secondary_language_5(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 5", self.get_table_headers(), True)

    def get_cell_secondary_language_6(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 6", self.get_table_headers(), True)

    def get_cell_secondary_language_7(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Secondary Language 7", self.get_table_headers(), True)

    def get_cell_hide(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Hide", self.get_table_headers(), True)

    def get_cell_web_booking(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Webbooking", self.get_table_headers(), True)

    def get_cell_business_account_no(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Business Account No.", self.get_table_headers(), True)

    def get_cell_city_name(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "City Name", self.get_table_headers(), True)

    def get_cell_contact_1(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Contact 1", self.get_table_headers(), True)

    def get_cell_contact_2(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Contact 2", self.get_table_headers(), True)

    def get_cell_contact_type(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Contact Type", self.get_table_headers(), True)

    def get_cell_country(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Country", self.get_table_headers(), True)

    def get_cell_location(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Location", self.get_table_headers(), True)

    def get_cell_postal_code(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Postal Code", self.get_table_headers(), True)

    def get_cell_province(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Province", self.get_table_headers(), True)

    def get_cell_street_1(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Street 1", self.get_table_headers(), True)

    def get_cell_street_2(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Street 2", self.get_table_headers(), True)

    def get_cell_street_3(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Street 3", self.get_table_headers(), True)

    def get_cell_state(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "State", self.get_table_headers(), True)

    def get_cell_latitude(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Latitude", self.get_table_headers(), True)

    def get_cell_longitude(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Longitude", self.get_table_headers(), True)

    def get_cell_create_date_utc(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Create Date UTC", self.get_table_headers(), True)

    def get_cell_change_date_utc(self, row):
        return self._grid_table_body().get_row_data_by_header(row, "Change Date UTC", self.get_table_headers(), True)

    def click_previous(self):
        self._grid_table_body().click_previous()

    def click_next(self):
        self._grid_table_body().click_next()

    def select_pagination(self, number: int):
        self._grid_table_body().select_pagination(number)

    def print_row(self, row):
        """
        Print a table data in the console.
        """
        # Extract Keys From Headers Dict
        # We need to process the Table Header to Get the Columns name and extract
        # all the 'keys' names and convert in to array
        headers = list(self.get_table_headers().keys())
        data = []

        address_code = self.get_cell_address_code(row) or "-"
        customer_address_type = self.get_cell_customer_address_type(row) or "-"
        customer_id = self.get_cell_customer_id(row) or "-"
        customer_match_code = self.get_cell_customer_match_code(row) or "-"
        customer_name = self.get_cell_customer_name(row) or "-"
        address_line_1 = self.get_cell_address_line_1(row) or "-"
        address_line_2 = self.get_cell_address_line_2(row) or "-"
        address_line_3 = self.get_cell_address_line_3(row) or "-"
        address_line_4 = self.get_cell_address_line_4(row) or "-"
        address_line_5 = self.get_cell_address_line_5(row) or "-"
        address_line_6 = self.get_cell_address_line_6(row) or "-"
        address_line_7 = self.get_cell_address_line_7(row) or "-"
        secondary_language_1 = self.get_cell_secondary_language_1(row) or "-"
        secondary_language_2 = self.get_cell_secondary_language_2(row) or "-"
        secondary_language_3 = self.get_cell_secondary_language_3(row) or "-"
        secondary_language_4 = self.get_cell_secondary_language_4(row) or "-"
        secondary_language_5 = self.get_cell_secondary_language_5(row) or "-"
        secondary_language_6 = self.get_cell_secondary_language_6(row) or "-"
        secondary_language_7 = self.get_cell_secondary_language_7(row) or "-"
        hide = self.get_cell_hide(row) or "-"
        webbooking = self.get_cell_web_booking(row) or "-"
        business_account_no = self.get_cell_business_account_no(row) or "-"
        city_name = self.get_cell_city_name(row) or "-"
        contact_1 = self.get_cell_contact_1(row) or "-"
        contact_2 = self.get_cell_contact_2(row) or "-"
        contact_type = self.get_cell_contact_type(row) or "-"
        country = self.get_cell_country(row) or "-"
        location = self.get_cell_location(row) or "-"
        postal_code = self.get_cell_postal_code(row) or "-"
        province = self.get_cell_province(row) or "-"
        street_1 = self.get_cell_street_1(row) or "-"
        street_2 = self.get_cell_street_2(row) or "-"
        street_3 = self.get_cell_street_3(row) or "-"
        state = self.get_cell_state(row) or "-"
        latitude = self.get_cell_latitude(row) or "-"
        longitude = self.get_cell_longitude(row) or "-"
        create_date_utc = self.get_cell_create_date_utc(row) or "-"
        change_date_utc = self.get_cell_change_date_utc(row) or "-"

        data.append([address_code, customer_address_type, customer_id, customer_match_code, customer_name,
                     address_line_1, address_line_2, address_line_3, address_line_4, address_line_5, address_line_6,
                     address_line_7,
                     secondary_language_1, secondary_language_2, secondary_language_3, secondary_language_4,
                     secondary_language_5, secondary_language_6, secondary_language_7,
                     hide, webbooking, business_account_no, city_name, contact_1, contact_2, contact_type, country,
                     location,
                     postal_code, province, street_1, street_2, street_3, state, latitude, longitude, create_date_utc,
                     change_date_utc
                     ])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
