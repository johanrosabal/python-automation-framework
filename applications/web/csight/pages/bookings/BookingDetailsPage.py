from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.pages.bookings.booking_details_tabs.CargoDetailsTab import CargoDetailsTab
from applications.web.csight.pages.bookings.booking_details_tabs.CasesTab import CasesTab
from applications.web.csight.pages.bookings.booking_details_tabs.OptionalServicesTab import OptionalServicesTab
from applications.web.csight.pages.bookings.booking_details_tabs.RoutesDetailsTab import RoutesDetailsTab
from applications.web.csight.pages.bookings.booking_details_tabs.DocumentsDetailsTab import DocumentsDetailsTab
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('BookingDetailsPage')


class BookingDetailsPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the BookingDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/bookingDetail?id={ID}"
        # xPaths Containers
        self._tabs = "//ul[@role='tablist']/li"
        # Locator definitions
        self._button_quick_update = (By.XPATH, "//button[text()='Quick Update']", "Quick Update [Button]")
        self._tab_routes_details = (By.XPATH, f"{self._tabs}/a[contains(text(),'Route Details')]", "Routes Details [Tab]")
        self._tab_cargo_details = (By.XPATH, f"{self._tabs}/a[contains(text(),'Cargo Details')]", "Cargo Details [Tab]")
        self._tab_operational_services = (By.XPATH, f"{self._tabs}/a[contains(text(),'Operational Services')]", "Operational Services [Tab]")
        self._tab_party_details = (By.XPATH, f"{self._tabs}/a[contains(text(),'Party Details')]", "Party Details [Tab]")
        self._tab_rate_details = (By.XPATH, f"{self._tabs}/a[contains(text(),'Rate Details')]", "Rate Details [Tab]")
        self._tab_payments_receipts = (By.XPATH, f"{self._tabs}/a[contains(text(),'Payment Receipts')]", "Payment Receipts [Tab]")
        self._tab_optional_services = (By.XPATH, f"{self._tabs}/a[contains(text(),'Optional Services')]", "Optional Services [Tab]")
        self._tab_reference_numbers = (By.XPATH, f"{self._tabs}/a[contains(text(),'Reference Numbers')]", "Reference Numbers [Tab]")
        self._tab_load_list = (By.XPATH, f"{self._tabs}/a[contains(text(),'Load List')]", "Load List [Tab]")
        self._tab_booking_remarks = (By.XPATH, f"{self._tabs}/a[contains(text(),'Booking Remarks')]", "Booking Remarks [Tab]")
        self._tab_documents = (By.XPATH, f"{self._tabs}/a[contains(text(),'Documents')]", "Documents [Tab]")
        self._tab_bill_of_lading = (By.XPATH, f"{self._tabs}/a[contains(text(),'Bill Of Lading')]", "Bill Of Lading [Tab]")
        self._tab_history = (By.XPATH, f"{self._tabs}/a[contains(text(),'History')]", "History [Tab]")
        self._tab_cases = (By.XPATH, f"({self._tabs}/a[contains(text(),'Cases')])[2]", "Cases [Tab]")
        self._tab_secondary_bookings = (By.XPATH, f"{self._tabs}/a[contains(text(),'Secondary Bookings')]", "Secondary Bookings [Tab]")
        self._tab_multiple_bookings = (By.XPATH, f"{self._tabs}/a[contains(text(),'Multiple Bookings')]", "Multiple Bookings [Tab]")

        # Sub-Components
        self.tab_content_routes_details = RoutesDetailsTab.get_instance()
        self.tab_content_cargo_details = CargoDetailsTab.get_instance()
        self.tab_content_cases_details = CasesTab.get_instance()
        self.tab_content_documents_details = DocumentsDetailsTab.get_instance()
        self.tab_content_optional_services_details = OptionalServicesTab.get_instance()
        self.buttons = Buttons.get_instance()
        self.loadings = Loadings.get_instance()

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

    # LOADING COMPONENT ------------------------------------------------------------------------------------------------
    def is_not_visible_spinner(self):
        self.loadings.is_not_visible_spinner()
        return self

    # TOP BUTTONS ------------------------------------------------------------------------------------------------------

    def click_generate_multiple_bol(self):
        self.buttons.click_generate_multiple_bol()
        return self

    def click_update_cargo_details(self):
        self.buttons.click_update_cargo_details()
        return self

    def click_update(self):
        self.buttons.click_update()
        self.loadings.wait_until_loading_not_present()
        return self

    def click_generate_bol_number(self):
        self.buttons.click_generate_bol_number()
        return self

    def click_create_shipping_instructions(self):
        self.buttons.click_create_shipment_instructions()
        return self

    def click_resubmit(self):
        self.buttons.click_resubmit()
        return self

    def click_cancel(self):
        self.buttons.click_cancel()
        return self

    def click_rebook(self):
        self.buttons.click_rebook()
        return self

    def click_download(self):
        self.buttons.click_download()
        return self

    def click_email(self):
        self.buttons.click_email()
        return self

    def click_assignment_complete(self):
        self.buttons.click_assignment_complete()
        return self

    def click_check_submission_status(self):
        self.buttons.click_check_submission_status()
        return self

    # HEADER -----------------------------------------------------------------------------------------------------------
    def click_quick_update(self):
        self.click().set_locator(self._button_quick_update, self._name).single_click()
        return self

    # TABS ------------------------------------------------------------------------------------------------------------

    def click_tab_routes_details(self):
        self.click().set_locator(self._tab_routes_details, self._name).single_click()
        self.scroll().set_locator(self._tab_routes_details).to_element(pixels=-30)
        return self

    def click_tab_cargo_details(self):
        self.click().set_locator(self._tab_cargo_details, self._name).single_click().pause(1)
        self.scroll().set_locator(self._tab_cargo_details).to_element(pixels=-100)
        return self

    def get_cargo_details(self):
        return self.tab_content_cargo_details

    def click_tab_operational_services(self):
        self.click().set_locator(self._tab_operational_services, self._name).single_click()
        self.scroll().set_locator(self._tab_operational_services).to_element(-100)
        return self

    def click_tab_party_details(self):
        self.click().set_locator(self._tab_party_details, self._name).single_click()
        self.scroll().set_locator(self._tab_party_details).to_element(-100)
        return self

    def click_tab_rate_details(self):
        self.click().set_locator(self._tab_rate_details, self._name).single_click()
        self.scroll().set_locator(self._tab_rate_details).to_element(-100)
        return self

    def click_tab_payments_receipts(self):
        self.click().set_locator(self._tab_payments_receipts, self._name).single_click()
        self.scroll().set_locator(self._tab_payments_receipts).to_element(-100)
        return self

    def click_tab_optional_services(self):
        self.click().set_locator(self._tab_optional_services, self._name).single_click()
        self.scroll().set_locator(self._tab_optional_services).to_element(-100)
        return self

    def click_tab_reference_numbers(self):
        self.click().set_locator(self._tab_reference_numbers, self._name).single_click()
        self.scroll().set_locator(self._tab_reference_numbers).to_element(-100)
        return self

    def click_tab_load_list(self):
        self.click().set_locator(self._tab_load_list, self._name).single_click()
        return self

    def click_tab_booking_remarks(self):
        self.click().set_locator(self._tab_booking_remarks, self._name).single_click()
        return self

    def click_tab_documents(self):
        self.click().set_locator(self._tab_documents, self._name).single_click().pause(3)
        self.scroll().set_locator(self._tab_documents).to_element(-100)
        return self

    def click_tab_bill_of_ladings(self):
        self.click().set_locator(self._tab_bill_of_lading, self._name).single_click()
        return self

    def click_tab_history(self):
        self.click().set_locator(self._tab_history, self._name).single_click()
        return self

    def click_tab_cases(self):
        self.click().set_locator(self._tab_cases, self._name).single_click()
        self.scroll().set_locator(self._tab_cases).to_element(-100)
        return self

    def click_tab_secondary_bookings(self):
        self.click().set_locator(self._tab_secondary_bookings, self._name).single_click()
        return self

    def click_tab_multiple_bookings(self):
        self.click().set_locator(self._tab_multiple_bookings, self._name).single_click()
        return self

    # MAIN INFORMATION -------------------------------------------------------------------------------------------------
    def get_booking_id(self):
        locator = (By.XPATH, "(//div[@class='summary-head']//h5//span)[1]", "Booking ID [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_booking_status(self):
        # self.is_not_visible_spinner()
        self.pause(5)
        locator = (By.XPATH, "(//div[@class='summary-head']//h5//span)[2]", "Booking Status [Text]")
        self.element().set_locator(locator).is_visible()
        return self.get_text().set_locator(locator, self._name).highlight(duration=2).by_text().lstrip()

    def get_account(self):
        locator = (By.XPATH, "//span[contains(text(),'Account')]/following-sibling::b/span", "Account [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_contract_number(self):
        locator = (By.XPATH, "//span[contains(text(),'Contract Number')]/following-sibling::span", "Contract Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_origin(self):
        locator = (By.XPATH, "//span[contains(text(),'Origin')]/following-sibling::span", "Origin [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_pre_carriage_mode(self):
        locator = (By.XPATH, "//span[contains(text(),'Pre-carriage Mode')]/following-sibling::span", "Pre-carriage Mode [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_final_destination(self):
        locator = (By.XPATH, "//span[contains(text(),'Final Destination')]/following-sibling::span", "Final Destination [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_on_carriage_mode(self):
        locator = (By.XPATH, "//span[contains(text(),'On-carriage Mode')]/following-sibling::span", "On-carriage Mode [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_booking_source(self):
        locator = (By.XPATH, "//span[contains(text(),'Booking Source')]/following-sibling::span", "Booking Source [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_hazardous_booking(self):
        locator = (By.XPATH, "//span[contains(text(),'Hazardous Booking')]/following-sibling::span", "Hazardous Booking [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_quote_number(self):
        locator = (By.XPATH, "//span[contains(text(),'Quote Number')]/following-sibling::span", "Quote Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_in_bond_required(self):
        locator = (By.XPATH, "//span[contains(text(),'In-bond Required')]/following-sibling::span", "In-bond Required [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_equipment_substitution(self):
        locator = (By.XPATH, "//span[contains(text(),'Equipment Substitution')]/following-sibling::span", "Equipment Substitution [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_pending_reason(self):
        locator = (By.XPATH, f"//span[contains(text(),'Pending Reason')]/../b/ul/li/span", "Pending Reason [Text]")
        return self.element().set_locator(locator).get_list_text()

    def get_pending_reason_find(self, find):
        locator = (By.XPATH, f"//span[contains(text(),'Pending Reason')]/..//ul/li/span[contains(text(),'{find}')]", "Pending Reason [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def click_pending_reason_approved(self, number):
        locator = (By.XPATH, f"(//a/u[text()='Approve'])[{number}]", f"Approved Pending Reason [{number}]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_approved_pending_reason_yes(self):
        locator = (By.XPATH, "//span[@class='slds-radio']/label/span[text()='Yes']", "Approved YES Pending Reason")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_approved_confirmation_update(self):
        self.buttons.click_update_confirmation().pause(5)
        return self

    def click_approved_pending_reason_no(self):
        locator = (By.XPATH, "//span[@class='slds-radio']/label/span[text()='No']", "Approved NO Pending Reason")
        self.click().set_locator(locator, self._name).single_click()
        self.buttons.click_cancel_confirmation()
        return self

    def get_cargo_release_location(self):
        locator = (By.XPATH, "//span[contains(text(),'Cargo Release Location')]/following-sibling::b/span", "Cargo Release Location [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_customs_clearence_location(self):
        locator = (By.XPATH, "//span[contains(text(),'Customs Clearence Location')]/following-sibling::b/span", "Customs Clearence Location [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_SCAC(self):
        locator = (By.XPATH, "//span[contains(text(),'SCAC')]/following-sibling::span", "SCAC[Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_load_listed_status(self):
        locator = (By.XPATH, "//span[contains(text(),'Load Listed Status')]/following-sibling::b", "Load Listed Status [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_cargo_ready_for_transport(self):
        locator = (By.XPATH, "//span[contains(text(),'Cargo Ready for Transport')]/following-sibling::span", "Cargo Ready for Transport [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_booking_initiated_on(self):
        locator = (By.XPATH, "//span[contains(text(),'Booking Initiated on')]/following-sibling::b", "Booking Initiated on [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_booking_active_date(self):
        locator = (By.XPATH, "//span[contains(text(),'Booking Active Date')]/following-sibling::b", "Booking Active Date [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_booking_by(self):
        locator = (By.XPATH, "//span[contains(text(),'Booked by')]/following-sibling::b", "Booked by [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_contact(self):
        locator = (By.XPATH, "//span[contains(text(),'Contact')]/following-sibling::span", "Contact [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_payment_terms(self):
        locator = (By.XPATH, "//span[contains(text(),'Payment Terms')]/following-sibling::span", "Payment Terms [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_reserved_BOL_Number(self):
        locator = (By.XPATH, "//span[contains(text(),'Reserved BOL Number')]/following-sibling::b", "Reserved BOL Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_ITN_Number(self):
        locator = (By.XPATH, "//span[contains(text(),'ITN Number')]/following-sibling::span", "ITN Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_exemption_clause(self):
        locator = (By.XPATH, "//span[contains(text(),'Exemption Clause')]/following-sibling::span", "Exemption Clause [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_softship_booking_number(self):
        locator = (By.XPATH, "//span[contains(text(),'Softship Booking Number')]/following-sibling::b", "Softship Booking Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_created_by(self):
        locator = (By.XPATH, "//span[contains(text(),'Created By')]/following-sibling::b", "Created By [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_assigned_to(self):
        locator = (By.XPATH, "//span[contains(text(),'Assigned to')]/following-sibling::span", "Assigned to [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_assigned_date_and_time(self):
        locator = (By.XPATH, "//span[contains(text(),'Assigned Date & Time')]/following-sibling::span", "Assigned Date & Time [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_primary_booking(self):
        locator = (By.XPATH, "//span[contains(text(),'Primary Booking')]/following-sibling::b", "Primary Booking [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_original_booking_number(self):
        locator = (By.XPATH, "//span[contains(text(),'Original Booking Number')]/following-sibling::b", "Original Booking Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()
