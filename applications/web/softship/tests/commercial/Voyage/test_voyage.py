from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from core.ui.common.BaseTest import user
from applications.web.softship.pages.commercial.Voyage.VoyageFormPage import VoyageFormPage
from applications.web.softship.pages.commercial.Voyage.VoyagePage import VoyagePage
from applications.web.softship.config.decorators import softship
from applications.web.softship.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.utils.decorator import test


logger = setup_logger('TestVoyage')


@pytest.mark.web
@softship
class TestVoyage(SoftshipBaseTest):

    menu = SoftshipMenu.get_instance()
    voyage_form = VoyageFormPage.get_instance()
    voyage = VoyagePage.get_instance()

    @test(test_case_id="MDS-0001", test_description="Create Voyage")
    def test_voyage_display_information(self, softship_login_commercial):
        voyage_number = "5013"
        # 01. Go to Commercial > Voyage > Update Voyage
        self.menu.app_commercial.menu_voyage.menu_update_voyage(pause=1)
        # 02. Display Table Information
        self.voyage.click_select(pause=1)
        self.voyage.click_new(pause=1)
        # 03. Fill Main Information Form
        self.voyage_form.fill_out_voyage_information(
            service="Mexico US Service",
            vessel="Sonderborg",
            vessel_owner="STANDARD SHIPOWNER",
            voyage_number=f"MEX{voyage_number}",
            second_voyage_number=f"{voyage_number}W",
            customs_declarations_number="",
            financial_voyage_period="3/10/2025",
            operator="SEABOARD MARINE LTD",
            transport_mode="Owned",
            commercial_service="Mexico US Service",
        )
        # 04. Fill Details Form
        self.voyage_form.fill_out_details_information()

        port_calls = [
            {"port": "Gulfport, MS", "eta": "3/3/2025 12:00 AM", "ets": "3/3/2025 12:00 PM", "status": "PP", "type": "Load"},
            {"port": "Tuxpan, Mexico", "eta": "3/6/2025 12:00 AM", "ets": "3/6/2025 12:00 PM", "status": "PP", "type": "Both"},
            {"port": "Gulfport, MS", "eta": "3/10/2025 08:00 AM", "ets": "3/10/2025 07:00 PM", "status": "PP", "type": "Discharge"},
        ]

        self.voyage_form.enter_multiple_ports(port_calls)
        self.voyage_form.click_save_and_close()
        # Show Records Items
        self.voyage.click_select_toggle(show=True)
        # Enter Search Criteria
        queries = [
            {"field_name": "Source", "field_operator": "equal", "field_value": "Commercial"},
            {"field_name": "Voyage Number", "field_operator": "contains", "field_value": voyage_number},
        ]

        self.voyage.queries_search(queries)

        # Getting Row Information First Row
        self.voyage.get_table_row(1)
        self.pause(5)
        self.menu.logout()
