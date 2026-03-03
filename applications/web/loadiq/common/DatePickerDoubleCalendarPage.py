import allure
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from applications.web.loadiq.common.LoadIQPage import LoadIQPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('DatePickerDoubleCalendarPage')


class DatePickerDoubleCalendarPage(LoadIQPage):
    def __init__(self, driver):
        """
        Initialize the DatePickerDoubleCalendarPage instance.
        """
        super().__init__(driver)
        self._driver = driver
        self._name = self.__class__.__name__

        # Locator definitions
        self._modal = (By.CSS_SELECTOR, '.md-drppicker.shown', "Date Picker Modal [Visible]")
        self._left_calendar = (By.CSS_SELECTOR, '.calendar.left', "Left Calendar [Container]")
        self._right_calendar = (By.CSS_SELECTOR, '.calendar.right', "Right Calendar [Container]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = DatePickerDoubleCalendarPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def wait_for_modal_to_be_visible(self, timeout=15):
        """Wait for the date picker modal to become visible"""
        self.element().wait(self._modal, timeout=timeout)
        return self

    def is_modal_visible(self):
        """Check if date picker modal is visible"""
        return self.element().is_displayed(self._modal)

    @allure.step("Select Today range")
    def select_today(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Today']", "Today [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        # Screenshot
        self.screenshot().attach_to_allure(name="Today Date Filter")
        self.pause(1)
        return self

    @allure.step("Select Next week range")
    def select_next_week(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Next week']", "Next Week [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        # Screenshot
        self.screenshot().attach_to_allure(name="Next Week Date Filter")
        self.pause(2)
        return self

    @allure.step("Select Next 10 days range")
    def select_next_10_days(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Next 10 days']", "Next 10 Days [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()

        # Screenshot
        self.screenshot().attach_to_allure(name="Next 10 Days Date Filter")
        self.pause(2)
        return self

    @allure.step("Select This Month range")
    def select_this_month(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='This Month']", "This Month [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()

        # Screenshot
        self.screenshot().attach_to_allure(name="This Month Date Filter")
        self.pause(2)
        return self

    @allure.step("Select Next Month range")
    def select_next_month(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Next Month']", "Next Month [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()

        # Screenshot
        self.screenshot().attach_to_allure(name="This Next Month Filter")
        self.pause(2)
        return self

    @allure.step("Select Before range: {date}")
    def select_before(self, date: str = None, days_off: int = None):
        """
        Select 'Before' range with a specific date or days offset.

        Args:
            date (str, optional): Date in MM/DD/YY or MM/DD/YYYY format (e.g., '12/09/25' or '12/09/2025')
            days_off (int, optional): Days offset from today (positive = future, negative = past)

        Examples:
            # Using specific date
            .select_before(date="12/31/2025")

            # Using days offset (30 days from today)
            .select_before(days_off=30)

            # Using days offset (7 days ago)
            .select_before(days_off=-7)
        """
        # 1. Select 'Before' option first
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Before']", "Before [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()

        # 2. Determine target date (either from date param or days_off)
        if days_off is not None:
            target_date = self._calculate_date_from_days_off(days_off)
            logger.info(f"Before range calculated date from offset {days_off}: {target_date}")
        elif date is not None:
            target_date = date
            logger.info(f"Before range with specific date: {target_date}")
        else:
            raise ValueError("Either 'date' or 'days_off' parameter must be provided")

        # 3. Parse target date (handle both YY and YYYY formats)
        target_month, target_day, target_year = self._parse_date(target_date)

        # 4. Navigate to the correct month in LEFT calendar
        self._navigate_calendar_to_month('left', target_month, target_year)

        # 5. Select the specific day from LEFT calendar
        self._select_day_from_calendar(str(target_day), 'left', index=1)

        return self

    @allure.step("Select Equals Date: {date}")
    def select_equals_date(self, date: str):
        """
        Select a specific date using the 'Equals' option.

        Args:
            date (str): Date in MM/DD/YY or MM/DD/YYYY format (e.g., '12/09/25' or '12/09/2025')
        """
        # 1. Select 'Equals' option first
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Equals']", "Equals [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()

        # 2. Parse target date (handle both YY and YYYY formats)
        target_month, target_day, target_year = self._parse_date(date)

        # 3. Navigate to the correct month in LEFT calendar
        self._navigate_calendar_to_month('left', target_month, target_year)

        # 4. Select the specific day from LEFT calendar
        self._select_day_from_calendar(str(target_day), 'left', index=1)
        # 5. CLick Apply
        self.apply_selection()

        return self

    @allure.step("Select After range: {date}")
    def select_after(self, date: str = None, days_off: int = None):
        """
        Select 'After' range with a specific date or days offset.

        Args:
            date (str, optional): Date in MM/DD/YY or MM/DD/YYYY format (e.g., '12/09/25' or '12/09/2025')
            days_off (int, optional): Days offset from today (positive = future, negative = past)

        Examples:
            # Using specific date
            .select_after(date="01/01/2026")

            # Using days offset (30 days from today)
            .select_after(days_off=30)

            # Using days offset (7 days ago)
            .select_after(days_off=-7)
        """
        # 1. Select 'After' option first
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='After']", "After [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()

        # 2. Determine target date (either from date param or days_off)
        if days_off is not None:
            target_date = self._calculate_date_from_days_off(days_off)
            logger.info(f"After range calculated date from offset {days_off}: {target_date}")
        elif date is not None:
            target_date = date
            logger.info(f"After range with specific date: {target_date}")
        else:
            raise ValueError("Either 'date' or 'days_off' parameter must be provided")

        # 3. Parse target date (handle both YY and YYYY formats)
        target_month, target_day, target_year = self._parse_date(target_date)

        # 4. Navigate to the correct month in LEFT calendar
        self._navigate_calendar_to_month('left', target_month, target_year)

        # 5. Select the specific day from LEFT calendar
        self._select_day_from_calendar(str(target_day), 'left', index=1)

        # 6. Apply selection
        self.apply_selection()

        return self

    @allure.step("Select Custom Range: {start_date} to {end_date}")
    def select_custom_range(self, start_date, end_date):
        """
        Select a custom date range.

        Args:
            start_date (str): Start date in MM/DD/YY or MM/DD/YYYY format (e.g., '12/25/25' or '12/25/2025')
            end_date (str): End date in MM/DD/YY or MM/DD/YYYY format (e.g., '01/10/26' or '01/10/2026')
        """
        # Click Custom Range button
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Custom range']", "Custom Range [Button]")
        self.element().is_present(locator=locator, timeout=5)
        self.pause(2)
        self.click() \
            .set_locator(locator, self._name) \
            .highlight() \
            .single_click()

        # Parse dates (handle both YY and YYYY formats)
        start_month, start_day, start_year = self._parse_date(start_date)
        end_month, end_day, end_year = self._parse_date(end_date)

        # Check if both dates are in the same month and year
        same_month = (start_month == end_month) and (start_year == end_year)

        if same_month:
            # Both dates are in the same month - use only LEFT calendar
            logger.info(f"Both dates in same month: {start_month}/{start_year}")

            # Position LEFT calendar to the target month
            self._navigate_calendar_to_month('left', start_month, start_year)

            # Select start date from LEFT calendar (index=1)
            self._select_day_from_calendar(day=str(start_day), calendar_side='left', index=1)

            # Select end date from LEFT calendar (index=2) - same month, different day
            self._select_day_from_calendar(day=str(end_day), calendar_side='left', index=1)
        else:
            # Dates are in different months - use both calendars
            logger.info(f"Dates in different months: {start_month}/{start_year} to {end_month}/{end_year}")

            # Position LEFT calendar to start_date month
            self._navigate_calendar_to_month('left', start_month, start_year)

            # Select start date from LEFT calendar (index=1)
            self._select_day_from_calendar(day=str(start_day), calendar_side='left', index=1)

            # Position RIGHT calendar to end_date month
            self._navigate_calendar_to_month('right', end_month, end_year)

            # Select end date from RIGHT calendar (index=2)
            self._select_day_from_calendar(day=str(end_day), calendar_side='right', index=2)

        start_date_ = start_date.replace("/", "_").replace("-", "_")
        end_date_ = end_date.replace("/", "_").replace("-", "_")

        self.screenshot().attach_to_allure(name=f"Custom Range Start Date {start_date_} End Date {end_date_}")

        # Apply selection
        self.apply_selection()

        return self

    @allure.step("Select Custom Range with Days Offset: Start {days_off_start} days, End {days_off_end} days")
    def select_custom_range_days_off(self, days_off_start: int, days_off_end: int):
        """
        Select a custom date range using days offset from today.

        Args:
            days_off_start (int): Days offset for start date (positive = future, negative = past)
            days_off_end (int): Days offset for end date (positive = future, negative = past)
        """
        # Calculate dates based on days offset from today
        start_date, end_date = self._calculate_dates_from_days_off(days_off_start, days_off_end)

        logger.info(f"Calculated dates from offsets: {start_date} to {end_date}")

        # Call the existing select_custom_range method with calculated dates
        return self.select_custom_range(start_date, end_date)

    # ==================== Helper Methods ====================
    @staticmethod
    def _calculate_date_from_days_off(days_off: int):
        """Calculate a single date based on days offset from today."""
        today = datetime.now()
        target_date = today + timedelta(days=days_off)
        return target_date.strftime("%m/%d/%Y")

    @staticmethod
    def _calculate_dates_from_days_off(days_off_start: int, days_off_end: int):
        """
        Calculate start and end dates based on days offset from today.

        Returns:
            tuple: (start_date_str, end_date_str) in MM/DD/YYYY format
        """
        today = datetime.now()

        start_date = today + timedelta(days=days_off_start)
        end_date = today + timedelta(days=days_off_end)

        start_date_str = start_date.strftime("%m/%d/%Y")
        end_date_str = end_date.strftime("%m/%d/%Y")

        return start_date_str, end_date_str

    def _parse_date(self, date_str: str):
        """
        Parse date string handling both YY and YYYY formats.

        Args:
            date_str (str): Date in MM/DD/YY or MM/DD/YYYY format

        Returns:
            tuple: (month, day, year) as integers
        """
        parts = date_str.split('/')
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])

        # Convert YY to YYYY (00-68 = 2000-2068, 69-99 = 1969-1999)
        if year < 100:
            if year <= 68:
                year += 2000
            else:
                year += 1900

        return month, day, year

    def _get_current_month_year(self, calendar_side: str = 'left'):
        """
        Get the current month and year displayed in the specified calendar.

        Args:
            calendar_side (str): 'left' or 'right'

        Returns:
            tuple: (month_num, year_num) - e.g., (2, 2026)
        """
        # Locator for calendar month header
        header_locator = (
            By.XPATH,
            f"//div[contains(@class,'shown')]//div[contains(@class, 'calendar {calendar_side}')]//th[@colspan='5' and contains(@class, 'month')]",
            f"{calendar_side.capitalize()} Calendar Month Header"
        )

        # Get month header text (e.g., "Feb  2026" or "Dec  2025")
        month_text = self.get_text().set_locator(header_locator, self._name).by_text().strip()

        # Parse month and year
        parts = month_text.split()
        month_name = parts[0]
        year = int(parts[1])

        # Convert month name to number
        month_num = self._month_name_to_number(month_name)

        return month_num, year

    @staticmethod
    def _month_name_to_number(month_name: str) -> int:
        """Convert month abbreviation to number"""
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
            'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
            'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        return month_map.get(month_name, 1)

    def _navigate_calendar_to_month(self, calendar_side: str, target_month: int, target_year: int):
        """
        Navigate the specified calendar to the target month and year.

        Args:
            calendar_side (str): 'left' or 'right'
            target_month (int): Target month (1-12)
            target_year (int): Target year (e.g., 2025)
        """
        max_attempts = 60  # Safety limit to prevent infinite loops
        attempts = 0

        while attempts < max_attempts:
            # Get current month/year from specified calendar
            current_month, current_year = self._get_current_month_year(calendar_side)

            # Create datetime objects for comparison
            current = datetime(current_year, current_month, 1)
            target = datetime(target_year, target_month, 1)

            # Check if we've reached the target
            if current == target:
                logger.info(f"Reached target month in {calendar_side} calendar: {target_month}/{target_year}")
                return

            # Determine navigation direction
            if target < current:
                # Target is in the past - click previous
                logger.info(
                    f"Navigating {calendar_side.upper()} back: {current_month}/{current_year} -> {target_month}/{target_year}")
                self._click_previous_month(calendar_side)
            else:
                # Target is in the future - click next
                logger.info(
                    f"Navigating {calendar_side.upper()} forward: {current_month}/{current_year} -> {target_month}/{target_year}")
                self._click_next_month(calendar_side)

            attempts += 1

        raise Exception(
            f"Failed to navigate {calendar_side} calendar to {target_month}/{target_year} after {max_attempts} attempts")

    def _click_previous_month(self, calendar_side: str = 'left'):
        """Click the previous month arrow on the specified calendar"""
        locator = (
            By.XPATH,
            f"//div[contains(@class,'shown')]//th[contains(@class, 'prev') and contains(@class, 'available')]",
            f"{calendar_side.capitalize()} Calendar Previous Month Arrow"
        )
        self.element().is_present(locator, 5)
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        # Wait for animation/transition
        self.element().wait((
            By.XPATH,
            f"//div[contains(@class,'shown')]//div[contains(@class, 'calendar {calendar_side}')]//th[@colspan='5']"
        ), timeout=3)

    def _click_next_month(self, calendar_side: str = 'right'):
        """Click the next month arrow on the specified calendar"""
        locator = (
            By.XPATH,
            f"//div[contains(@class,'shown')]//th[contains(@class, 'next') and contains(@class, 'available')]",
            f"{calendar_side.capitalize()} Calendar Next Month Arrow"
        )
        self.element().is_present(locator, 5)
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        # Wait for animation/transition
        self.element().wait((
            By.XPATH,
            f"//div[contains(@class,'shown')]//div[contains(@class, 'calendar {calendar_side}')]//th[@colspan='5']"
        ), timeout=3)

    def _select_day_from_calendar(self, day: str, calendar_side: str = 'left', index: int = 1):
        """
        Select a specific day in the specified calendar.

        Args:
            day (str): Day to select (e.g., '9', '25')
            calendar_side (str): 'left' or 'right'
            index (int): 1 for first occurrence (LEFT), 2 for second occurrence (RIGHT)
        """
        # Create locator for the day in the specified calendar
        day_locator = (
            By.XPATH,
            f"//div[contains(@class,'shown')]//div[contains(@class, 'calendar {calendar_side}')]//td[contains(@class, 'available') and not(contains(@class, 'off'))]//span[normalize-space()='{day}']/..",
            f"Day {day} in {calendar_side.capitalize()} Calendar"
        )

        # Wait for the day to be available and click it
        self.element().is_present(locator=day_locator, timeout=5)
        self.click() \
            .set_locator(day_locator, self._name) \
            .highlight() \
            .single_click()

        logger.info(f"Selected day {day} from {calendar_side} calendar (Index {index})")

    # ==================== Action Methods ====================

    @allure.step("Apply date selection")
    def apply_selection(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()='Apply']", "Apply [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        return self

    @allure.step("Clear date selection")
    def clear_selection(self):
        locator = (By.XPATH, "//div[contains(@class,'shown')]//button[text()=' Clear ']", "Clear [Button]")
        self.click() \
            .set_locator(locator, self._name) \
            .single_click()
        return self

# ========================================
# USAGE EXAMPLES
# ========================================


"""
# Example 1: Select 'Before' with specific date
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_before(date="12/31/2025")

# Example 2: Select 'Before' with days offset (30 days from today)
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_before(days_off=30)

# Example 3: Select 'After' with specific date
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_after(date="01/01/2026")

# Example 4: Select 'After' with days offset (7 days from today)
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_after(days_off=7)

# Example 5: Select 'Equals' with specific date
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_equals_date("12/09/2025")

# Example 6: Select custom range with specific dates
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_custom_range("12/01/2025", "03/31/2026")

# Example 7: Select custom range with days offset
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_custom_range_days_off(7, 30)

# Example 8: Select predefined ranges
DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_today()

DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_next_week()

DatePickerDoubleCalendarPage.get_instance() \
    .wait_for_modal_to_be_visible() \
    .select_this_month()
"""
