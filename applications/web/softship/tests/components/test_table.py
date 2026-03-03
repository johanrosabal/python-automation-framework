import pytest

from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.config.decorators import softship
from applications.web.softship.pages.masterdata.basic.agencies.AgencyPage import AgencyPage
from applications.web.softship.pages.masterdata.basic.agencies.AgencyPlacesRelation import AgencyPlacesRelation
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import user
from core.utils.decorator import test

logger = setup_logger('TestTable')


@pytest.mark.web
@softship
class TestTable(SoftshipBaseTest):

    menu = SoftshipMenu.get_instance()
    agency = AgencyPage.get_instance()
    agency_places_relation = AgencyPlacesRelation.get_instance()

    # @pytest.mark.skip(reason="Skipping this test temporarily.")
    @test(test_case_id="MDS-0002", test_description="New Table")
    def test_table_new(self, softship_login_finance):
        row = 1
        self.menu.app_master_data.menu_basic.link_agency(pause=2)
        self.agency.click_select()

        self.agency.select_pagination(10)
        self.agency.print_row(row)
        self.agency.check_record(index=row)
        self.agency.check_all()
        self.agency.click_edit_icon(index=row)

        self.pause(10)

    # @pytest.mark.skip(reason="Skipping this test temporarily.")
    @test(test_case_id="MDS-0003", test_description="Old Table")
    def test_table_legacy(self):
        row = 2
        self.menu.app_master_data.menu_basic.link_agency_places_relation(pause=2)
        self.agency_places_relation.click_select()

        self.agency_places_relation.select_pagination(25)
        self.agency_places_relation.print_row(row)
        self.agency_places_relation.check_record(index=row)
        self.agency_places_relation.check_all()

        self.pause(10)


