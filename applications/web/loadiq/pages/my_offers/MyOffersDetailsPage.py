import allure
from selenium.webdriver.common.by import By
from pathlib import Path
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from selenium.webdriver.common.keys import Keys
from core.utils.table_formatter import TableFormatter

logger = setup_logger('MyOffersDetailsPage')


class MyOffersDetailsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the MyOffersDetailsPage instance.
        """
        super().__init__(driver)
        # Driver

        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/my-offers"


        # --- Offert details view locators---
        # These are using before clicking to expand an offer.
        details_container = "//div[contains(@class, 'load-detail-holder')]"
        # Hazmat Details
        self.txt_hazmat_details = (By.XPATH, f"{details_container}//h4[text()='Hazmat Details']", "Details - Hazmat Details [Text]")
        self._txt_hazmat_un_details = (By.XPATH, f"{details_container}//span[contains(., 'UN')]/following-sibling::span", "Details - Hazmat UN [Text]")
        self._txt_hazmat_class_details = (By.XPATH, f"{details_container}//span[contains(., 'Hazmat Class')]/following-sibling::span", "Details - Hazmat Class [Text]")
        self._txt_hazmat_packing_group_details = (By.XPATH, f"{details_container}//span[contains(., 'Packing Group')]/following-sibling::span", "Details - Packing Group [Text]")
        self._txt_hazmat_phone_details = (By.XPATH, f"{details_container}//span[contains(., 'Phone')]/following-sibling::span", "Details - Hazmat Phone [Text]")
        self._txt_hazmat_proper_shipping_name_details = (By.XPATH, f"{details_container}//span[contains(., 'Proper Shipping Name')]/following-sibling::span", "Details - Proper Shipping Name [Text]")

        # Description and Instructions
        self._txt_commodity_description_details = (By.XPATH, f"{details_container}//h4[text()='Commodity Description']/following-sibling::p", "Details - Commodity Description [Text]")
        self._txt_shipment_instructions_details = (By.XPATH, f"{details_container}//h4[text()='Shipment Instructions']/following-sibling::p", "Details - Shipment Instructions [Text]")

        # Appointment Dates
        self._txt_origin_appointment_details = (By.XPATH, f"{details_container}//h4[text()='Appointment Date at Origin']/following-sibling::p", "Details - Origin Appointment [Text]")
        self._txt_destination_appointment_details = (By.XPATH, f"{details_container}//h4[text()='Appointment Date at Destination']/following-sibling::p", "Details - Destination Appointment [Text]")

        # Load Value
        self._txt_load_value_linehaul_details = (By.XPATH, f"{details_container}//p[contains(text(), 'Linehaul:')]", "Details - Linehaul Value [Text]")
        self._txt_load_value_fuel_details = (By.XPATH, f"{details_container}//p[contains(text(), 'Fuel:')]", "Details - Fuel Value [Text]")
        self._txt_load_value_accessorials_details = (By.XPATH, f"{details_container}//p[contains(text(), 'Accessorials:')]", "Details - Accessorials Value [Text]")

        # Action Buttons
        self._btn_bid_details = (By.XPATH, f"{details_container}//button[normalize-space()='Bid']", "Details - Bid [Button]")
        self._btn_book_now_details = (By.XPATH, f"{details_container}//button[normalize-space()='Book Now']", "Details - Book Now [Button]")
        self._btn_update_bid_details = (By.XPATH, f"{details_container}//button[normalize-space()='Update Bid']", "Details - Bid [Button]")
        self._btn_withdraw_details = (By.XPATH, f"{details_container}//button[normalize-space()='Withdraw']", "Details - Bid [Button]")
        self._btn_accept_tender_details = (By.XPATH, f"{details_container}//button[normalize-space()='Accept Tender']", "Details - Accept Tender [Button]")
        self._btn_reject_tender_details = (By.XPATH, f"{details_container}//button[normalize-space()='Reject Tender']", "Details - Reject Tender [Button]")

        # --- Bid modal offers Locators ---
        # These are used AFTER clicking the 'Bid' button.
        bid_modal_container = "//div[contains(@class, 'modal-content')]"
        self._txt_title_bid_modal = (By.XPATH, f"{bid_modal_container}//h4[text()=' Bid']", "Bid Modal - Title [Text]")
        self._txt_shipment_no_bid_modal = (By.XPATH, f"{bid_modal_container}//label[contains(., 'Shipment #:')]/following-sibling::label", "Bid Modal - Shipment No. [Text]")
        self._txt_input_amount_bid_modal = (By.XPATH, f"{bid_modal_container}//input[@formcontrolname='totalBidAmount']", "Bid Modal - Bid Amount [Input]")
        self._txt_input_expiration_date_bid_modal = (By.XPATH, f"{bid_modal_container}//input[@formcontrolname='expirationDate']", "Bid Modal - Expiration Date [Input]")
        self._txt_input_time_hour_bid_modal = (By.XPATH, f"{bid_modal_container}//ngb-timepicker//input[@aria-label='Hours']", "Bid Modal - Time Hour [Input]")
        self._txt_input_time_minute_bid_modal = (By.XPATH, f"{bid_modal_container}//ngb-timepicker//input[@aria-label='Minutes']", "Bid Modal - Time Minute [Input]")
        self._txt_button_time_period_bid_modal = (By.XPATH, f"{bid_modal_container}//ngb-timepicker//button[contains(@class,'btn-outline-primary')]", "Bid Modal - AM/PM [Button]")
        self._select_select_equipment_bid_modal = (By.XPATH, f"{bid_modal_container}//mat-select[@formcontrolname='substituteEquipmentCode']", "Bid Modal - Equipment Substitution [Select]")
        self._toggle_toggle_auto_accept_bid_modal = (By.XPATH, f"{bid_modal_container}//input[@formcontrolname='autoAcceptTender']/following-sibling::div", "Bid Modal - Auto Accept Tender [Toggle]")
        self._btn_button_place_bid_bid_modal = (By.XPATH, f"{bid_modal_container}//button[contains(., 'Place Bid')]", "Bid Modal - Place Bid [Button]")

        # Locators for the 'Place Bid' Confirmation Modal
        self._txt_confirmation_message = (By.XPATH, "//span[contains(text(), 'Are you sure you want to place the bid?')]", "Confirmation Message [Text]")
        self._btn_yes_confirm = (By.XPATH, "//div[contains(@class, 'modal-body')]//button[.//span[text()='Yes']]", "Yes Confirmation [Button]")
        self._btn_no_cancel = (By.XPATH, "//div[contains(@class, 'modal-body')]//button[.//span[text()='NO']]", "No Cancel [Button]")

        # Locators for the 'Bid Success' Modal
        self._txt_success_message = (By.XPATH, "//mat-dialog-container//div[@class='htmlError']//div", "Success Message [Text]")
        self._btn_ok = (By.XPATH, "//mat-dialog-container//button[.//span[text()='OK']]", "OK Button [Button]")

        # --- Locators for the 'Update Bid' Modal ---
        # These are used AFTER clicking the 'Update bid' button.
        self._txt_title_update_bid_update_modal = (By.XPATH, "//div[@class='modal-header']//h4", "Update Bid Title [Text]")
        self._txt_shipment_number_update_modal = (By.XPATH, "//label[text()='Shipment #:&nbsp;']/following-sibling::label", "Shipment Number [Text]")
        self._input_bid_amount_update_modal = (By.XPATH, "//input[@formcontrolname='totalBidAmount']", "Bid Amount [Input]")
        self._input_expiration_date_update_modal = (By.XPATH, "//input[@formcontrolname='expirationDate']", "Expiration Date [Input]")
        self._select_equipment_substitution_update_modal = (By.XPATH, "//mat-select[@formcontrolname='substituteEquipmentCode']", "Equipment Substitution [Dropdown]")
        self._toggle_auto_accept_tender_update_modal = (By.XPATH, "//input[@formcontrolname='autoAcceptTender']", "Auto Accept Tender [Toggle]")
        self._btn_update_bid_submit_update_modal = (By.XPATH, "//div[@class='modal-footer']//button[contains(., 'Update Bid')]", "Update Bid Submit [Button]")
        self._btn_cancel_update_modal = (By.XPATH, "//div[@class='modal-footer']//button[contains(., 'Cancel')]", "Cancel [Button]")

        # --- Locators for the 'Accept Tender' Modal ---
        # These are used AFTER clicking the 'Accept Tender' button.

        # Modal Container
        self._modal_accept_tender = (By.CLASS_NAME, "modal-content", "Accept Tender Modal")

        # Close Button
        self._btn_close = (By.CSS_SELECTOR, "button[data-cy='closebtn']", "Close modal button [Icon]")

        # Texts
        self._txt_modal_title = (By.XPATH, "//h4[text()='Accept Tender']", "Modal Title [Text]")
        self._txt_bid_amount = (By.XPATH, "//span[contains(text(), 'Bid Amount:')]", "Bid Amount [Text]")
        self._txt_origin_location = (By.XPATH, "//li[contains(@class, 'accept-load--orgin')]//span", "Origin Location [Text]")
        self._txt_destination_location = (By.XPATH, "//li[contains(@class, 'accept-load--destination')]//span", "Destination Location [Text]")
        self._txt_date = (By.XPATH, "//div[contains(@class, 'accept-load--date')]//span", "Date [Text]")
        self._txt_alert_message = (By.XPATH, "//div[@aria-live='assertive']", "Alert Message [Text]")

        # Buttons
        self._btn_accept_tender_modal = (By.CSS_SELECTOR, "button[data-cy='accepttenderbtn']", "Accept Tender Button")
        self._btn_reject_tender_modal = (By.CSS_SELECTOR, "button[data-cy='declinetenderbtn']", "Reject Tender Button")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = MyOffersDetailsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    # =======================================   Methods for offer details view   =======================================
    def is_hazmat_details_displayed(self):
        try:
            return self.element().set_locator(self.txt_hazmat_details, self._name).is_visible()
        except:
            return False

    def get_hazmat_un_details_text(self):
        return self.get_text().set_locator(self._txt_hazmat_un_details, self._name).by_text()

    def get_hazmat_class_details_text(self):
        return self.get_text().set_locator(self._txt_hazmat_class_details, self._name).by_text()

    def get_hazmat_packing_group_details_text(self):
        return self.get_text().set_locator(self._txt_hazmat_packing_group_details, self._name).by_text()

    def get_hazmat_phone_details_text(self):
        return self.get_text().set_locator(self._txt_hazmat_phone_details, self._name).by_text()

    def get_hazmat_proper_shipping_name_details_text(self):
        return self.get_text().set_locator(self._txt_hazmat_proper_shipping_name_details, self._name).by_text()

    # dictionary with all hazmat details
    def get_hazmat_details(self):
        hazmat_details = {
            "UN": self.get_hazmat_un_details_text(),
            "Hazmat Class": self.get_hazmat_class_details_text(),
            "Packing Group": self.get_hazmat_packing_group_details_text(),
            "Phone": self.get_hazmat_phone_details_text(),
            "Proper Shipping Name": self.get_hazmat_proper_shipping_name_details_text()
        }
        return hazmat_details

    def get_commodity_description_details_text(self):
        return self.get_text().set_locator(self._txt_commodity_description_details, self._name).by_text()

    def get_shipment_instructions_details_text(self):
        return self.get_text().set_locator(self._txt_shipment_instructions_details, self._name).by_text()

    def get_origin_appointment_details_text(self):
        return self.get_text().set_locator(self._txt_origin_appointment_details, self._name).by_text()

    def get_destination_appointment_details_text(self):
        return self.get_text().set_locator(self._txt_destination_appointment_details, self._name).by_text()

        # dictionary with all hazmat details
    def get_appointment_dates(self):
        appointment_dates = {
            "pickup_Date": self.get_origin_appointment_details_text(),
            "delivery_Date": self.get_destination_appointment_details_text()
        }
        return appointment_dates

    def get_load_value_linehaul_details_text(self):
        return self.get_text().set_locator(self._txt_load_value_linehaul_details, self._name).by_text()

    def get_load_value_fuel_details_text(self):
        return self.get_text().set_locator(self._txt_load_value_fuel_details, self._name).by_text()

    def get_load_value_accessorials_details_text(self):
        return self.get_text().set_locator(self._txt_load_value_accessorials_details, self._name).by_text()

    def click_bid_details_button(self):
        self.click().set_locator(self._btn_bid_details, self._name).single_click().pause(2)
        return self

    def click_book_now_details_button(self):
        self.click().set_locator(self._btn_book_now_details, self._name).single_click()
        return self

    def click_update_bid_details_button(self):
        self.click().set_locator(self._btn_update_bid_details, self._name).single_click().pause(2)
        return self

    def click_withdraw_details_button(self):
        self.click().set_locator(self._btn_withdraw_details, self._name).single_click().pause(2)
        return self

    def click_accept_tender_details_button(self):
        self.click().set_locator(self._btn_accept_tender_details, self._name).single_click().pause(2)
        return self

    def click_reject_tender_details_button(self):
        self.click().set_locator(self._btn_reject_tender_details, self._name).single_click()
        return self

    # =====================================   Methods for bid modal interactions   =====================================
    def get_bid_modal_title_text(self):
        return self.get_text().set_locator(self._txt_title_bid_modal, self._name).by_text()

    def get_bid_modal_shipment_no_text(self):
        return self.get_text().set_locator(self._txt_shipment_no_bid_modal, self._name).by_text()

    def enter_bid_amount(self, amount: str):
        self.click().set_locator(self._txt_input_amount_bid_modal, self._name).single_click().pause(2)
        self.send_keys().set_locator(self._txt_input_amount_bid_modal, self._name).set_text(amount)
        return self

    def get_bid_amount_value(self):
        return self.get_text().set_locator(self._txt_input_amount_bid_modal, self._name).by_attribute("value")

    def enter_expiration_date(self, date: str):
        self.send_keys().set_locator(self._txt_input_expiration_date_bid_modal, self._name).clear().set_text(date)
        return self

    def get_expiration_date_value(self):
        return self.get_text().set_locator(self._txt_input_expiration_date_bid_modal, self._name).by_attribute(
                "value")

    def enter_time_hour(self, hour: str):
        self.send_keys().set_locator(self._txt_input_time_hour_bid_modal, self._name).clear().set_text(hour)
        return self

    def get_time_hour_value(self):
        return self.get_text().set_locator(self._txt_input_time_hour_bid_modal, self._name).by_attribute("value")

    def enter_time_minute(self, minute: str):
        self.send_keys().set_locator(self._txt_input_time_minute_bid_modal, self._name).clear().set_text(minute).set_text(Keys.TAB)
        return self

    def get_time_minute_value(self):
        return self.get_text().set_locator(self._txt_input_time_minute_bid_modal, self._name).by_attribute("value")

    def click_time_period_button(self):
        self.click().set_locator(self._txt_button_time_period_bid_modal, self._name).single_click().pause(4)
        return self

    def get_time_period_text(self):
        return self.get_text().set_locator(self._txt_button_time_period_bid_modal, self._name).by_text()

    def click_equipment_substitution_dropdown(self):
        self.click().set_locator(self._select_select_equipment_bid_modal, self._name).single_click()
        return self

    def toggle_auto_accept_tender(self):
        self.click().set_locator(self._toggle_toggle_auto_accept_bid_modal, self._name).single_click()
        return self

    def is_auto_accept_tender_enabled(self):
        try:
            checkbox_element = self.driver.find_element(*self._toggle_toggle_auto_accept_bid_modal[:2])
            return "checked" in checkbox_element.get_attribute("class") or checkbox_element.is_selected()
        except:
            return False

    def click_place_bid_button(self):
        self.click().set_locator(self._btn_button_place_bid_bid_modal, self._name).single_click().pause(4)
        return self

    def is_place_bid_button_enabled(self):
        try:
            return self.element().set_locator(self._btn_button_place_bid_bid_modal, self._name).is_enabled()
        except:
            return False
    # ===================================   END Methods for bid modal interactions   ===================================

    # =================================   Methods for Update Bid modal interactions   ==================================

    def get_confirmation_message_text(self):
        return self.get_text().set_locator(self._txt_title_update_bid_update_modal, self._name).by_text()

    def get_confirmation_message_text(self):
        return self.get_text().set_locator(self._txt_shipment_number_update_modal, self._name).by_text()

    def enter_input_update_bid_amount(self, minute: str):
        self.send_keys().set_locator(self._input_bid_amount_update_modal, self._name).clear().set_text(minute)
        return self

    def enter_time_minute_update_modal(self, minute: str):
        self.send_keys().set_locator(self._input_expiration_date_update_modal, self._name).clear().set_text(minute)
        return self

    def click_auto_accept_tender_place_bid_button_update_modal(self):
        self.click().set_locator(self._toggle_auto_accept_tender_update_modal, self._name).single_click().pause(4)
        return self

    def click_update_bid_button_update_modal(self):
        self.click().set_locator(self._btn_update_bid_submit_update_modal, self._name).single_click().pause(4)
        return self


    # ==============================   END Methods for Update Bid modal interactions   =================================

    # ================================== Methods for confirmation modal interactions ===================================
    def get_confirmation_message_text(self):
        return self.get_text().set_locator(self._txt_confirmation_message, self._name).by_text()

    def is_confirmation_message_displayed(self):
        try:
            return self.element().set_locator(self._txt_confirmation_message, self._name).is_visible()
        except:
            return False

    def click_yes_confirm_button(self):
        self.click().set_locator(self._btn_yes_confirm, self._name).single_click().pause(4)
        return self

    def click_no_cancel_button(self):
        self.click().set_locator(self._btn_no_cancel, self._name).single_click().pause(1)
        return self
    # ================================ END Methods for confirmation modal interactions =================================

    # ==================================== Methods for success message interactions ====================================
    def get_success_message_text(self):
        return self.get_text().set_locator(self._txt_success_message, self._name).by_text()

    def click_ok_button(self):
        self.click().set_locator(self._btn_ok, self._name).single_click().pause(1)
        return self
    # ================================== END Methods for success message interactions ==================================


    def get_modal_accept_tender_text(self):
        return self.get_text().set_locator(self._txt_modal_title, self._name).by_text()

    def get_modal_title_text(self):
        return self.get_text().set_locator(self._txt_modal_title, self._name).by_text()

    def get_modal_origin_location_text(self):
        return self.get_text().set_locator(self._txt_origin_location, self._name).by_text()

    def get_modal_destination_location_text(self):
        return self.get_text().set_locator(self._txt_destination_location, self._name).by_text()

    def get_modal_date_text(self):
        return self.get_text().set_locator(self._txt_date, self._name).by_text()

    def click_btn_accept_tender_modal(self):
        self.click().set_locator(self._btn_accept_tender_modal, self._name).single_click().pause(1)
        return self

    def click_btn_reject_tender_modal(self):
        self.click().set_locator(self._btn_reject_tender_modal, self._name).single_click().pause(1)
        return self

    def get_alert_message_text(self):
        return self.get_text().set_locator(self._txt_alert_message, self._name).by_text()