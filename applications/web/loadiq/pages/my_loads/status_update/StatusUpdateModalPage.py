import allure


from selenium.webdriver.common.by import By

from applications.web.loadiq.components.DataPickerComponent import DataPickerComponent
from applications.web.loadiq.pages.my_loads.status_update.CheckCallModalPage import CheckCallModalPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('BidParametersPage')


class StatusUpdateModalPage(BasePage):

    @allure.step("{step_name}")
    def take_screenshot(self, step_name: str):
        """Helper method to take screenshots with Allure"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"Screenshot - {step_name}",
            attachment_type=allure.attachment_type.PNG
        )

    def __init__(self, driver):
        """
        Initialize the Status Update instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/list"
        # Locator definitions
        self._lbl_title = (By.XPATH, "//h4[@class='mb-0']", "Status Update [Title]")
        self._tbl_status_update = (By.XPATH, "//table[@class='table iq-tbl mb-0']", "Status Update [Table]")
        self._btn_update = (By.XPATH, "//button[@type='submit']", "Update [Button]")
        self._btn_add_check_call = (By.XPATH, "//button/span[contains(text(), 'Add Check Call')]", "Add Check Call [Button]")
        self._btn_close = (By.XPATH, "//button[@aria-label='Close dialog']", "Close [Button]")
        self._row_stop = (By.XPATH, "//tr[@ng-reflect-name='{row_index}']", "Row Line[Row Table]")
        self._error_message = (By.XPATH, "//span[@class='text-danger' and contains(text(),'Error')]", "Error Message Modal Message")

        # Scheduled Date Locators
        self._cell_scheduled_arrival = (By.XPATH, "//tr[@ng-reflect-name='{row_index}']//td[3]", "Scheduled Arrival [Cell]")
        self._cell_scheduled_departure = (By.XPATH, "//tr[@ng-reflect-name='{row_index}']//td[4]", "Scheduled Departure [Cell]")

        self._btn_clear = (By.XPATH, "//div[contains(@class,'shown')]//button[text()=' Clear ']", "Clear [Button]")

        # Check Call Modal Page
        self.check_call = CheckCallModalPage.get_instance()

        # Data Picker Component
        self.data_picker = DataPickerComponent.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = StatusUpdateModalPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def get_modal_title_text(self):
        return self.get_text().set_locator(self._lbl_title, self._name).by_text()

    def get_error_validation_message(self):
        self.element().is_present(self._error_message, timeout=5)
        self.screenshot().attach_to_allure(name="Error Validation for Invalid Date")
        return self.get_text().set_locator(self._error_message, self._name).by_text()

    def click_update_button(self):
        self.click().set_locator(self._btn_update, self._name).single_click()
        return self

    def get_update_button_enabled(self):
        locator = (By.XPATH, "//button[@type='submit']", "Button Update Enabled or Disabled")
        return self.element().get_element(locator, 5).is_enabled()

    def click_add_check_call_button(self):
        self.click().set_locator(self._btn_add_check_call, self._name).single_click()
        return self

    def is_add_check_call_enabled(self):
        return self.element().is_enabled_js(locator=self._btn_add_check_call, timeout=5, debug=True)

    def click_close_button(self):
        self.click().set_locator(self._btn_close, self._name).single_click()
        return self

    def click_datetimepicker_icon_actual_arrival(self, row_index: int):
        locator = (By.XPATH,
                   f"//td[@class= 'iq-tbl-header' and normalize-space(.)='{row_index}']/ancestor::tr//input[@formcontrolname='actualArrival']/following-sibling::button[contains(@class, 'new-calendericon')]",
                   f"Datetimepicker Actual Arrival [Icon]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_datetimepicker_icon_actual_departure(self, row_index: int):
        locator = (By.XPATH,
                   f"//td[@class= 'iq-tbl-header' and normalize-space(.)='{row_index}']/ancestor::tr//input[@formcontrolname='actualDeparture']/following-sibling::button[contains(@class, 'new-calendericon')]",
                   f"Datetimepicker Actual Arrival [Icon]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def select_datetime_and_apply(self, days_offset: int, hour: int, minute: int = 0):
        """
        Combines date selection, time selection, and apply button click into one method.

        :param days_offset: Number of days to add or subtract from today.
                           Negative values go to past dates, positive to future dates.
        :param hour: Hour to select (0-23 format, 24-hour time)
        :param minute: Minute to select (0-59), default is 0

        Example:
            select_datetime_and_apply(days_offset=-7, hour=14, minute=30)  # 7 days ago at 14:30
            select_datetime_and_apply(days_offset=0, hour=9, minute=0)     # Today at 09:00
        """
        self.data_picker.select_date_in_datetimepicker(days_offset)
        self.data_picker.select_time_in_datetimepicker(hour, minute)
        self.data_picker.click_apply_button()
        logger.info(f"Selected datetime (offset: {days_offset} days, time: {hour:02d}:{minute:02d}) and clicked Apply")
        return self

    def click_clear_button(self):
        """
        Clicks the Clear button in the datetimepicker to clear the selection.
        """
        self.click().set_locator(self._btn_clear, self._name).single_click()
        logger.info("Clicked Clear button in datetimepicker")
        return self

    def select_reason_code(self, row_index: int, reason_code: str):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Arrival')]/../../../tbody/tr[{row_index}]/td[7]//mat-select[@formcontrolname='reasoncode']/div", "Reason Code by Row Index [Select]")
        self.click().set_locator(locator, self._name).highlight().single_click()
        option_locator = (By.XPATH, f"//mat-option//span[contains(text(), '{reason_code}')]", f"Reason Code Option [{reason_code}]")
        self.element().is_present(locator=option_locator, timeout=3)
        self.click().set_locator(option_locator, self._name).single_click()
        self.screenshot().attach_to_allure(name=f"Selected Reason Code {reason_code}, Row Index {row_index}")
        self.scroll().to_top()
        return self

    def get_reason_code(self, row_index: int):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Arrival')]/../../../tbody/tr[{row_index}]/td[7]//span[@class='mat-mdc-select-min-line']", f"Get Reason Code Selected Row Index [{row_index}]")
        return self.get_text().set_locator(locator).by_text()

    def is_title_visible(self):
        return self.element().set_locator(self._lbl_title, self._name).is_visible()

    def is_modal_displayed(self):
        return self.is_title_visible()

    def verify_all_elements(self):
        """
        Verifies that all mapped elements in the modal are visible.
        """
        locators_to_verify = [
            self._lbl_title,
            self._tbl_status_update,
            self._btn_update,
            self._btn_add_check_call,
            self._btn_close,
            self._btn_clear
        ]

        missing = self.verify_locators().verify_page_locators(locators_to_verify)
        assert not missing, f"The following elements are missing from the Status Update Modal: {missing}"

    def verify_all_schedule_fields(self, num_rows: int = 2):
        """
        Verifies that 'Actual Arrival' and 'Actual Departure' fields are present
        for the first 'num_rows' rows in the schedule table.

        Each row is expected to have:
          - 'Actual Arrival' in column 5
          - 'Actual Departure' in column 6

        Args:
            num_rows (int): Number of rows to verify (default: 2).
        """
        locators_to_verify = [
            self._lbl_title,
            self._tbl_status_update,
            self._btn_update,
            self._btn_add_check_call,
            self._btn_close
        ]

        # Generate locators for each row (1-based indexing)
        for row_index in range(1, num_rows + 1):
            # Add locator for 'Actual Arrival' (column 5)
            locators_to_verify.append(
                self.get_schedule_field_present(
                    row_index=row_index,
                    col_index=5,
                    field=f"Row {row_index}: Actual Arrival"
                )
            )
            # Add locator for 'Actual Departure' (column 6)
            locators_to_verify.append(
                self.get_schedule_field_present(
                    row_index=row_index,
                    col_index=6,
                    field=f"Row {row_index}: Actual Departure"
                )
            )

        # Verify all generated locators are present on the page
        missing = self.verify_locators().verify_page_locators(locators_to_verify)

        # Assert that no elements are missing; fail with a clear message if any are
        assert not missing, f"The following elements are missing from the Status Update Modal: {missing}"

        return self

    def enter_container_number(self, text: str):
        locator = (By.XPATH, "//label[text()='Container Number']/..//input", "Container Number [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def click_checkbox_bobtail(self):
        locator = (By.XPATH, "//label[text()=' Bobtail (No container attached) ']", "Bobtail [Checkbox]")
        self.element().is_present(locator, 5)
        self.click().set_locator(locator).single_click()
        return self

    def click_submit(self):
        locator = (By.XPATH, "//button[contains(text(),'Submit')]", "Submit [Button]")
        self.click().set_locator(locator).single_click().pause(1)
        return self

    def get_scheduled_arrival_text(self, row_index: int = 1):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Arrival')]/../../../tbody/tr[{row_index}]/td[3]", f"Scheduled Arrival [{row_index}][Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_scheduled_actual_arrival_text(self, row_index: int = 1):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Arrival')]/../../../tbody/tr[{row_index}]/td[5]", f"Scheduled Arrival [{row_index}][Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_scheduled_arrival_enabled(self, row_index: int = 1):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Arrival')]/../../../tbody/tr[{row_index}]/td[5]//input", f"Scheduled Arrival [{row_index}][Cell]")
        return self.element().get_element(locator=locator, timeout=3).is_enabled()
        # return self.element().set_locator(locator).is_enabled()

    def get_schedule_field_present(self, row_index: int = 1, col_index: int = 1, field: str = ""):
        locator = (By.XPATH, f"//th[contains(text(),'Stop')]/../../../tbody/tr[{row_index}]/td[{col_index}]//input", f"{field} ")
        self.element().is_present(locator=locator, timeout=5)
        return locator

    def get_actual_arrival_checkmark(self, row_index: int = 1, col_index: int = 5):

        locator = (By.XPATH, f"//th[contains(text(),'Actual Arrival')]/../../../tbody/tr[{row_index}]/td[{col_index}]//div[contains(@class,'datepickerDiv')]/button[2]")

        button = self.element().get_element(locator=locator, timeout=30)
        style = button.get_attribute("style")

        if "pointer-events: none" in (style or ""):
            return True
        else:
            return False

    def get_scheduled_departure_text(self, row_index: int = 1):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Departure')]/../../../tbody/tr[{row_index}]/td[4]", f"Scheduled Departure [{row_index}][Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_scheduled_actual_departure_text(self, row_index: int = 1):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Departure')]/../../../tbody/tr[{row_index}]/td[6]", f"Scheduled Departure [{row_index}][Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_scheduled_departure_enabled(self, row_index: int = 1):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Departure')]/../../../tbody/tr[{row_index}]/td[6]//input", f"Scheduled Departure [{row_index}][Cell]")
        return self.element().get_element(locator=locator, timeout=3).is_enabled()
        # return self.element().set_locator(locator).is_enabled()

    # Get the message alert text after status update
    def get_status_update_message(self, index: int = 1):
        locator = (By.XPATH, f"(//div[@matsnackbarlabel])[{index}]", f"Getting Alert Message [{index}][Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def update_actual_arrival(self, row_index=0, days_offset: int = 0, hour: int = 0, minute: int = 0):
        self.enter_actual_arrival(row_index, days_offset, hour, minute)
        self.click_update_button()
        return self

    def enter_actual_arrival(self, row_index=0, days_offset: int = 0, hour: int = 0, minute: int = 0):
        self.click_datetimepicker_icon_actual_arrival(row_index)
        self.select_datetime_and_apply(days_offset, hour, minute)
        self.take_screenshot("Select date and time for Actual Arrival")
        return self

    def enter_actual_arrival_with_text(self, row_index: int = 0, text: str = "", clear=False):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Departure')]/../../../tbody/tr[{row_index}]/td[5]//input", "Enter Actual Arrival [Input Field]")
        if clear:
            self.send_keys().set_locator(locator).highlight().clear()
        else:
            self.send_keys().set_locator(locator).highlight().set_text(text)
        return self

    def enter_actual_departure_with_text(self, row_index: int = 0, text: str = "", clear=False):
        locator = (By.XPATH, f"//th[contains(text(),'Scheduled Departure')]/../../../tbody/tr[{row_index}]/td[6]//input", "Enter Actual Arrival [Input Field]")
        if clear:
            self.send_keys().set_locator(locator).highlight().clear()
        else:
            self.send_keys().set_locator(locator).highlight().set_text(text)
        return self

    def update_actual_departure(self, row_index=0, days_offset: int = 0, hour: int = 0, minute: int = 0):
        self.enter_actual_departure(row_index, days_offset, hour, minute)
        self.click_update_button()
        return self

    def enter_actual_departure(self, row_index=0, days_offset: int = 0, hour: int = 0, minute: int = 0):
        self.click_datetimepicker_icon_actual_departure(row_index)
        self.select_datetime_and_apply(days_offset, hour, minute)
        self.take_screenshot("Select date and time for Actual Departure")
        return self

    def is_not_visible_modal_status(self):
        locator = (By.XPATH, "//div[@id='shipment-status-update-dialog']", "Modal is not visible")
        return self.element().is_not_visible(locator=locator, timeout=30)

    def is_visible_modal_status(self):
        locator = (By.XPATH, "//div[@id='shipment-status-update-dialog']", "Modal is not visible")
        return self.element().is_present(locator=locator, timeout=5)
