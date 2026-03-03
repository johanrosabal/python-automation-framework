import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SalesInvoicingMenu')


class SalesInvoicingMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=3"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_sales_tariffs = (By.XPATH, "//a[text()='Sales Tariffs']", "Sales Tariffs Link")
        self.__link_sales_tariffs_extended = (By.XPATH, "//a[text()='Sales Tariffs Extended']", "Sales Tariffs Extended Link")
        self.__link_not_invoiced_bs_l = (By.XPATH, "//a[text()='Not Invoiced Bs/L']", "Not Invoiced Bs/L Link")
        self.__link_other_invoice_credit_note = (By.XPATH, "//a[text()='Other Invoice / Credit Note']", "Other Invoice / Credit Note Link")
        self.__link_receive_payments = (By.XPATH, "//a[text()='Receive Payments']", "Receive Payments Link")
        self.__link_short_form_booking = (By.XPATH, "//a[text()='Short Form (Booking)']", "Short Form (Booking) Link")
        self.__link_short_form_special_search = (By.XPATH, "//a[text()='Short Form (Special Search)']", "Short Form (Special Search) Link")
        self.__link_short_form_inv_receiver = (By.XPATH, "//a[text()='Short Form (Inv.Receiver)']", "Short Form (Inv.Receiver) Link")
        self.__link_agreement_overview = (By.XPATH, "//a[text()='Agreement Overview']", "Agreement Overview Link")
        self.__link_processing_vsa_bookings = (By.XPATH, "//a[text()='Processing VSA bookings']", "Processing VSA bookings Link")
        self.__link_customer_vsa = (By.XPATH, "//a[text()='CustomerVSA']", "CustomerVSA Link")
        self.__link_not_invoiced_bookings = (By.XPATH, "//a[text()='Not Invoiced Bookings']", "Not Invoiced Bookings Link")
        self.__link_not_invoiced_demurrage_and_detention = (By.XPATH, "//a[text()='Not Invoiced Demurrage and Detention']", "Not Invoiced Demurrage and Detention Link")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["finance"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Sales Tariffs")
    def link_sales_tariffs(self, pause: int = 0):
        self._load_page(self.__link_sales_tariffs, pause)
        return self

    @allure.step("Menu Sales Tariffs Extended")
    def link_sales_tariffs_extended(self, pause: int = 0):
        self._load_page(self.__link_sales_tariffs_extended, pause)
        return self

    @allure.step("Menu Not Invoiced Bs/L")
    def link_not_invoiced_bs_l(self, pause: int = 0):
        self._load_page(self.__link_not_invoiced_bs_l, pause)
        return self

    @allure.step("Menu Other Invoice / Credit Note")
    def link_other_invoice_credit_note(self, pause: int = 0):
        self._load_page(self.__link_other_invoice_credit_note, pause)
        return self

    @allure.step("Menu Receive Payments")
    def link_receive_payments(self, pause: int = 0):
        self._load_page(self.__link_receive_payments, pause)
        return self

    @allure.step("Menu Short Form (Booking)")
    def link_short_form_booking(self, pause: int = 0):
        self._load_page(self.__link_short_form_booking, pause)
        return self

    @allure.step("Menu Short Form (Special Search)")
    def link_short_form_special_search(self, pause: int = 0):
        self._load_page(self.__link_short_form_special_search, pause)
        return self

    @allure.step("Menu Short Form (Inv.Receiver)")
    def link_short_form_inv_receiver(self, pause: int = 0):
        self._load_page(self.__link_short_form_inv_receiver, pause)
        return self

    @allure.step("Menu Agreement Overview")
    def link_agreement_overview(self, pause: int = 0):
        self._load_page(self.__link_agreement_overview, pause)
        return self

    @allure.step("Menu Processing VSA bookings")
    def link_processing_vsa_bookings(self, pause: int = 0):
        self._load_page(self.__link_processing_vsa_bookings, pause)
        return self

    @allure.step("Menu CustomerVSA")
    def link_customer_vsa(self, pause: int = 0):
        self._load_page(self.__link_customer_vsa, pause)
        return self

    @allure.step("Menu Not Invoiced Bookings")
    def link_not_invoiced_bookings(self, pause: int = 0):
        self._load_page(self.__link_not_invoiced_bookings, pause)
        return self

    @allure.step("Menu Not Invoiced Demurrage and Detention")
    def link_not_invoiced_demurrage_and_detention(self, pause: int = 0):
        self._load_page(self.__link_not_invoiced_demurrage_and_detention, pause)
        return self
