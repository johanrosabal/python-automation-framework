import allure
from datetime import datetime
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from applications.web.loadiq.common.LoadIQPage import LoadIQPage
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = setup_logger('ShipmentTrackingPage')


class ShipmentTrackingPage(BasePage):

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
        self._input_search_by1 = (By.XPATH, "//input[@type='text' and contains(@placeholder,'Search by Load Number')]","Search by [Input]")
        self._btn_button_search1 = (By.XPATH, "//button[contains(@mattooltip,'Search')]","Search by [Button]")
        self._checkbox_include_close1 = (By.XPATH, "//input[@id='switchViewClosedLoads']","Include Close [Checkbox]")
        self._btn_button_sort_by_ship_date1 = (By.XPATH, "//span[contains(text(), 'Ship date')]","Sort by ship date [Button]")
        self._btn_button_sort_by_status1 = (By.XPATH, "//span[contains(text(), 'Status')]","Sort by status [Button]")
        self._btn_button_sort_by_origin1 = (By.XPATH, "//span[@class='input-group-text cursor-pointer' and normalize-space(text())='Origin']","Sort by Origin [Button]")
        self._text_total_records1 = (By.XPATH, "//span[contains(text(),'Total records:')]","Get total records [Output]")
        self._list_container1 = "//div[contains(@class,'listingSide')]","List loads [Select]"
        self._text_role_type = (By.XPATH, "//div[@class='pull-left']/span[@class='fw-bold']", "Get role type record [Output]")
        self._txt_stop_details_tab = (By.XPATH, "//*[@id='ngb-nav-3']", "Get text type tab [Text]")
        self._btn_closed_records = (By.XPATH, "//app-submitted-shipments//label[1]/div", "Closed records button [Button]")
        self._modal_stop_details = (By.XPATH, "//h4[contains(text(), 'Stop Details')]", "Stop Details [Modal]")
        self._tab_document_details = (By.XPATH, "//*[@id='ngb-nav-2']", "Docuement Details [Tab]")
        self._msg_stop_details_modal_tittle = (By.XPATH, "//app-shipment-detail//h4", "Stop details tittle (modal) [OutPut]")
        self._btn_view_image = (By.XPATH, "//app-upload-bol//table//tbody//tr//td[6]","View image button [Tab]")
        self._btn_cancel_order = (By.XPATH, "//span[contains(text(), 'Cancel')]","Cancel button [Button]")
        self._btn_cancel_order_screen= (By.XPATH, "//app-shipment-cancel-popup//div[2]//button[1]","Cancel button pop-up[Button]")
        self._msg_cancel_confirmation= (By.XPATH, "//span[@class='mat-simple-snack-bar-content']","Cancel button pop-up confirmation[Output]")
        self._msg_stop_details_modal_tittle = (By.XPATH, "//app-shipment-detail//h4", "Stop details tittle (modal) [Out]")
        self._btn_download_image = (By.XPATH, "//app-upload-bol//table//tbody//tr//td[7]", "View download button [Tab]")
        #Load list
        self._tbl_loads = (By.XPATH, "//div[contains(@class,'load-list')]", "Search a load number [Output]")
        self._btn_edit_booking_number  = (By.XPATH, "//span[contains(@class, 'iq-icon--edit')]", "Edit booking number [Button]")
        self._input_booking_number = (By.XPATH, "//app-update-pickup-number//input", "Enter booking number [Field/Input]")
        self._msg_update_confirmation = (By.XPATH, "//div[@matsnackbarlabel]", "Warning confirmation [Output]")
        self._btn_edit_booking_number_update = (By.XPATH, "//button[.//span[text()='Update']]", "Click booking number update [Button]")
        self._img_logo_hazmat=	By.XPATH, ("//app-submitted-shipments//ul/li/span", "Hazmat logo [Logo]")
        #Hazmat tab
        self._tbl_freight_item  = (By.XPATH, "//hazmat-detail-tab//table//th[1]//a", "Hazmat freight item [Text]")
        self._tbl_un_na_number  = (By.XPATH, "//hazmat-detail-tab//table//th[2]//a", "Hazmat UN/NA Number  [Text]")
        self._tbl_hazmat_class  = (By.XPATH, "//hazmat-detail-tab//table//th[3]//a", "Hazmat Hazmat Class  [Text]")
        self._tbl_packing_group  = (By.XPATH, "//hazmat-detail-tab//table//th[4]//a", "Hazmat Packing Group  [Text]")
        self._tbl_phone  = (By.XPATH, "//hazmat-detail-tab//table//th[5]//a", "Hazmat phone[Text]")
        self._tbl_proper_shipping_name  = (By.XPATH, "//hazmat-detail-tab//table//th[6]//a", "Hazmat Proper Shipping Name data[Text]")
        self._tbl_freight_item_data  = (By.XPATH, "//table//td[1]", "Hazmat freight item data[Output]")
        self._tbl_un_na_number_data  = (By.XPATH, "//table//td[2]", "Hazmat UN/NA Number data[Output]")
        self._tbl_hazmat_class_data  = (By.XPATH, "//table//td[3]", "Hazmat Hazmat Class data[Output]")
        self._tbl_packing_group_data  = (By.XPATH, "//table//td[4]", "Hazmat Packing Group data[Output]")
        self._tbl_phone_data = (By.XPATH, "//table//td[5]", "Hazmat phone data[Output]")
        self._tbl_proper_shipping_name_data  = (By.XPATH, "//table//td[6]", "Hazmat Proper Shipping Name data[Output]")
        self._tbl_hazmat_details = (By.XPATH, "//app-shipment-detail//hazmat-detail-tab", "Hazmat Table[Table]")
        self._tab_hazmat_details = (By.XPATH, "//app-shipment-detail//ul/li[6]/a", "Hazmat Proper Shipping Name data[Output]")
        self._tbl_shipment_id_data= (By.XPATH, "//div[@class='load-number-text']", "Shipment ID[Output]")
        self._tab_shipment_details = (By.XPATH, "//app-submitted-shipments//app-shipment-detail//ul/li[1]/a", "Shipment details tab[Tab]")
        #Feeback option
        self._input_feedback_comment = (By.XPATH, "//div[@class='note-editable']","Feedback comment[Input]")
        self._lbl_feedback_confirmation = (By.XPATH, "//div[contains(text(), 'Feedback submitted successfully')]", "Feedback confirmation[Label]",)
        self._btn_feedback_cancel = (By.XPATH, "/html/body/app-root/app-feedback-form/div[2]/form/div[2]/div/button[2]", "Feedback cancel button[Button]")
        self._btn_feedback_submit = (By.XPATH, "/html/body/app-root/app-feedback-form/div[2]/form/div[2]/div/button[1]", "Feedback submit button[Button]")
        self._btn_feedback = (By.XPATH, "/html/body/app-root/app-feedback-form/div[1]/button", "Feedback button[Button]")
        #Finance details
        self._tab_finance_details = (By.XPATH, "//app-shipment-detail//ul/li[3]/a", "Finance details[Tab]")
        self._tbl_fuel_field = (By.XPATH, "//financial-detail-tab//ul/li[2]/span[1]", "Text fuel text[Field]")
        self._tbl_fuel_item_data = (By.XPATH, "//financial-detail-tab//ul/li[2]/span[2]", "Fuel data[Data]")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = ShipmentTrackingPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    @allure.step("Enter Search By: {search_by}")
    def enter_search_by(self, search_by: str):
        self.send_keys().set_locator(self._input_search_by1, self._name).clear().set_text(search_by)
        return self

    @allure.step("Click Search")
    def click_search(self):
        self.click().set_locator(self._btn_button_search1, self._name).single_click().pause(2)
        return self

    @allure.step("Check Include Closed")
    def checkbox_include_closed(self, value: bool):
        self.radio().set_locator(self._checkbox_include_close1, self._name).set_value(value)
        return self

    @allure.step("Click Ship date")
    def click_sort_by_ship_date(self):
        self.click().set_locator(self._btn_button_sort_by_ship_date1, self._name).single_click()
        return self

    @allure.step("Click Status")
    def click_sort_by_status(self):
        self.click().set_locator(self._btn_button_sort_by_status1, self._name).single_click()
        return self

    @allure.step("Click Origin")
    def click_sort_by_origin(self):
        self.click().set_locator(self._btn_button_sort_by_origin1, self._name).single_click()
        return self

    @allure.step("Click Closed button")
    def click_closed_button(self):
        self.click().set_locator(self._btn_closed_records, self._name).single_click()
        return self

    @allure.step("Click Stop details")
    def click_stop_details(self):
        self.click().set_locator(self._txt_stop_details_tab, self._name).single_click()
        return self

    @allure.step("Click document details")
    def click_document_details(self):
        self.click().set_locator(self._tab_document_details, self._name).single_click()
        return self

    @allure.step("Click view image")
    def click_view_image(self):
        self.click().set_locator(self._btn_view_image, self._name).single_click()
        return self

    @allure.step("Click download image")
    def click_download_image(self):
        self.click().set_locator(self._btn_download_image, self._name).single_click()
        return self

    @allure.step("Total Records")
    def get_total_records(self):
        return self.get_text().set_locator(self._text_total_records1, self._name).by_text()

    def click_track_record_item(self, index: int):
        xpath = f"({self._list_container1})[{str(index)}]"
        locator = (By.XPATH, xpath, f"Track Record [{str(index)}]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def get_origin_datetime_track(self, index: int):
        xpath = f"({str(self._list_container1)}/div/div[contains(@class,'minus')]/div[2]/span[2])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Origin Datetime Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_destination_datetime_track(self, index: int):
        xpath = f"({str(self._list_container1)}/div/div[contains(@class,'minus')]/div[3]/span[2])[{str(index)}]"
        locator = (By.XPATH, xpath, f"Destination Datetime Track [{str(index)}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_text_card_label(self):
        return self.get_text().set_locator(self._text_role_type, self._name).by_text().strip()

    def get_text_stop_details_tab(self):
        return self.get_text().set_locator(self._txt_stop_details_tab, self._name).by_text().strip()

    def is_stop_details_modal_present(self):
        try:
            return self.element().set_locator(self._modal_stop_details, self._name).is_visible()
        except Exception:
            return False

    def is_view_document_present(self):
        try:
            return self.element().set_locator(self._btn_view_image, self._name).is_visible()
        except Exception:
            return False

    def is_download_document_present(self):
        try:
            return self.element().set_locator(self._btn_download_image, self._name).is_visible()
        except Exception:
            return False

    def get_tracking_number(self, index: int):
        self.pause(10)
        xpath_base = self._tbl_loads[1]
        xpath = f"({xpath_base}//span[contains(@class,'text-primary fw-medium fnt-12 d-block')])[{index}]"
        locator = (By.XPATH, xpath, "Shipment Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    from datetime import datetime

    def update_booking_number(self):
        # Generate a booking update using timestamp
        new_booking_number = "Test" + datetime.now().strftime("%Y%m%d%H%M%S")
        # Click "Edit Booking Number" button
        self.click().set_locator(self._btn_edit_booking_number, self._name).single_click().pause()
        # Sent the new number
        self.send_keys().set_locator(self._input_booking_number, self._name).clear().set_text(new_booking_number)
        # Click "Update" button
        self.click().set_locator(self._btn_edit_booking_number_update, self._name).single_click().pause(5)

        return new_booking_number

    def get_current_booking_number(self):
        return self.get_text().set_locator(self._input_booking_number, self._name).read()

    def get_booking_number_update_confirmation(self):
        return self.get_text().set_locator(self._msg_update_confirmation, self._name).by_text().strip()

    def search_by_hazmat(self, search_by: str):
        self.send_keys().set_locator(self._input_search_by1, self._name).clear().set_text(search_by)
        self.click().set_locator(self._btn_button_search1, self._name).single_click().pause()
        return self

    def get_all_hazmat_column(self):
        # Visibility of the hazmat table
        if not self.element().set_locator(self._tbl_hazmat_details).is_visible():
            raise AssertionError("[ERROR] Hazmat table is not visible. Unable to extract the columns names.")
        # If the table is visible, ensure that all text fields are properly set , confirming no errors occurred while getting the text.
        def get_text(locator, column):
            try:
                text = self.get_text().set_locator(locator).by_text()
                return text.strip() if text else "[EMPTY]"
            except Exception as e:
                logger.error(f"Error obtaining the column name '{column}': {e}")
                return "[ERROR]"
        return {
            "Freight Item": get_text(self._tbl_freight_item, "Freight Item"),
            "UN/NA Number": get_text(self._tbl_un_na_number, "UN/NA Number"),
            "Hazmat Class": get_text(self._tbl_hazmat_class, "Hazmat Class"),
            "Packing Group": get_text(self._tbl_packing_group, "Packing Group"),
            "Phone": get_text(self._tbl_phone, "Phone"),
            "Proper Shipping Name": get_text(self._tbl_proper_shipping_name, "Proper Shipping Name")
        }


    def click_hazmat_tab(self):
        self.click().set_locator(self._tab_hazmat_details, self._name).single_click()
        return self

    def get_all_hazmat_information(self):
        hazmat_locators = {
            "shipment_id": self._tbl_shipment_id_data,
            "un_na_number": self._tbl_un_na_number_data,
            "hazmat_class": self._tbl_hazmat_class_data,
            "hazmat_contact_number": self._tbl_phone_data,
            "packing_group": self._tbl_packing_group_data,
            "proper_shipping_name": self._tbl_proper_shipping_name_data
        }
        return {
            key: self.get_text().set_locator(locator, self._name).by_text()
            for key, locator in hazmat_locators.items()
        }

    def get_feedback_confirmation_message(self):
        return self.get_text().set_locator(self._lbl_feedback_confirmation, self._name).by_text()

    def send_feedback(self, text):
        self.click().set_locator(self._btn_feedback, self._name).single_click().pause()
        self.send_keys().set_locator(self._input_feedback_comment, self._name).clear().set_text(text)
        self.click().set_locator(self._btn_feedback_submit, self._name).single_click().pause(5)
        return self

    def get_fuel_info(self):
        fuel_text = self.get_text().set_locator(self._tbl_fuel_field, self._name).by_text()
        fuel_value = self.get_text().set_locator(self._tbl_fuel_item_data, self._name).by_text()
        return {"label": fuel_text, "value": fuel_value}

    def click_finance_details_tab(self):
        self.click().set_locator(self._tab_finance_details, self._name).single_click()
        return self

    def click_shipment_details_tab(self):
        self.click().set_locator(self._tab_shipment_details, self._name).single_click()
        return self