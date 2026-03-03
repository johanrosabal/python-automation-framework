import allure

from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.common.SoftshipPage import SoftshipPage
from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('BookingQueryPage')


class BookingQueryPage(SoftshipPage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/Query/Index/BookingAdvanced"
        self._module_url = None
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root = (By.XPATH, "//table[contains(@id,'table')]", "Bookings Table")
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

    def get_cell_booking_number(self, row):
        return self._grid_table().get_row_data_by_header(
            row_index=row,
            header_name="Booking No.",
            headers=self.get_table_headers(),
            old_table=False
        )

    def get_cell_booking_ref(self, row):
        return self._grid_table().get_row_data_by_header(row, "Booking Ref.", self.get_table_headers(), True)

    def get_cell_agency(self, row):
        return self._grid_table().get_row_data_by_header(row, "Agency", self.get_table_headers(), True)

    def get_cell_customer_id(self, row):
        return self._grid_table().get_row_data_by_header(row, "Customer ID", self.get_table_headers(), True)

    def get_cell_customer_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "Customer Name", self.get_table_headers(), True)

    def get_cell_create_date(self, row):
        return self._grid_table().get_row_data_by_header(row, "Create Date", self.get_table_headers(), True)

    def get_cell_change_date(self, row):
        return self._grid_table().get_row_data_by_header(row, "Change Date", self.get_table_headers(), True)

    def get_cell_ready_date(self, row):
        return self._grid_table().get_row_data_by_header(row, "Ready Date", self.get_table_headers(), True)

    def get_cell_receipt_term(self, row):
        return self._grid_table().get_row_data_by_header(row, "Receipt Term", self.get_table_headers(), True)

    def get_cell_delivery_term(self, row):
        return self._grid_table().get_row_data_by_header(row, "Delivery Term", self.get_table_headers(), True)

    def get_cell_booking_status(self, row):
        return self._grid_table().get_row_data_by_header(row, "Booking Status", self.get_table_headers(), True)

    def get_cell_operational_status(self, row):
        return self._grid_table().get_row_data_by_header(row, "Operational Status", self.get_table_headers(), True)

    def get_cell_from(self, row):
        return self._grid_table().get_row_data_by_header(row, "From", self.get_table_headers(), True)

    def get_cell_from_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "From Name", self.get_table_headers(), True)

    def get_cell_from_sublocation(self, row):
        return self._grid_table().get_row_data_by_header(row, "From Sublocation", self.get_table_headers(), True)

    def get_cell_from_sublocation_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "From Sublocation Name", self.get_table_headers(), True)

    def get_cell_to(self, row):
        return self._grid_table().get_row_data_by_header(row, "To", self.get_table_headers(), True)

    def get_cell_to_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "To Name", self.get_table_headers(), True)

    def get_cell_to_sublocation_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "To Sublocation Name", self.get_table_headers(), True)

    def get_cell_eta_pod(self, row):
        return self._grid_table().get_row_data_by_header(row, "ETA POD", self.get_table_headers(), True)

    def get_cell_pod_sublocation(self, row):
        return self._grid_table().get_row_data_by_header(row, "POD Sublocation", self.get_table_headers(), True)

    def get_cell_vessel(self, row):
        return self._grid_table().get_row_data_by_header(row, "Vessel", self.get_table_headers(), True)

    def get_cell_voyage(self, row):
        return self._grid_table().get_row_data_by_header(row, "Voyage", self.get_table_headers(), True)

    def get_cell_booking_type(self, row):
        return self._grid_table().get_row_data_by_header(row, "Booking Type", self.get_table_headers(), True)

    def get_cell_created_by(self, row):
        return self._grid_table().get_row_data_by_header(row, "Created By", self.get_table_headers(), True)

    def get_cell_changed_by(self, row):
        return self._grid_table().get_row_data_by_header(row, "Changed By", self.get_table_headers(), True)

    def get_cell_documentation_status(self, row):
        return self._grid_table().get_row_data_by_header(row, "Documentation Status", self.get_table_headers(), True)

    def get_cell_assignment_status(self, row):
        return self._grid_table().get_row_data_by_header(row, "Assignment Status", self.get_table_headers(), True)

    def get_cell_contract_no(self, row):
        return self._grid_table().get_row_data_by_header(row, "Contract No.", self.get_table_headers(), True)

    def click_previous(self):
        self._grid_table().click_previous()

    def click_next(self):
        self._grid_table().click_next()

    def select_pagination(self, number: int):
        self._grid_table().select_pagination(number)

    def print_row(self, row):

        headers = list(self.get_table_headers().keys())
        data = []

        booking_number = self.get_cell_booking_number(row) or "-"
        booking_ref = self.get_cell_booking_ref(row) or "-"
        agency = self.get_cell_agency(row) or "-"
        customer_id = self.get_cell_customer_id(row) or "-"
        customer_name = self.get_cell_customer_name(row) or "-"
        create_date = self.get_cell_create_date(row) or "-"
        change_date = self.get_cell_change_date(row) or "-"
        ready_date = self.get_cell_ready_date(row) or "-"
        receipt_term = self.get_cell_receipt_term(row) or "-"
        delivery_term = self.get_cell_delivery_term(row) or "-"
        booking_status = self.get_cell_booking_status(row) or "-"
        operational_status = self.get_cell_operational_status(row) or "-"
        from_location = self.get_cell_from(row) or "-"
        from_name = self.get_cell_from_name(row) or "-"
        from_sublocation = self.get_cell_from_sublocation(row) or "-"
        from_sublocation_name = self.get_cell_from_sublocation_name(row) or "-"
        to = self.get_cell_to(row) or "-"
        to_name = self.get_cell_to_name(row) or "-"
        to_sublocation_name = self.get_cell_to_sublocation_name(row) or "-"
        eta_pod = self.get_cell_eta_pod(row) or "-"
        pod_sublocation = self.get_cell_pod_sublocation(row) or "-"
        vessel = self.get_cell_vessel(row) or "-"
        voyage = self.get_cell_voyage(row) or "-"
        booking_type = self.get_cell_booking_type(row) or "-"
        created_by = self.get_cell_created_by(row) or "-"
        changed_by = self.get_cell_changed_by(row) or "-"
        documentation_status = self.get_cell_documentation_status(row) or "-"
        assignment_status = self.get_cell_assignment_status(row) or "-"
        contract_no = self.get_cell_contract_no(row) or "-"

        data.append([booking_number, booking_ref, agency, customer_id, customer_name, create_date,
                     change_date, ready_date, receipt_term, delivery_term, booking_status, operational_status,
                     from_location, from_name, from_sublocation, from_sublocation_name, to, to_name,
                     to_sublocation_name, eta_pod, pod_sublocation, vessel, voyage, booking_type, created_by,
                     changed_by, documentation_status, assignment_status, contract_no])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
