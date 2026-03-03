import allure
from selenium.webdriver.common.by import By

from applications.web.softship.pages.masterdata.basic.customer_suppliers.address.AddressPage import AddressPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('BasicMenu')


class BasicMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Basic Manu instance.
        """
        super().__init__(driver)
        self._driver = driver
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=1"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        # Links
        self.__link_agency = (By.XPATH, "//a[text()='Agency']", "Agency Link")
        self.__link_agency_commission = (By.XPATH, "//a[text()='Agency Commission']", "Agency Commission Link")
        self.__link_agency_commission_rules = (
            By.XPATH, "//a[text()='Agency Commission Rules']", "Agency Commission Rules Link")
        self.__link_agency_places_relation = (
            By.XPATH, "//a[text()='Agency Places Relation']", "Agency Places Relation Link")
        self.__link_company = (By.XPATH, "//a[text()='Company']", "Company Link")
        self.__link_customer_supplier = (By.XPATH, "//a[text()='Customer/Supplier']", "Customer/Supplier Link")
        self.__link_customer_supplier_query = (
            By.XPATH, "//a[text()='Customer/Supplier Query']", "Customer/Supplier Query Link")
        self.__link_customer_supplier_type = (
            By.XPATH, "//a[text()='Customer/Supplier Type']", "Customer/Supplier Type Link")
        self.__link_customer_supplier_contact = (
            By.XPATH, "//a[text()='Customer/Supplier Contact']", "Customer/Supplier Contact Link")
        self.__link_address = (By.XPATH, "//a[text()='Address']", "Address Link")
        self.__link_address_new = (By.XPATH, "//a[text()='Address New']", "Address New Link")
        self.__link_customer_freight_tariff_relation = (
            By.XPATH, "//a[text()='Customer Freight Tariff Relation']", "Customer Freight Tariff Relation Link")
        self.__link_customer_bkg_relation = (
            By.XPATH, "//a[text()='Customer Bkg Relation']", "Customer Bkg Relation Link")
        self.__link_customer_distribution = (
            By.XPATH, "//a[text()='Customer Distribution']", "Customer Distribution Link")
        self.__link_customer_freight_terms = (
            By.XPATH, "//a[text()='Customer Freight Terms']", "Customer Freight Terms Link")
        self.__link_customer_group = (By.XPATH, "//a[text()='Customer Group']", "Customer Group Link")
        self.__link_customer_independent_distribution = (
            By.XPATH, "//a[text()='Customer Independent Distribution']", "Customer Independent Distribution Link")
        self.__link_customer_rel_bkg_field_valid = (
            By.XPATH, "//a[text()='Customer Rel Bkg Field Valid']", "Customer Rel Bkg Field Valid Link")
        self.__link_customer_teus = (By.XPATH, "//a[text()='Customer Teus']", "Customer Teus Link")
        self.__link_bill_address = (By.XPATH, "//a[text()='Bill Address']", "Bill Address Link")
        self.__link_customer_trucker = (By.XPATH, "//a[text()='Customer Trucker']", "Customer Trucker Link")
        self.__link_define_event_cargo_status = (
            By.XPATH, "//a[text()='Define Event Cargo Status']", "Define Event Cargo Status Link")
        self.__link_define_ICS_status = (By.XPATH, "//a[text()='Define ICS Status']", "Define ICS Status Link")
        self.__link_stamp_text = (By.XPATH, "//a[text()='Stamp Text']", "Stamp Text Link")
        self.__link_standard_text = (By.XPATH, "//a[text()='Standard Text']", "Standard Text Link")
        self.__link_export_booking_select = (
            By.XPATH, "//a[text()='Export Booking Select']", "Export Booking Select Link")
        self.__link_export_schedule_booking = (
            By.XPATH, "//a[text()='Export Schedule Booking']", "Export Schedule Booking Link")
        self.__link_define_customs_messages = (
            By.XPATH, "//a[text()='Define Customs Messages']", "Define Customs Messages Link")
        self.__link_invoice_on_hold = (By.XPATH, "//a[text()='Invoice On Hold']", "Invoice On Hold Link")

    @allure.step("Load Basic Page")
    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Link Agency")
    def link_agency(self, pause: int = 0):
        self._load_page(self.__link_agency, pause)
        return self

    @allure.step("Link Agency Commission")
    def link_agency_commission(self, pause: int = 0):
        self._load_page(self.__link_agency_commission, pause)
        return self

    @allure.step("Link Agency Commission Rules")
    def link_agency_commission_rules(self, pause: int = 0):
        self._load_page(self.__link_agency_commission_rules, pause)
        return self

    @allure.step("Link Agency Places Relation")
    def link_agency_places_relation(self, pause: int = 0):
        self._load_page(self.__link_agency_places_relation, pause)
        return self

    @allure.step("Link Company")
    def link_company(self, pause: int = 0):
        self._load_page(self.__link_company, pause)
        return self

    @allure.step("Link Customer/Supplier")
    def link_customer_supplier(self, pause: int = 0):
        self._load_page(self.__link_customer_supplier, pause)
        return self

    @allure.step("Link Customer/Supplier Query")
    def link_customer_supplier_query(self, pause: int = 0):
        self._load_page(self.__link_customer_supplier_query, pause)
        return self

    @allure.step("Link Customer/Supplier Type")
    def link_customer_supplier_type(self, pause: int = 0):
        self._load_page(self.__link_customer_supplier_type, pause)
        return self

    @allure.step("Link Customer/Supplier Contact")
    def link_customer_supplier_contact(self, pause: int = 0):
        self._load_page(self.__link_customer_supplier_contact, pause)
        return self

    @allure.step("Link Address")
    def link_address(self, pause: int = 0):
        self._load_page(self.__link_address, pause)
        return self

    @allure.step("Link Address New")
    def link_address_new(self, pause: int = 0):
        self._load_page(self.__link_address_new, pause)
        return AddressPage(self._driver)

    @allure.step("Link Customer Freight Tariff Relation")
    def link_customer_freight_tariff_relation(self, pause: int = 0):
        self._load_page(self.__link_customer_freight_tariff_relation, pause)
        return self

    @allure.step("Link Customer Bkg Relation")
    def link_customer_bkg_relation(self, pause: int = 0):
        self._load_page(self.__link_customer_bkg_relation, pause)
        return self

    @allure.step("Link Customer Distribution")
    def link_customer_distribution(self, pause: int = 0):
        self._load_page(self.__link_customer_distribution, pause)
        return self

    @allure.step("Link Customer Freight Terms")
    def link_customer_freight_terms(self, pause: int = 0):
        self._load_page(self.__link_customer_freight_terms, pause)
        return self

    @allure.step("Link Customer Group")
    def link_customer_group(self, pause: int = 0):
        self._load_page(self.__link_customer_group, pause)
        return self

    @allure.step("Link Customer Independent Distribution")
    def link_customer_independent_distribution(self, pause: int = 0):
        self._load_page(self.__link_customer_independent_distribution, pause)
        return self

    @allure.step("Link Customer Rel Bkg Field Valid")
    def link_customer_rel_bkg_field_valid(self, pause: int = 0):
        self._load_page(self.__link_customer_rel_bkg_field_valid, pause)
        return self

    @allure.step("Link Customer Teus")
    def link_customer_teus(self, pause: int = 0):
        self._load_page(self.__link_customer_teus, pause)
        return self

    @allure.step("Link Bill Address")
    def link_bill_address(self, pause: int = 0):
        self._load_page(self.__link_bill_address, pause)
        return self

    @allure.step("Link Customer Trucker")
    def link_customer_trucker(self, pause: int = 0):
        self._load_page(self.__link_customer_trucker, pause)
        return self

    @allure.step("Link Define Event Cargo Status")
    def link_define_event_cargo_status(self, pause: int = 0):
        self._load_page(self.__link_define_event_cargo_status, pause)
        return self

    @allure.step("Link Define ICS Status")
    def link_define_ics_status(self, pause: int = 0):
        self._load_page(self.__link_define_ICS_status, pause)
        return self

    @allure.step("Link Stamp Text")
    def link_stamp_text(self, pause: int = 0):
        self._load_page(self.__link_stamp_text, pause)
        return self

    @allure.step("Link Standard Text")
    def link_standard_text(self, pause: int = 0):
        self._load_page(self.__link_standard_text, pause)
        return self

    @allure.step("Link Export Booking Select")
    def link_export_booking_select(self, pause: int = 0):
        self._load_page(self.__link_export_booking_select, pause)
        return self

    @allure.step("Link Export Schedule Booking")
    def link_export_schedule_booking(self, pause: int = 0):
        self._load_page(self.__link_export_schedule_booking, pause)
        return self

    @allure.step("Link Define Customs Messages")
    def link_define_customs_messages(self, pause: int = 0):
        self._load_page(self.__link_define_customs_messages, pause)
        return self

    @allure.step("Link Invoice On Hold")
    def link_invoice_on_hold(self, pause: int = 0):
        self._load_page(self.__link_invoice_on_hold, pause)
        return self
