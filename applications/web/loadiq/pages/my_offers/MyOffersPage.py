import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage


logger = setup_logger('MyOffersPage')


class MyOffersPage(BasePage):

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
        self.relative = "/shipment/my-offers"

        # Locator definitions
        self._noload = (By.XPATH, "//h5[text()='Sorry, we couldn't find any results.']","Message [Output]")
        self._input_search_by = (By.XPATH, "//input[@type='text' and contains(@placeholder,'Search by')]","Search by [Input]")
        self._button_search = (By.XPATH, "//button[@mattooltip='Search']","Search by [Button]")
        self._checkbox_include_close = (By.XPATH, "//label[@for='switchViewClosedLoads'][1]", "Include Closed [Checkbox]")
        self._button_sort_by_ship_date = (By.XPATH, "//div/span[text()='Ship date']","Sort by ship date  [Button]")
        self._button_sort_by_status = (By.XPATH, "//div/span[text()='Status']","Sort by status  [Button]")
        self._button_sort_by_origin = (By.XPATH, "//div/span[text()='Origin']","Sort by origin [Button]")
        self._text_total_records = (By.XPATH, "//span[contains(@class, 'search-result')]", "Total Records [Text]")
        self._list_container = "//div[contains(@class, 'listingSide')]//div[@class='row']/div"
        self._get_ship_date="////span[normalize-space(.)='Ship date']/following-sibling::span//*[name() = 'svg']"
        self._no_load = (By.XPATH,"//h5[contains(text(), 'Sorry, we couldn't find any results.')]")

        # --- Table locators by Shipment No. ---
        # This is the base table. Replace '{shipment_no}' with the actual shipment number.
        self._row_by_shipment_no = "//span[contains(text(), '{shipment_no}')]/ancestor::tr[contains(@class, 'accordion-header')]"

        # The following tuples now contain XPath templates.
        # You must format them with a shipment_no before using them.
        self._txt_shipment_no = (self._row_by_shipment_no + "/td[1]//span[contains(@class, 'text-primary')]", "Shipment No [Text]")
        self._txt_shipment_status = (self._row_by_shipment_no + "/td[1]//span[contains(@class, 'badge')]", "Shipment Status [Text]")
        self._txt_trip_id = (self._row_by_shipment_no + "/td[2]//span", "Trip ID [Text]")
        self._txt_low_bid = (self._row_by_shipment_no + "/td[3]//span", "Low Bid [Text]")
        self._txt_book_now_price = (self._row_by_shipment_no + "/td[4]/div/span/span[1]", "Book Now Price [Text]")
        self._txt_book_now_rpm = (self._row_by_shipment_no + "/td[4]/div/span/span[2]", "Book Now RPM [Text]")
        self._txt_my_bid = (self._row_by_shipment_no + "/td[5]//span", "My Bid [Text]")
        self._txt_miles = (self._row_by_shipment_no + "/td[6]//span", "Miles [Text]")
        self._txt_weight = (self._row_by_shipment_no + "/td[7]//span", "Weight [Text]")
        self._txt_pickup_date = (self._row_by_shipment_no + "/td[8]//span", "Pick Up Date [Text]")
        self._txt_origin = (self._row_by_shipment_no + "/td[9]//span", "Origin [Text]")
        self._txt_destination = (self._row_by_shipment_no + "/td[10]//span", "Destination [Text]")
        self._txt_trailer_type = (self._row_by_shipment_no + "/td[11]//span", "Trailer Type [Text]")
        self._chk_expedite = (self._row_by_shipment_no + "/td[12]", "Expedite [Checkbox]")
        self._txt_age = (self._row_by_shipment_no + "/td[13]//span/span", "Age [Text]")
        self._txt_time_left = (self._row_by_shipment_no + "/td[14]//span", "Time Left [Text]")
        self._btn_accept_reject = (self._row_by_shipment_no + "/td[15]//button", "Accept / Reject [Button]")
        self._ico_favorite = (self._row_by_shipment_no + "/td[16]//a", "Favorite Icon [Button]")
        self._ico_hazmat = (self._row_by_shipment_no + "/td[16]//img[contains(@src, 'hazmat')]", "Hazmat Icon [Image]")

        # Load Value
        self._txt_load_value = (self._row_by_shipment_no + "/ancestor::tbody//h4[contains(text(), 'Load Value')]")
        self._txt_load_value_linehaul = (self._row_by_shipment_no + "/ancestor::tbody//p[contains(text(), 'Linehaul:')]")
        self._txt_load_value_fuel = (self._row_by_shipment_no + "/ancestor::tbody//h4[contains(text(), 'Fuel:')]")
        self._txt_load_value_accessorials = (self._row_by_shipment_no + "/ancestor::tbody//h4[contains(text(), 'Accessorials:')]")

        #Stops Number
        self.stops_no = "/ancestor::tbody//b[contains(text(), 'Stops ("'{stops_no}'")')]"

        #Load Acceptance / Rejection
        self._btn_accept_tender = "/ancestor::tbody//button[contains(text(), 'Accept Tender')]"
        self._modal_accept_tender_title = "//div[contains(@class,'modal-body')]//h4[contains(text(),'Accept Tender')]"
        self._modal_accept_tender_bid_amount = "//div[contains(@class,'modal-body')]//span[contains(text(),'Bid Amount')]"
        self._modal_accept_tender_origin = "//div[contains(@class,'modal-body')]//span[contains(text(),'{origin}')]"
        self._modal_accept_tender_destination = "//div[contains(@class,'modal-body')]//span[contains(text(),'{destination}')]"
        self._modal_accept_tender_accept_button = (By.XPATH,"//div[contains(@class,'modal-body')]//span[contains(text(),'Accept Tender')]")
        self._modal_accept_tender_reject_button = (By.XPATH,"//div[contains(@class,'modal-body')]//span[contains(text(),'Reject Tender')]")

        self._text_accept_tender_confirmation = "//div[contains(text(), 'Tender accepted successfully.')]"
        self._text_reject_tender_confirmation = "//div[contains(text(), 'Tender rejected successfully.')]"

        self._btn_reject_tender = "/ancestor::tbody//button[contains(text(), 'Reject Tender')]"

        self._span_bad_address_warning_message = "//span[contains(text(),'We were unable to validate 1 or more of these addresses. For validation, please reach out to your Crowley representative for assistance.')]"
        self._button_dismiss_bad_address_warning_message = "//button/span[contains(text(),'Dismiss')]"
        ##self.my_payment##pendiente en renombrar  = MyOffersPage.get_instance()

        # Assign Load to Carrier # pending work here -- map all locator to this modal
        #self._modal_content = "//div[contains(@class,'modal-dialog')]"
        #self._input_search_carrier = (
        #By.XPATH, "//div[contains(@class,'modal-dialog')]//input[@placeholder='Search by Name, MC#, DOT#, SCAC Code']")
        #self._input_carrier_rate = (
        #By.XPATH, "//div[contains(@class,'modal-dialog')]//input[@placeholder='Enter Rate']")
        #self._button_assign_load = (
        #By.XPATH, "//div[contains(@class,'modal-dialog')]//button/span[contains(text(),'Assign Load')]")
        #self._button_cancel_load = (
        #By.XPATH, "//div[contains(@class,'modal-dialog')]//button/span[contains(text(),'Cancel')]")
        #self._button_close_modal = (
        #By.XPATH, "//div[contains(@class,'modal-dialog')]///button[contains(@class,'btn-close')]")
        #self._upload_documents = (
        #By.XPATH, "//div[contains(@class,'modal-dialog')]//*[@id='bolAttachments']/div[2]/div[1]/div/button")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = MyOffersPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    @allure.step("Enter Search By: {search_by}")
    def enter_search_by(self, search_by: str):
        self.send_keys().set_locator(self._input_search_by, self._name).clear().set_text(search_by)
        return self

    @allure.step("Click Search")
    def click_search(self):
        self.click().set_locator(self._button_search, self._name).single_click().pause(5)
        return self


    @allure.step("Check Include Closed")
    def checkbox_include_closed(self):
        self.click().set_locator(self._checkbox_include_close, self._name).single_click().pause(1)
        return self


    @allure.step("Click Ship date")
    def click_sort_by_ship_date(self):
        self.click().set_locator(self._button_sort_by_ship_date, self._name).single_click()
        return self

    def get_text_results(self, expected_text= "Sorry, we couldn't find any results."):
        result_elements1 = self.driver.find_elements(By.XPATH, '//h5[contains(text(), "Sorry, we couldn\'t find any results.")]')

        return any(expected_text in el.text for el in result_elements1)

    @allure.step("Click Status")
    def click_sort_by_status(self):
        self.click().set_locator(self._button_sort_by_status, self._name).single_click()
        return self

    @allure.step("Click Origin")
    def click_sort_by_origin(self):
        self.click().set_locator(self._button_sort_by_origin, self._name).single_click()
        return self


    @allure.step("Total Records")
    def get_total_records(self):
        return self.get_text().set_locator(self._text_total_records, self._name).by_text()

    def click_track_record_item(self, index: int):
        xpath = f"({self._list_container})[{str(index)}]"
        locator = (By.XPATH, xpath, f"Track Record [{str(index)}]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def no_load_results(self):
        try:
            element = self.element().wait(self._noload, 5)
            return element is not None
        except Exception as e:
            logger.error(f"{str(e)}")
            return False

    def get_shipment_tracker(self, index: int):
        xpath = f"({self._list_container}//span[contains(@class, 'text-primary') and contains(@class, 'fw-medium')])[{str(index)}]"
        locator = (By.XPATH, xpath, "Shipment Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    # =============================   Methods for shipment-specific locators from table=================================
    @allure.step("Get Shipment Number for shipment: {shipment_no}")
    def get_shipment_no_text(self, shipment_no: str):
        xpath = self._txt_shipment_no[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_shipment_no[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Shipment Status for shipment: {shipment_no}")
    def get_shipment_status_text(self, shipment_no: str):
        xpath = self._txt_shipment_status[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_shipment_status[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Trip ID for shipment: {shipment_no}")
    def get_trip_id_text(self, shipment_no: str):
        xpath = self._txt_trip_id[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_trip_id[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Low Bid for shipment: {shipment_no}")
    def get_low_bid_text(self, shipment_no: str):
        xpath = self._txt_low_bid[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_low_bid[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Book Now Price for shipment: {shipment_no}")
    def get_book_now_price_text(self, shipment_no: str):
        xpath = self._txt_book_now_price[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_book_now_price[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Book Now RPM for shipment: {shipment_no}")
    def get_book_now_rpm_text(self, shipment_no: str):
        xpath = self._txt_book_now_rpm[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_book_now_rpm[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get My Bid for shipment: {shipment_no}")
    def get_my_bid_text(self, shipment_no: str):
        xpath = self._txt_my_bid[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_my_bid[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Miles for shipment: {shipment_no}")
    def get_miles_text(self, shipment_no: str):
        xpath = self._txt_miles[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_miles[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Weight for shipment: {shipment_no}")
    def get_weight_text(self, shipment_no: str):
        xpath = self._txt_weight[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_weight[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Pickup Date for shipment: {shipment_no}")
    def get_pickup_date_text(self, shipment_no: str):
        xpath = self._txt_pickup_date[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_pickup_date[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Origin for shipment: {shipment_no}")
    def get_origin_text(self, shipment_no: str):
        xpath = self._txt_origin[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_origin[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Destination for shipment: {shipment_no}")
    def get_destination_text(self, shipment_no: str):
        xpath = self._txt_destination[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_destination[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Trailer Type for shipment: {shipment_no}")
    def get_trailer_type_text(self, shipment_no: str):
        xpath = self._txt_trailer_type[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_trailer_type[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Check Expedite status for shipment: {shipment_no}")
    def is_expedite_checked(self, shipment_no: str):
        xpath = self._chk_expedite[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._chk_expedite[1])
        return self.element().set_locator(locator, self._name).is_selected()

    @allure.step("Get Age for shipment: {shipment_no}")
    def get_age_text(self, shipment_no: str):
        xpath = self._txt_age[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_age[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Get Time Left for shipment: {shipment_no}")
    def get_time_left_text(self, shipment_no: str):
        xpath = self._txt_time_left[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._txt_time_left[1])
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Click Accept/Reject button for shipment: {shipment_no}")
    def click_accept_reject_button(self, shipment_no: str):
        xpath = self._btn_accept_reject[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._btn_accept_reject[1])
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Click Favorite icon for shipment: {shipment_no}")
    def click_favorite_icon(self, shipment_no: str):
        xpath = self._ico_favorite[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._ico_favorite[1])
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Check if Hazmat icon is visible for shipment: {shipment_no}")
    def is_hazmat_icon_visible(self, shipment_no: str):
        xpath = self._ico_hazmat[0].format(shipment_no=shipment_no)
        locator = (By.XPATH, xpath, self._ico_hazmat[1])
        try:
            return self.element().set_locator(locator, self._name).is_displayed()
        except:
            return False
    # ===========================   END Methods for shipment-specific locators from table===============================

    @allure.step("Check My Offers / Load Value elements")
    def check_load_value_elements(self, shipment_no: str):
        xpath = self._txt_load_value.format(shipment_no=shipment_no)
        self.driver.find_elements(By.XPATH,xpath)
        xpath_2 = self._txt_load_value_linehaul.format(shipment_no=shipment_no)
        self.driver.find_elements(By.XPATH,xpath_2)
        xpath_3 = self._txt_load_value_fuel.format(shipment_no=shipment_no)
        self.driver.find_elements(By.XPATH,xpath_3)
        xpath_4 = self._txt_load_value_accessorials.format(shipment_no=shipment_no)
        self.driver.find_elements(By.XPATH,xpath_4)
        return self

    @allure.step("Check Mid Stops Number: {shipment_no} {stops_no}")
    def check_mid_stops_number(self, shipment_no: str, stops_no: str):
        int_stops_no = int(stops_no)
        int_stops_no-=2
        stops_no = str(int_stops_no)
        xpath = self._row_by_shipment_no.format(shipment_no=shipment_no) + self.stops_no.format(stops_no=stops_no)
        self.driver.find_elements(By.XPATH,xpath)
        return self

    @allure.step("Click Accept button for shipment: {shipment_no}")
    def click_accept_tender_button(self, shipment_no: str):
        xpath = self._row_by_shipment_no.format(shipment_no=shipment_no) + self._btn_accept_tender
        locator = (By.XPATH, xpath)
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Check Accept Tender Modal Window: {origin} {destination}")
    def check_accept_tender_modal_window(self, origin: str, destination: str):
        self.driver.find_elements(By.XPATH, self._modal_accept_tender_title)
        self.driver.find_elements(By.XPATH, self._modal_accept_tender_bid_amount)
        self.driver.find_elements(By.XPATH, self._modal_accept_tender_origin.format(origin=origin))
        self.driver.find_elements(By.XPATH, self._modal_accept_tender_destination.format(destination=destination))
        self.driver.find_elements(By.XPATH, self._modal_accept_tender_accept_button)
        self.driver.find_elements(By.XPATH, self._modal_accept_tender_reject_button)
        return self


    @allure.step("Click Accept button in modal window confirmation")
    def click_accept_tender_button_modal_window(self):
        self.element().set_locator(self._modal_accept_tender_accept_button, self._name)
        self.element().is_present(self._modal_accept_tender_accept_button)
        self.click().set_locator(self._modal_accept_tender_accept_button, self._name).pause(1).single_click()
        return self

    @allure.step("Get Message for Accepting a Tender Correctly")
    def validate_accept_tender_success_message(self):
        locator = (By.XPATH, self._text_accept_tender_confirmation)
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        return self.get_text().set_locator(locator, self._name).by_text()

    @allure.step("Click Reject button for shipment: {shipment_no}")
    def click_reject_tender_button(self, shipment_no: str):
        xpath = self._row_by_shipment_no.format(shipment_no=shipment_no) + self._btn_reject_tender
        locator = (By.XPATH, xpath)
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Click Reject button in modal window confirmation")
    def click_reject_tender_button_modal_window(self):
        self.click().set_locator(self._modal_accept_tender_reject_button, self._name).double_click()
        return self

    @allure.step("Get Message for Rejecting a Tender Correctly")
    def validate_reject_tender_success_message(self):
        return self.get_text().set_locator((By.XPATH, self._text_reject_tender_confirmation), self._name).by_text()

    @allure.step("Check Accept Bad Address Tender Warning Modal Window")
    def validate_bad_address_tender_warning_message(self):
        self.element().set_locator((By.XPATH, self._span_bad_address_warning_message), self._name)
        self.element().is_present(By.XPATH, self._span_bad_address_warning_message)
        self.element().set_locator((By.XPATH, self._button_dismiss_bad_address_warning_message), self._name)
        self.element().is_present(By.XPATH, self._button_dismiss_bad_address_warning_message)
        return self

    @allure.step("Click Dismiss button in Badd Address Warning Modal Window")
    def click_dismiss_button_bad_address_tender_modal_window(self):
        locator = By.XPATH, self._button_dismiss_bad_address_warning_message
        self.element().set_locator(locator, self._name)
        self.element().is_present(locator)
        self.click().set_locator(locator, self._name).double_click()
        return self