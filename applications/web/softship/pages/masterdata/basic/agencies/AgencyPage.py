import allure
from selenium.webdriver.common.by import By
from applications.web.softship.common.SoftshipPage import SoftshipPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.softship.components.buttons.Buttons import Buttons
from core.utils.table_formatter import TableFormatter

logger = setup_logger('AgencyPage')


class AgencyPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the AgencyPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/Query/Index/Agency"
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._tbl_root = (By.XPATH, "//table[contains(@id,'table')]", "Agency Table")
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

    def click_select(self, pause: int = 3):
        self._buttons.click_select(pause)
        return self

    def click_select_toggle(self, pause: int = 1):
        self._buttons.click_select_toggle(pause)
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

    def click_export_excel(self, pause: int = 1):
        self._buttons.click_excel_export(pause)
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

    def get_cell_company(self, row):
        return self._grid_table().get_row_data_by_header(row, "Company", self.get_table_headers())

    def get_cell_agency(self, row):
        return self._grid_table().get_row_data_by_header(row, "Agency\n1", self.get_table_headers())

    def get_cell_agency_name(self, row):
        return self._grid_table().get_row_data_by_header(row, "Agency Name", self.get_table_headers())

    def get_cell_place(self, row):
        return self._grid_table().get_row_data_by_header(row, "Place", self.get_table_headers())

    def get_cell_cust_supp_no(self, row):
        return self._grid_table().get_row_data_by_header(row, "Cust./Supp. No.", self.get_table_headers())

    def get_cell_cust_supp_match_code(self, row):
        return self._grid_table().get_row_data_by_header(row, "Cust./Supp. Matchcode", self.get_table_headers())

    def get_cell_additional_email(self, row):
        return self._grid_table().get_row_data_by_header(row, "Additional Email", self.get_table_headers())

    def get_cell_control_office(self, row):
        return self._grid_table().get_row_data_by_header(row, "Control Office", self.get_table_headers())

    def get_cell_cost_centre(self, row):
        return self._grid_table().get_row_data_by_header(row, "Costcentre", self.get_table_headers())

    def get_cell_country(self, row):
        return self._grid_table().get_row_data_by_header(row, "Country", self.get_table_headers())

    def get_cell_customs_code(self, row):
        return self._grid_table().get_row_data_by_header(row, "Customs Code", self.get_table_headers())

    def get_cell_department(self, row):
        return self._grid_table().get_row_data_by_header(row, "Department", self.get_table_headers())

    def get_cell_email(self, row):
        return self._grid_table().get_row_data_by_header(row, "Email", self.get_table_headers())

    def get_cell_fax(self, row):
        return self._grid_table().get_row_data_by_header(row, "Fax", self.get_table_headers())

    def get_cell_group(self, row):
        return self._grid_table().get_row_data_by_header(row, "Group", self.get_table_headers())

    def get_cell_hide(self, row):
        return self._grid_table().get_row_data_by_header(row, "Hide", self.get_table_headers())

    def get_cell_place_of_booking(self, row):
        return self._grid_table().get_row_data_by_header(row, "Place of Booking", self.get_table_headers())

    def get_cell_principal(self, row):
        return self._grid_table().get_row_data_by_header(row, "Principal", self.get_table_headers())

    def get_cell_related_to_agency(self, row):
        return self._grid_table().get_row_data_by_header(row, "Related to Agency", self.get_table_headers())

    def get_cell_show_in_internet(self, row):
        return self._grid_table().get_row_data_by_header(row, "Show in Internet", self.get_table_headers())

    def get_cell_street(self, row):
        return self._grid_table().get_row_data_by_header(row, "Street", self.get_table_headers())

    def get_cell_sync_office(self, row):
        return self._grid_table().get_row_data_by_header(row, "Sync. Office", self.get_table_headers())

    def get_cell_telephone(self, row):
        return self._grid_table().get_row_data_by_header(row, "Telephone", self.get_table_headers())

    def get_cell_vat_id(self, row):
        return self._grid_table().get_row_data_by_header(row, "VAT ID", self.get_table_headers())

    def get_cell_website(self, row):
        return self._grid_table().get_row_data_by_header(row, "Website", self.get_table_headers())

    def get_cell_zipcode(self, row):
        return self._grid_table().get_row_data_by_header(row, "Zipcode", self.get_table_headers())

    def print_row(self, row):
        """
        Print a table data in the console.
        """
        # Extract Keys From Headers Dict
        # We need to process the Table Header to Get the Columns name and extract
        # all the 'keys' names and convert in to array
        headers = list(self.get_table_headers().keys())
        data = []

        company = self.get_cell_company(row) or "-"
        agency = self.get_cell_agency(row) or "-"
        agency_name = self.get_cell_agency_name(row) or "-"
        place = self.get_cell_place(row) or "-"
        cust_supp_no = self.get_cell_cust_supp_no(row) or "-"
        cust_supp_match_code = self.get_cell_cust_supp_match_code(row) or "-"
        additional_email = self.get_cell_additional_email(row) or "-"
        control_office = self.get_cell_control_office(row) or "-"
        cost_centre = self.get_cell_cost_centre(row) or "-"
        country = self.get_cell_country(row) or "-"
        customs_code = self.get_cell_customs_code(row) or "-"
        department = self.get_cell_department(row) or "-"
        email = self.get_cell_email(row) or "-"
        fax = self.get_cell_fax(row) or "-"
        group = self.get_cell_group(row) or "-"
        hide = self.get_cell_hide(row) or "-"
        place_of_booking = self.get_cell_place_of_booking(row) or "-"
        principal = self.get_cell_principal(row) or "-"
        related_to_agency = self.get_cell_related_to_agency(row) or "-"
        show_in_internet = self.get_cell_show_in_internet(row) or "-"
        street = self.get_cell_street(row) or "-"
        sync_office = self.get_cell_sync_office(row) or "-"
        telephone = self.get_cell_telephone(row) or "-"
        vat_id = self.get_cell_vat_id(row) or "-"
        website = self.get_cell_website(row) or "-"
        zipcode = self.get_cell_zipcode(row) or "-"

        data.append([company, agency, agency_name, place, cust_supp_no, cust_supp_match_code, additional_email,
                     control_office, cost_centre, country, customs_code, department, email, fax, group, hide,
                     place_of_booking, principal, related_to_agency, show_in_internet, street, sync_office,
                     telephone, vat_id, website, zipcode])

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
