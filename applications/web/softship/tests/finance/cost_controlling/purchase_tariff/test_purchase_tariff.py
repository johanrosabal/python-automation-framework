import allure
import pytest

from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.config.decorators import softship
from applications.web.softship.pages.finance.cost_controlling.purchase_tariff.PurchaseTariffPage import PurchaseTariffPage
from applications.web.softship.pages.masterdata.financial.purchase_tariff_criteria.PurchaseTariffCriteriaFormPage import PurchaseTariffCriteriaFormPage
from applications.web.softship.pages.masterdata.financial.purchase_tariff_criteria.PurchaseTariffCriteriaPage import PurchaseTariffCriteriaPage

from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.ui.common.BaseTest import user
from core.utils import helpers
from core.utils.decorator import test

logger = setup_logger('TestPurchaseTariff')


@pytest.fixture(scope="class")
def purchase_tariff_data():
    path = helpers.get_file_path("purchase_tariff.json")
    data = JSONReader().import_json(path)
    logger.info(f"[Fixture] 'purchase_tariff_data' data: {data}")
    return data


@pytest.fixture(scope="class")
def purchase_tariff_criteria_data():
    path = helpers.get_file_path("purchase_tariff_criteria.json")
    data = JSONReader().import_json(path)
    logger.info(f"[Fixture] 'purchase_tariff_criteria_data' data: {data}")
    return data


