import re

import allure
from selenium.webdriver.common.by import By
from applications.web.loadiq.components.shipment_details.DocumentsTab import DocumentsTab
from applications.web.loadiq.components.shipment_details.FinanceDetailsTab import FinanceDetailsTab
from applications.web.loadiq.components.shipment_details.HazmatDetailsTab import HazmatDetailsTab
from applications.web.loadiq.components.shipment_details.ShipmentDetailsTab import ShipmentDetailsTab
from applications.web.loadiq.components.shipment_details.StopDetailsTab import StopDetailsTab
from applications.web.loadiq.components.shipment_details.TrackingDetailsTab import TrackingDetailsTab
from applications.web.loadiq.components.shipment_details.AuditTrailTab import AudiTrailTab
from applications.web.loadiq.pages.my_loads.LoadInformationUpdatePage import LoadInformationUpdatePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from applications.web.loadiq.pages.my_loads.RequestAccessorialsPage import RequestAccessorialsPage

logger = setup_logger('MyLoadsPage')


class MyLoadsPage(BasePage):

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
        self.relative = "/shipment/list"

        # Locator definitions
        self._noload = (By.XPATH, "//h5[contains(text(), \"Sorry, we couldn't find any results\")]", "No Results Found [Message]")
        self._input_search_by = (By.XPATH, "//input[@type='text' and contains(@placeholder,'Search by')]", "Search by [Input]")
        self._button_search = (By.XPATH, "//button[@mattooltip='Search']", "Search [Button]")
        self._checkbox_include_close = (By.XPATH, "//label[@for='switchViewClosedLoads'][1]", "Include Closed [Checkbox]")
        self._button_sort_by_ship_date = (By.XPATH, "//div/span[text()='Ship date']", "Sort by ship date [Button]")
        self._button_sort_by_status = (By.XPATH, "//div/span[text()='Status']", "Sort by status [Button]")
        self._button_sort_by_origin = (By.XPATH, "//div/span[text()='Origin']", "Sort by origin [Button]")
        self._text_total_records = (By.XPATH, "//span[contains(@class, 'search-result')]", "Total Records [Text]")
        self._list_container = "//div[contains(@class, 'listingSide')]//div[@class='row']"
        self._get_ship_date = (By.XPATH, "//span[normalize-space(.)='Ship date']/following-sibling::span//*[name() = 'svg']", "Get ship date [Output]")
        self._no_load = (By.XPATH, "//h5[contains(text(), 'Sorry, we couldn't find any results.')]", "Message [Output]")
        self._confirmation_request_text = (By.XPATH, "//span[contains(text(), 'successfully submitted')]", "Message [Output text]")
        self._max_accessorials_text = (By.XPATH, "//span[contains(text(), 'you have exceeded the maximum allowance')]", "Message [Output text]")
        self._msg_error_alert = (By.XPATH, "//app-submitted-shipments//h5", "[Output text]", "Message [Output text]")
        self._lbl_load_no_found = (By.XPATH, "//app-submitted-shipments//h5", "Message [Output text]")
        self._msg_closed_load = (By.XPATH, "//app-shipment-detail/div/div/div[1]/div", "Message [Output text]")
        self._lbl_status_tag = (By.XPATH, "//*[contains(@class, 'iq-badge') and not(contains(@class, 'multistop'))]", "Status Tag [Label]")
        self._btn_status_tag = (By.XPATH, "// button / span[text() = ' Status Update']", "Status Update [Button]")
        self._btn_status_load_info_tag = (By.XPATH, "// button / span[text() = ' Update Load Info']", " Update Load Info [Button]")
        self._btn_complete_delivery = (By.XPATH, "//button[text()='Complete Delivery']", "Complete Delivery [Button]")
        self.request_accessorials = RequestAccessorialsPage.get_instance()
        #  Finance details fields
        self._txt_linehaul_charge_field = (By.XPATH, "//span[normalize-space(text())='Linehaul Charge']", "Linehaul Charge field [Text]")
        self._txt_fuel_field = (By.XPATH, "//span[normalize-space(text())='Fuel']", "Fuel field [Text]")
        self._txt_accessorials_field = (By.XPATH, "//span[normalize-space(text())='Accessorials']", "Accessorials field [Text]")
        self._txt_total_charge_field = (By.XPATH, "//span[normalize-space(text())='Total Charge']", "Total Charge field [Text]")
        self._txt_payment_status_field = (By.XPATH, "//span[normalize-space(text())='Payment status']", "Payment status field [Text]")
        self._txt_invoice_date_field = (By.XPATH, "//span[normalize-space(text())='Invoice Date']", "Invoice Date field [Text]")
        self._txt_check_number_field = (By.XPATH, "//span[normalize-space(text())='Check Number']", "Check Number field [Text]")
        self._txt_paid_amount_field = (By.XPATH, "//span[normalize-space(text())='Paid Amount']", "Paid Amount field [Text]")
        self._txt_invoice_number_field = (By.XPATH, "//span[normalize-space(text())='Invoice Number']", "Invoice Number field [Text]")
        self._txt_pro_number_field = (By.XPATH, "//span[normalize-space(text())='Pro Number']", "Pro Number field [Text]")
        #  Finance details values
        self._modal_finance_details = (By.XPATH, "//financial-detail-tab//div[position()=1]//div[position()=1]", "Finance detail [Modal]")
        self._output_linehaul_charge_field = (By.XPATH, "//li[span[normalize-space(text())='Linehaul Charge']]/span[contains(@class,'fw-semi-bold')]", "Linehaul Charge field [Output]")
        self._output_fuel_field = (By.XPATH, "//li[span[normalize-space(text())='Fuel']]/span[contains(@class,'fw-semi-bold')]", "Fuel field [Output]")
        self._output_accessorials_field = (By.XPATH, "//li[span[normalize-space(text())='Accessorials']]/span[contains(@class,'fw-semi-bold')]", "Accessorials field [Output]")
        self._output_total_charge_field = (By.XPATH, "//li[span[normalize-space(text())='Total Charge']]/span[contains(@class,'fw-semi-bold')]", "Total Charge field [Output]")
        self._output_payment_status_field = (By.XPATH, "//li[span[normalize-space(text())='Payment status']]/span[contains(@class,'fw-semi-bold')]", "Payment status field [Output]")
        self._output_invoice_date_field = (By.XPATH, "//li[span[normalize-space(text())='Invoice Date']]/span[contains(@class,'fw-semi-bold')]", "Invoice Date field [Output]")
        self._output_check_number_field = (By.XPATH, "//li[span[normalize-space(text())='Check Number']]/span[contains(@class,'fw-semi-bold')]", "Check Number field [Output]")
        self._output_paid_amount_field = (By.XPATH, "//li[span[normalize-space(text())='Paid Amount']]/span[contains(@class,'fw-semi-bold')]", "Paid Amount field [Output]")
        self._output_invoice_number_field = (By.XPATH, "//li[span[normalize-space(text())='Invoice Number']]/span[contains(@class,'fw-semi-bold')]", "Invoice Number field [Output]")
        self._btn_pro_number_edit = (By.XPATH, "//span[@mattooltip='Edit Pro Number.']", "Pro Number edit button [Button]")
        #  Finance details-Accessorial fields
        self._txt_accessorials_title = (By.XPATH, "//financial-detail-tab//shipment-request-accessorials-list//h4", "Accessorials title + amount of records (#) [Text]")
        self._txt_accessorials_amount_accessorial = (By.XPATH, "//span[@class='accessorialCount']", "Amount of records (#) [Text]")
        self._txt_accessorial_date = (By.XPATH, "//th[contains(@class,'cdk-column-dateCreated')]", "Date field [Text]")
        self._txt_accessorial_status = (By.XPATH, "//th[contains(@class,'cdk-column-accessorialStatus')]", "Status field [Text]")
        self._txt_accessorial_amount = (By.XPATH, "//th[contains(@class,'cdk-column-accessorialTypeDisplayValue')]", "Accessorial Type field [Text]")
        self._txt_accessorial_type = (By.XPATH, "//th[contains(@class,'cdk-column-totalCharge')]", "Amount field [Text]")
        self._txt_accessorial_documents = (By.XPATH, "//th[contains(@class,'cdk-column-documents ')]", "Documents field [Text]")
        self._txt_accessorial_description = (By.XPATH, "//th[contains(@class,'cdk-column-accessorialChargeType')]", "Description field [Text]")
        #  Finance details-Accessorial values
        self._txt_accessorial_no_records_found = (By.XPATH, "//shipment-request-accessorials-list//table//tr[1]/td[1]", "No records found [Text]")
        self._txt_accessorial_date_value = (By.XPATH, "//td[contains(@class, 'cdk-column-dateCreated')]", "Date value [Text]")
        self._txt_accessorial_status_value = (By.XPATH, "//td[contains(@class, 'cdk-column-accessorialStatus')]", "Status value [Text]")
        self._txt_accessorial_type_value = (By.XPATH, "//td[contains(@class, 'cdk-column-accessorialTypeDisplayValue')]", "Type value [Text]")
        self._txt_accessorial_amount_value = (By.XPATH, "//td[contains(@class, 'cdk-column-totalCharge')]", "Amount value [Text]")
        self._txt_accessorial_documents_value = (By.XPATH, "//td[contains(@class, 'cdk-column-documents')]", "Documents value [Text]")
        self._txt_accessorial_description_value = (By.XPATH, "//span[contains(text(), 'successfully submitted')]")

        self._load_by_load_number = "//div[contains(@class,'a-load-list')]//span[contains(text(), '{load_number}')]"

        #  Tabs: Shipment Details, Tracking Details, Finance Details, Documents, Stop Details, Hazmat Details, Audi Trail
        self._tab_shipment_details = (By.XPATH, "//a[contains(text(),'Shipment Details')]", "Shipment Details tab [Tab]")
        self._tab_tracking_details = (By.XPATH, "//a[contains(text(),'Tracking Details')]", "Tracking Details tab [Tab]")
        self._tab_finance_details = (By.XPATH, "//a[contains(text(),'Finance Details')]", "Finance details tab [Tab]")
        self._tab_documents = (By.XPATH, "//a[contains(text(),'Documents')]", "Documents tab [Tab]")
        self._tab_stop_details = (By.XPATH, "//a[contains(text(),'Stop Details')]", "Stop Details tab [Tab]")
        self._tab_hazmat_details = (By.XPATH, "//a[contains(text(),'Hazmat Details')]", "Hazmat Details tab [Tab]")
        self._tab_audit_details = (By.XPATH, "//a[contains(text(),'Audit Trails')]", "Audit Trail tab [Tab]")

        self._load_by_load_number = "//div[contains(@class,'a-load-list')]//span[contains(text(), '{load_number}')]"
        self._origin_bad_address_icon = "//span[contains(text(),'Pre-Scheduled Appointment')]/ancestor::div[contains(@class,'address-column')][1]//img[contains(@class,'bad-address')]"
        self._destination_bad_address_icon = "//span[contains(text(),'Pre-Scheduled Appointment')]/ancestor::div[contains(@class,'address-column')][2]//img[contains(@class,'bad-address')]"
        self._bad_address_tooltip = "//div[@role='tooltip' and contains(text(), 'We were unable to validate 1 or more of these addresses. For validation, please reach out to your Crowley representative for assistance.')]"
        self._no_load_message = (By.XPATH, "//div[contains(@class,'no-load')]/h5", "No Load Messages")

        # Tabs Content
        self.tab_shipment_details = ShipmentDetailsTab.get_instance()
        self.tab_tracking_details = TrackingDetailsTab.get_instance()
        self.tab_finance_details = FinanceDetailsTab.get_instance()
        self.tab_documents = DocumentsTab.get_instance()
        self.tab_stops_details = StopDetailsTab.get_instance()
        self.tab_hazmat_details = HazmatDetailsTab.get_instance()
        self.tab_audit_details = AudiTrailTab.get_instance()

        # Components
        self.upload_information_update = LoadInformationUpdatePage.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = MyLoadsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def enter_search_by(self, search_by: str):
        self.send_keys().set_locator(self._input_search_by, self._name).clear().set_text(search_by).pause(2)

        return self

    def click_search(self):
        self.click().set_locator(self._button_search, self._name).single_click().pause(2)
        return self

    def click_filter(self):
        locator = (By.XPATH, "//button/span[text()='Filter']/..", "Click Filter [Button]")
        self.click().set_locator(locator, self._name).single_click().pause(3)
        return self

    def checkbox_include_closed(self):
        self.click().set_locator(self._checkbox_include_close, self._name).single_click().pause(1)
        return self

    def click_sort_by_ship_date(self):
        self.click().set_locator(self._button_sort_by_ship_date, self._name).single_click()
        return self

    def get_ship_dates(self):
        date_elements = self.driver.find_elements_by_css_selector("//h5[contains(text(), 'Sorry, we couldn't find any results.')]")
        return [el.text for el in date_elements]

    def get_text_results(self, expected_text="Sorry, we couldn't find any results."):
        result_elements1 = self.driver.find_elements(By.XPATH, '//h5[contains(text(), "Sorry, we couldn\'t find any results.")]')
        return any(expected_text in el.text for el in result_elements1)

    def click_sort_by_status(self):
        self.click().set_locator(self._button_sort_by_status, self._name).single_click()
        return self

    def click_sort_by_origin(self):
        self.click().set_locator(self._button_sort_by_origin, self._name).single_click()
        return self

    def get_total_records(self):
        self.element().is_present(self._text_total_records, 5)
        text = self.get_text().set_locator(self._text_total_records, self._name).by_text()
        text = str(text.replace("Total records: ", "")).strip()
        return int(text)

    def click_track_record_item(self, index: int):
        xpath = f"({self._list_container})[{str(index)}]"
        locator = (By.XPATH, xpath, f"Track Record [{str(index)}]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def center_item_list(self, index: int = 1):
        locator = (By.XPATH, f"(//div[contains(@class, 'listingSide')]//div[@class='row']//div[contains(@class,'mainList')])[{index}]", "Item List Container")
        self.scroll().set_locator(locator=locator).to_element(pixels=-100)
        return self

    def get_track_status(self, index: int = 1):
        xpath = f"(//div[contains(@class, 'listingSide')]//div[@class='row']//div[contains(@class, 'parent-track-status')]/div[1])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Track Status [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).pause(2).by_text()

    def get_multi_stop(self, index: int = 1):
        xpath = f"(//div[contains(@class, 'listingSide')]//div[@class='row']//div[contains(@class, 'parent-track-status')]/div[2])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Track Status [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).pause(2).by_text()

    def get_letter_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[1]/span)[{str(index)}]"
        locator = (By.XPATH, xpath, f"Letter Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_carrier_name_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[1]/div/div/span[1])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Carrier Name Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_carrier_number_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[1]/div/div/span[2])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Carrier Number Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def get_equipment_type(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]//span[contains(@class, 'equipment')])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Equipment Type [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def get_origin_address_title_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span/span)[{str(index)}]"
        locator = (By.XPATH, xpath, f"Origin Address Title Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_destination_address_title_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span/span)[{str(index)}]"
        locator = (By.XPATH, xpath, f"Destination Address Title Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_origin_datetime_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span[2])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Origin Datetime Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_destination_datetime_track(self, index: int):
        xpath = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span[2])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Destination Datetime Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_origin_address_details_track(self, index: int):
        xpath_address_name = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span/span)[{str(index)}]"
        locator_address_name = (By.XPATH, xpath_address_name, f"Origin Address Track: Type [{str(index)}]")

        xpath_type = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span/div/div/span[1])[{str(index)}]"
        locator_type = (By.XPATH, xpath_type, f"Origin Address Track: Type [{str(index)}]")

        xpath_line_1 = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span/div/div/span[2])[{str(index)}]"
        locator_l1 = (By.XPATH, xpath_line_1, f"Origin Address Track: Line 1 [{str(index)}]")

        xpath_line_2 = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span/div/div/span[3])[{str(index)}]"
        locator_l2 = (By.XPATH, xpath_line_2, f"Origin Address Track: Line 2 [{str(index)}]")

        xpath_line_3 = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[2]/span/div/div/span[4])[{str(index)}]"
        locator_l3 = (By.XPATH, xpath_line_3, f"Origin Address Track: Line 3 [{str(index)}]")

        # Mouse Over Origin Address Name to Show Tool Tip Address Details
        self.click().set_locator(locator_address_name, self._name).mouse_over()

        details = {
            "type": self.get_text().set_locator(locator_type, self._name).by_text(),
            "line_1": self.get_text().set_locator(locator_l1, self._name).by_text(),
            "line_2": self.get_text().set_locator(locator_l2, self._name).by_text(),
            "line_3": self.get_text().set_locator(locator_l3, self._name).by_text()
        }
        return details

    def get_destination_address_details_track(self, index: int):
        xpath_address_name = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span/span)[{str(index)}]"
        locator_address_name = (By.XPATH, xpath_address_name, f"Destination Address Track: Type [{str(index)}]")

        xpath_type = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span/div/div/span[1])[{str(index)}]"
        locator_type = (By.XPATH, xpath_type, f"Destination Address Track: Type [{str(index)}]")

        xpath_line_1 = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span/div/div/span[2])[{str(index)}]"
        locator_l1 = (By.XPATH, xpath_line_1, f"Destination Address Track: Line 1 [{str(index)}]")

        xpath_line_2 = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span/div/div/span[3])[{str(index)}]"
        locator_l2 = (By.XPATH, xpath_line_2, f"Destination Address Track: Line 2 [{str(index)}]")

        xpath_line_3 = f"({str(self._list_container)}//div[contains(@class,'minus')]/div[3]/span/div/div/span[4])[{str(index)}]"
        locator_l3 = (By.XPATH, xpath_line_3, f"Destination Address Track: Line 3 [{str(index)}]")

        # Mouse Over Origin Address Name to Show Tool Tip Address Details
        self.click().set_locator(locator_address_name, self._name).mouse_over()

        details = {
            "type": self.get_text().set_locator(locator_type, self._name).by_text(),
            "line_1": self.get_text().set_locator(locator_l1, self._name).by_text(),
            "line_2": self.get_text().set_locator(locator_l2, self._name).by_text(),
            "line_3": self.get_text().set_locator(locator_l3, self._name).by_text()
        }
        return details

    def get_card_track_information(self, index: int):
        return {
            "status": self.get_track_status(index),
            "letter_track":  self.get_letter_track(index),
            "carrier_name": self.get_carrier_name_track(index),
            "carrier_number": self.get_carrier_number_track(index),
            "equipment_type": self.get_equipment_type(index),
            "origin_address_title": self.get_origin_address_title_track(index),
            "destination_address_title": self.get_destination_address_title_track(index),
            "origin_datetime_track": self.get_origin_datetime_track(index),
            "origin_address_details_track": self.get_origin_address_details_track(index),
            "destination_datetime_track": self.get_destination_datetime_track(index),
            "destination_address_details_track": self.get_destination_address_details_track(index)
        }

    def no_load_results(self):
        try:
            element = self.element().wait(self._noload, 5)
            return element is not None
        except Exception as e:
            logger.error(f"{e.msg}")
            return False

    def get_shipment_tracker(self, index: int):
        xpath = f"({self._list_container}//span[contains(@class, 'text-primary') and contains(@class, 'fw-medium')])[{str(index)}]"
        locator = (By.XPATH, xpath, "Shipment Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    @allure.step("Check if 'Sort by Status' button is visible")
    def ship_date_sort_is_present(self):
        return self.element().set_locator(self._button_sort_by_ship_date, self._name).is_visible()

    @allure.step("Check if 'Sort by Status' button is visible")
    def status_sort_is_present(self):
        return self.element().set_locator(self._button_sort_by_status, self._name).is_visible()

    @allure.step("Check if 'Sort by Origin' button is visible")
    def origin_sort_is_present(self):
        return self.element().set_locator(self._button_sort_by_origin, self._name).is_visible()

    @allure.step("Get Result Message")
    def validate_accessorial_popup(self):
        return self.get_text().set_locator(self._confirmation_request_text, self._name).by_text()

    @allure.step("Get Message")
    def validate_load_not_found(self):
        return self.get_text().set_locator(self._lbl_load_no_found, self._name).by_text()

    @allure.step("Get Result Message")
    def validate_single_closed_load(self):
        return self.get_text().set_locator(self._msg_closed_load, self._name).by_text()

    @allure.step("Get Message")
    def validate_single_load(self):
        return self.get_text().set_locator(self._lbl_load_no_found, self._name).by_text()

    def click_update_status_button(self):
        self.click().set_locator(self._btn_status_tag, self._name).single_click()
        return self

    def click_update_load_info_button(self):
        self.click().set_locator(self._btn_status_load_info_tag, self._name).single_click()
        return self

    # create is complete delivery method

    def is_complete_delivery_button_visible(self):
        return self.element().is_present(locator=self._btn_complete_delivery, timeout=5)

    # click complete delivery button method
    def click_complete_delivery_button(self):
        self.click().set_locator(self._btn_complete_delivery, self._name).single_click()
        return self

    def click_finance_details_tab(self):
        self.click().set_locator(self._tab_finance_details, self._name).single_click()
        return self

    def click_finance_details_modal(self):
        self.click().set_locator(self._txt_linehaul_charge_field, self._name).single_click()
        return self

    def are_finance_fields_visible(self):
        fields = [
            self._txt_linehaul_charge_field,
            self._txt_fuel_field,
            self._txt_accessorials_field,
            self._txt_total_charge_field,
            self._txt_payment_status_field,
            self._txt_invoice_date_field,
            self._txt_check_number_field,
            self._txt_paid_amount_field,
            self._txt_invoice_number_field,
            self._txt_pro_number_field,
            self._btn_pro_number_edit
        ]

        return self.element().are_fields_visible(elements_to_validate=fields, page=self._name)

    def are_accessorial_fields_visible(self):
        fields = [
            self._txt_accessorial_date,
            self._txt_accessorial_status,
            self._txt_accessorial_amount,
            self._txt_accessorial_type,
            self._txt_accessorial_documents,
        ]
        return self.element().are_fields_visible(elements_to_validate=fields, page=self._name)

    def are_accessorial_values_visible(self):
        fields = [
            self._txt_accessorial_date_value,
            self._txt_accessorial_status_value,
            self._txt_accessorial_type_value,
            self._txt_accessorial_amount_value,
            self._txt_accessorial_documents_value,
        ]
        return self.element().are_fields_visible(elements_to_validate=fields, page=self._name)

    def validate_accessorial_amount(self):
        return self.get_text().set_locator(self._txt_accessorials_amount_accessorial, self._name).by_text()

    def validate_and_check_accessorials(self):
        try:
            # "Get the text from the element that shows if there are any records."
            element = self.element().set_locator(self._txt_accessorial_no_records_found, self._name)
            text = element.get_text().strip().lower()

            # Validate if the text shows that no records are available and validates fields.
            if "no records found" in text:
                # Verify columns
                fields_ok = self.are_accessorial_fields_visible()
                return {
                    "status": fields_ok,
                    "message": "Accessorial columns validation failed." if not fields_ok else "Accessorial columns are present.",
                    "source": "Columns"
                }
            else:
                #  Verify values after verifying if values are present.
                values_ok = self.are_accessorial_values_visible()
                return {
                    "status": values_ok,
                    "message": "Accessorial values validation failed." if not values_ok else "Accessorial values are present.",
                    "source": "Values"
                }
        except Exception as e:
            return {
                "status": False,
                "message": f"Exception during accessorials validation: {str(e)}",
                "source": "Exception"
            }

    def get_text_no_records_found(self):
        return self.get_text().set_locator(self._txt_accessorial_no_records_found, self._name).by_text()

    def scroll_to_linehaul_charge(self):
        self.scroll().set_locator(self._txt_linehaul_charge_field, page=self._name) \
            .to_element(pixels=-100)

    def get_charge_comparison(self):
        # Get all values as text
        linehaul = self.get_text().set_locator(self._output_linehaul_charge_field, self._name).by_text()
        fuel = self.get_text().set_locator(self._output_fuel_field, self._name).by_text()
        accessorials = self.get_text().set_locator(self._output_accessorials_field, self._name).by_text()
        total = self.get_text().set_locator(self._output_total_charge_field, self._name).by_text()
        # Convert to float
        linehaul_value = float(linehaul.replace("$", ""))
        fuel_value = float(fuel.replace("$", ""))
        accessorials_value = float(accessorials.replace("$", ""))
        total_value = float(total.replace("$", ""))
        # Generate the operation
        calculated_sum = linehaul_value + fuel_value + accessorials_value
        is_correct = abs(calculated_sum - total_value) < 0.01
        # Show all values in console
        print("Comparison financial values:")
        print(f"  Linehaul:      {linehaul_value}")
        print(f"  Fuel:          {fuel_value}")
        print(f"  Accessorials:  {accessorials_value}")
        print(f"  Sum:           {calculated_sum}")
        print(f"  Total Charge:  {total_value}")
        print(f"  Matches?: {'Yes' if is_correct else 'No'}")
        # Return a dictionary
        return {
            "linehaul": linehaul_value,
            "fuel": fuel_value,
            "accessorials": accessorials_value,
            "total_displayed": total_value,
            "calculated_sum": calculated_sum,
            "correct": is_correct
        }

    def click_tab_shipment(self):
        self.click().set_locator(self._tab_shipment_details).single_click()
        return self

    def click_tab_tracking_details(self):
        self.click().set_locator(self._tab_tracking_details).single_click()
        return self

    def click_tab_finance_details(self):
        self.click().set_locator(self._tab_finance_details).single_click()
        return self

    def click_tab_documents(self):
        self.click().set_locator(self._tab_documents).single_click()
        return self

    def click_tab_stop_details(self):
        self.click().set_locator(self._tab_stop_details).single_click()
        return self

    def click_tab_hazmat_details(self):
        self.click().set_locator(self._tab_hazmat_details).single_click()
        return self

    def click_tab_audit_trail(self):
        self.click().set_locator(self._tab_audit_details).single_click()
        return self

    @allure.step("Validate Load Present")
    def validate_load_present(self, load_number):
        self.driver.find_element(By.XPATH, self._load_by_load_number.format(load_number=load_number))
        return self

    @allure.step("Select Load")
    def select_load(self, load_number):
        locator = By.XPATH, self._load_by_load_number.format(load_number=load_number)
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Validate Origin Bad Address Icon Present")
    def validate_origin_bad_address_icon_present(self):
        locator = By.XPATH, self._origin_bad_address_icon
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        return self

    @allure.step("Move Over Origin Bad Address Icon")
    def move_over_origin_bad_address_icon(self):
        locator = By.XPATH, self._origin_bad_address_icon
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        self.click().set_locator(locator, self._name).mouse_over()
        return self

    @allure.step("Validate Origin Bad Address Tooltip")
    def validate_bad_address_tooltip(self):
        locator = By.XPATH, self._bad_address_tooltip
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        return self

    @allure.step("Validate Destination Bad Address Icon Present")
    def validate_destination_bad_address_icon_present(self):
        locator = By.XPATH, self._destination_bad_address_icon
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        return self

    @allure.step("Move Over Destination Bad Address Icon")
    def move_over_destination_bad_address_icon(self):
        locator = By.XPATH, self._destination_bad_address_icon
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        self.click().set_locator(locator, self._name).mouse_over()
        return self

    @allure.step("Move Over Destination Bad Address Icon")
    def get_no_load_message(self):
        self.element().is_present(self._no_load, 5)
        return self.get_text().set_locator(self._no_load_message).by_text()

    def is_not_visible_no_load_message(self):
        return self.element().is_not_visible(locator=self._no_load_message, timeout=3)

    def click_clear_filter(self):
        locator = (By.XPATH, "//a[text()='Clear filter']", "Clear Filter [Link Action]")
        self.click().set_locator(locator).single_click().pause(3)
        return self

    @allure.step("Get Pagination Information")
    def get_pagination_info(self) -> dict:
        """
        Extracts and returns pagination details as a dictionary.

        Returns:
            dict: {
                'start_record': int,
                'end_record': int,
                'total_records': int,
                'page_size': int (calculated)
            }
        """
        locator = (By.XPATH, "//div[contains(@class, 'paginator-range')]/div", "Paginator Range Text")

        # Get text using your framework's element method
        paginator_text = self.get_text().set_locator(locator=locator).by_text().strip()

        # Extract numbers with regex
        numbers = re.findall(r'\d+', paginator_text)

        if len(numbers) < 3:
            logger.error(f"Could not parse pagination: '{paginator_text}'")
            return {}

        start_record = int(numbers[0])
        end_record = int(numbers[1])
        total_records = int(numbers[2])

        # Calculate page size
        page_size = end_record - start_record + 1

        result = {
            'start_record': start_record,
            'end_record': end_record,
            'total_records': total_records,
            'page_size': page_size
        }

        logger.info(f"Pagination: {result}")
        return result
