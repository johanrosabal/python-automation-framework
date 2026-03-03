from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
import time
import pytest
from applications.web.loadiq.pages.my_loads.MyLoadsPage import MyLoadsPage

logger = setup_logger('MyLoadsPageFinance)')

@pytest.mark.web
@loadiq
class TestMyLoadsFinance(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    finance = MyLoadsPage.get_instance()
    validLoad= "BY_10000273749"

    @test(test_case_id="CT-3093",test_description="Verify that the Finance Details tab displays correct financial fields and accessorial records if present",feature="byShipDate",skip=False)
    def test_my_loads_finance_details(self, load_iq_login_carrier_portal):
        # Move to the 'My Loads' section in the Carrier Portal.
        self.menu.carrier_portal.menu_my_loads(pause=2)
        # Enter a valid load ID to search for financial details and execute the search for the specified load.
        self.finance.enter_search_by(self.validLoad)
        self.finance.click_search()
        # Open the Finance Details tab to view financial information and scroll to the linehaul charge section to ensure visibility.
        self.finance.click_finance_details_tab()
        self.finance.scroll_to_linehaul_charge()
        # Assert that all expected financial fields are visible and assert that accessorial validation passed; otherwise, report the source and error message.
        assert self.finance.are_finance_fields_visible(), "One or more fields are not visible in the Finance Details tab."
        accessorial_result = self.finance.validate_and_check_accessorials()
        assert accessorial_result["status"], f"{accessorial_result['source'].capitalize()} check failed: {accessorial_result['message']}"

    @test(test_case_id="CT-3095",test_description="Verify that the Total Charge equals the sum of Linehaul, Fuel, and Accessorials",feature="byShipDate",skip=False)
    def test_my_loads_finance_details_total_charge(self, load_iq_login_carrier_portal):
        # Move to the 'My Loads' section in the Carrier Portal.
        self.menu.carrier_portal.menu_my_loads()
        # Enter a valid load ID to search for financial details and execute the search for the specified load.
        self.finance.enter_search_by(self.validLoad)
        self.finance.click_search()
        # Open the Finance Details tab to view financial information
        self.finance.click_finance_details_tab()
        # Validate that information matches correctly
        assert self.finance.get_charge_comparison()["correct"], "The total charge does not match the sum of the finance details."
