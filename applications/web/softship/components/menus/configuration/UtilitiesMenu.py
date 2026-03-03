import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('UtilitiesMenu')


class UtilitiesMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=2"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__nav_application_action = (By.XPATH, "//a[text()='Application Action']", "Application Action Link")
        self.__nav_control_code = (By.XPATH, "//a[text()='Control Code']", "Control Code Link")
        self.__nav_control_code_description = (By.XPATH, "//a[text()='Control Code Description']", "Control Code Description Link")
        self.__nav_edi_distribution = (By.XPATH, "//a[text()='EDI Distribution']", "EDI Distribution Link")
        self.__nav_interface_formats = (By.XPATH, "//a[text()='Interface Formats']", "Interface Formats Link")
        self.__nav_interface_settings = (By.XPATH, "//a[text()='Interface Settings']", "Interface Settings Link")
        self.__nav_invoice_serial_numbering = (By.XPATH, "//a[text()='Invoice Serial Numbering']", "Invoice Serial Numbering Link")
        self.__nav_message = (By.XPATH, "//a[text()='Message']", "Message Link")
        self.__nav_invoice_print_specification = (By.XPATH, "//a[text()='Invoice Print Specification']", "Invoice Print Specification Link")
        self.__nav_smarts = (By.XPATH, "//a[text()='Smarts']", "Smarts Link")
        self.__nav_switch_declaration = (By.XPATH, "//a[text()='Switch Declaration']", "Switch Declaration Link")
        self.__nav_switch_state = (By.XPATH, "//a[text()='Switch State']", "Switch State Link")
        self.__nav_user_defined_events = (By.XPATH, "//a[text()='User Defined Events']", "User Defined Events Link")
        self.__nav_settings_service = (By.XPATH, "//a[text()='Settings Service']", "Settings Service Link")
        self.__nav_pessimistic_line_bill_of_lading_locks = (By.XPATH, "//a[text()='Pessimistic LINE Bill Of Lading Locks']", "Pessimistic LINE Bill Of Lading Locks Link")
        self.__nav_pessimistic_line_booking_locks = (By.XPATH, "//a[text()='Pessimistic LINE Booking Locks']", "Pessimistic LINE Booking Locks Link")
        self.__nav_pessimistic_line_quotation_locks = (By.XPATH, "//a[text()='Pessimistic LINE Quotation Locks']", "Pessimistic LINE Quotation Locks Link")
        self.__nav_scheduler_control_center = (By.XPATH, "//a[text()='Scheduler Control Center']", "Scheduler Control Center Link")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["configuration"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Application Action")
    def link_application_action(self, pause: int = 0):
        self._load_page(self.__nav_application_action, pause)
        return self

    @allure.step("Menu Control Code")
    def link_control_code(self, pause: int = 0):
        self._load_page(self.__nav_control_code, pause)
        return self

    @allure.step("Menu Control Code Description")
    def link_control_code_description(self, pause: int = 0):
        self._load_page(self.__nav_control_code_description, pause)
        return self

    @allure.step("Menu EDI Distribution")
    def link_edi_distribution(self, pause: int = 0):
        self._load_page(self.__nav_edi_distribution, pause)
        return self

    @allure.step("Menu Interface Formats")
    def link_interface_formats(self, pause: int = 0):
        self._load_page(self.__nav_interface_formats, pause)
        return self

    @allure.step("Menu Interface Settings")
    def link_interface_settings(self, pause: int = 0):
        self._load_page(self.__nav_interface_settings, pause)
        return self

    @allure.step("Menu Invoice Serial Numbering")
    def link_invoice_serial_numbering(self, pause: int = 0):
        self._load_page(self.__nav_invoice_serial_numbering, pause)
        return self

    @allure.step("Menu Message")
    def link_message(self, pause: int = 0):
        self._load_page(self.__nav_message, pause)
        return self

    @allure.step("Menu Invoice Print Specification")
    def link_invoice_print_specification(self, pause: int = 0):
        self._load_page(self.__nav_invoice_print_specification, pause)
        return self

    @allure.step("Menu Smarts")
    def link_smarts(self, pause: int = 0):
        self._load_page(self.__nav_smarts, pause)
        return self

    @allure.step("Menu Switch Declaration")
    def link_switch_declaration(self, pause: int = 0):
        self._load_page(self.__nav_switch_declaration, pause)
        return self

    @allure.step("Menu Switch State")
    def link_switch_state(self, pause: int = 0):
        self._load_page(self.__nav_switch_state, pause)
        return self

    @allure.step("Menu User Defined Events")
    def link_user_defined_events(self, pause: int = 0):
        self._load_page(self.__nav_user_defined_events, pause)
        return self

    @allure.step("Menu Settings Service")
    def link_settings_service(self, pause: int = 0):
        self._load_page(self.__nav_settings_service, pause)
        return self

    @allure.step("Menu Settings Service")
    def link_settings_service(self, pause: int = 0):
        self._load_page(self.__nav_settings_service, pause)
        return self

    @allure.step("Menu Pessimistic LINE Bill Of Lading Locks")
    def link_pessimistic_line_bill_of_lading_locks(self, pause: int = 0):
        self._load_page(self.__nav_pessimistic_line_bill_of_lading_locks, pause)
        return self

    @allure.step("Menu Pessimistic LINE Booking Locks")
    def link_pessimistic_line_booking_locks(self, pause: int = 0):
        self._load_page(self.__nav_pessimistic_line_booking_locks, pause)
        return self

    @allure.step("Menu Pessimistic LINE Quotation Locks")
    def link_pessimistic_line_quotation_locks(self, pause: int = 0):
        self._load_page(self.__nav_pessimistic_line_quotation_locks, pause)
        return self

    @allure.step("Menu Scheduler Control Center")
    def link_scheduler_control_center(self, pause: int = 0):
        self._load_page(self.__nav_scheduler_control_center, pause)
        return self
