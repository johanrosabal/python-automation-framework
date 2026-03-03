import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('MyPaymentsPage')


class MyPaymentsPage(BasePage):

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
        self.relative = "/shipment/my-payments"

        # Locator definitions

        self._button_search= (By.XPATH, "//button[@mattooltipposition='below']","Search record [Button]")
        self._noload = (By.XPATH, "//h5[contains(text(), 'Sorry, we couldn')]","Message [Output]")
        self._input_search_by = (By.XPATH, "//input[@type='text' and contains(@placeholder,'Search by')]","Search by [Input]")
        self._list_container = (By.XPATH,"//div[contains(@class, 'custom-table')]","List of container [Select]")
        self._no_load = (By.XPATH,"//h5[contains(text(), 'Sorry, we couldn')]","Message [Output]")
        self._button_export =  (By.XPATH,"//button[contains(@class, 'iq-btn iq-btn--secondary')]","Export records [Button]")
        self._format_excel = (By.XPATH,"//span[text()='Excel']","Export excel format [Button]")
        self._format_csv = (By.XPATH, "//span[text()='CSV']","Export csvf format [Button]")
        self._button_cancel = (By.XPATH, "//span[text()=' Cancel']","Cancel export [Button]")
        self._button_export_popup = (By.XPATH, "//button/span[text()='Export']","Popup export [Button]")
        self._current_date_from = (By.XPATH, "//input[@name='fromPickUpDate']","Current date from  [Input]")
        self._current_date_to = (By.XPATH, "//input[@name='toPickUpDate']","Current date to  [Input]")
        self._input_range_date_from_day = (By.XPATH, "//td[contains(@class, 'available') and not(contains(@class, 'disabled'))]","Range date from [Input]")
        self._input_range_date_to_day = (By.XPATH, "//td[contains(@class, 'active') and contains(@class, 'start-date') and contains(@class, 'today')]","Range date to [Input]")
        self._calendar_button2 = (By.XPATH, "(//button[@tabindex='-1'][.//img[contains(@src, 'calendar')]])[2]","Calendar2 [Button]")
        self._calendar_button1 = (By.XPATH, "(//button[@tabindex='-1'][.//img[contains(@src, 'calendar')]]","Calendar1 [Button]")
        self._field_linehaul_charge = (By.XPATH, "//a[contains(text(), 'Linehaul Charge')]","Linehaul Charge data [Input]")
        self._field_fuel = (By.XPATH, "//a[contains(text(), 'Fuel')]","Fuel data [Input]")
        self._field_accessorials = (By.XPATH, "//a[contains(text(), 'Accessorials')]","Accessorials data [Input]")
        self._field_shipment_number = (By.XPATH, "//a[contains(text(), 'Shipment No.')]","Shipment number data [Input]")
        self._field_pro_number = (By.XPATH, "//a[contains(text(), 'Pro Number')]","Pro number data [Input]")
        self._field_ship_date = (By.XPATH, "//a[contains(text(), 'Ship Date')]","Ship date data [Input]")
        self._field_shipper = (By.XPATH, "//a[contains(text(), 'Shipper')]","Shipper data [Input]")
        self._field_origin = (By.XPATH, "//a[contains(text(), 'Origin')]","Origin data [Input]")
        self._field_destination = (By.XPATH, "//a[contains(text(), 'Destination')]","Destination data [Input]")
        self._field_weight = (By.XPATH, "//a[contains(text(), 'Weight')]","Weight data [Input]")
        self._field_pieces = (By.XPATH, "//a[contains(text(), 'Pieces')]","Pieces data [Input]")
        self._field_total_charge = (By.XPATH, "//a[contains(text(), 'Total Charge')]","Total Charge data [Input]")
        self._pro_number = (By.XPATH, "//app-my-payment//table//tr/td[2]//span[2]","Pro number data [Input]")
        self._new_pro_number_input = (By.XPATH,"//app-update-pro-number//input","Pro number new data [Input]")
        self._click_input_update = (By.XPATH,"//app-update-pro-number//div[3]/button[1]/span","Update [Button]")



        self._field_linehaul_currency = (By.XPATH, "//app-my-payment//table//tr//td[9]//span","Linehaul Currency field [Output]")
        self._field_fuel_currency = (By.XPATH, "//app-my-payment//table//tr//td[10]//span","Fuel Currency field [Output]")
        self._field_accessorials_currency = (By.XPATH, "//app-my-payment//table//tr//td[11]//span","Accesorial Currency field [Output]")
        self._field_total_currency = (By.XPATH, "//app-my-payment//table//tr//td[12]//span","Total Currency field [Output]")
        self._updated_po_text = (By.XPATH, "//div[contains(text(), 'updated successfully')]" , "Update Message [Output]")
        self._download_text_export_excel_and_csv = (By.XPATH, "//div[contains(text(), 'payments exported successfully')]", "Update Message [Output]")
        self._text_feedback_confirmation = (By.XPATH, "//div[contains(text(), 'Feedback submitted successfully')]", "Confirmation Message [Output]")

        self._button_feedback = (By.XPATH, "//*[@id='mybutton']/button","Feedback field [Input]")
        self._enter_comment = (By.XPATH,  "//div[@class='note-editable']","Enter comment field [Input]")
        self._feedback_submit = (By.XPATH, "//button[@data-cy='feedbacksubmit']","Submit comment [Button]")
        self._feedback_cancel = (By.XPATH, "//button[@data-cy='feedbackclose']","Cancel comment [Button]")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = MyPaymentsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def no_load_results(self):
        try:
            element = self.element().wait(self._no_load, 5)
            return element is not None
        except Exception as e:
            logger.error(f"{e.msg}")
            return False

    #@allure.step("Enter Search By: {search_by}")
    def enter_search_by(self, search_by: str):
        self.send_keys().set_locator(self._input_search_by, self._name).clear().set_text(search_by)

        return self

    @allure.step("Click Search")
    def click_search(self):
        self.click().set_locator(self._button_search, self._name).single_click().pause(2)
        return self


    @allure.step("Click export popup")
    def click_popup_export(self):
        self.click().set_locator(self._button_export_popup, self._name).single_click().pause(2)
        return self


    @allure.step("Click calendar")
    def click_calendar2(self):
        self.click().set_locator(self._calendar_button2, self._name).single_click().pause(2)
        return self

    @allure.step("Click calendar")
    def click_calendar1(self):
        self.click().set_locator(self._calendar_button1, self._name).single_click().pause(2)
        return self



    @allure.step("Click export format=excel")
    def select_format_excel(self):
        self.click().set_locator(self._format_excel, self._name).single_click().pause(2)
        return self


    @allure.step("Click export format=csv")
    def select_format_csv(self):
        self.click().set_locator(self._format_csv, self._name).single_click().pause(2)
        return self


    @allure.step("Click export")
    def click_export_button(self):
        self.click().set_locator(self._button_export, self._name).single_click().pause(2)
        return self

    @allure.step("Check Include Closed")
    def checkbox_include_closed(self):
        self.click().set_locator(self._checkbox_include_close, self._name).single_click().pause(1)
        return self

    @allure.step("Click current date from")
    def click_current_date_from(self):
        self.click().set_locator(self._current_date_from, self._name).single_click().pause(2)
        return self

    @allure.step("Click Current date to")
    def click_current_date_to(self):
        self.click().set_locator(self._current_date_to, self._name).single_click().pause(2)
        return self


    @allure.step("Click from date")
    def click_from_date(self):
        self.click().set_locator(self._input_range_date_from_day, self._name).single_click().pause(2)
        return self


    @allure.step("Click to date")
    def click_to_date(self):
        self.click().set_locator(self._input_range_date_to_day, self._name).single_click().pause(2)
        return self

    @allure.step("Click Ship date")
    def click_sort_by_ship_date(self):
        self.click().set_locator(self._button_sort_by_ship_date, self._name).single_click()
        return self

    def get_ship_dates(self):
        # Ubica todos los elementos que contienen las fechas de envío en la página.
        # Por ejemplo, si cada fecha se encuentra en un <span> con la clase "ship-date":
        date_elements = self.driver.find_elements_by_css_selector("//h5[contains(text(), 'Sorry, we couldn't find any results.')]")
        # Extrae el texto y conviértelo a objetos datetime si es necesario.
        # Aquí se asume que las fechas están en un formato de cadena comparable.
        return [el.text for el in date_elements]

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


    def _enter_day_from_day(self, text):
        self.send_keys().set_locator(self._current_date_from, self._name).clear().set_text(text)
        return self

    def _enter_day_to_day(self, text):
        self.send_keys().set_locator(self._current_date_to, self._name).clear().set_text(text)
        return self

    def no_load_results_no_load(self):
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


    def get_shipment_tracker_number(self, index: int):
        xpath = f"(//span[contains(@class, 'text-primary') and contains(@class, 'fw-bold')])[{str(index)}]"
        locator = (By.XPATH, xpath, "Shipment Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    @allure.step("Get Message for a valid input")
    def validate_po_update(self):
        return self.get_text().set_locator(self._updated_po_text, self._name).by_text()

    @allure.step("Get Message for a valid download")
    def validate_download_excel_and_csv_text(self):
        return self.get_text().set_locator(self._download_text_export_excel_and_csv, self._name).by_text()

    @allure.step("Get Message for a valid feedback")
    def validate_feedback_text(self):
        return self.get_text().set_locator(self._text_feedback_confirmation, self._name).by_text()


    def enter_export_range(self,fromdate,currentdate):
        # Enter Days Range
        self._enter_day_from_day(fromdate)
        self._enter_day_to_day(currentdate)

        return self

    def get_all_charge_texts1(self):
        elements = {
            "Linehaul Charge": self._field_linehaul_charge,
            "Fuel": self._field_fuel,
            "Accessorials": self._field_accessorials

        }
        results = {}
        for label, locator in elements.items():

            text = self.get_text().set_locator(locator, self._name).by_text().strip()
            results[label] = text

        return results

    @allure.step("Click feedback")
    def click_feedback(self):
        self.click().set_locator(self._button_feedback, self._name).single_click().pause()
        return self


    def enter_comment(self, text):
        self.send_keys().set_locator(self._enter_comment, self._name).clear().set_text(text)
        return self


    def click_feedback_submit(self):
        self.click().set_locator(self._feedback_submit, self._name).single_click().pause()
        return self

    def click_feedback_cancel(self):
        self.click().set_locator(self._feedback_cancel, self._name).single_click().pause()
        return self

    def get_all_charge_texts(self):
        elements = {
            "Linehaul Charge": self._field_linehaul_charge,
            "Fuel": self._field_fuel,
            "Accessorials": self._field_accessorials,
            "Shipment No":self._field_shipment_number,
            "Pro Number":self._field_pro_number,
            "Ship Date":self._field_ship_date,
            "Shipper":self._field_shipper,
            "Origin":self._field_origin,
            "Destination":self._field_destination,
            "Pieces":self._field_pieces,
            "Weight":self._field_weight,
            "Total Charge":self._field_total_charge,
        }
        results = {}
        for label, locator in elements.items():
            text = self.get_text().set_locator(locator, self._name).by_text().strip()
            results[label] = text

        return results

    def update_pro_number(self, new_pro_number):
        # Click the PRO number field
        self.click().set_locator(self._pro_number, self._name).single_click().pause()
        # Enter the new PRO number
        self.send_keys().set_locator(self._new_pro_number_input, self._name).clear().set_text(new_pro_number)
        # Click the update button
        self.click().set_locator(self._click_input_update, self._name).single_click().pause()
        return self

    def get_all_charge_fields(self):
        elements = {
            "Linehaul Charge Field": self._field_linehaul_currency,
            "Fuel Field": self._field_fuel_currency,
            "Accessorials Field": self._field_accessorials_currency,
            "Total Charge Field":self._field_total_currency,
        }
        results = {}
        for label, locator in elements.items():
            text = self.get_text().set_locator(locator, self._name).by_text().strip()
            results[label] = text

        return results