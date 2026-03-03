import time
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('DataPickerComponent')


class DataPickerComponent(BasePage):

    def __init__(self, driver):
        """
        Initialize the DataPickerComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Locator definitions

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def select_date_in_datetimepicker(self, days_offset: int, index:int = 1):
        """
        Selects a date in the opened datetimepicker based on days offset from today.

        :param days_offset: Number of days to add or subtract from today.
                           Negative values go to past dates, positive to future dates.
                           Example: -7 selects 7 days ago, +7 selects 7 days from now

        """

        # Calculate the target date
        target_date = datetime.now() + timedelta(days=days_offset)
        target_day = target_date.day
        target_month = target_date.month
        target_year = target_date.year

        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        # Calculate how many months to navigate
        months_to_navigate = (target_year - current_year) * 12 + (target_month - current_month)

        # Selector for navigation buttons (ngx-daterangepicker specific)
        next_button_selector = f"(//div[contains(@class, 'shown')]//th[@class='next available'])"
        prev_button_selector = f"(//div[contains(@class, 'shown')]//th[@class='prev available'])"

        # Navigate to the correct month
        if months_to_navigate > 0:
            # Navigate forward (next months)
            for _ in range(months_to_navigate):
                next_button_locator = (By.XPATH, next_button_selector, "Next Month [Button]")
                self.click().set_locator(next_button_locator, self._name).single_click()
                time.sleep(0.3)
        elif months_to_navigate < 0:
            # Navigate backward (previous months)
            for _ in range(abs(months_to_navigate)):
                prev_button_locator = (By.XPATH, prev_button_selector, "Previous Month [Button]")
                self.click().set_locator(prev_button_locator, self._name).single_click()
                time.sleep(0.3)

        # Click on the target day (ngx-daterangepicker has td.available with span inside)
        # The day is in a span inside td, and we need to exclude 'off' class for days from other months
        # We click on the td element (not the span) to avoid click interception
        day_selector = f"(//div[contains(@class, 'shown')]//td[contains(@class, 'available') and not(contains(@class, 'off'))]/span[text()='{target_day}'])[{index}]"

        day_locator = (By.XPATH, day_selector, f"Day {target_day} [Button]")
        self.click().set_locator(day_locator, self._name).javascript_click()
        logger.info(f"Selected date: {target_month}/{target_day}/{target_year} (offset: {days_offset} days)")

        return self

    def enter_date_time_text(self, text: str = None):
        locator = (By.XPATH, f"//input[@placeholder='Date']", "Enter Date [Input Box]")
        self.send_keys().set_locator(locator=locator).clear().set_text_by_character(text)
        return self

    def select_time_in_datetimepicker(self, hour: int, minute: int = 0):
        """
        Selects a time in the opened datetimepicker.

        :param hour: Hour to select (0-23 format, 24-hour time)
        :param minute: Minute to select (0-59), default is 0

        Example:
            select_time_in_datetimepicker(14, 30)  # Selects 14:30 (2:30 PM)
            select_time_in_datetimepicker(9, 0)    # Selects 09:00 (9:00 AM)
        """
        # Validate input
        if not (0 <= hour <= 23):
            raise ValueError(f"Hour must be between 0 and 23, got {hour}")
        if not (0 <= minute <= 59):
            raise ValueError(f"Minute must be between 0 and 59, got {minute}")

        # Select hour using dropdown
        hour_select_locator = (By.XPATH,
                               f"(//div[contains(@class, 'shown')]//div[@class='calendar-time']//select[contains(@class, 'hourselect')])",
                               "Hour [Select]")
        self.scroll().set_locator(locator=hour_select_locator).to_element(pixels=-100)
        self.dropdown().set_locator(hour_select_locator, self._name).by_value(str(hour))

        # Select minute using dropdown
        minute_select_locator = (By.XPATH,
                                 f"(//div[contains(@class, 'shown')]//div[@class='calendar-time']//select[contains(@class, 'minuteselect')])",
                                 "Minute [Select]")
        self.dropdown().set_locator(minute_select_locator, self._name).by_value(str(minute))

        logger.info(f"Selected time: {hour:02d}:{minute:02d}")

        return self

    def click_apply_button(self):
        """
        Clicks the Apply button in the datetimepicker to confirm the selection.
        """
        btn_apply = (By.XPATH, f"(//div[contains(@class, 'shown')]//button[text()='Apply'])", "Apply [Button]")
        self.click().set_locator(btn_apply, self._name).single_click()
        logger.info("Clicked Apply button in datetimepicker")
        return self
