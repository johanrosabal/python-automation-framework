import pytest
import allure

from applications.web.csight.components.menus.CSightMenu import CSightMenu
from applications.web.csight.pages.equipment_events.create_equipment_events.CreateEquipmentEventsPage import \
    CreateEquipmentEventsPage
from core.ui.common.BaseTest import BaseTest, user
from applications.web.csight.config.decorators import csight
from applications.web.csight.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.web.csight.pages.equipment_events.EquipmentEventsPage import EquipmentEventsPage
from core.asserts.AssertCollector import AssertCollector
from core.utils.json_data_helper import JSONDataHelper

logger = setup_logger('TestEquipmentEvents')


@pytest.fixture(scope="session")
def equipment_event_data():
    path = "../../data/equipment_events/CT-2783.json"
    data = JSONReader().import_json(path)
    data = helpers.parse_dynamic_dates_values(data)
    return data


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.web
@csight
class TestEquipmentEvents(BaseTest):

    menu = CSightMenu.get_instance()
    equipment_page = EquipmentEventsPage.get_instance()
    create_equipment_events = CreateEquipmentEventsPage.get_instance()

    @allure.title("Verify Equipment Events Module Opens Successfully")
    @allure.description("This test has the ability to open the Equipment Events module from the header and verifies that the Create Equipment Event form is displayed correctly.")
    @allure.tag("CSIGHT")
    @allure.link("https://crowley.atlassian.net/browse/CT-4686", name="Jira")
    @allure.testcase("CT-4686")
    @allure.feature("Open Equipment Events Module")
    @test(test_case_id="4686", test_description="Open Equipment Events Module", feature="Equipment Events", skip=False)
    def test_open_equipment_events(self, csight_login):

        # Click Create Equipment Events
        self.menu.click_menu_equipment_events()
        self.equipment_page.click_create_equipment_events()

        # Verify Current Location
        AssertCollector.assert_equal_message(
            expected=self.create_equipment_events.get_equipment_events_link(),
            actual=self.create_equipment_events.get_navigation(),
            message="Equipment Events URL Verification",
            method_name="verify_equipment_events_link"
        )

    @allure.title("Create a gate in full Container")
    @allure.description("This test creates a gate event for a full container in the Equipment Events module.")
    @allure.tag("CSIGHT")
    @allure.link("https://crowley.atlassian.net/browse/CT-2783", name="Jira")
    @allure.testcase("CT-2783")
    @allure.feature("Create a gate in full Container")
    @test(test_case_id="2783", test_description="Create a gate in full Container", feature="Equipment Events", skip=False)
    def test_gate_in_equipment_events(self, csight_login, equipment_event_data, shared_data):

        # Setting Equipment Data
        self.equipment_page.load_page()
        # Create Equipment Event
        self.equipment_page.click_create_equipment_events()
        # Enter Equipment Information
        self.create_equipment_events.fill_equipment_information(event_equipment_data=equipment_event_data)
        # Save Data
        self.create_equipment_events.click_create_equipment_event()

        AssertCollector.assert_equal_message(
            expected=True,
            actual=self.equipment_page.popup_success_message_is_visible(),
            message="Equipment Event Creation Verification",
            method_name="verify_equipment_event_creation"
        )
