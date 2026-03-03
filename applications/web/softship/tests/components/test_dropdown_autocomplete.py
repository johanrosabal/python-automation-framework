from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.config.decorators import softship
from applications.web.softship.pages.masterdata.financial.purchase_tariff_criteria.PurchaseTariffCriteriaFormPage import \
    PurchaseTariffCriteriaFormPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import user
from core.utils.decorator import test

logger = setup_logger('TestDropdownAutocomplete')


@pytest.mark.web
@softship
class TestDropdownAutocomplete(SoftshipBaseTest):

    @test(test_case_id="MDS-0000", test_description="Test Dropdown Autocomplete by Label Text")
    def test_table_new(self, softship_login_finance):
        (
            PurchaseTariffCriteriaFormPage
            .get_instance()
            .load_page()
            .select_tariff_type("VOYAGE")
            .select_rate_category_assignment("Ocean Additionals")
            .search_rate_available_criteria("Agency")
            .search_rate_available_criteria("Book From")
            .search_rate_available_criteria("Car Manufacturer")
            .check_used_criteria("Agency")
            .clear_used_criteria("Car Manufacturer")
            .clear_list_used_criteria()
            .pause(10)
        )
