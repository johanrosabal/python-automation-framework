import allure
from selenium.webdriver.common.by import By
from applications.web.softship.common.SoftshipPage import SoftshipPage
from applications.web.softship.components.alert.AlertDialogBox import AlertDialogBox
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter

logger = setup_logger('PurchaseTariffPage')


class PurchaseTariffPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the PurchaseTariffPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/Query/Index/PurchaseTariff"
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

    def click_save(self, pause: int = 1):
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
        # CheckBox on this page is located on column 5
        self._grid_table_body().click_edit_icon(index=(index+1), column=5)
        return self

    def click_table_header_id(self):
        self._grid_table_head().click_table_header_by_text(header_text="ID", old_table=True)
        self.pause(1)
        return self

    def get_table_column_id(self):
        rows = self._grid_table_body().get_row_count()
        column = []
        for i in range(1, rows):
            cell = self.get_cell_id(i+1)
            # Working with Numbers Convert String to Int
            column.append(int(cell))
        return column

    def get_table_column_type(self):
        rows = self._grid_table_body().get_row_count()
        column = []
        for i in range(1, rows):
            cell = self.get_cell_type(i+1)
            column.append(cell)
        return column

    def get_table_column_valid_from(self):
        rows = self._grid_table_body().get_row_count()
        column = []
        for i in range(1, rows):
            cell = self.get_cell_valid_from(i+1)
            column.append(cell)
        return column

    def click_table_header_type(self):
        self._grid_table_head().click_table_header_by_text(header_text="Type", old_table=True)
        return self

    def click_table_header_valid_from(self):
        self._grid_table_head().click_table_header_by_text(header_text="Valid From", old_table=True)
        return self

    def get_table_headers(self):
        if self._tbl_headers is None:
            self._tbl_headers = self._grid_table_head().get_table_headers(old_table=True)
        return self._tbl_headers

    def get_cell_id(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="ID",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_type(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Type",
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

    def get_cell_comment(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Comment",
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

    def get_cell_calc(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Calc.",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_business_unit(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="BusinessUnit",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_prio(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Prio.",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_vessel(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Vessel",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_vessel_class(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Vessel Class",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_deadweight(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Deadweight",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_deadweight(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Deadweight",
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

    def get_cell_to_sublocation_pod_berth(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="To Sublocation/Pod Berth",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_book_from(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Book From",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_book_to(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Book To",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_plor_zip_id(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="PLOR Zip ID",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_plor_zip(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="PLOR Zip",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_plod_zip_id(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="PLOD Zip ID",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_plod_zip(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="PLOD Zip",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_commodity(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Commodity",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_tariff_reference_id(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Reference ID",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_tariff_reference(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Tariff Reference",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_supplier(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Supplier",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_supplier_match_code(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Supplier Match Code",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_segment(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Segment",
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

    def get_cell_size_type(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Size/Type",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_cont_grp(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Cont. Grp",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_cont_size(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Cont. Size",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_cont_type(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Cont. Type",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_s_o(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="S/O",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_empty_container(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Empty container",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_non_operative_reefer_nor(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Non-operative reefer (NOR)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_feeder(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Feeder",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_direct(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Direct",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_transship(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Transship",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_weight_in_kg(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Weight (in kg)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_weight_in_kg(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Weight (in kg)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_meas_in_m_3(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Meas (in m³)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_meas_in_m_3(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Meas (in m³)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_revtons(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Revtons",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_revtons(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Revtons",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_length_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Length (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_length_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Length (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_width_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Width (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_width_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Width (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_height_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Height (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_height_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Height (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_cont_over_height_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Cont. Over Height (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_cont_over_height_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Cont. Over Height (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_cont_over_width_left_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Cont. Over Width Left (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_cont_over_width_left_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Cont. Over Width Left (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_cont_over_width_right_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Cont. Over Width Right (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_cont_over_width_right_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Cont. Over Width Right (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_cont_over_length_front_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Cont. Over Length Front (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_cont_over_length_front_in_cm(self, row):
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="max. Cont. Over Length Front (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_cont_over_length_door_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Cont. Over Length Door (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_cont_over_length_door_in_cm(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Cont. Over Length Door (in cm)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_cont_over_weight_in_kg(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Cont. Over Weight (in kg)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_cont_over_weight_in_kg(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Cont. Over Weight (in kg)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_vessel_draft_in_m(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Vessel Draft (in m)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_vessel_draft_in_m(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Vessel Draft (in m)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_vessel_length_in_m(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Vessel Length (in m)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_vessel_length_in_m(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Vessel Length (in m)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_vessel_gross_tons(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Vessel Gross Tons",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_vessel_gross_tons(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Vessel Gross Tons",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_vessel_net_tons(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Vessel Net Tons",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_vessel_net_tons(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Vessel Net Tons",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_vessel_m3(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Vessel m3",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_vessel_m3(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Vessel m3",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_service(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Service",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_route(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Route",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_ship_type(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Ship. Type",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_ship_cond(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Ship. Cond",
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

    def get_cell_dispo_code(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Dispo Code",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_imdg(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. IMDG",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_imdg(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. IMDG",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_imdg_un_no(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="IMDG UN No.",
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

    def get_cell_valid_from_t(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Valid From (T)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_valid_to_t(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Valid To (T)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_valid_days(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Valid Days",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_receipt_term(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Receipt Term",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_delivery_terms_to(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Delivery Terms To",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_car_manufacturer(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Car Manufacturer",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_car_type(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Car Type",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_cargo_t(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Cargo T",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_show_alw(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Show Alw.",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_deleted(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Deleted",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_imdg_in_quotation_booking_bl(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="IMDG in Quotation/Booking/BL?",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_i_o(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="I/O",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_manifest_t(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Manifest T",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_customer(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Customer",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_customer_match_code(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Customer Match Code",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_stat_period(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Stat. Period",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_stat_period(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Stat. Period",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_voyage_from(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Voyage From",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_voyage_to(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Voyage To",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_creation_user(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Creation User",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_creation_date(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Creation Date",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_update_user(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Update User",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_update_date(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Update Date",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_add_costs(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Add. Costs",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_freight_term(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Freight Term",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_out_of_gauge_oog(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Out of gauge (OOG)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_rail_contract(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Rail Contract",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_rail_plan_no(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Rail Plan No",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_country_origin(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Country Origin",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_country_destination(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Country Destination",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_ocean_freight(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Ocean Freights",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_ocean_freight(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Ocean Freights",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_min_vessel_rgt(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Min. Vessel RGT",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_max_vessel_rgt(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Max. Vessel RGT",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_release_location(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Release Location",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_release_sublocation(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Release Sublocation",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_return_location(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Return Location",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_return_sublocation(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Return Sublocation",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_via(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Via",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_via_berth(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Via Berth",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_distance_from_in_km(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Distance From in KM",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_distance_to_in_km(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Distance To in KM",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_distance_from_in_mi(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Distance From in MI",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_distance_to_in_mi(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Distance To in MI",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_slot_operator(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Slot Operator",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_line_service(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Line Service",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_booking_class(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Booking Class",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_customer_rating(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Customer Rating",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_exclude_from_matching(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Exclude From Matching",
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

    def get_cell_change_of_destination(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Change of Destination",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_number_of_extra_stops_inbound(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Number of extra stops Inbound",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_number_of_extra_stops_outbound(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Number of extra stops Outbound",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_receipt_condition(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Receipt Condition",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_delivery_condition(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Delivery Condition",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_from_drayage_option(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="From Drayage Option",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_to_drayage_option(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="To Drayage Option",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_from_max_no_of_stopovers_min(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="From Max No. of Stopovers Min",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_from_max_no_of_stopovers_max(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="From Max No. of Stopovers Max",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_to_max_no_of_stopovers_min(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="To Max No. of Stopovers Min",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_to_max_no_of_stopovers_max(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="To Max No. of Stopovers Max",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_propulsion(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Propulsion",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_handl_ind(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Handl.Ind.",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_optional_services_condition(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Optional Services (Condition)",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_stack_level(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Stack Level",
            headers=self.get_table_headers(),
            old_table=True
        )

    def get_cell_criteria_names(self, row):
        self.get_table_headers()
        return self._grid_table_body().get_row_data_by_header(
            row_index=row,
            header_name="Criteria Names",
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

        id_ = self.get_cell_id(row) or "-"
        type_ = self.get_cell_type(row) or "-"
        position_amount = self.get_cell_position_amount(row) or "-"
        comment = self.get_cell_comment(row) or "-"
        valid_from = self.get_cell_valid_from(row) or "-"
        valid_to = self.get_cell_valid_to(row) or "-"
        calc = self.get_cell_calc(row) or "-"
        business_unit = self.get_cell_business_unit(row) or "-"
        prio = self.get_cell_prio(row) or "-"
        vessel = self.get_cell_vessel(row) or "-"
        vessel_class = self.get_cell_vessel_class(row) or "-"
        min_deadweight = self.get_cell_min_deadweight(row) or "-"
        max_deadweight = self.get_cell_max_deadweight(row) or "-"
        from_pol = self.get_cell_from_pol(row) or "-"
        from_sublocation_pol_berth = self.get_cell_from_sublocation_pol_berth(row) or "-"
        to_pod = self.get_cell_to_pod(row) or "-"
        to_sublocation_pod_berth = self.get_cell_to_sublocation_pod_berth(row) or "-"
        book_from = self.get_cell_book_from(row) or "-"
        book_to = self.get_cell_book_to(row) or "-"
        plor_zip_id = self.get_cell_plor_zip_id(row) or "-"
        plor_zip = self.get_cell_plor_zip(row) or "-"
        plod_zip_id = self.get_cell_plod_zip_id(row) or "-"
        plod_zip = self.get_cell_plod_zip(row) or "-"
        commodity = self.get_cell_commodity(row) or "-"
        tariff_reference_id = self.get_cell_tariff_reference_id(row) or "-"
        tariff_reference = self.get_cell_tariff_reference(row) or "-"
        supplier = self.get_cell_supplier(row) or "-"
        supplier_match_code = self.get_cell_supplier_match_code(row) or "-"
        segment = self.get_cell_segment(row) or "-"
        package = self.get_cell_package(row) or "-"
        size_type = self.get_cell_size_type(row) or "-"
        cont_grp = self.get_cell_cont_grp(row) or "-"
        cont_size = self.get_cell_cont_size(row) or "-"
        cont_type = self.get_cell_cont_type(row) or "-"
        s_o = self.get_cell_s_o(row) or "-"
        empty_container = self.get_cell_empty_container(row) or "-"
        non_operative_reefer_nor = self.get_cell_non_operative_reefer_nor(row) or "-"
        feeder = self.get_cell_feeder(row) or "-"
        direct = self.get_cell_direct(row) or "-"
        transship = self.get_cell_transship(row) or "-"
        min_weight_in_kg = self.get_cell_min_weight_in_kg(row) or "-"
        max_weight_in_kg = self.get_cell_max_weight_in_kg(row) or "-"
        min_meas_in_m_3 = self.get_cell_min_meas_in_m_3(row) or "-"
        max_meas_in_m_3 = self.get_cell_max_meas_in_m_3(row) or "-"
        min_revtons = self.get_cell_min_revtons(row) or "-"
        max_revtons = self.get_cell_max_revtons(row) or "-"
        min_length_in_cm = self.get_cell_min_length_in_cm(row) or "-"
        max_length_in_cm = self.get_cell_max_length_in_cm(row) or "-"
        min_width_in_cm = self.get_cell_min_width_in_cm(row) or "-"
        max_width_in_cm = self.get_cell_max_width_in_cm(row) or "-"
        min_height_in_cm = self.get_cell_min_height_in_cm(row) or "-"
        max_height_in_cm = self.get_cell_max_height_in_cm(row) or "-"
        min_cont_over_height_in_cm = self.get_cell_min_cont_over_height_in_cm(row) or "-"
        max_cont_over_height_in_cm = self.get_cell_max_cont_over_height_in_cm(row) or "-"
        min_cont_over_width_left_in_cm = self.get_cell_min_cont_over_width_left_in_cm(row) or "-"
        max_cont_over_width_left_in_cm = self.get_cell_max_cont_over_width_left_in_cm(row) or "-"
        min_cont_over_width_right_in_cm = self.get_cell_min_cont_over_width_right_in_cm(row) or "-"
        max_cont_over_width_right_in_cm = self.get_cell_max_cont_over_width_right_in_cm(row) or "-"
        min_cont_over_length_front_in_cm = self.get_cell_min_cont_over_length_front_in_cm(row) or "-"
        max_cont_over_length_front_in_cm = self.get_cell_max_cont_over_length_front_in_cm(row) or "-"
        min_cont_over_length_door_in_cm = self.get_cell_min_cont_over_length_door_in_cm(row) or "-"
        max_cont_over_length_door_in_cm = self.get_cell_max_cont_over_length_door_in_cm(row) or "-"
        min_cont_over_weight_in_kg = self.get_cell_min_cont_over_weight_in_kg(row) or "-"
        max_cont_over_weight_in_kg = self.get_cell_max_cont_over_weight_in_kg(row) or "-"
        min_vessel_draft_in_m = self.get_cell_min_vessel_draft_in_m(row) or "-"
        max_vessel_draft_in_m = self.get_cell_max_vessel_draft_in_m(row) or "-"
        min_vessel_length_in_m = self.get_cell_min_vessel_length_in_m(row) or "-"
        max_vessel_length_in_m = self.get_cell_max_vessel_length_in_m(row) or "-"
        min_vessel_gross_tons = self.get_cell_min_vessel_gross_tons(row) or "-"
        max_vessel_gross_tons = self.get_cell_max_vessel_gross_tons(row) or "-"
        min_vessel_net_tons = self.get_cell_min_vessel_net_tons(row) or "-"
        max_vessel_net_tons = self.get_cell_max_vessel_net_tons(row) or "-"
        min_vessel_m3 = self.get_cell_min_vessel_m3(row) or "-"
        max_vessel_m3 = self.get_cell_max_vessel_m3(row) or "-"
        service = self.get_cell_service(row) or "-"
        route = self.get_cell_route(row) or "-"
        ship_type = self.get_cell_ship_type(row) or "-"
        ship_cond = self.get_cell_ship_cond(row) or "-"
        transport_mode = self.get_cell_transport_mode(row) or "-"
        dispo_code = self.get_cell_dispo_code(row) or "-"
        min_imdg = self.get_cell_min_imdg(row) or "-"
        max_imdg = self.get_cell_max_imdg(row) or "-"
        imdg_un_no = self.get_cell_imdg_un_no(row) or "-"
        agency = self.get_cell_agency(row) or "-"
        valid_from_t = self.get_cell_valid_from_t(row) or "-"
        valid_to_t = self.get_cell_valid_to_t(row) or "-"
        valid_days = self.get_cell_valid_days(row) or "-"
        receipt_term = self.get_cell_receipt_term(row) or "-"
        delivery_terms_to = self.get_cell_delivery_terms_to(row) or "-"
        car_manufacturer = self.get_cell_car_manufacturer(row) or "-"
        car_type = self.get_cell_car_type(row) or "-"
        cargo_t = self.get_cell_cargo_t(row) or "-"
        show_alw = self.get_cell_show_alw(row) or "-"
        deleted = self.get_cell_deleted(row) or "-"
        imdg_in_quotation_booking_bl = self.get_cell_imdg_in_quotation_booking_bl(row) or "-"
        i_o = self.get_cell_i_o(row) or "-"
        manifest_t = self.get_cell_manifest_t(row) or "-"
        customer = self.get_cell_customer(row) or "-"
        customer_match_code = self.get_cell_customer_match_code(row) or "-"
        min_stat_period = self.get_cell_min_stat_period(row) or "-"
        max_stat_period = self.get_cell_max_stat_period(row) or "-"
        voyage_from = self.get_cell_voyage_from(row) or "-"
        voyage_to = self.get_cell_voyage_to(row) or "-"
        creation_user = self.get_cell_creation_user(row) or "-"
        creation_date = self.get_cell_creation_date(row) or "-"
        update_user = self.get_cell_update_user(row) or "-"
        update_date = self.get_cell_update_date(row) or "-"
        add_costs = self.get_cell_add_costs(row) or "-"
        freight_term = self.get_cell_freight_term(row) or "-"
        out_of_gauge_oog = self.get_cell_out_of_gauge_oog(row) or "-"
        rail_contract = self.get_cell_rail_contract(row) or "-"
        rail_plan_no = self.get_cell_rail_plan_no(row) or "-"
        country_origin = self.get_cell_country_origin(row) or "-"
        country_destination = self.get_cell_country_destination(row) or "-"
        min_ocean_freight = self.get_cell_min_ocean_freight(row) or "-"
        max_ocean_freight = self.get_cell_max_ocean_freight(row) or "-"
        min_vessel_rgt = self.get_cell_min_vessel_rgt(row) or "-"
        max_vessel_rgt = self.get_cell_max_vessel_rgt(row) or "-"
        release_location = self.get_cell_release_location(row) or "-"
        release_sublocation = self.get_cell_release_sublocation(row) or "-"
        return_location = self.get_cell_return_location(row) or "-"
        return_sublocation = self.get_cell_return_sublocation(row) or "-"
        via = self.get_cell_via(row) or "-"
        via_berth = self.get_cell_via_berth(row) or "-"
        distance_from_in_km = self.get_cell_distance_from_in_km(row) or "-"
        distance_to_in_km = self.get_cell_distance_to_in_km(row) or "-"
        distance_from_in_mi = self.get_cell_distance_from_in_mi(row) or "-"
        distance_to_in_mi = self.get_cell_distance_to_in_mi(row) or "-"
        slot_operator = self.get_cell_slot_operator(row) or "-"
        line_service = self.get_cell_line_service(row) or "-"
        booking_class = self.get_cell_booking_class(row) or "-"
        customer_rating = self.get_cell_customer_rating(row) or "-"
        exclude_from_matching = self.get_cell_exclude_from_matching(row) or "-"
        devanning = self.get_cell_devanning(row) or "-"
        crossdocking = self.get_cell_crossdocking(row) or "-"
        change_of_destination = self.get_cell_change_of_destination(row) or "-"
        number_of_extra_stops_inbound = self.get_cell_number_of_extra_stops_inbound(row) or "-"
        number_of_extra_stops_outbound = self.get_cell_number_of_extra_stops_outbound(row) or "-"
        receipt_condition = self.get_cell_receipt_condition(row) or "-"
        delivery_condition = self.get_cell_delivery_condition(row) or "-"
        from_drayage_option = self.get_cell_from_drayage_option(row) or "-"
        to_drayage_option = self.get_cell_to_drayage_option(row) or "-"
        from_max_no_of_stopovers_min = self.get_cell_from_max_no_of_stopovers_min(row) or "-"
        from_max_no_of_stopovers_max = self.get_cell_from_max_no_of_stopovers_max(row) or "-"
        to_max_no_of_stopovers_min = self.get_cell_to_max_no_of_stopovers_min(row) or "-"
        to_max_no_of_stopovers_max = self.get_cell_to_max_no_of_stopovers_max(row) or "-"
        propulsion = self.get_cell_propulsion(row) or "-"
        handl_ind = self.get_cell_handl_ind(row) or "-"
        optional_services_condition = self.get_cell_optional_services_condition(row) or "-"
        stack_level = self.get_cell_stack_level(row) or "-"
        criteria_names = self.get_cell_criteria_names(row) or "-"

        data.append(
            [id_, type_, position_amount, comment, valid_from, valid_to, calc, business_unit, prio, vessel,
             vessel_class, min_deadweight, max_deadweight, from_pol, from_sublocation_pol_berth, to_pod,
             to_sublocation_pod_berth, book_from, book_to, plor_zip_id, plor_zip, plod_zip_id, plod_zip, commodity,
             tariff_reference_id, tariff_reference, supplier, supplier_match_code, segment, package, size_type,
             cont_grp, cont_size, cont_type, s_o, empty_container, non_operative_reefer_nor, feeder, direct, transship,
             min_weight_in_kg, max_weight_in_kg, min_meas_in_m_3, max_meas_in_m_3, min_revtons, max_revtons,
             min_length_in_cm, max_length_in_cm, min_width_in_cm, max_width_in_cm, min_height_in_cm, max_height_in_cm,
             min_cont_over_height_in_cm, max_cont_over_height_in_cm, min_cont_over_width_left_in_cm,
             max_cont_over_width_left_in_cm, min_cont_over_width_right_in_cm, max_cont_over_width_right_in_cm,
             min_cont_over_length_front_in_cm, max_cont_over_length_front_in_cm, min_cont_over_length_door_in_cm,
             max_cont_over_length_door_in_cm, min_cont_over_weight_in_kg, max_cont_over_weight_in_kg,
             min_vessel_draft_in_m, max_vessel_draft_in_m, min_vessel_length_in_m, max_vessel_length_in_m,
             min_vessel_gross_tons, max_vessel_gross_tons, min_vessel_net_tons, max_vessel_net_tons, min_vessel_m3,
             max_vessel_m3, service, route, ship_type, ship_cond, transport_mode, dispo_code, min_imdg, max_imdg,
             imdg_un_no, agency, valid_from_t, valid_to_t, valid_days, receipt_term, delivery_terms_to,
             car_manufacturer, car_type, cargo_t, show_alw, deleted, imdg_in_quotation_booking_bl, i_o, manifest_t,
             customer, customer_match_code, min_stat_period, max_stat_period, voyage_from, voyage_to, creation_user,
             creation_date, update_user, update_date, add_costs, freight_term, out_of_gauge_oog, rail_contract,
             rail_plan_no, country_origin, country_destination, min_ocean_freight, max_ocean_freight, min_vessel_rgt,
             max_vessel_rgt, release_location, release_sublocation, return_location, return_sublocation, via, via_berth,
             distance_from_in_km, distance_to_in_km, distance_from_in_mi, distance_to_in_mi, slot_operator,
             line_service, booking_class, customer_rating, exclude_from_matching, devanning, crossdocking,
             change_of_destination, number_of_extra_stops_inbound, number_of_extra_stops_outbound, receipt_condition,
             delivery_condition, from_drayage_option, to_drayage_option, from_max_no_of_stopovers_min,
             from_max_no_of_stopovers_max, to_max_no_of_stopovers_min, to_max_no_of_stopovers_max, propulsion,
             handl_ind, optional_services_condition, stack_level, criteria_names

             ])

        # Print Console Row table
        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return self

    def _return_index(self, column_name: str):
        header_map = self.get_table_headers()
        column_index = header_map[column_name] + 2
        logger.info(f"_return_index:[{column_name}][{column_index}]")
        return [column_index, column_name]

    @allure.step("Select Type: {text}")
    def set_cell_select_type(self, row: int, text: str):
        self.dropdown_autocomplete() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row+1), text=text, column_index=self._return_index("Type"), column_list_match=1)
        return self

    @allure.step("Enter Comment: {text}")
    def set_cell_enter_comment(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.send_keys() \
            .set_locator_by_table(table_xpath=self._tbl_root_body) \
            .by_table_text(row=(row+1), text=text, column_index=self._return_index("Comment"))
        return self

    @allure.step("Valid From: {text}")
    def set_cell_enter_valid_from(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.send_keys() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row+1), text=text, column_index=self._return_index("Valid From"))
        return self

    @allure.step("Valid To: {text}")
    def set_cell_enter_valid_to(self, row: int, text: str):
        # Row 2 is the first Row Visible: row+1
        self.send_keys() \
            .set_locator_by_table(self._tbl_root_body) \
            .by_table_text(row=(row+1), text=text, column_index=self._return_index("Valid To"))
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

    def verify_row_data(self, row,  tariff_type, comment, valid_from, valid_to):
        row = row + 1
        cell_tariff_type = self.get_cell_type(row)
        cell_comment = self.get_cell_comment(row)
        cell_valid_from = self.get_cell_valid_from(row)
        cell_valid_to = self.get_cell_valid_to(row)

        assert cell_tariff_type == tariff_type, f"Error:[Type] Expected text '{tariff_type}' but found '{cell_tariff_type}'"
        assert cell_comment == comment, f"Error:[Comment] Expected text '{comment}' but found '{cell_comment}'"
        assert cell_valid_from == valid_from, f"Error:[Valid From] Expected text '{valid_from}' but found '{cell_valid_from}'"
        assert cell_valid_to == valid_to, f"Error:[Valid To] Expected text '{valid_to}' but found '{cell_valid_to}'"
        return self

    # Edit Fields --------------------------------------------------------------------------------------------
    @allure.step("Edit Internal Calculation Rule: Row: {row}, Charge: {charge}, Plus or Minus: {plus_minus}, Currency: {currency}, Rate: {rate}, Per: {per}, Var: {var_code}, Invoice: {invoice_currency}")
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

    @allure.step("Saved Internal Calculation Rule")
    def verify_saved_internal_calculation(self):
        toast_actual = self.alert.get_toast_detail()
        toast_expected = "Operation completed successfully."
        self.screenshot().attach_to_allure("Saved Internal Calculation Rule", self._name)
        # Assert with a custom error message
        assert toast_actual == toast_expected, f"[Error][verify_saved_internal_calculation]: Expected text '{toast_expected}' but found '{toast_actual}'"
        self.pause(3)
        return self

    def verify_position_amount(self, row, position_amount):
        row = row + 1
        actual = self.get_cell_position_amount(row)
        expected = position_amount
        self.screenshot().attach_to_allure("Update Position Amount", self._name)
        # Assert with a custom error message
        assert actual == expected, f"[Error][verify_position_amount]: Expected text '{expected}' but found '{actual}'"

    def verify_comment(self, row, comment):
        row = row + 1
        actual = self.get_cell_comment(row)
        expected = comment
        self.screenshot().attach_to_allure("Copy Comment", self._name)
        # Assert with a custom error message
        assert actual == expected, f"[Error][verify_comment]: Expected text '{expected}' but found '{actual}'"

    def verify_table_footer(self, message):
        expected = message
        actual = self.table_footer()
        # Assert with a custom error message
        assert actual == expected, f"[Error] Verify Table Footer Message: Expected text '{expected}' but found '{actual}'"
        return self