@pytest.mark.web
@softship
class TestPurchaseTariff(SoftshipBaseTest):

    menu = SoftshipMenu.get_instance()
    purchase_tariff_type = PurchaseTariffCriteriaPage.get_instance()
    purchase_tariff_criteria_form = PurchaseTariffCriteriaFormPage.get_instance()
    purchase_tariff = PurchaseTariffPage.get_instance()

    @test(test_case_id="CT-1267", test_description="Add Purchase Tariffs Type", feature="Purchase Tariffs", skip=False)
    def test_add_purchase_tariff_type(self, softship_login_master_data, purchase_tariff_criteria_data, record_property):
        record_property("test_key", "CT-1267")
        search_expression = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['search_expression']
        data = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['add']['data']
        expected = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['add']['expected']

        # Under Master Data
        # 01. Go to Purchase Tariff Criteria Type : MasterData > Financial > Purchase Tariff Criteria
        self.menu.app_master_data.menu_financial.link_purchase_tariff_criteria()
        # 02. Click on 'New' Button
        self.purchase_tariff_type.click_new()
        # 03.01. Complete Form Information: Tariff Type, Rate Category and Available Criteria
        self.purchase_tariff_criteria_form.select_tariff_type(data['type'])
        self.purchase_tariff_criteria_form.select_rate_category_assignment(data['rate_category'])
        self.purchase_tariff_criteria_form.search_rate_available_criteria_list(data['rate_available'])
        # 03.02. Save Form Information
        self.purchase_tariff_criteria_form.click_save()
        self.purchase_tariff_criteria_form.verify_saved_data()
        self.purchase_tariff_criteria_form.click_close()
        # 04. Show Search Expression Fields
        self.purchase_tariff_type.click_select_toggle()
        # 05. Search Expression
        self.purchase_tariff_type.query_search(
            field_name=search_expression['type'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        # 06. Search Results Verification
        self.purchase_tariff_type.verify_search_results(
            row=expected['row'],
            tariff_type=expected['type'],
            matching_criteria=expected['matching_code']
        )

    @test(test_case_id="CT-1274", test_description="Edit Purchase Tariffs Type", feature="Purchase Tariffs", skip=False)
    def test_edit_purchase_tariff_type(self, purchase_tariff_criteria_data, record_property):
        record_property("test_key", "CT-1274")
        search_expression = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['search_expression']
        data = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['edit']['data']
        expected = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['edit']['expected']

        # 01. Go to MasterData > Financial > Purchase Tariff Criteria
        self.menu.app_master_data.menu_financial.link_purchase_tariff_criteria()
        # 02. Click Select Toggle
        self.purchase_tariff_type.click_select_toggle()
        # 03. Search Expression Fields
        self.purchase_tariff_type.query_search(
            field_name=search_expression['type'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        # 04.01 Click Edit Icon
        self.purchase_tariff_type.click_edit_icon(data['row'])
        # 04.02 Remove Used Criteria
        self.purchase_tariff_criteria_form.clear_used_criteria(data['used_criteria'])
        # 04.03 Save Form Changes and Close
        self.purchase_tariff_criteria_form.click_save()
        self.purchase_tariff_criteria_form.verify_saved_data()
        self.purchase_tariff_criteria_form.click_close()
        # 05. Search Expression
        self.purchase_tariff_type.click_select_toggle()
        self.purchase_tariff_type.query_search(
            field_name=search_expression['type'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        self.purchase_tariff_type.verify_search_results(
            row=expected['row'],
            tariff_type=expected['type'],
            matching_criteria=expected['matching_code']
        )
        self.menu.logout()

    @test(test_case_id="CT-1268", test_description="Add Purchase Tariffs", feature="Purchase Tariffs", skip=False)
    def test_add_purchase_tariff(self, softship_login_finance, purchase_tariff_data, record_property):
        record_property("test_key", "CT-1268")
        search_expression = purchase_tariff_data['tests']['purchase_tariff']['search_expression']
        data = purchase_tariff_data['tests']['purchase_tariff']['add']['data']
        expected = purchase_tariff_data['tests']['purchase_tariff']['add']['expected']

        # 01. Go to Finance > Cost / Controlling / Purchase Tariff Extend
        self.menu.app_finance.menu_cost_controlling.link_purchase_tariffs_extended()
        # self.purchase_tariff.load_page()
        # 02. Click Select button
        self.purchase_tariff.click_select()
        # 03. Click New Button
        self.purchase_tariff.click_new()
        # 04. Complete Form Information
        self.purchase_tariff.set_cell_select_type(row=data['row'], text=data['type'])
        self.purchase_tariff.set_cell_enter_comment(row=data['row'], text=data['comment'])
        self.purchase_tariff.set_cell_enter_valid_from(row=data['row'], text=data['valid_from'])
        self.purchase_tariff.set_cell_enter_valid_to(row=data['row'], text=data['valid_to'])
        self.purchase_tariff.click_save()
        # 04.01 Verify Save Confirmation Alert
        self.purchase_tariff.verify_saved_data()
        # 04.03 Verify Table Grid Information
        self.purchase_tariff.click_select_toggle()
        self.purchase_tariff.query_search(
            field_name=search_expression['name'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        self.purchase_tariff.verify_row_data(
            row=expected['row'],
            tariff_type=expected['type'],
            comment=expected['comment'],
            valid_from=expected['valid_from'],
            valid_to=expected['valid_to']
        )

    @test(test_case_id="CT-1269", test_description="Edit Purchase Tariffs", feature="Purchase Tariffs", skip=False)
    def test_edit_purchase_tariff(self, purchase_tariff_data, record_property):
        record_property("test_key", "CT-1269")
        search_expression = purchase_tariff_data['tests']['purchase_tariff']['search_expression']
        data = purchase_tariff_data['tests']['purchase_tariff']['edit']['data']
        expected = purchase_tariff_data['tests']['purchase_tariff']['edit']['expected']

        # 01. Go to Finance > Cost / Controlling / Purchase Tariff Extend
        self.menu.app_finance.menu_cost_controlling.link_purchase_tariffs_extended()
        # 02. Click Select Toggle button
        self.purchase_tariff.click_select()
        self.purchase_tariff.click_select_toggle()
        # 03. Search Expression
        self.purchase_tariff.query_search(
            field_name=search_expression['name'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        # 04. Click Edit Icon
        self.purchase_tariff.click_edit_icon(data['row'])
        # 04.01 Adding Internal Calculation Rule Info
        self.purchase_tariff.internal_calculation_rule(
            row=data['row'],
            charge=data['charge'],
            plus_minus=data['plus_minus'],
            currency=data['currency'],
            rate=str(data['rate']),
            per=data['per'],
            var_code=data['var_code'],
            invoice_currency=data['invoice_currency']
        )
        # 04.02 Save Form Changes
        self.purchase_tariff.click_save()
        # 04.03 Information Save Alert
        self.purchase_tariff.verify_saved_internal_calculation()
        # 05. Check Position Amount Value Updated
        self.purchase_tariff.verify_position_amount(
            row=expected['row'],
            position_amount=expected['position_amount']
        )

    @test(test_case_id="CT-1270", test_description="Copy Purchase Tariffs", feature="Purchase Tariffs", skip=False)
    def test_copy_purchase_tariff(self, purchase_tariff_data, record_property):
        record_property("test_key", "CT-1270")
        search_expression = purchase_tariff_data['tests']['purchase_tariff']['search_expression']
        data = purchase_tariff_data['tests']['purchase_tariff']['copy']['data']
        expected = purchase_tariff_data['tests']['purchase_tariff']['copy']['expected']

        # 01. Go to Finance > Cost / Controlling / Purchase Tariff Extend
        self.menu.app_finance.menu_cost_controlling.link_purchase_tariffs_extended()
        # 02. Click Select Toggle button
        self.purchase_tariff.click_select()
        self.purchase_tariff.click_select_toggle()
        # 03. Search Expression
        self.purchase_tariff.query_search(
            field_name=search_expression['name'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        # 04. Click Checkbox
        self.purchase_tariff.check_record(index=data['row'])
        # 05.01 Click Copy
        self.purchase_tariff.click_copy()
        # 05.02 Edit Comment Field on Copy Line
        self.purchase_tariff.set_cell_enter_comment(data['row'], text=data['comment'])
        # 05.03 Save Changes
        self.purchase_tariff.click_save()
        # 05.04 Copy Confirmation Alert
        self.purchase_tariff.verify_saved_data()
        # 06. Search Expression
        self.purchase_tariff.click_select()
        self.purchase_tariff.click_select_toggle()
        self.purchase_tariff.query_search(
            field_name=expected['search_expression']['type'],
            field_operator=expected['search_expression']['operator'],
            field_value=expected['search_expression']['value']
        )
        # 07. Validate Comment Field
        self.purchase_tariff.verify_comment(row=expected['row'], comment=expected['comment'])

    @test(test_case_id="CT-1273", test_description="Delete Purchase Tariffs", feature="Purchase Tariffs", skip=False)
    def test_delete_purchase_tariff(self, purchase_tariff_data, record_property):
        record_property("test_key", "CT-1273")
        search_expression = purchase_tariff_data['tests']['purchase_tariff']['search_expression']
        data = purchase_tariff_data['tests']['purchase_tariff']['delete']['data']
        expected = purchase_tariff_data['tests']['purchase_tariff']['delete']['expected']

        # 01. Go to Finance > Cost / Controlling / Purchase Tariff Extend
        self.menu.app_finance.menu_cost_controlling.link_purchase_tariffs_extended()
        # 02. Click Select Toggle button
        self.purchase_tariff.click_select()
        self.purchase_tariff.click_select_toggle()
        # 03. Search Expression
        self.purchase_tariff.query_search(
            field_name=search_expression['name'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        # 04. Check Records Checkbox for Delete Process
        # self.purchase_tariff.check_record(index=1)
        # self.purchase_tariff.check_record(index=2)
        self.purchase_tariff.check_multiple_records(multiple_list=data['rows'])
        # 05. Click on Delete after select rows
        self.purchase_tariff.click_delete()
        # 06. Confirmation [YES] Button Tooltip
        self.purchase_tariff.click_confirmation_yes()
        self.purchase_tariff.click_save()
        # 06.01 Confirmation Alert
        self.purchase_tariff.verify_saved_data()
        # 06.02 No Records Found
        self.purchase_tariff.verify_table_footer(message=expected['message'])

    @test(test_case_id="CT-1490", test_description="Filter Search Expression Purchase Tariff", feature="Purchase Tariffs", skip=False)
    def test_filter_search_expression_purchase_tariff(self, purchase_tariff_data, record_property):
        record_property("test_key", "CT-1490")

        # Load Page
        self.purchase_tariff.load_page()
        self.purchase_tariff.click_select()
        self.purchase_tariff.select_pagination(25)
        self.purchase_tariff.click_select_toggle()
        # Search Criteria
        search_expression = purchase_tariff_data['tests']['purchase_tariff']['filter_search_expression']['search_expression']
        self.purchase_tariff.queries_search(search_expression)
        # Get Type Column Items
        column_type = self.purchase_tariff.get_table_column_type()
        all_verify = all(item == "SCOD" for item in column_type)
        # Check Values
        if all_verify:
            logger.info(f"All items are 'SCOD': {column_type}")
        else:
            logger.error(f"Not all items are 'SCOD': {column_type}")
            pytest.fail(f"Not all items are 'SCOD': {column_type}")

    @test(test_case_id="CT-1275", test_description="Delete Purchase Tariffs Type", feature="Purchase Tariffs", skip=False)
    def test_delete_purchase_tariff_type(self, softship_login_master_data, purchase_tariff_criteria_data, record_property):
        record_property("test_key", "CT-1275")
        search_expression = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['search_expression']
        data = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['delete']['data']
        expected = purchase_tariff_criteria_data['tests']['purchase_tariff_criteria']['delete']['expected']

        # 01. Go to Purchase Tariff Criteria Type
        self.menu.app_master_data.menu_financial.link_purchase_tariff_criteria()
        # self.purchase_tariff_type.load_page()
        # 02. Click Select Toggle
        self.purchase_tariff_type.click_select()
        self.purchase_tariff_type.click_select_toggle()
        # 03. Search Expression Fields
        self.purchase_tariff_type.query_search(
            field_name=search_expression['name'],
            field_operator=search_expression['operator'],
            field_value=search_expression['value']
        )
        # 04. Check Record to be Deleted
        self.purchase_tariff_type.check_multiple_records(multiple_list=data['rows'])
        self.purchase_tariff_type.click_delete()
        # 05. Confirmation [YES] Button Tooltip
        self.purchase_tariff_type.click_confirmation_yes()
        # 05.01 Confirmation Alert
        self.purchase_tariff_type.verify_data_deleted()
        # 05.02 No Records Found
        self.purchase_tariff_type.verify_table_footer(message=expected['message'])
        self.menu.logout()




