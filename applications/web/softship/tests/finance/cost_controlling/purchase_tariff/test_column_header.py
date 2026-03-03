from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.config.decorators import softship
from applications.web.softship.pages.finance.cost_controlling.purchase_tariff.PurchaseTariffPage import PurchaseTariffPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import user
from core.utils.decorator import test

logger = setup_logger('TestColumns')


@pytest.mark.web
@softship
class TestColumns(SoftshipBaseTest):
    purchase_tariff = PurchaseTariffPage.get_instance()

    @test(test_case_id="CT-1267", test_description="Add Purchase Tariffs Type", feature="Purchase Tariffs")
    def test_add_purchase_tariff_type(self, softship_login_finance, record_property):

        # Load Page
        self.purchase_tariff.load_page()
        # Shows Rows Table
        self.purchase_tariff.click_select()
        # Read Table Headers
        self.purchase_tariff.get_table_headers()
        # Display Search Expression Fields
        self.purchase_tariff.click_select_toggle()
        # Apply Search Criteria
        search_expression = [
            {"field_name": "Type", "field_operator": "equal", "field_value": "VOYPORT"},
            {"field_name": "Valid From", "field_operator": "equal", "field_value": "1/1/2017"},
            {"field_name": "Valid To", "field_operator": "equal", "field_value": "3/18/2019"},
            {"field_name": "Supplier", "field_operator": "equal", "field_value": "1037420"},
            {"field_name": "Comment", "field_operator": "contains", "field_value": "Vessel Assist"}
        ]
        self.purchase_tariff.queries_search(search_expression)

        # COLUMN ID VERIFICATION --------------------------------------------------------------------------------------
        # Get Original 'ID' Sort Items
        column_id_original = self.purchase_tariff.get_table_column_id()
        # Click on 'ID' Column to sort Data
        self.purchase_tariff.click_table_header_id()
        column_id_ascending = self.purchase_tariff.get_table_column_id()
        # Verify Ascending 'ID' Column
        assert column_id_ascending == column_id_original, "Column ID is not sorted in ascending order"
        # Click on 'ID' Column to sort Data Descending
        self.purchase_tariff.click_table_header_id()
        column_id_descending = self.purchase_tariff.get_table_column_id()
        assert column_id_descending == sorted(column_id_original, reverse=True), "Column 'ID' is not sorted in descending order"

        logger.info(f"Column ID > Original Order: {column_id_original}")
        logger.info(f"Column ID > Original Ascending: {column_id_ascending}")
        logger.info(f"Column ID > Original Descending: {column_id_descending}")

        # COLUMN TYPE VERIFICATION --------------------------------------------------------------------------------------
        # Get Original 'Type' Sort Items
        column_type_original = self.purchase_tariff.get_table_column_type()
        # Click on 'Type' Column to sort Data
        self.purchase_tariff.click_table_header_type()
        column_type_ascending = self.purchase_tariff.get_table_column_type()
        # Verify Ascending 'Type' Column
        assert column_type_ascending == column_type_original, "Column 'Type' is not sorted in ascending order"
        # Click on 'Type' Column to sort Data Descending
        self.purchase_tariff.click_table_header_type()
        column_type_descending = self.purchase_tariff.get_table_column_type()
        assert column_type_descending == sorted(column_type_original, reverse=True), "Column 'Type' is not sorted in descending order"

        # COLUMN VALID FROM VERIFICATION -------------------------------------------------------------------------------
        # Get Original 'Valid From' Sort Items
        column_valid_from_original = self.purchase_tariff.get_table_column_valid_from()
        # Click on 'Valid From' Column to sort Data
        self.purchase_tariff.click_table_header_valid_from()
        column_valid_from_ascending = self.purchase_tariff.get_table_column_valid_from()
        # Verify Ascending 'Valid From' Column
        assert column_valid_from_ascending == column_valid_from_original, "Column 'Valid From' is not sorted in ascending order"
        # Click on 'Valid From' Column to sort Data Descending
        self.purchase_tariff.click_table_header_valid_from()
        column_valid_from_descending = self.purchase_tariff.get_table_column_valid_from()
        assert column_valid_from_descending == sorted(column_valid_from_original, reverse=True), "Column 'Valid From' is not sorted in descending order"
        self.pause(5)
