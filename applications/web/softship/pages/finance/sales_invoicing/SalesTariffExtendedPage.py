import allure
from selenium.webdriver.common.by import By

from applications.web.softship.components.alert.AlertDialogBox import AlertDialogBox
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from core.ui.common.BaseApp import BaseApp
from applications.web.softship.common.SoftshipPage import SoftshipPage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('SalesTariff_ExtendedPage')


class SalesTariff_ExtendedPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the sales_tariff_extended instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Query/Index/SalesTariffBasic"
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

    def click_select(self, pause: int = 3):
        self._buttons.click_select(pause)
        return self

    def click_select_toggle(self, show=True, pause: int = 1):
        self._buttons.click_select_toggle(show=show, pause=pause)
        return self

    def click_edit(self, pause: int = 1):
        self._buttons.click_edit(pause)
        return self

    def click_new(self, pause: int = 2):
        self._buttons.click_new(pause)
        return self

    def click_copy(self, pause: int = 1):
        self._buttons.click_copy(pause)
        return self

    def click_multi_update(self, pause: int = 1):
        self._buttons.click_multi_update(pause)
        return self

    def click_multi_update_details(self, pause: int = 1):
        self._buttons.click_multi_update_details(pause)
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

    def click_save(self, pause: int = 2):
        self._buttons.click_save(pause)
        return self

    def click_cancel(self, pause: int = 1):
        self._buttons.click_cancel(pause)
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

    def click_expire_and_copy(self, pause: int = 1):
        self._buttons.click_expire_and_copy(pause)
        return self

    def click_export_changes(self, pause: int = 1):
        self._buttons.click_export_changes(pause)
        return self

    def click_tariff_export(self, pause: int = 1):
        self._buttons.click_tariff_export(pause)
        return self

    def click_change_history(self, pause: int = 1):
        self._buttons.click_change_history(pause)
        return self

    @allure.step("Query Search : field {field_name}, operator {field_operator}, value {field_value}")
    def query_search(self, field_name="", field_operator="", field_value=""):
        QuerySearchComponent(self._driver).execute_query(
            field_name=field_name,
            field_operator=field_operator,
            field_value=field_value,
            press_enter=True
        )
        # self.pause(3)
        return self

    def queries_search(self, queries):
        QuerySearchComponent(self._driver).execute_queries(queries)
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
        self._grid_table_body().check_rows(index=(index + 1), column=2)
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
        # CheckBox on this page is located on column 5
        self._grid_table_body().click_edit_icon(index=(index+1), column=5)
        return self

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

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table_head().get_table_headers(old_table=True)
        return self._tbl_headers

    def _return_index(self, column_name: str):
        header_map = self.get_table_headers()
        column_index = header_map[column_name] + 2
        logger.info(f"_return_index:[{column_name}][{column_index}]")
        return [column_index, column_name]

    def click_table_header_package(self):
        self._grid_table_head().click_table_header_by_text(header_text="Package", old_table=True)
        return self

    def get_cell_tariff_id(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Id",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_original_sales_tariff_id(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Original Sales Tariff Id",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_tariff_name(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Name",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_level(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Level",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_position_amount(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Position Amount",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_tariff_level_code(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Level Code",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_tariff_level_name(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Level Name",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_from_pol(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="From/Pol",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_from_sublocation_pol_berth(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="From Sublocation/Pol Berth",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_to_pod(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="To/Pod",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_agency(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Agency",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_package(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Package",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_valid_from(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Valid From",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_valid_to(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Valid To",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_change_frequency(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Change Frequency",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_sales_tariff_remark(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Sales Tariff Remark",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_cargo(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Cargo",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_short_from(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Short From",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_devanning(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Devanning",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_crossdocking(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Crossdocking",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_transport_mode(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Transport Mode",
            headers=self.get_table_headers(),
            old_table=True
        )

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

        tarrif_id = self.get_cell_tariff_id(row) or "-"
        original_sales_tariff_id = self.get_cell_original_sales_tariff_id(row) or "-"
        tariff_name = self.get_cell_tariff_name(row) or "-"
        level = self.get_cell_level(row) or "-"
        position_amount = self.get_cell_position_amount(row) or "-"
        tariff_level_code = self.get_cell_tariff_level_code(row) or "-"
        tariff_level_name = self.get_cell_tariff_level_name(row) or "-"
        from_pol = self.get_cell_from_pol(row) or "-"
        from_sublocation_pol_berth = self.get_cell_from_sublocation_pol_berth(row) or "-"
        to_pod = self.get_cell_to_pod(row) or "-"
        package = self.get_cell_package(row) or "-"
        valid_from = self.get_cell_valid_from(row) or "-"
        valid_to = self.get_cell_valid_to(row) or "-"
        sales_tariff_remark = self.get_cell_sales_tariff_remark(row) or "-"
        transport_mode = self.get_cell_transport_mode(row) or "-"

        data.append([tarrif_id, original_sales_tariff_id, tariff_name, level, position_amount, tariff_level_code,
                     tariff_level_name, from_pol, from_sublocation_pol_berth, to_pod, package, valid_from, valid_to,
                     sales_tariff_remark, transport_mode
                     ])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return self

    # Table Editable Fields --------------------------------------------------------------------------------------------
    @allure.step("Enter Tariff Name: {text}")
    def set_cell_enter_tariff_name(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.send_keys() \
            .set_locator_by_table(table_xpath=self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Tariff Name"))
        return self

    @allure.step("Enter Level: {text}")
    def set_cell_enter_level(self, row: int, text: str):
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Level"), column_list_match=1)
        return self

    @allure.step("Enter From/Pol: {text}")
    def set_cell_enter_from_pol(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("From/Pol"), column_list_match=1)
        return self

    @allure.step("Enter To/Pod: {text}")
    def set_cell_enter_to_pod(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("To/Pod"), column_list_match=1)
        return self

    @allure.step("Enter To To Sublocation/Pod Berth: {text}")
    def set_cell_enter_to_sublocation_pod_beth(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("To Sublocation/Pod Berth"), column_list_match=1)
        return self

    @allure.step("Enter Agency: {text}")
    def set_cell_enter_agency(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Agency"), column_list_match=1)
        return self

    @allure.step("Enter Package: {text}")
    def set_cell_enter_package(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Package"), column_list_match=1)
        return self

    @allure.step("Enter Valid From: {text}")
    def set_cell_enter_valid_from(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.send_keys() \
            .set_locator_by_table(table_xpath=self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Valid From"))
        return self

    @allure.step("Enter Change Frequency: {text}")
    def set_cell_enter_change_frequency(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Change Frequency"), column_list_match=1)
        return self

    @allure.step("Enter Shipper's Own: {text}")
    def set_cell_enter_shippers_own(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Shipper's Own"), column_list_match=1)
        return self

    @allure.step("Enter Sales Tariff Remark: {text}")
    def set_cell_enter_sales_tariff_remark(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.send_keys() \
            .set_locator_by_table(table_xpath=self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Sales Tariff Remark"))
        return self

    @allure.step("Enter Cargo: {text}")
    def set_cell_enter_cargo(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Cargo"), column_list_match=2)
        return self

    @allure.step("Enter Short : {text}")
    def set_cell_enter_short_from(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Short Form"), column_list_match=1)
        return self

    @allure.step("Enter Transport Mode : {text}")
    def set_cell_enter_transport_mode(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Transport Mode"), column_list_match=1)
        return self

    @allure.step("Enter Devanning: {text}")
    def set_cell_enter_devanning(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Devanning"), column_list_match=1)
        return self

    @allure.step("Enter Crossdocking: {text}")
    def set_cell_enter_crossdocking(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row + 1), text=text, column_index=self._return_index("Crossdocking"), column_list_match=1)
        return self

    def fill_out_sales_tariff_form(self, row, tariff_name, level, from_pol, to_pod, to_sublocation_pod_berth, agency, package, valid_from, shippers_own,
                                   change_frequency, sales_tariff_remark, cargo, short_from, transport_mode, devanning, crossdocking):

        self.set_cell_enter_tariff_name(row, tariff_name)
        self.set_cell_enter_level(row, level)
        self.set_cell_enter_from_pol(row, from_pol)
        self.set_cell_enter_to_pod(row, to_pod)

        if to_sublocation_pod_berth != "":
            self.set_cell_enter_to_sublocation_pod_beth(row, to_sublocation_pod_berth)

        self.set_cell_enter_agency(row, agency)
        self.set_cell_enter_package(row, package)
        self.set_cell_enter_valid_from(row, valid_from)  # Ask about Date Rule

        if shippers_own != "":
            self.set_cell_enter_shippers_own(row, shippers_own)

        self.set_cell_enter_change_frequency(row, change_frequency)
        self.set_cell_enter_sales_tariff_remark(row, sales_tariff_remark)
        self.set_cell_enter_cargo(row, cargo)
        self.set_cell_enter_short_from(row, short_from)
        self.set_cell_enter_transport_mode(row, transport_mode)
        self.set_cell_enter_devanning(row, devanning)
        self.set_cell_enter_crossdocking(row, crossdocking)

        return self

    # Edit Fields --------------------------------------------------------------------------------------------
    @allure.step(
        "Edit Internal Calculation Rule: Row: {row}, Charge: {charge}, Plus or Minus: {plus_minus}, Currency: {currency}, Rate: {rate}, Per: {per}, Var: {var_code}, Invoice: {invoice_currency}")
    def internal_calculation_rule(self, row, charge, plus_minus, currency, rate, per, var_code, invoice_currency):

        row = row - 1
        xpath_section_container = "//div[@class='details-view-content-container tabable']"
        section_container = (By.XPATH, xpath_section_container, "[Internal Calculation Rule ID] Section")
        container = self.element().wait(section_container).is_displayed()

        if container:
            # XPaths Fields
            xpath_charge = (By.XPATH, f"//input[@id='charge{row}']", " Charge Field ")
            xpath_plus_minus = (By.XPATH, f"//input[@id='plusOrMinus{row}']", "Plus or Minus Field")
            xpath_currency = (By.XPATH, f"//input[@id='currency{row}']", "Currency Field")
            xpath_rate = (By.XPATH, f"//input[@id='rate{row}']", "Rate Field")
            xpath_per = (By.XPATH, f"//input[@id='per{row}']", "Per Field")
            xpath_vat_code = (By.XPATH, f"//input[@id='vatCode{row}']", "Vat Field")
            xpath_invoice_currency = (By.XPATH, f"//input[@id='invoiceCurrency{row}']", "Invoice Currency Field")

            self.send_keys().set_locator(xpath_charge, self._name).clear().set_text(charge).highlight()
            self.send_keys().set_locator(xpath_plus_minus, self._name).clear().set_text(plus_minus).highlight()
            self.send_keys().set_locator(xpath_currency, self._name).clear().set_text(currency).highlight()
            self.send_keys().set_locator(xpath_rate, self._name).clear().set_text(rate).highlight()
            self.send_keys().set_locator(xpath_per, self._name).clear().set_text(per).highlight()
            self.send_keys().set_locator(xpath_vat_code, self._name).clear().set_text(var_code).highlight()
            self.send_keys().set_locator(xpath_invoice_currency, self._name).clear().set_text(invoice_currency).highlight()

        return self

    def verify_row_data(self, row, tariff_name, level, from_pol, to_pod, agency, package, valid_from, change_frequency,
                        sales_tariff_remark, cargo, short_from, devanning, crossdocking):

        row = row + 1
        cell_tariff_name = self.get_cell_tariff_name(row)
        cell_level = self.get_cell_level(row)
        cell_from_pol = self.get_cell_from_pol(row)
        cell_to_pod = self.get_cell_to_pod(row)
        cell_agency = self.get_cell_agency(row)
        cell_package = self.get_cell_package(row)
        cell_valid_from = self.get_cell_valid_from(row)
        cell_valid_change_frequency = self.get_cell_change_frequency(row)
        cell_valid_sales_tariff_remark = self.get_cell_sales_tariff_remark(row)
        cell_valid_cargo = self.get_cell_cargo(row)
        cell_valid_short_from = self.get_cell_short_from(row)
        cell_valid_devanning = self.get_cell_devanning(row)
        cell_valid_crossdocking = self.get_cell_crossdocking(row)

        assert cell_tariff_name == tariff_name, f"Error:[tariff_type] Expected text '{tariff_name}' but found '{cell_tariff_name}'"
        assert cell_level == level, f"Error:[level] Expected text '{level}' but found '{cell_level}'"
        assert cell_from_pol == level, f"Error:[from_pol] Expected text '{from_pol}' but found '{cell_from_pol}'"
        assert cell_to_pod == to_pod, f"Error:[to_pod] Expected text '{to_pod}' but found '{cell_to_pod}'"
        assert cell_agency == agency, f"Error:[agency] Expected text '{agency}' but found '{cell_agency}'"
        assert cell_package == package, f"Error:[package] Expected text '{package}' but found '{cell_package}'"
        assert cell_valid_from == valid_from, f"Error:[valid_from] Expected text '{valid_from}' but found '{cell_valid_from}'"
        assert cell_valid_change_frequency == change_frequency, f"Error:[change_frequency] Expected text '{change_frequency}' but found '{cell_valid_change_frequency}'"
        assert cell_valid_sales_tariff_remark == sales_tariff_remark, f"Error:[sales_tariff_remark] Expected text '{sales_tariff_remark}' but found '{cell_valid_sales_tariff_remark}'"
        assert cell_valid_cargo == cargo, f"Error:[cargo] Expected text '{cargo}' but found '{cell_valid_cargo}'"
        assert cell_valid_short_from == short_from, f"Error:[short_from] Expected text '{short_from}' but found '{cell_valid_short_from}'"
        assert cell_valid_devanning == devanning, f"Error:[devanning] Expected text '{devanning}' but found '{cell_valid_devanning}'"
        assert cell_valid_crossdocking == crossdocking, f"Error:[crossdocking] Expected text '{crossdocking}' but found '{cell_valid_crossdocking}'"

        return self

    @allure.step("Verify Data Saved")
    def verify_saved_data(self):
        toast_actual = self.alert.get_toast_detail()
        toast_expected = "Data has been saved."
        self.screenshot().attach_to_allure("Verify Tariff Type", self._name)
        # Assert with a custom error message
        assert toast_actual == toast_expected, f"Error: Expected text '{toast_expected}' but found '{toast_actual}'"
        self.pause(3)
        return self

    @allure.step("Saved Internal Calculation Rule")
    def verify_saved_internal_calculation(self):
        toast_actual = self.alert.get_toast_detail()
        toast_expected = "Operation completed successfully."
        self.screenshot().attach_to_allure("Saved Internal Calculation Rule", self._name)
        # Assert with a custom error message
        assert toast_actual == toast_expected, f"[Error][verify_saved_internal_calculation]: Expected text '{toast_expected}' but found '{toast_actual}'"
        self.pause(3)
        return self








