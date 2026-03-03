import allure
from selenium.webdriver.common.by import By
from applications.web.loadiq.common.DatePickerDoubleCalendarPage import DatePickerDoubleCalendarPage
from applications.web.loadiq.common.LoadIQPage import LoadIQPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('MyLoadsFiltersComponent')


class MyLoadsFiltersComponent(LoadIQPage):
    def __init__(self, driver):
        """
        Initialize the MyLoadsFiltersComponent instance.
        """
        super().__init__(driver)
        self._driver = driver
        self._name = self.__class__.__name__

        # Components
        self.date_picker_double_calendar = DatePickerDoubleCalendarPage.get_instance()

        # Locator definitions - ALL XPaths
        self._modal = (By.XPATH, "//div[@id='modalFilter' and contains(@class, 'show')]", "Filters Modal [Visible]")
        self._input_delivery_date = (By.XPATH, "//input[@name='pickupDaterange' and @placeholder='Select delivery date']", "Delivery Date [Input]")
        self._input_pickup_date = (By.XPATH, "//input[@name='pickupDaterange' and @placeholder='Select pickup date']", "Pickup Date [Input]")

        self._input_origin_search_by_city = (By.XPATH, "//input[@id='originCityFilter']/..", "Origin: Search By City [Radio]")
        self._input_origin_search_by_state = (By.XPATH, "//input[@id='originStateFilter']/..", "Origin: Search By State [Radio]")
        self._dropdown_origin_state = (By.XPATH, "//origin-filter//ng-multiselect-dropdown[@placeholder='Select State']", "Origin: State Dropdown")
        self._dropdown_origin_city_state = (By.XPATH, "(//origin-filter//input[@placeholder='Search City, State'])[1]", "Origin: Search Input")
        self._dropdown_origin_radius = (By.XPATH, "//origin-filter//mat-select[@placeholder='Select radius']", "Origin: Radius Select")

        self._input_destination_search_by_city = (By.XPATH, "//input[@id='destinationCityFilter']/..", "Destination: Search By City [Radio]")
        self._input_destination_search_by_state = (By.XPATH, "//input[@id='destinationStateFilter']/..", "Destination: Search By State [Radio]")
        self._dropdown_destination_state = (By.XPATH, "//destination-filter//ng-multiselect-dropdown[@placeholder='Select State']", "Destination: State Dropdown")
        self._dropdown_destination_city_state = (By.XPATH, "(//destination-filter//input[@placeholder='Search City, State'])[1]", "Destination: Search Input")
        self._dropdown_destination_radius = (By.XPATH, "//destination-filter//mat-select[@placeholder='Select radius']", "Destination: Radius Select")
        self._dropdown_status = (By.XPATH, "//status-filter//ng-multiselect-dropdown[@placeholder='Select status']", "Status Dropdown")
        self._dropdown_equipment = (By.XPATH, "//other-filter//mat-select[@placeholder='Select Equipment']", "Equipment Dropdown")
        self._btn_hazmat_yes = (By.XPATH, "//input[@id='hfilter1']/..", "Hazmat: Yes [Radio]")
        self._btn_hazmat_all = (By.XPATH, "//input[@id='hfilter2']/..", "Hazmat: All [Radio]")
        self._btn_hazmat_no = (By.XPATH, "//input[@id='hfilter3']/..", "Hazmat: No [Radio]")
        self._btn_apply_all = (By.XPATH, "//div[@class='modal-footer']//button[contains(@class, 'iq-btn--primary') and not(contains(@class, 'outline'))]", "Apply [Button]")
        self._btn_clear_all = (By.XPATH, "//div[@class='modal-footer']//button[contains(@class, 'iq-btn--primary-outline')]", "Clear All [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = MyLoadsFiltersComponent(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def wait_for_modal_to_be_visible(self, timeout=15):
        """Wait for the filters modal to become visible"""
        self.element().wait(self._modal, timeout=timeout)
        return self

    def is_modal_visible(self):
        """Check if filters modal is visible"""
        return self.element().is_present(locator=self._modal, timeout=5)

    def are_fields_filters_visible(self):
        """
        Validates that all filter fields (Origin and Destination) are visible in the modal.

        Returns:
            tuple: (bool, list)
                - bool: True if all are visible, False otherwise.
                - list: List of field names that are NOT visible (empty if all pass).
        """
        # List of locators defined in __init__ to be validated
        fields = [
            self._input_origin_search_by_city,
            self._input_origin_search_by_state,
            self._dropdown_origin_city_state,
            self._dropdown_origin_radius,
            self._input_destination_search_by_city,
            self._input_destination_search_by_state,
            self._dropdown_destination_city_state,
            self._dropdown_destination_radius,
            self._input_delivery_date,
            self._input_pickup_date,
            self._dropdown_status,
            self._dropdown_equipment,
            self._btn_hazmat_yes,
            self._btn_hazmat_no,
            self._btn_hazmat_all,
            self._btn_apply_all,
            self._btn_clear_all
        ]

        return self.element().are_fields_visible(elements_to_validate=fields, page=self._name)

    @allure.step("Set Origin search by city")
    def set_origin_search_by_city(self):
        self.click() \
            .set_locator(self._input_origin_search_by_city, self._name) \
            .highlight() \
            .single_click()
        return self

    @allure.step("Set Origin search by state")
    def set_origin_search_by_state(self):

        self.click() \
            .set_locator(self._input_origin_search_by_state, self._name) \
            .highlight() \
            .single_click()
        return self

    def select_origin_state(self, status_values: list):
        """
        Select multiple status values from the dropdown.

        Args:
            status_values (list): List of status values to select (e.g., ['Completed', 'In Transit'])
        """

        # Open dropdown
        self.click() \
            .set_locator(self._dropdown_origin_state, self._name) \
            .highlight() \
            .single_click()

        # Select each status
        for status in status_values:
            status_checkbox = (
                By.XPATH,
                f"//origin-filter//li[contains(@class, 'multiselect-item-checkbox')]//div[text()='{status}']/preceding-sibling::input/..",
                f"Status Checkbox: {status}"
            )
            self.click() \
                .set_locator(status_checkbox, self._name) \
                .highlight() \
                .single_click()

        self.screenshot().attach_to_allure(name="Origin State Options Selected")
        # Close dropdown by clicking outside
        self.click() \
            .set_locator((By.XPATH, "//body"), self._name) \
            .single_click()
        return self

    @allure.step("Enter Origin search text: {search_city_state}")
    def enter_origin_search_city_state(self, search_city_state: str):

        self.send_keys() \
            .set_locator(self._dropdown_origin_city_state, self._name) \
            .highlight() \
            .set_text(search_city_state)

        option = (By.XPATH, f"//button/div/span[contains(text(),'{search_city_state}')]", "Search By City, Name [Select Option Modal]")
        self.element().is_present(locator=option, timeout=10)
        self.click().set_locator(option).highlight().single_click()
        return self

    @allure.step("Select Origin radius: {radius_value}")
    def select_origin_radius(self, radius_value: str):
        self.click() \
            .set_locator(self._dropdown_origin_radius, self._name) \
            .highlight() \
            .single_click()

        # Click the specific radius option
        radius_option = (By.XPATH, f"//mat-option/span[normalize-space()='{radius_value}']", f"Radius Option: {radius_value}")
        self.click() \
            .set_locator(radius_option, self._name) \
            .highlight() \
            .single_click()
        return self

    @allure.step("Set Destination search by city")
    def set_destination_search_by_city(self):

        self.click() \
            .set_locator(self._input_destination_search_by_city, self._name) \
            .highlight() \
            .single_click()
        return self

    @allure.step("Set Destination search by state")
    def set_destination_search_by_state(self):

        self.click() \
            .set_locator(self._input_destination_search_by_state, self._name) \
            .highlight() \
            .single_click()
        return self

    def select_destination_state(self, status_values: list):
        """
        Select multiple status values from the dropdown.

        Args:
            status_values (list): List of status values to select (e.g., ['Completed', 'In Transit'])
        """

        # Open dropdown
        self.click() \
            .set_locator(self._dropdown_destination_state, self._name) \
            .highlight() \
            .single_click()

        # Select each status
        for status in status_values:
            status_checkbox = (
                By.XPATH,
                f"//destination-filter//li[contains(@class, 'multiselect-item-checkbox')]//div[text()='{status}']/preceding-sibling::input/..",
                f"Status Checkbox: {status}"
            )
            self.click() \
                .set_locator(status_checkbox, self._name) \
                .highlight() \
                .single_click()

        # Close dropdown by clicking outside
        self.click() \
            .set_locator((By.XPATH, "//body"), self._name) \
            .highlight() \
            .single_click()
        return self

    @allure.step("Enter Destination search text: {search_city_state}")
    def enter_destination_search_city_state(self, search_city_state: str):

        self.send_keys() \
            .set_locator(self._dropdown_destination_city_state, self._name) \
            .highlight() \
            .set_text(search_city_state)

        option = (By.XPATH, f"//button/div/span[contains(text(),'{search_city_state}')]", "Search By City, Name [Select Option Modal]")
        self.element().is_present(locator=option, timeout=10)
        self.click().set_locator(option).highlight().single_click()
        return self

    @allure.step("Select Destination radius: {radius_value}")
    def select_destination_radius(self, radius_value: str):

        self.click() \
            .set_locator(self._dropdown_destination_radius, self._name) \
            .single_click()

        radius_option = (By.XPATH, f"//mat-option/span[normalize-space()='{radius_value}']", f"Radius Option: {radius_value}")
        self.click() \
            .set_locator(radius_option, self._name) \
            .single_click()
        return self

    @allure.step("Open Pickup Date picker")
    def open_pickup_date_picker(self):
        self.scroll().set_locator(self._input_pickup_date).to_element()
        self.click() \
            .set_locator(self._input_pickup_date, self._name) \
            .single_click()
        return self

    @allure.step("Set Pickup Date: {start_date} to {end_date}")
    def set_pickup_date_range(self, start_date: str, end_date: str):
        """
        Set a pickup date range using the date picker.

        Args:
            start_date (str): Start date in MM/DD/YY format (e.g., 12/25/25)
            end_date (str): End date in MM/DD/YY format (e.g., 01/10/26)
        """
        self.open_pickup_date_picker()
        self.date_picker_double_calendar.wait_for_modal_to_be_visible().select_custom_range(start_date, end_date)
        return self

    @allure.step("Set Pickup Date: {start_date} to {end_date}")
    def set_pickup_date_range_days_off(self, start_date: int, end_date: int):
        """
        Set a pickup date range using the date picker.

        Args:
            start_date (str): Start date in MM/DD/YY format (e.g., 12/25/25)
            end_date (str): End date in MM/DD/YY format (e.g., 01/10/26)
        """
        self.open_pickup_date_picker()
        self.date_picker_double_calendar.wait_for_modal_to_be_visible().select_custom_range_days_off(start_date, end_date)
        return self

    @allure.step("Open Delivery Date picker")
    def open_delivery_date_picker(self):
        self.scroll().set_locator(self._input_delivery_date).to_element()
        self.click() \
            .set_locator(self._input_delivery_date, self._name) \
            .single_click()
        return self

    @allure.step("Set Delivery Date: {start_date} to {end_date}")
    def set_delivery_date_range(self, start_date: str, end_date: str):
        """
        Set a delivery date range using the date picker.

        Args:
            start_date (str): Start date in MM/DD/YY format (e.g., '12/25/25')
            end_date (str): End date in MM/DD/YY format (e.g., '01/10/26')
        """
        self.open_delivery_date_picker()
        self.date_picker_double_calendar.wait_for_modal_to_be_visible().select_custom_range(start_date, end_date)
        return self

    @allure.step("Set Delivery Date: {start_date} to {end_date}")
    def set_delivery_date_range_days_off(self, start_date: int, end_date: int):
        """
        Set a pickup date range using the date picker.

        Args:
            start_date (str): Start date in MM/DD/YY format (e.g., 12/25/25)
            end_date (str): End date in MM/DD/YY format (e.g., 01/10/26)
        """
        self.open_delivery_date_picker()
        self.date_picker_double_calendar.wait_for_modal_to_be_visible().select_custom_range_days_off(start_date, end_date)
        return self

    def get_delivery_date_range(self):
        self.pause(2)
        return self.get_text().set_locator(self._input_delivery_date).by_attribute("value")

    def get_pickup_date_range(self):
        self.pause(2)
        return self.get_text().set_locator(self._input_pickup_date).by_attribute("value")

    @allure.step("Select Status: {status_values_list}")
    def select_status(self, status_values_list: list):
        """
        Select multiple status values from the dropdown.

        Args:
            status_values_list (list): List of status values to select (e.g., ['Completed', 'In Transit'])
        """

        self.scroll().set_locator(locator=self._dropdown_status).to_element()
        # Open dropdown
        self.click() \
            .set_locator(self._dropdown_status, self._name) \
            .highlight() \
            .single_click()

        # Select each status
        for status in status_values_list:
            status_checkbox = (
                By.XPATH,
                f"//status-filter//li[contains(@class, 'multiselect-item-checkbox')]//div[text()='{status}']/preceding-sibling::input/..",
                f"Status Checkbox: {status}"
            )
            self.click() \
                .set_locator(status_checkbox, self._name) \
                .highlight() \
                .single_click()

        self.screenshot().attach_to_allure(name="Status Options Selected")
        # Close dropdown by clicking outside
        self.click() \
            .set_locator((By.XPATH, "//body"), self._name) \
            .single_click()
        return self

    @allure.step("Select Equipment: {equipment_value}")
    def select_equipment(self, equipment_value: str):

        self.scroll().set_locator(locator=self._dropdown_equipment).to_element()
        self.click() \
            .set_locator(self._dropdown_equipment, self._name) \
            .highlight() \
            .single_click()

        equipment_option = (
            By.XPATH,
            f'//mat-option[@role="option"]//span[contains(text(),"{equipment_value}")]',
            f"Equipment Option: {equipment_value}"
        )
        self.element().is_present(locator=equipment_option, timeout=10)
        self.click() \
            .set_locator(equipment_option, self._name) \
            .single_click()
        return self

    @allure.step("Get Equipment Options List")
    def get_equipment_options_list(self) -> list:
        """
        Opens the Equipment dropdown and returns a list of all available option texts.

        Returns:
            list: List of strings containing the equipment options (e.g., ["53' Dry Van", "Flatbed", ...])
        """
        options_list = []

        try:
            # 1. Scroll to and open the dropdown
            self.scroll().set_locator(locator=self._dropdown_equipment).to_element()
            self.click() \
                .set_locator(self._dropdown_equipment, self._name) \
                .highlight() \
                .single_click()

            # 2. Define locator for ALL options in the dropdown
            all_options_locator = (
                By.XPATH,
                "//mat-option[@role='option']//span",
                "Equipment Options [All]"
            )

            # 3. Wait for options to be visible and get the web elements
            # Note: Using self.driver.find_elements to get a list of WebElements
            options_elements = self.element().wait(locator=all_options_locator, timeout=10).find_elements(by=By.XPATH, value=all_options_locator[1])

            self.screenshot().attach_to_allure(name="Equipment Dropdown Options")

            # 4. Extract text from each element
            for element in options_elements:
                text = element.text.strip()
                if text:  # Avoid empty strings
                    options_list.append(text)

            logger.info(f"Found {len(options_list)} equipment options: {options_list}")

        except Exception as e:
            logger.error(f"Error retrieving equipment options: {e}")
            # Ensure dropdown is closed if an error occurs
            self.click().set_locator((By.XPATH, "//body"), self._name).single_click()
            raise e

        finally:
            # 5. Close the dropdown by clicking outside to leave UI in a clean state
            self.click() \
                .set_locator((By.XPATH, "//body"), self._name) \
                .single_click()

        return options_list

    @allure.step("Set Hazmat: {hazmat_option}")
    def set_hazmat(self, hazmat_option: str):
        """
        Set Hazmat filter option.

        Args:
            hazmat_option (str): 'Yes', 'All', or 'No'
        """
        # Other Filters

        self.scroll().set_locator(locator=self._btn_hazmat_yes).to_element()

        if hazmat_option.lower() == 'yes':
            locator = self._btn_hazmat_yes
        elif hazmat_option.lower() == 'no':
            locator = self._btn_hazmat_no
        else:  # 'all' or default
            locator = self._btn_hazmat_all

        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        return self

    @allure.step("Apply all filters")
    def click_apply_filters(self):

        self.scroll().set_locator(locator=self._btn_apply_all).to_element()
        self.click() \
            .set_locator(self._btn_apply_all, self._name) \
            .single_click()
        self.pause(seconds=2)
        self.screenshot().attach_to_allure(name="After Filter Applied")
        return self

    @allure.step("Clear all filters")
    def click_clear_all_filters(self):

        self.scroll().set_locator(locator=self._btn_clear_all).to_element()
        self.click() \
            .set_locator(self._btn_clear_all, self._name) \
            .single_click()
        return self


# ========================================
# USAGE EXAMPLES
# ========================================

"""
# Example 1: Set filters and apply
MyLoadsFiltersComponent.get_instance() \
    .wait_for_modal_to_be_visible() \
    .set_origin_search_by_city() \
    .enter_origin_search_city_state(search_city_state="Florida, NY") \
    .select_origin_radius(radius_value="25") \
    .set_destination_search_by_city() \
    .enter_destination_search_city_state(search_city_state="California City, CA") \
    .select_destination_radius(radius_value="25") \
    .select_status(status_values_list=["Completed", "Delivered"]) \
    .select_equipment(equipment_value="53' Dry Van") \
    .set_hazmat(hazmat_option="Yes")

# Example 2: Clear all filters
MyLoadsFiltersComponent.get_instance() \
    .wait_for_modal_to_be_visible() \
    .clear_all_filters()
"""
# ========================================
# USAGE EXAMPLES with Date Picker with 2 Calendars
# ========================================
# Example Today
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_pickup_date_picker() \
#     .date_picker_double_calendar.select_today()
#
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_delivery_date_picker() \
#     .date_picker_double_calendar.select_today()

# Example Next Week
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_pickup_date_picker() \
#     .date_picker_double_calendar.select_next_week()
#
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_delivery_date_picker() \
#     .date_picker_double_calendar.select_next_week()

# Example Next 10 Days
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_pickup_date_picker() \
#     .date_picker_double_calendar.select_next_10_days()
#
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_delivery_date_picker() \
#     .date_picker_double_calendar.select_next_10_days()

# Example This Month
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_pickup_date_picker() \
#     .date_picker_double_calendar.select_this_month()
#
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_delivery_date_picker() \
#     .date_picker_double_calendar.select_this_month()

# Example Before Date Format 00/00/0000
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_pickup_date_picker() \
#     .date_picker_double_calendar.select_before(date="02/01/2026")

# Example Before Days Off
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_delivery_date_picker() \
#     .date_picker_double_calendar.select_before(days_off=-1)

# Example Equals
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .open_pickup_date_picker() \
#     .date_picker_double_calendar \
#     .select_equals_date(date="01/01/2026")

# Example Custom Range with Date
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .set_pickup_date_range(start_date="01/29/2026", end_date="04/01/2026") \
#     .set_delivery_date_range(start_date="01/29/2026", end_date="04/01/2026")

# Example Custom Range with Days Off
# self.my_loads_filters \
#     .wait_for_modal_to_be_visible() \
#     .set_pickup_date_range_days_off(start_date=-72, end_date=0) \
#     .set_delivery_date_range_days_off(start_date=-72, end_date=0)
