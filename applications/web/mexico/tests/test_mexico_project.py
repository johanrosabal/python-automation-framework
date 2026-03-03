from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.fixtures.fixtures import *
from applications.web.mexico.config.decorators import softship
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.pages.finance.sales_invoicing.SalesTariffExtendedPage import SalesTariff_ExtendedPage
from applications.web.softship.pages.commercial.Voyage.VoyageFormPage import VoyageFormPage
from applications.web.softship.pages.commercial.Voyage.VoyagePage import VoyagePage
from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers
from core.utils.decorator import test
from core.ui.common.BaseTest import user

logger = setup_logger('TestMexicoProject')


@pytest.mark.web
@softship
class TestMexicoProject(SoftshipBaseTest):

    menu = SoftshipMenu.get_instance()
    sales_tariff_extended = SalesTariff_ExtendedPage.get_instance()
    voyage_form = VoyageFormPage.get_instance()
    voyage = VoyagePage.get_instance()

    @test(test_case_id="MDS-0001", test_description="Create Voyage", feature="Mexico Project", skip=False)
    def test_voyage_create_routes(self, softship_login_commercial):
        # Precondition: Read JSON File
        data = JSONReader().import_json(helpers.get_file_path("mexico_routes.json"))
        data = helpers.parse_dynamic_dates_values(data)
        # Data Sections From JSON
        main_information = data['tests']['main_information']
        details_information = data['tests']['details_information']
        port_calls = data['tests']['port_calls']
        search_expression = data['tests']['search_expression']

        helpers.print_json(title="Create Voyage Mexico Project", data=data)
        # 01. Go to Commercial > Voyage > Update Voyage
        self.menu.app_commercial.menu_voyage.menu_update_voyage(pause=1)
        # 02. Display Table Information
        self.voyage.click_select(pause=1)
        self.voyage.click_new(pause=1)
        # 03. Fill Main Information Form
        self.voyage_form.fill_out_voyage_information(
            service=main_information['service'],
            vessel=main_information['vessel'],
            vessel_owner=main_information['vessel_owner'],
            voyage_number=main_information['voyage_number'],
            second_voyage_number=main_information['second_voyage_number'],
            customs_declarations_number=main_information['customs_declarations_number'],
            financial_voyage_period=main_information['financial_voyage_period'],
            operator=main_information['operator'],
            transport_mode=main_information['transport_mode'],
            commercial_service=main_information['commercial_service'],
        )
        # 04. Fill Details Form
        self.voyage_form.fill_out_details_information(
            toggle_details=details_information['toggle_details'],
            offshore_days=details_information['offshore_days'],
            publish_voyage=details_information['publish_voyage'],
            remarks=details_information['remarks'],
            carriers_agent_ecs=details_information['carriers_agent_ecs']

        )
        # Enter Port Calls List
        self.voyage_form.enter_multiple_ports(port_calls)
        self.voyage_form.click_save_and_close()

        # Show Records Items
        self.voyage.click_select_toggle(show=True)
        # Enter Search Criteria
        self.voyage.queries_search(search_expression)

        # Getting First Row Filtered Information
        if self.voyage.validate_data_results():
            self.voyage.get_table_row(1)

        # Logout User From Commercial Mode
        self.menu.logout()

    @test(test_case_id="MX-0001", test_description="Finance Module: Level 1 | USGPT | MXTUX | Mexico", feature="Mexico Project", skip=False)
    def test_finance_create_sales_tariff_level_1(self, softship_login_finance):
        # Precondition: Read JSON File
        data = JSONReader().import_json(helpers.get_file_path("mexico_tariff_extended.json"))
        data = helpers.parse_dynamic_dates_values(data)
        # Data Sections From JSON
        main_information = data['tests']['sales_tariff_extended']['level_1']['information']
        search_expression = data['tests']['sales_tariff_extended']['level_1']['search_expression']
        internal_calculation = data['tests']['sales_tariff_extended']['level_1']['internal_calculation']

        #  Login with Fixture Finance Module > softship_login_finance
        # Go To: Sales Invoicing > Sales Tariff Extended
        self.menu.app_finance.menu_sales_invoice.link_sales_tariffs_extended()
        # Click Select to Display Records and Enable 'New' Button
        self.sales_tariff_extended.click_select()
        # Click on 'New' Button to add a new record
        self.sales_tariff_extended.click_new()
        # Fill Out Fields Columns

        self.sales_tariff_extended.fill_out_sales_tariff_form(
            row=main_information['row'],
            tariff_name=main_information['tariff_name'],
            level=main_information['level'],
            from_pol=main_information['from_pol'],
            to_pod=main_information['to_pod'],
            agency=main_information['agency'],
            package=main_information['package'],
            valid_from=main_information['valid_from'],
            shippers_own=main_information['shippers_own'],
            change_frequency=main_information['change_frequency'],
            sales_tariff_remark=main_information['sales_tariff_remark'],
            cargo=main_information['cargo'],
            short_from=main_information['short_from'],
            transport_mode=main_information['transport_mode'],
            devanning=main_information['devanning'],
            crossdocking=main_information['crossdocking'],
            to_sublocation_pod_berth=main_information['to_sublocation_pod_berth']
        )
        # Save New Item
        self.sales_tariff_extended.click_save()
        # Verify Save Confirmation Alert
        self.sales_tariff_extended.verify_saved_data()
        # Search Record Created Record
        self.sales_tariff_extended.click_select_toggle(show=True)
        # Apply Filter
        self.sales_tariff_extended.queries_search(search_expression)
        # Select First Row
        self.sales_tariff_extended.click_edit_icon(main_information['row'])
        # Click Edit New Record
        # Adding Internal Calculation Rule Inf
        self.sales_tariff_extended.internal_calculation_rule(
            row=internal_calculation['row'],
            charge=internal_calculation['charge'],
            plus_minus=internal_calculation['plus_minus'],
            currency=internal_calculation['currency'],
            rate=internal_calculation['rate'],
            per=internal_calculation['per'],
            var_code=internal_calculation['var_code'],
            invoice_currency=internal_calculation['invoice_currency']
        )
        # Save Edit Changes
        self.sales_tariff_extended.click_save()
        # Verify Save Edit
        self.sales_tariff_extended.verify_saved_internal_calculation()

    @test(test_case_id="MX-0002", test_description="Finance Module: Level 61 | USMOB | USGPT | TRUCK | US Inland", feature="Mexico Project", skip=False)
    def test_finance_create_sales_tariff_level_61(self):
        # Precondition: Read JSON File
        data = JSONReader().import_json(helpers.get_file_path("mexico_tariff_extended.json"))
        data = helpers.parse_dynamic_dates_values(data)
        # Data Sections From JSON
        main_information = data['tests']['sales_tariff_extended']['level_61']['information']
        search_expression = data['tests']['sales_tariff_extended']['level_61']['search_expression']
        internal_calculation = data['tests']['sales_tariff_extended']['level_61']['internal_calculation']

        #  Login with Fixture Finance Module > softship_login_finance
        # Go To: Sales Invoicing > Sales Tariff Extended
        self.menu.app_finance.menu_sales_invoice.link_sales_tariffs_extended()
        # Click Select to Display Records and Enable 'New' Button
        self.sales_tariff_extended.click_select()
        # Click on 'New' Button to add a new record
        self.sales_tariff_extended.click_new()
        # Fill Out Fields Columns
        self.sales_tariff_extended.fill_out_sales_tariff_form(
            row=main_information['row'],
            tariff_name=main_information['tariff_name'],
            level=main_information['level'],
            from_pol=main_information['from_pol'],
            to_pod=main_information['to_pod'],
            agency=main_information['agency'],
            package=main_information['package'],
            valid_from=main_information['valid_from'],
            shippers_own=main_information['shippers_own'],
            change_frequency=main_information['change_frequency'],
            sales_tariff_remark=main_information['sales_tariff_remark'],
            cargo=main_information['cargo'],
            short_from=main_information['short_from'],
            transport_mode=main_information['transport_mode'],
            devanning=main_information['devanning'],
            crossdocking=main_information['crossdocking'],
            to_sublocation_pod_berth=main_information['to_sublocation_pod_berth']
        )
        # Save New Item
        self.sales_tariff_extended.click_save()
        # Verify Save Confirmation Alert
        self.sales_tariff_extended.verify_saved_data()
        # Search Record Created Record
        self.sales_tariff_extended.click_select_toggle(show=True)
        # Apply Filter
        self.sales_tariff_extended.queries_search(search_expression)
        # Select First Row
        self.sales_tariff_extended.click_edit_icon(main_information['row'])
        # Click Edit New Record
        # Adding Internal Calculation Rule Inf
        self.sales_tariff_extended.internal_calculation_rule(
            row=internal_calculation['row'],
            charge=internal_calculation['charge'],
            plus_minus=internal_calculation['plus_minus'],
            currency=internal_calculation['currency'],
            rate=internal_calculation['rate'],
            per=internal_calculation['per'],
            var_code=internal_calculation['var_code'],
            invoice_currency=internal_calculation['invoice_currency']
        )
        # Save Edit Changes
        self.sales_tariff_extended.click_save()
        # Verify Save Edit
        self.sales_tariff_extended.verify_saved_internal_calculation()

    @test(test_case_id="MX-0003", test_description="Finance Module: Level 63 | CABRP | USMOB | RAIL | Non-CASS US Inland", feature="Mexico Project", skip=False)
    def test_finance_create_sales_tariff_level_63(self):
        # Precondition: Read JSON File
        data = JSONReader().import_json(helpers.get_file_path("mexico_tariff_extended.json"))
        data = helpers.parse_dynamic_dates_values(data)
        # Data Sections From JSON
        main_information = data['tests']['sales_tariff_extended']['level_63']['information']
        search_expression = data['tests']['sales_tariff_extended']['level_63']['search_expression']
        internal_calculation = data['tests']['sales_tariff_extended']['level_63']['internal_calculation']
        #  Login with Fixture Finance Module > softship_login_finance
        # Go To: Sales Invoicing > Sales Tariff Extended
        self.menu.app_finance.menu_sales_invoice.link_sales_tariffs_extended()
        # Click Select to Display Records and Enable 'New' Button
        self.sales_tariff_extended.click_select()
        # Click on 'New' Button to add a new record
        self.sales_tariff_extended.click_new()
        # Fill Out Fields Columns

        self.sales_tariff_extended.fill_out_sales_tariff_form(
            row=main_information['row'],
            tariff_name=main_information['tariff_name'],
            level=main_information['level'],
            from_pol=main_information['from_pol'],
            to_pod=main_information['to_pod'],
            agency=main_information['agency'],
            package=main_information['package'],
            valid_from=main_information['valid_from'],
            shippers_own=main_information['shippers_own'],
            change_frequency=main_information['change_frequency'],
            sales_tariff_remark=main_information['sales_tariff_remark'],
            cargo=main_information['cargo'],
            short_from=main_information['short_from'],
            transport_mode=main_information['transport_mode'],
            devanning=main_information['devanning'],
            crossdocking=main_information['crossdocking'],
            to_sublocation_pod_berth=main_information['to_sublocation_pod_berth']
        )
        # Save New Item
        self.sales_tariff_extended.click_save()
        # Verify Save Confirmation Alert
        self.sales_tariff_extended.verify_saved_data()
        # Search Record Created Record
        self.sales_tariff_extended.click_select_toggle(show=True)
        # Apply Filter
        self.sales_tariff_extended.queries_search(search_expression)
        # Re-Enter Cargo Value, because it is not saving on 'New' Record
        # Select First Row
        self.sales_tariff_extended.click_edit_icon(main_information['row'])
        # Click Edit New Record
        # Adding Internal Calculation Rule Inf
        self.sales_tariff_extended.internal_calculation_rule(
            row=internal_calculation['row'],
            charge=internal_calculation['charge'],
            plus_minus=internal_calculation['plus_minus'],
            currency=internal_calculation['currency'],
            rate=internal_calculation['rate'],
            per=internal_calculation['per'],
            var_code=internal_calculation['var_code'],
            invoice_currency=internal_calculation['invoice_currency']
        )
        # Save Edit Changes
        self.sales_tariff_extended.click_save()
        # Verify Save Edit
        self.sales_tariff_extended.verify_saved_internal_calculation()

    @test(test_case_id="MX-0004", test_description="Finance Module: Level 61 | $0OO5 | CABRP | TRUCK | US Inland", feature="Mexico Project", skip=False)
    def test_finance_create_sales_tariff_level_61_sublocation(self,softship_login_finance):
        # Precondition: Read JSON File
        data = JSONReader().import_json(helpers.get_file_path("mexico_tariff_extended.json"))
        data = helpers.parse_dynamic_dates_values(data)
        # Data Sections From JSON
        main_information = data['tests']['sales_tariff_extended']['level_61_sublocation']['information']
        search_expression = data['tests']['sales_tariff_extended']['level_61_sublocation']['search_expression']
        internal_calculation = data['tests']['sales_tariff_extended']['level_61_sublocation']['internal_calculation']
        #  Login with Fixture Finance Module > softship_login_finance
        # Go To: Sales Invoicing > Sales Tariff Extended
        self.menu.app_finance.menu_sales_invoice.link_sales_tariffs_extended()
        # Click Select to Display Records and Enable 'New' Button
        self.sales_tariff_extended.click_select()
        # Click on 'New' Button to add a new record
        self.sales_tariff_extended.click_new()
        # Fill Out Fields Columns
        self.sales_tariff_extended.fill_out_sales_tariff_form(
            row=main_information['row'],
            tariff_name=main_information['tariff_name'],
            level=main_information['level'],
            from_pol=main_information['from_pol'],
            to_pod=main_information['to_pod'],
            agency=main_information['agency'],
            package=main_information['package'],
            valid_from=main_information['valid_from'],
            shippers_own=main_information['shippers_own'],
            change_frequency=main_information['change_frequency'],
            sales_tariff_remark=main_information['sales_tariff_remark'],
            cargo=main_information['cargo'],
            short_from=main_information['short_from'],
            transport_mode=main_information['transport_mode'],
            devanning=main_information['devanning'],
            crossdocking=main_information['crossdocking'],
            to_sublocation_pod_berth=main_information['to_sublocation_pod_berth']
        )
        # Save New Item
        self.sales_tariff_extended.click_save()
        # Verify Save Confirmation Alert
        self.sales_tariff_extended.verify_saved_data()
        # Search Record Created Record
        self.sales_tariff_extended.click_select_toggle(show=True)
        # Apply Filter
        self.sales_tariff_extended.queries_search(search_expression)
        # Select First Row
        self.sales_tariff_extended.click_edit_icon(main_information['row'])
        # Click Edit New Record
        # Adding Internal Calculation Rule Inf
        self.sales_tariff_extended.internal_calculation_rule(
            row=internal_calculation['row'],
            charge=internal_calculation['charge'],
            plus_minus=internal_calculation['plus_minus'],
            currency=internal_calculation['currency'],
            rate=internal_calculation['rate'],
            per=internal_calculation['per'],
            var_code=internal_calculation['var_code'],
            invoice_currency=internal_calculation['invoice_currency']
        )
        # Save Edit Changes
        self.sales_tariff_extended.click_save()
        # Verify Save Edit
        self.sales_tariff_extended.verify_saved_internal_calculation()
        self.menu.logout()
