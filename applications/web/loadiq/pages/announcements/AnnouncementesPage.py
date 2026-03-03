import allure
from selenium.webdriver.common.by import By

from applications.web.loadiq.common.DateUtils import DateUtils
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage


logger = setup_logger('AnnouncementsPage')


class AnnouncementsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the MyLoadsPage instance.
        """
        super().__init__(driver)
        # Driver

        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/announcement-manage"

        # Locator definitions
        self.table_announcements_column_start_date = (By.XPATH, "//th//a[contains(text(), 'Start Date')]")
        self.table_announcements_column_type = (By.XPATH, "//th//a[contains(text(), 'Type')]")
        self.table_announcements_column_end_date = (By.XPATH, "//th//a[contains(text(), 'End Date')]")
        self.table_announcements_column_message = (By.XPATH, "//th//a[contains(text(), 'Message')]")
        self.table_announcements_column_status = (By.XPATH, "//th//a[contains(text(), 'Status')]")
        self.table_announcements_column_action = (By.XPATH, "//th//a[contains(text(), 'Action')]")

        self.table_announcements_data_start_date = (By.XPATH, "//td[count(//th[contains(normalize-space(.), 'Start Date')]/preceding-sibling::th)+1]")
        self.table_announcements_data_end_date = (By.XPATH, "//td[count(//th[contains(normalize-space(.), 'End Date')]/preceding-sibling::th)+1]")

        self.button_add_announcements = (By.XPATH, "//span[contains(text(), 'Add Announcement')]")
        #Add Announcement Window
        self.window_add_announcements_title = (By.XPATH, "//h4[contains(text(), 'Add Announcement')]")
        self.window_add_announcements_label_type = (By.XPATH, "//label[contains(text(),'Announcement Type')]")
        self.window_add_announcements_dropdown_type = (By.XPATH, "//span[contains(text(), 'Select Type')]")
        self.window_add_announcements_dropdown_option = "//span[contains(text(), '{option}') and contains(@class,'list-item')]"
        self.window_add_announcements_label_message = (By.XPATH, "//label[contains(text(), 'Message')]")
        self.window_add_announcements_txt_message = (By.XPATH, "//textarea[contains(@placeholder, 'Content')]")
        self.window_add_announcements_label_start_date = (By.XPATH, "//label[contains(text(), 'Start Date/Time')]")
        self.window_add_announcements_label_end_date = (By.XPATH, "//label[contains(text(), 'End Date/Time')]")
        self.window_add_announcements_input_start_date = (By.XPATH,"//label[contains(text(), 'Start Date/Time')]/following-sibling::div//input")
        self.window_add_announcements_input_end_date = (By.XPATH,"//label[contains(text(), 'End Date/Time')]/following-sibling::div//input")
        self.window_add_announcements_date_picker_start_date = (By.XPATH,"//label[contains(text(), 'Start Date/Time')]/following-sibling::div//button")
        self.window_add_announcements_date_picker_end_date = (By.XPATH,"//label[contains(text(), 'End Date/Time')]/following-sibling::div//button")
        self.window_add_announcements_date_picker_start_date_selected = (By.XPATH, "//td[contains(@class, 'active') and contains(@class, 'available') and (contains(@class, 'today'))]")
        self.window_add_announcements_date_picker_end_date_selected = (By.XPATH, "//td[contains(@class, 'active') and contains(@class, 'available') and not(contains(@class, 'today'))]")
        self.window_add_announcements_button_create = (By.XPATH, "//button/span[contains(text(), 'Create')]")
        self.window_add_announcements_button_cancel = (By.XPATH, "//button[@type='button']/span[contains(text(), 'Cancel')]")
        self.message_announcement_added_successfully = (By.XPATH, "//div[contains(text(), 'Announcement saved sucessfully!')]")
        self.window_add_announcements_start_date_error_message = (By.XPATH, "//label[contains(text(), 'Start Date/Time')]/following-sibling::div//span[contains(text(),'Selected end date/time should be greater than start date/time.')]")
        self.window_add_announcements_end_date_error_message = (By.XPATH, "//label[contains(text(), 'End Date/Time')]/following-sibling::div//span[contains(text(),'Selected end date/time should be greater than start date/time.')]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = AnnouncementsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    @allure.step("Check Announcements Table Columns")
    def check_announcements_table_columns(self):
        self.element().set_locator(self.table_announcements_column_start_date, self._name)
        self.element().is_present(self.table_announcements_column_start_date)

        self.element().set_locator(self.table_announcements_column_type, self._name)
        self.element().is_present(self.table_announcements_column_type)

        self.element().set_locator(self.table_announcements_column_end_date, self._name)
        self.element().is_present(self.table_announcements_column_end_date)

        self.element().set_locator(self.table_announcements_column_message, self._name)
        self.element().is_present(self.table_announcements_column_message)

        self.element().set_locator(self.table_announcements_column_status, self._name)
        self.element().is_present(self.table_announcements_column_status)

        self.element().set_locator(self.table_announcements_column_action, self._name)
        self.element().is_present(self.table_announcements_column_action)
        return self

    @allure.step("Check start date end date formats")
    def check_start_date_end_date_formats(self):
        start_date = self.get_text().set_locator(self.table_announcements_data_start_date, self._name).by_text()
        start_date = start_date.rsplit(" ", 1)[0]
        assert (DateUtils.validate_date_time_format(start_date) == True)

        end_date = self.get_text().set_locator(self.table_announcements_data_end_date, self._name).by_text()
        end_date = end_date.rsplit(" ", 1)[0]
        assert (DateUtils.validate_date_time_format(end_date) == True)

    @allure.step("Check Add Announcements Window")
    def check_add_announcements_window(self):
        self.element().set_locator(self.window_add_announcements_title, self._name)
        self.element().is_present(self.window_add_announcements_title)

        self.element().set_locator(self.window_add_announcements_label_type, self._name)
        self.element().is_present(self.window_add_announcements_label_type)

        self.element().set_locator(self.window_add_announcements_dropdown_type, self._name)
        self.element().is_present(self.window_add_announcements_dropdown_type)

        self.click().set_locator(self.window_add_announcements_dropdown_type, self._name).single_click()

        locator_option_informative =  (By.XPATH, self.window_add_announcements_dropdown_option.format(option="Informative"))
        self.element().set_locator(locator_option_informative, self._name)
        self.element().is_present(locator_option_informative)

        locator_option_system =  (By.XPATH, self.window_add_announcements_dropdown_option.format(option="System"))
        self.element().set_locator(locator_option_system, self._name)
        self.element().is_present(locator_option_system)

        self.click().set_locator(self.window_add_announcements_dropdown_type, self._name).single_click()

        self.element().set_locator(self.window_add_announcements_label_message, self._name)
        self.element().is_present(self.window_add_announcements_label_message)

        self.element().set_locator(self.window_add_announcements_txt_message, self._name)
        self.element().is_present(self.window_add_announcements_txt_message)

        self.element().set_locator(self.window_add_announcements_label_start_date, self._name)
        self.element().is_present(self.window_add_announcements_label_start_date)

        self.element().set_locator(self.window_add_announcements_input_start_date, self._name)
        self.element().is_present(self.window_add_announcements_input_start_date)

        self.element().set_locator(self.window_add_announcements_label_end_date, self._name)
        self.element().is_present(self.window_add_announcements_label_end_date)

        self.element().set_locator(self.window_add_announcements_input_end_date, self._name)
        self.element().is_present(self.window_add_announcements_input_end_date)

        self.element().set_locator(self.window_add_announcements_button_create, self._name)
        self.element().is_present(self.window_add_announcements_button_create)

        self.element().set_locator(self.window_add_announcements_button_cancel, self._name)
        self.element().is_present(self.window_add_announcements_button_cancel)

        return self


    @allure.step("Click Add Announcements Button")
    def click_add_announcements_button(self):
        self.click().set_locator(self.button_add_announcements).single_click()
        return self

    @allure.step("Add Announcements Select Type")
    def add_announcements_select_type(self, option):
        self.click().set_locator(self.window_add_announcements_dropdown_type).single_click()

        locator = (By.XPATH, self.window_add_announcements_dropdown_option.format(option=option))
        self.click().set_locator(locator).single_click().pause(3)
        return self

    @allure.step("Add Announcements Enter Message")
    def add_announcements_enter_message(self, message):
        self.send_keys().set_locator(self.window_add_announcements_txt_message).set_text(message)
        return self

    @allure.step("Add Announcements Get Message Entered")
    def add_announcements_get_message_entered(self):
        message = self.element().set_locator(self.window_add_announcements_txt_message).get_attribute()
        return message

    @allure.step("Add Announcements Enter Start Date (Today)")
    def add_announcements_enter_start_date(self, date):
        self.send_keys().set_locator(self.window_add_announcements_input_start_date).set_text(date)
        self.click().set_locator(self.window_add_announcements_date_picker_start_date).single_click()
        self.click().set_locator(self.window_add_announcements_date_picker_start_date_selected).single_click()
        return self

    @allure.step("Add Announcements Enter Start Date (Future)")
    def add_announcements_enter_start_date_future(self, date):
        self.send_keys().set_locator(self.window_add_announcements_input_start_date).set_text(date)
        self.click().set_locator(self.window_add_announcements_date_picker_start_date).single_click()
        self.click().set_locator(self.window_add_announcements_date_picker_end_date_selected).single_click()
        return self

    @allure.step("Add Announcements Enter End Date")
    def add_announcements_enter_end_date(self, date):
        self.send_keys().set_locator(self.window_add_announcements_input_end_date).set_text(date)
        self.click().set_locator(self.window_add_announcements_date_picker_end_date).single_click()
        self.click().set_locator(self.window_add_announcements_date_picker_end_date_selected).single_click()
        return self

    @allure.step("Validate Add Announcements Start/End Datetime Error Message")
    def validate_add_announcement_start_end_datetime_error_message(self):
        self.element().set_locator(self.window_add_announcements_start_date_error_message, self._name)
        self.element().is_present(self.window_add_announcements_start_date_error_message)

        self.element().set_locator(self.window_add_announcements_end_date_error_message, self._name)
        self.element().is_present(self.window_add_announcements_end_date_error_message)
        return self

    @allure.step("Click Add Announcements Create Button")
    def click_add_announcements_create_button(self):
        self.click().set_locator(self.window_add_announcements_button_create).single_click()
        return self

    @allure.step("Click Add Announcements Cancel Button")
    def click_add_announcements_cancel_button(self):
        self.click().set_locator(self.window_add_announcements_button_cancel).single_click()
        return self

    @allure.step("Get Message for Accepting a Tender Correctly")
    def validate_announcement_added_success_message(self):
        self.element().set_locator(self.message_announcement_added_successfully, self._name)
        self.element().is_present(self.message_announcement_added_successfully)
        return self