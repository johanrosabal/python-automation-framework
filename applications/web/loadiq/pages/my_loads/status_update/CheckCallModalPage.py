from selenium.webdriver.common.by import By
from applications.web.loadiq.components.DataPickerComponent import DataPickerComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CheckCallModalPage')


class CheckCallModalPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the CheckCallModalPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._modal = "//div[contains(@id,'shipment-status-update-dialog')]//h4[text()='Check Call']/../../.."
        # Data Picker Component
        self.data_picker = DataPickerComponent.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def is_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Check Call Modal Visible")
        return self.element().is_present(locator=locator, timeout=5)

    def is_not_visible(self):
        locator = (By.XPATH, f"{self._modal}", "Check Call Modal Not Visible")
        return self.element().is_not_visible(locator=locator, timeout=5)

    def enter_location(self, text: str = None):
        locator = (By.XPATH, f"{self._modal}//input", "Enter Location [Input Box]")
        self.send_keys().set_locator(locator=locator).set_text(text)

        if text is not "":
            button = (By.XPATH, f"//ngb-typeahead-window//button//span[text()='{text}']/../..", "Click Option Button")
            self.element().is_present(locator=button, timeout=5)
            self.click().set_locator(locator=button).highlight().single_click()

        return self

    def get_error_location(self):
        locator = (By.XPATH, f"{self._modal}//label[text()='Location']/../..//span[@class='margin-top-error']", "Location Error Message")
        return self.get_text().set_locator(locator).by_text()

    def enter_date_time(self, days_offset: int, hour: int, minute: int, date_text: str = None):
        self.click_calendar_icon()

        if date_text is not None:
            self.data_picker.enter_date_time_text(date_text)
        else:
            self.data_picker.select_date_in_datetimepicker(days_offset=days_offset)
            self.data_picker.select_time_in_datetimepicker(hour=hour, minute=minute)

        return self

    def get_error_date_time(self):
        locator = (By.XPATH, f"{self._modal}//label[text()='Date/Time']/../../div/div/div/div[2]//span", "Location Error Message")
        return self.get_text().set_locator(locator).by_text()

    def enter_comments(self, text: str):
        locator = (By.XPATH, f"{self._modal}//label[text()='Comments']/..//textarea", "Enter Location [Input Box]")
        self.send_keys().set_locator(locator=locator).set_text(text)
        return self

    def click_update(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()=' Update']", "Click Update Button")
        self.click().set_locator(locator=locator).single_click()
        return self

    def click_apply(self):
        self.data_picker.click_apply_button()
        return self

    def click_cancel(self):
        locator = (By.XPATH, f"{self._modal}//button/span[text()=' Cancel']", "Click Cancel Button")
        self.click().set_locator(locator=locator).single_click()
        return self

    def fill_check_call(self, location, days_offset, hour, minute, comments, date_text):
        self.enter_location(location)
        self.enter_date_time(days_offset=days_offset, hour=hour, minute=minute, date_text=date_text)
        self.enter_comments(comments).screenshot().attach_to_allure(name="Complete Check Call Modal")

        return self

    def click_calendar_icon(self):
        locator = (By.XPATH, f"{self._modal}//button[contains(@class, 'new-calendericon')]", "Click Calendar Icon [Button]")
        self.click().set_locator(locator=locator).single_click()
        return self

    def click_calendar_close_icon(self):
        locator = (By.XPATH, f"{self._modal}//button[contains(@class, 'new-calendercross')]", "Click Calendar Close Icon [Button]")
        self.click().set_locator(locator=locator).single_click()
        return self
