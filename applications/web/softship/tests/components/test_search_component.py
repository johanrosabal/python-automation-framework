import pytest

from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.components.search.QuerySearchAdvanceComponent import QuerySearchAdvanceComponent
from applications.web.softship.components.search.QuerySearchComponent import QuerySearchComponent
from applications.web.softship.config.decorators import softship
from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import user
from core.utils.decorator import test
from applications.web.softship.pages.masterdata.basic.customer_suppliers.address.AddressPage import AddressPage

logger = setup_logger('TestMasterDataCustomerSuppliersAddress')


@pytest.mark.web
@softship
class TestSearchComponent(SoftshipBaseTest):
    # Init App
    menu = SoftshipMenu.get_instance()
    address_new = AddressPage.get_instance()
    search = QuerySearchComponent.get_instance()
    searchAdvance = QuerySearchAdvanceComponent.get_instance()

    @pytest.mark.skip(reason="Skipping this test temporarily.")
    @test(test_case_id="MDS-0002", test_description="Query Search Components")
    def test_query_search_components(self, softship_login_master_data):

        self.menu.app_master_data.menu_basic.link_address_new()

        queries = [
            {"field_name": "City Name", "field_operator": "equal", "field_value": "Baltimore, MD"},
            {"field_name": "Customer Address Type", "field_operator": "equal", "field_value": "BT"},
            {"field_name": "Customer Match Code", "field_operator": "equal", "field_value": "4622081"}
        ]

        self.search.execute_queries(queries)
        self.pause(5)

    @test(test_case_id="MDS-0004", test_description="Query Search Advance Components")
    def test_query_search_advance_components(self):
        self.menu.app_master_data.menu_basic.link_customer_supplier_query()

        queries = [
            {"field_name": "Country", "field_operator": "equal", "field_value": "US"},
            {"field_name": "Customer Id", "field_operator": "equal", "field_value": "0100246"},
            {"field_name": "Match Code", "field_operator": "equal", "field_value": "0100246"}
        ]

        self.searchAdvance.execute_queries(queries)
        self.pause(5)

