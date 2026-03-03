import pytest
from selenium.webdriver.common.by import By

from applications.web.csight.components.loadings.Loadings import Loadings
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('RoutesPage')

# Global Variable
if not hasattr(pytest, 'BOOKING_RESULTS'):
    pytest.BOOKING_RESULTS = []


class RoutesComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the RoutesPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__

        # Set Class Data
        self.booking_data = None

        # Locator definitions
        self._tab_routes = (By.XPATH, "//div[@data-label='Routes']", "Routes [Tab]")

        # Locator definitions
        self._xpath_route_container = "(//div[contains(@class,'veloz-routes')])"
        self._link_action_price = (By.XPATH, "//a[@id='Price']", "Sort by Price [Link Action]")
        self._link_action_transit_time = (By.XPATH, "//a[@id='Duration']", "Sort by Transit Time [Link Action]")
        self._toggle_show_all_routes = (By.XPATH, "//span[@data-toggle-description]", "Show All Routes [Toggle Button]")
        # Sub-Components
        self.loadings = Loadings.get_instance()

    def load_tab(self):
        self.click().set_locator(self._tab_routes, self._name).single_click()
        return self

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def set_booking_data(self, data=None):
        """ Set Booking Data and share with all fill methods """
        self.booking_data = data
        return self

    # SORT ITEMS -------------------------------------------------------------------------------------------------------
    def click_sort_by_price(self):
        self.click().set_locator(self._link_action_price, self._name).single_click()
        return self

    def click_sort_by_transit_time(self):
        self.click().set_locator(self._link_action_transit_time, self._name).single_click()
        return self

    def check_rates_not_available_and_skip(self, result):
        """
        Check if the "fares unavailable" message is on the page.
        If it is, update the result and fail the test.
        """
        locator = (By.XPATH, "//div/div[@class='col-12']/h5", "No Rates Available Text")
        body_text = self.get_text().set_locator(locator=locator, timeout=10).by_text()

        if body_text is None:
            body_text = ""

        if "Rates are not immediately available for your selected combination." in body_text:
            result["test_status"] = "FAIL"
            result["booking_message"] = "Rates Not Available"
            return True
        else:
            return False

    def click_and_get_route_item_information(self, route_item=None):
        """
        Click to Select Route Item
        """
        vessel_name = ""
        voyage_number = ""
        route_item = ""

        # Set Up Booking Data if Argument is None
        if self.booking_data:
            route_item = self.booking_data['tests']['data']['booking']['routes']['routes_item']
            vessel_name = self.booking_data['tests']['data']['booking']['routes']['vessel_name']
            voyage_number = self.booking_data['tests']['data']['booking']['routes']['voyage_number']

        # If Users Provides Vessel Name and Voyage Number
        if vessel_name != "" and voyage_number != "":
            routes = self.get_routes_count()
            for route in range(1, routes + 1):
                if self.get_vessel_name(index=route) == vessel_name and self.get_voyage_number(
                        index=route_item) == voyage_number:
                    route_item = route
                else:
                    logger.warning(f"Vessel Name [{vessel_name}] and/or Voyage Number [{voyage_number}] not found")

        self.loadings.is_not_visible_spinner()
        # Internal XPath because we have here an index value
        locator = (By.XPATH, f"{self._xpath_route_container}[{route_item}]//input[@type='checkbox']/..//span[1]",
                   f"Route Check Selection [{route_item}]")
        # Select Route JSON Field 'routes_item'
        self.element().wait(locator=locator, timeout=15)
        self.element().set_locator(locator).is_enabled()
        self.click().set_locator(locator).highlight().pause(3).single_click()

        item_container = (By.XPATH, f"{self._xpath_route_container}[{route_item}]",
                          f"Route Container: {self._xpath_route_container}[{route_item}]")
        self.scroll().set_locator(item_container).to_element(pixels=-150)

        return self.get_route_item_information(index=route_item)

    def get_routes_count(self):
        locator = (By.XPATH, self._xpath_route_container, "Routes Items")
        return self.element().set_locator(locator).get_list_count()

    # ITEM INFORMATION -------------------------------------------------------------------------------------------------
    def get_origin_terminal(self, index):
        # Internal XPath because we have here an index value
        locator = (By.XPATH, f"((//div[contains(@class,'veloz-routes')])[{index}]//i[text()='Port'])[1]/../span[1]",
                   f"Origin Terminal [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_origin_city_state(self, index):
        # Internal XPath because we have here an index value
        locator = (By.XPATH, f"((//div[contains(@class,'veloz-routes')])[{index}]//i[text()='Port'])[1]/../span[2]",
                   f"Origin Terminal [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_destination_terminal(self, index):
        # Internal XPath because we have here an index value
        locator = (By.XPATH, f"((//div[contains(@class,'veloz-routes')])[{index}]//i[text()='Port'])[2]/../span[1]",
                   f"Destination Terminal [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_destination_city_state(self, index):
        # Internal XPath because we have here an index value
        locator_full_text = (By.XPATH, f"((//div[contains(@class,'veloz-routes')])[{index}]//i[text()='Port'])[2]/..",
                             f"Destination City State [{index}]")
        destination_terminal = self.get_destination_terminal(index)
        full_text = self.get_text().set_locator(locator_full_text, self._name).by_text()
        return full_text.replace("Port", "").replace(destination_terminal, "").replace("\n", "")

    def get_est_sail_date(self, index):
        locator = (By.XPATH,
                   f"(//div[contains(@class,'veloz-routes')])[{index}]/h6/span[contains(.,'Est. Sail Date')]//b[2] | (//div[contains(@class,'veloz-routes')])[{index}]/h6/span[contains(.,'Est. Sail Date')]//b[1]",
                   f"Est. Sail Date [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_transit_time(self, index):
        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]//span[@class='transit-time-head']/b",
                   f"Transit Time [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_est_arrival_date(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//span[contains(text(),'Est. Arrival Date')]/lightning-formatted-date-time",
                   f"Est. Arrival Date [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_est_cargo_availability(self, index):
        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]//span[contains(text(),'Est. Arrival Date')]/b",
                   f"Est. Cargo Availability [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_vessel_name(self, index):
        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]//span[contains(.,'Vessel Name')]/span",
                   f"Vessel Name [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_voyage_number(self, index):
        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]//span[contains(.,'Voyage Number')]/span",
                   f"Voyage Number [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_route_price_amount(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@class='route-price-details']//lightning-formatted-number",
                   f"Route Price Amount [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def click_route_rate_details_show_hide(self, index):
        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]//h6[contains(@class,'view-route-details')]/a",
                   f"Route / Rate Details [{index}]")
        self.click().set_locator(locator, self._name).single_click()
        return

    def click_rate_details_tab(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//ul[@class='slds-tabs_scoped__nav']/li/a[text()='Rate Details']",
                   f"Route / Rate Details [{index}]")
        self.click().set_locator(locator, self._name).single_click()
        return

    def click_route_details_tab(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//ul[@class='slds-tabs_scoped__nav']/li/a[text()='Route Details']",
                   f"Route / Rate Details [{index}]")
        self.click().set_locator(locator, self._name).single_click()
        return

    def click_disclaimers_tab(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//ul[@class='slds-tabs_scoped__nav']/li/a[text()='Disclaimers']",
                   f"Route / Rate Details [{index}]")
        self.click().set_locator(locator, self._name).single_click()
        return

    def get_table_rate_details_item(self, index, row):
        locator = (
        By.XPATH, f"{self._xpath_route_container}[{index}]//div[@id='rate-details']//table/tbody/tr[{row}]/td[2]",
        f"Rate Details Table Row Item [{row}] Index: [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_rate_details_quantity(self, index, row):
        locator = (
        By.XPATH, f"{self._xpath_route_container}[{index}]//div[@id='rate-details']//table/tbody/tr[{row}]/td[4]",
        f"Rate Details Table Row Quantity[{row}] Index: [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_rate_details_rates_amount(self, index, row):
        locator = (
        By.XPATH, f"{self._xpath_route_container}[{index}]//div[@id='rate-details']//table/tbody/tr[{row}]/td[5]",
        f"Rate Details Table Row Quantity[{row}] Index: [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_route_details_origin(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@id='route-details']//div[contains(@class,'route-vert-path')]/div[1]/span/..",
                   f"Route Details: Origin [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_route_details_destination(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@id='route-details']//div[contains(@class,'route-vert-path')]/div[2]/span[2]/..",
                   f"Route Details: Destination [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_route_details_vessel_name(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@id='route-details']//div[contains(@class,'route-det-vessel-voyage')]/div/div[1]/span",
                   f"Route Details: Vessel Name [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_route_details_voyage_number(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@id='route-details']//div[contains(@class,'route-det-vessel-voyage')]/div/div[2]/span",
                   f"Route Details: Voyage Number [{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_route_details_port_cut_off_notes(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@id='route-details']//div[contains(@class,'cut-off-notes')]//ul/li",
                   f"Route Details: Port Cut Off Notes [{index}]")
        return self.element().set_locator(locator, self._name).get_list_text()

    def get_route_details_disclaimers(self, index):
        locator = (By.XPATH,
                   f"{self._xpath_route_container}[{index}]//div[@id='clauses']//ul[contains(@class,'route-terms-conditions')]",
                   f"Disclaimer: Disclaimers [{index}]")
        return self.element().set_locator(locator, self._name).get_list_text()

    def get_route_item_information(self, index=1):

        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]", "Item Selected")

        # Scroll to Item
        self.scroll().set_locator(locator).to_element(pixels=-100)
        self.highlight_element().set_locator(locator).highlight_element()

        # Read Values
        est_sail_date = self.get_est_sail_date(index) or "-"
        est_arrival_date = self.get_est_arrival_date(index) or "-"
        est_cargo_availability = self.get_est_cargo_availability(index) or "-"
        transit_time = self.get_transit_time(index) or "-"
        vessel_name = self.get_vessel_name(index) or "-"
        voyage_number = self.get_voyage_number(index) or "-"
        origin_terminal = self.get_origin_terminal(index) or "-"
        origin_city_state = self.get_origin_city_state(index) or "-"
        destination_terminal = self.get_destination_terminal(index) or "-"
        destination_city_state = self.get_destination_city_state(index) or "-"
        route_price_amount = self.get_route_price_amount(index) or "-"

        headers = [
            "Est. Sail Date",
            "Est. Arrival Date",
            "Est. Cargo Availability",
            "Transit Time",
            "Vessel Name",
            "Voyage Number",
            "Origin Terminal",
            "Origin City / State",
            "Destination Terminal",
            "Destination City / State",
            "Route Price Amount"
        ]

        values = [
            est_sail_date,
            est_arrival_date,
            est_cargo_availability,
            transit_time,
            vessel_name,
            voyage_number,
            origin_terminal,
            origin_city_state,
            destination_terminal,
            destination_city_state,
            route_price_amount
        ]

        # Create Dictionary
        routes_info_dict = dict(zip(headers, values))

        # Create Table
        TableFormatter().set_headers(headers).set_data([values]).to_grid()

        return routes_info_dict

    def select_route_item_information(self, index=1):
        locator = (By.XPATH, f"{self._xpath_route_container}[{index}]//label[contains(@class,'checkbox__label')]",
                   f"Select Item Route [{index}]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def get_select_route_item_information(self, index=1):
        locator = (
        By.XPATH, f"{self._xpath_route_container}[{index}]//label[contains(@class,'checkbox__label')]/..//input",
        f"Select Item Route [{index}]")
        return self.checkbox().set_locator(locator).is_selected()
