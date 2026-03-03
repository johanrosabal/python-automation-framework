
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.pages.my_loads.MyLoadsPage import MyLoadsPage
from applications.web.loadiq.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
import time
import pytest
logger = setup_logger('MyLoadsPage')

@pytest.mark.web
@loadiq
class TestMyLoadsFilters(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    filters = MyLoadsPage.get_instance()
    loadClosed= "LD24091200001"


    # 01. Verify the user is logged into carrier Portal (Use PreDefine Login Fixture)
    @test(test_case_id="CT-1994", test_description="Verify filter by Ship date", feature="byShipDate",skip=False)
    def test_my_loads_filter(self, load_iq_login_carrier_portal):

        #("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        #("Loading existing shipments and including closed loads...")
        self.filters.load_page()
        self.filters.checkbox_include_closed()
        #("Performing search...")
        #"Sorting by ship date..."
        self.filters.click_sort_by_ship_date()
        #Assertion: Verify button is present
        assert self.filters.ship_date_sort_is_present(), "'Sort by Origin' button is not present"

    @test(test_case_id="CT-2615", test_description="Verify filter by status", feature="byStatus",skip=False)
    def test_my_loads_filter_status(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.filters.load_page()
        #"Include closed items and sorting by status"
        self.filters.checkbox_include_closed()
        self.filters.click_sort_by_status()
        # Assertion: Verify button is present
        assert self.filters.status_sort_is_present(), "'Sort by Origin' button is not present"

    # TEST CASE NOT APPLY, THE ORIGIN BUTTON WAS REMOVED FROM THE UI
    @test(test_case_id="CT-2616", test_description="Verify filter by origin", feature="byOrigin",skip=True)
    def test_my_loads_filter_origin(self,):

        self.menu.carrier_portal.menu_my_loads()
        self.filters.load_page()
        # ("Navigating to 'My Loads' page...")
        self.filters.checkbox_include_closed()
        self.filters.click_sort_by_origin()
        #Verify button is present
        assert self.filters.origin_sort_is_present(), "'Sort by Origin' button is not present"

    @test(test_case_id="CT-1993", test_description="Verify filter enable closed items/Ensure search functionality for closed records", feature="SearchBar",skip=True)
    def test_my_loads_filter_closed_items(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.filters.load_page()
        # "Include closed items and search an existing load"
        self.filters.checkbox_include_closed()
        self.filters.enter_search_by(search_by=self.loadClosed)
        self.filters.click_search()

        # Validate that the closed load appears
        actual_load_id = self.filters.validate_single_closed_load()
        assert actual_load_id == self.loadClosed, f"Expected load ID '{self.loadClosed}', but got '{actual_load_id}'"

    @test(test_case_id="CT-1992", test_description="Verify filter disable closed items", feature="SearchBar",skip=True)
    def test_my_loads_filter_dis_closed_items(self,):
        # ("Navigates to 'My Loads' page...")
        self.menu.carrier_portal.menu_my_loads()
        self.filters.load_page()
        # Include closed items
        self.filters.checkbox_include_closed()
        self.filters.checkbox_include_closed()
        # "Search an invalid load"
        self.filters.enter_search_by(search_by=self.loadClosed)
        self.filters.click_search()
        # Validates the load search result via text UI.
        actual_message = self.filters.validate_single_load()
        expected_message = "Sorry, we couldn't find any results."
        assert actual_message != expected_message, (
            "Error: The 'load' was not found"
        )










