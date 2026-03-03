from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('Buttons')


class Buttons(BasePage):

    def __init__(self, driver):
        """
        Initialize the Buttons instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/web/index.php/auth/login"
        # Locator definitions

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def click_use_filters(self):
        locator = (By.XPATH, "//button[contains(@class,'use-filter-button')]", "USE FILTERS [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def select_sort_by(self, sort_by: str):
        locator = (By.XPATH, "//select[contains(@class,'sort-filter-select pull-left')]", F"SORT BY {sort_by} [Select Dropdown Option]")
        self.dropdown().set_locator(locator, self._name).by_text(sort_by)
        return self

    def click_sort_by(self, sort_by: str):
        locator = (By.XPATH, f"//span[@class='sorting-options']//span[text()='{sort_by}']", F"SORT BY {sort_by} [Click Button]")
        self.click().set_locator(locator, self._name).single_click().pause(1)
        return self

    def click_apply(self):
        locator = (By.XPATH, "//button[contains(text(),'Apply')]", "USE FILTERS: APPLY [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_clear_all(self):
        locator = (By.XPATH, "//button[contains(text(),'Clear All')]", "USE FILTERS: CLEAR ALL [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def enter_search_the_list(self, text):
        locator = (By.XPATH, "//input[@type='search'][@placeholder='Search the list']", "Search the list [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    # Pagination -------------------------------------------------------------------------------------------------------
    def click_refresh_icon(self):
        locator = (By.XPATH, "//button[contains(@class, 'refresh-icon')]", "REFRESH ICON [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def select_view_pages(self, number):
        locator = (By.XPATH, "(//select[@name='showRecords'])[1]", "View [Select]")
        self.dropdown().set_locator(locator, self._name).by_text(number)
        return self

    def click_previous_page(self):
        locator = (By.XPATH, "(//button[contains(@class, 'pagination-left')])[1]", "PREVIOUS [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_next_page(self):
        locator = (By.XPATH, "(//button[contains(@class, 'pagination-right')])[1]", "PREVIOUS [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_tab_button_with_label(self, label: str):
        locator = (By.XPATH, f"//a[@role='tab'][text()='{label}']", f"Click {label.upper()} [Tab]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_button_with_label(self, label: str):
        locator = (By.XPATH, f"//button[text()='{label}']", f"Click {label.upper()} [Button]")
        self.click().set_locator(locator, self._name).highlight().single_click()
        return self

    def click_tab_more(self):
        locator = (By.XPATH, f"//button[text()='More']", f"Click MORE [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    # Booking Details --------------------------------------------------------------------------------------------------

    def click_generate_multiple_bol(self):
        self.scroll().to_top()
        self.click_button_with_label("GENERATE MULTIPLE BOL")  # Booking Details |
        return self

    def click_update_cargo_details(self):
        self.scroll().to_top()
        self.click_button_with_label("Update Cargo Details")  # Booking Details |
        return self

    def click_update(self):
        locator = (By.XPATH, "//button[text()='UPDATE' or text()='Update']", "Update [Button]")  # Booking Details |
        self.scroll().to_top()
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_generate_bol_number(self):
        self.scroll().to_top()
        self.click_button_with_label("Generate BOL Number")  # Booking Details |
        return self

    def click_create_shipment_instructions(self):
        self.scroll().to_top()
        self.click_button_with_label("Create Shipping Instructions")  # Booking Details |
        return self

    def click_resubmit(self):
        self.scroll().to_top()
        self.click_button_with_label("ReSubmit")  # Booking Details |
        return self

    def click_rebook(self):
        self.scroll().to_top()
        self.click_button_with_label("ReBook")  # Booking Details |
        return self

    def click_cancel(self):
        locator = (By.XPATH, "//button[text()='CANCEL' or text()='Cancel']", "Cancel [Button]")  # Booking Details |
        self.scroll().to_top()
        self.click().set_locator(locator).single_click()
        return self

    def click_download(self):
        self.scroll().to_top()
        self.click_button_with_label("Download")  # Booking Details |
        return self

    def click_email(self):
        self.scroll().to_top()
        self.click_button_with_label("Email")  # Booking Details |
        return self

    def click_assignment_complete(self):
        self.scroll().to_top()
        self.click_button_with_label("Assignment Complete")  # Booking Details |
        return self

    def click_check_submission_status(self):
        self.scroll().to_top()
        self.click_button_with_label("Check Submission Status")  # Booking Details |
        return self

    # Create Bookings --------------------------------------------------------------------------------------------------
    def click_next(self):
        self.scroll().to_bottom()
        self.click_button_with_label("Next")  # Create Bookings
        return self

    def click_back(self):
        self.scroll().to_bottom()
        self.click_button_with_label("Back")  # Create Bookings
        return self

    def click_save(self):
        self.scroll().to_bottom()
        self.click_button_with_label("Save")  # Create Bookings
        return self

    def click_cancel_booking(self):
        self.scroll().to_bottom()
        self.click_button_with_label("Cancel Booking")  # Create Bookings
        return self

    def click_create_booking(self):
        self.scroll().to_bottom()
        self.click_button_with_label("Create Booking")  # Create Bookings
        return self

    def click_cancel_update(self):
        self.scroll().to_bottom()
        self.click_button_with_label("Cancel Update")  # Create Bookings
        return self

    def click_proceed(self):
        locator = (By.XPATH, "//button[@title='Proceed']", "Proceed [Button]")  # Modal Create Bookings
        self.scroll().set_locator(locator).to_element(pixels=-80)
        self.click().set_locator(locator).single_click()
        return self

    def click_remove(self):
        locator = (By.XPATH, "//button[@title='Remove']", "Remove [Button]")  # Modal Create Bookings
        self.scroll().set_locator(locator).to_element(pixels=-80)
        self.click().set_locator(locator).single_click()
        return self

    def click_go_to_event_list(self):
        locator = (By.XPATH, "//button[@title='GO TO EVENTS LIST']", "GO TO EVENTS LIST [Button]")  # Modal Equipment Events
        self.scroll().set_locator(locator).to_element(pixels=-80)
        self.click().set_locator(locator).single_click()
        return self

    def click_create_new_at_this_location(self):
        locator = (By.XPATH, "//button[@title='CREATE NEW AT THIS LOCATION']", "CREATE NEW AT THIS LOCATION [Button]")  # Modal Equipment Events
        self.scroll().set_locator(locator).to_element(pixels=-80)
        self.click().set_locator(locator).single_click()
        return self

    def click_create_new(self):
        locator = (By.XPATH, "//button[@title='CREATE NEW']", "CREATE NEW [Button]")  # Modal Equipment Events
        self.scroll().set_locator(locator).to_element(pixels=-80)
        self.click().set_locator(locator).single_click()
        return self

    def click_ok(self):
        locator = (By.XPATH, "(//button[@title='OK'])[1]", "OK [Button]")  # Modal Create Bookings
        visible = self.element().set_locator(locator).is_visible()
        logger.info(f"Modal with OK Button: {visible}")
        self.click().set_locator(locator).single_click()
        return self

    def click_update_booking(self):
        locator = (By.XPATH, "//button[@title='Update Booking']", "Update Booking [Button]")  # Create Bookings
        self.click().set_locator(locator).single_click()
        return self

    # MODAL ------------------------------------------------------------------------------------------------------------

    def click_cancel_confirmation(self):
        locator = (By.XPATH, "//button[text()='CANCEL' or text()='Cancel']", "Modal Cancel [Button]")  # Booking Details |
        self.click().set_locator(locator).single_click()
        return self

    def click_update_confirmation(self):
        locator = (By.XPATH, "//button[text()='UPDATE' or text()='Update']", "Modal Update [Button]")  # Booking Details |
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_continue_update(self):
        # Modal Button Appears when user Cancel Booking Update
        self.scroll().to_bottom()
        self.click_button_with_label("Continue Update")  # Create Bookings
        return self

    def click_confirm_cancellation(self):
        # Modal Button Appears when user Cancel Booking Update
        self.scroll().to_bottom()
        self.click_button_with_label("Confirm Cancellation")  # Create Bookings
        return self

    def click_close_modal(self):
        locator = (By.XPATH,"//i[contains(@class,'close-dlg')]","Close Modal")
        self.click().set_locator(locator).single_click()
        return self

    # MODAL EQUIPMENT EVENT --------------------------------------------------------------------------------------------------
