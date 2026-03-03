from selenium.webdriver.common.by import By
from tabulate import tabulate

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('CargoDetailsTab')


class CargoDetailsTab(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the CargoDetailsTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/Employees/s/bookingDetail?id={ID}"
        # Locator definitions
        self._xpath_commercial_container_details = "//b[contains(text(),'COMMERCIAL CONTAINER DETAILS')]/..//following-sibling::div/ul/li"
        self._xpath_operational_equipment_details = "//b[contains(text(),'OPERATIONAL EQUIPMENT DETAILS')]/..//following-sibling::div"
        self._xpath_commodities_details = "//b[contains(text(),'COMMODITIES')]/..//following-sibling::div/ul/li"

        # //section[@class='slds-accordion__section']//button

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

    # COMMERCIAL CONTAINER DETAILS -------------------------------------------------------------------------------------
    def get_commercial_container_summary_content(self):
        locator = (
            By.XPATH,
            f"({self._xpath_commercial_container_details}//h2//span[@title])[1]",
            "Commercial Container Details: Summary Title [Text Accordion]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_category(self):
        locator = (
            By.XPATH,
            f"{self._xpath_commercial_container_details}//span[text()='CATEGORY']/following-sibling::div/span",
            "Commercial Container Details: Category [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_container_type(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='CONTAINER TYPE']/following-sibling::div/span",
                   "Commercial Container Details: Container Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_quantity_1(self):
        locator = (
            By.XPATH,
            f"{self._xpath_commercial_container_details}//span[text()='QUANTITY']/following-sibling::div/span",
            "Commercial Container Details: Quantity [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    # ** Not visible for all container types
    def get_commercial_container_details_l_w_h(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='L/W/H']/following-sibling::div/span",
            "Commercial Container Details: L/W/H [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_length(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='LENGTH']/following-sibling::div/span",
            "Commercial Container Details: LENGTH [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    # ** Not visible for all container types
    def get_commercial_container_details_weight(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='WEIGHT']/following-sibling::div/span",
            "Commercial Container Details: WEIGHT [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    # ** Not visible for all container types
    def get_commercial_container_details_width(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='WIDTH']/following-sibling::div/span",
            "Commercial Container Details: WIDTH [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_cargo_wt_per_container(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='CARGO WT. PER CONTAINER']/following-sibling::div/span",
                   "Commercial Container Details: CARGO WT. PER CONTAINER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    # ** Not visible for all container types
    def get_commercial_container_details_volume(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='VOLUME']/following-sibling::div/span",
            "Commercial Container Details: VOLUME [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_crowley_equipment(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='CROWLEY EQUIPMENT']/following-sibling::div/span",
                   "Commercial Container Details: CROWLEY EQUIPMENT [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_shipper_owned(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='SHIPPER OWNED']/following-sibling::div/span",
                   "Commercial Container Details: SHIPPER OWNED [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_reefer(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='REEFER']/following-sibling::div/span",
            "Commercial Container Details: REEFER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_booked_temp(self):
        locator = (
            By.XPATH,
            f"{self._xpath_commercial_container_details}//span[text()='BOOKED TEMP']/following-sibling::div/span",
            "Commercial Container Details: BOOKED TEMP [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_ventilated(self):
        locator = (
            By.XPATH,
            f"{self._xpath_commercial_container_details}//span[text()='VENTILATED']/following-sibling::div/span",
            "Commercial Container Details: VENTILATED [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_ratings_commodity_category(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='RATING COMMODITY CATEGORY']/following-sibling::div/span",
                   "Commercial Container Details: RATING COMMODITY CATEGORY [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_actual_cargo_description(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='ACTUAL CARGO DESCRIPTION']/following-sibling::div/span",
                   "Commercial Container Details: ACTUAL CARGO DESCRIPTION [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_declared_value_of_cargo(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='DECLARED VALUE OF CARGO']/following-sibling::div/span",
                   "Commercial Container Details: ACTUAL CARGO DESCRIPTION [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_rcra(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='RCRA']/following-sibling::div/span",
            "Commercial Container Details: RCRA [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_waste(self):
        locator = (
            By.XPATH, f"{self._xpath_commercial_container_details}//span[text()='WASTE']/following-sibling::div/span",
            "Commercial Container Details: WASTE [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    # ** Not visible for all container types
    def get_commercial_container_details_proper_shipping_name(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}//span[text()='PROPER SHIPPING NAME']/following-sibling::div/span",
                   "Commercial Container Details: PROPER SHIPPING NAME [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    # ** Not visible for all container types
    def get_commercial_container_details_quantity_2(self):
        locator = (By.XPATH,
                   f"{self._xpath_commercial_container_details}(//span[text()='QUANTITY']/following-sibling::div/span)[2]",
                   "Commercial Container Details: Quantity [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commercial_container_details_empty_container_release_location(self):
        sub_container = "//b[text()='Empty Container Release Location']/.."
        locator_location = (By.XPATH,
                            f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'LOCATION')]/following-sibling::div/span)[1]",
                            "Commercial Container Details: Empty Container Release Location: LOCATION [text]")

        locator_sub_location = (By.XPATH,
                                f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'SUBLOCATION')]/following-sibling::div/span)[1]",
                                "Commercial Container Details: Empty Container Release Location: SUBLOCATION [text]")

        locator_date_time = (By.XPATH,
                             f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                             "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        data = {
            "SUMMARY TITLE": "Empty Container Release Location",
            "LOCATION": self.get_text().set_locator(locator_location, self._name).by_text() or "-",
            "SUBLOCATION": self.get_text().set_locator(locator_sub_location, self._name).by_text() or "-",
            "DATE & TIME": self.get_text().set_locator(locator_date_time, self._name).by_text() or "-",
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        return data

    def get_commercial_container_details_full_container_return_location(self):
        sub_container = "//b[text()='Full Container Return Location']/.."
        locator_location = (By.XPATH,
                            f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'LOCATION')]/following-sibling::div/span)[1]",
                            "Commercial Container Details: Empty Container Release Location: LOCATION [text]")

        locator_sub_location = (By.XPATH,
                                f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'SUBLOCATION')]/following-sibling::div/span)[1]",
                                "Commercial Container Details: Empty Container Release Location: SUBLOCATION [text]")

        locator_date_time = (By.XPATH,
                             f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                             "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        locator_remarks = (By.XPATH,
                           f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                           "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        data = {
            "SUMMARY TITLE": "Full Container Return Location",
            "LOCATION": self.get_text().set_locator(locator_location, self._name).by_text() or "-",
            "SUBLOCATION": self.get_text().set_locator(locator_sub_location, self._name).by_text() or "-",
            "DATE & TIME": self.get_text().set_locator(locator_date_time, self._name).by_text() or "-",
            "REMARKS": self.get_text().set_locator(locator_remarks, self._name).by_text() or "-",
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        return data

    def get_commercial_container_details_full_container_release_location(self):
        sub_container = "//b[text()='Full Container Release Location']/.."
        locator_location = (By.XPATH,
                            f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'LOCATION')]/following-sibling::div/span)[1]",
                            "Commercial Container Details: Empty Container Release Location: LOCATION [text]")

        locator_sub_location = (By.XPATH,
                                f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'SUBLOCATION')]/following-sibling::div/span)[1]",
                                "Commercial Container Details: Empty Container Release Location: SUBLOCATION [text]")

        locator_date_time = (By.XPATH,
                             f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                             "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        locator_remarks = (By.XPATH,
                           f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                           "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        data = {
            "SUMMARY TITLE": "Full Container Release Location",
            "LOCATION": self.get_text().set_locator(locator_location, self._name).by_text() or "-",
            "SUBLOCATION": self.get_text().set_locator(locator_sub_location, self._name).by_text() or "-",
            "DATE & TIME": self.get_text().set_locator(locator_date_time, self._name).by_text() or "-",
            "REMARKS": self.get_text().set_locator(locator_remarks, self._name).by_text() or "-",
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        return data

    def get_commercial_container_details_empty_container_return_location(self):
        sub_container = "//b[text()='Empty Container Return Location']/.."
        locator_location = (By.XPATH,
                            f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'LOCATION')]/following-sibling::div/span)[1]",
                            "Commercial Container Details: Empty Container Release Location: LOCATION [text]")

        locator_sub_location = (By.XPATH,
                                f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'SUBLOCATION')]/following-sibling::div/span)[1]",
                                "Commercial Container Details: Empty Container Release Location: SUBLOCATION [text]")

        locator_date_time = (By.XPATH,
                             f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                             "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        locator_remarks = (By.XPATH,
                           f"({self._xpath_commercial_container_details}{sub_container}//span[contains(text(),'DATE & TIME')]/following-sibling::div/span)[1]",
                           "Commercial Container Details: Empty Container Release Location: DATE & TIME [text]")

        data = {
            "SUMMARY TITLE": "Empty Container Return Location",
            "LOCATION": self.get_text().set_locator(locator_location, self._name).by_text() or "-",
            "SUBLOCATION": self.get_text().set_locator(locator_sub_location, self._name).by_text() or "-",
            "DATE & TIME": self.get_text().set_locator(locator_date_time, self._name).by_text() or "-",
            "REMARKS": self.get_text().set_locator(locator_remarks, self._name).by_text() or "-",
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        return data

    def get_commercial_details(self):
        summary = self.get_commercial_container_summary_content() or "-"
        category = self.get_commercial_container_details_category() or "-"
        container_type = self.get_commercial_container_details_container_type() or "-"
        quantity = self.get_commercial_container_details_quantity_1() or "-"
        length = self.get_commercial_container_details_length() or "-"
        width = self.get_commercial_container_details_width() or "-"
        cargo_wt_per_container = self.get_commercial_container_details_cargo_wt_per_container() or "-"
        crowley_equipment = self.get_commercial_container_details_crowley_equipment() or "-"
        shipper_owned = self.get_commercial_container_details_shipper_owned() or "-"
        reefer = self.get_commercial_container_details_reefer() or "-"
        booked_temp = self.get_commercial_container_details_booked_temp() or "-"
        ventilated = self.get_commercial_container_details_ventilated() or "-"
        rating_commodity_category = self.get_commercial_container_details_ratings_commodity_category() or "-"
        actual_cargo_description = self.get_commercial_container_details_actual_cargo_description() or "-"
        declared_value_of_cargo = self.get_commercial_container_details_declared_value_of_cargo() or "-"
        rcra = self.get_commercial_container_details_rcra() or "-"
        waste = self.get_commercial_container_details_waste() or "-"

        # Create a Dictionary
        data = {
            "SUMMARY TITLE": summary,
            "CATEGORY": category,
            "CONTAINER TYPE": container_type,
            "QUANTITY": quantity,
            "LENGTH": length,
            "WIDTH": width,
            "CARGO WT. PER CONTAINER": cargo_wt_per_container,
            "CROWLEY EQUIPMENT": crowley_equipment,
            "SHIPPER OWNED": shipper_owned,
            "REEFER": reefer,
            "BOOKED TEMP": booked_temp,
            "VENTILATED": ventilated,
            "RATING COMMODITY CATEGORY": rating_commodity_category,
            "ACTUAL CARGO DESCRIPTION": actual_cargo_description,
            "DECLARED VALUE OF CARGO": declared_value_of_cargo,
            "RCRA": rcra,
            "WASTE": waste,
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return data

    # OPERATIONAL CONTAINER DETAILS -------------------------------------------------------------------------------------

    def get_operational_equipment_details_equipment_number(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Equipment Number')]/following-sibling::div/span",
            "Operational Equipment Details: Equipment Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_container_size_type(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Container Size/Type')]/following-sibling::div/span",
            "Operational Equipment Details: Container Size/Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_seal_no(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Seal No.')]/following-sibling::div/span",
            "Operational Equipment Details: Seal No. [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_receipt_number_1(self):
        locator = (
            By.XPATH,
            f"({self._xpath_operational_equipment_details}//span[contains(text(),'RECEIPT NUMBER')]/following-sibling::div/span)[1]",
            "Operational Equipment Details: RECEIPT NUMBER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_receipt_number_2(self):
        locator = (
            By.XPATH,
            f"({self._xpath_operational_equipment_details}//span[contains(text(),'RECEIPT NUMBER')]/following-sibling::div/span)[2]",
            "Operational Equipment Details: RECEIPT NUMBER [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_address(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Address')]/following-sibling::div/span",
            "Operational Equipment Details: Address [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_sea_board_booking_number(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'SeaBoard Booking Number#')]/following-sibling::div/span",
            "Operational Equipment Details: SeaBoard Booking Number# [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_vgm(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'VGM')]/following-sibling::div/span",
            "Operational Equipment Details: SeaBoard Booking Number# [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_equipment_substitution(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[text()='Equipment Substitution']/following-sibling::lightning-input//input[@type='checkbox']",
            "Operational Equipment Details: Equipment Substitution [Text]")
        return self.element().set_locator(locator, self._name).get_attribute("value")

    def get_operational_equipment_details_cargo_weight(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Cargo Weight')]/following-sibling::div/span",
            "Operational Equipment Details: Cargo Weight [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_release_order_sent(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Release Order Sent')]/following-sibling::div/span",
            "Operational Equipment Details: Release Order Sent [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_contact_name(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Contact Name')]/following-sibling::div/span",
            "Operational Equipment Details: Contact Name [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_edi_status(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'EDI Status')]/following-sibling::div/span",
            "Operational Equipment Details: EDI Status [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_commercial_container_type(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Commercial Container Type')]/following-sibling::div/span",
            "Operational Equipment Details: Commercial Container Type [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_equipment_substitution_reason(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Equipment Substitution Reason')]/following-sibling::div/span",
            "Operational Equipment Details: Equipment Substitution Reason [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_reefer_temps_set(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Reefer Temps: set')]/following-sibling::div/span",
            "Operational Equipment Details: Reefer Temps: set [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_contact_number(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Contact Number')]/following-sibling::div/span",
            "Operational Equipment Details: Contact Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_allocated_release_date(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Allocated Release Date')]/following-sibling::div/span",
            "Operational Equipment Details: Allocated Release Date[Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_receive_date(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Receive Date')]/following-sibling::div/span",
            "Operational Equipment Details: Receive Date [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_reefer_temps_read(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Reefer Temps: Read')]/following-sibling::div/span",
            "Operational Equipment Details: Reefer Temps: Read [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_release_location(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Release Location')]/following-sibling::div/span",
            "Operational Equipment Details: Release Location[Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details_pickup_number(self):
        locator = (
            By.XPATH,
            f"{self._xpath_operational_equipment_details}//span[contains(text(),'Pickup#')]/following-sibling::div/span",
            "Operational Equipment Details: Pickup# [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_operational_equipment_details(self):
        equipment_number = self.get_operational_equipment_details_equipment_number() or "-"
        container_size_type = self.get_operational_equipment_details_container_size_type() or "-"
        seal_no = self.get_operational_equipment_details_serial_no() or "-"
        receive_date = self.get_operational_equipment_details_receive_date() or "-"
        receipt_number_1 = self.get_operational_equipment_details_receipt_number_1() or "-"
        receipt_number_2 = self.get_operational_equipment_details_receipt_number_2() or "-"
        address = self.get_operational_equipment_details_address() or "-"
        sea_board_booking_number = self.get_operational_equipment_details_sea_board_booking_number() or "-"
        vgm = self.get_operational_equipment_details_vgm() or "-"
        equipment_substitution = self.get_operational_equipment_details_equipment_substitution() or "-"
        equipment_substitution_reason = self.get_operational_equipment_details_equipment_substitution_reason() or "-"
        cargo_weight = self.get_operational_equipment_details_cargo_weight() or "-"
        release_order_sent = self.get_operational_equipment_details_release_order_sent() or "-"
        contact_name = self.get_operational_equipment_details_contact_name() or "-"
        contact_number = self.get_operational_equipment_details_contact_number() or "-"
        edi_status = self.get_operational_equipment_details_edi_status() or "-"
        commercial_container_type = self.get_operational_equipment_details_commercial_container_type() or "-"
        reefer_temps_set = self.get_operational_equipment_details_reefer_temps_set() or "-"
        reefer_temps_read = self.get_operational_equipment_details_reefer_temps_read() or "-"
        allocated_release_date = self.get_operational_equipment_details_allocated_release_date() or "-"
        release_location = self.get_operational_equipment_details_release_location() or "-"
        pickup_number = self.get_operational_equipment_details_pickup_number()

        # Create a Dictionary
        cargo_data = {
            "Equipment Number": equipment_number,
            "Container Size/Type": container_size_type,
            "Seal No.": seal_no,
            "Receive Date": receive_date,
            "RECEIPT NUMBER 1": receipt_number_1,
            "RECEIPT NUMBER 2": receipt_number_2,
            "Address": address,
            "SeaBoard Booking Number#": sea_board_booking_number,
            "VGM": vgm,
            "Equipment Substitution": equipment_substitution,
            "Equipment Substitution Reason": equipment_substitution_reason,
            "Cargo Weight": cargo_weight,
            "Release Order Sent": release_order_sent,
            "Contact Name": contact_name,
            "Contact Number": contact_number,
            "EDI Status": edi_status,
            "Commercial Container Type": commercial_container_type,
            "Reefer Temps: set": reefer_temps_set,
            "Reefer Temps: Read": reefer_temps_read,
            "Allocated Release Date": allocated_release_date,
            "Release Location": release_location,
            "Pickup#": pickup_number,
        }

        headers = ["Field", "Value"]
        table_data = [[key, value] for key, value in cargo_data.items()]
        logger.info(tabulate(table_data, headers, tablefmt="grid"))

        # Return Dictionary
        return cargo_data

    # COMMODITIES VEHICLE DETAILS -------------------------------------------------------------------------------------
    def click_commodity_accordion(self):

        accordion = (By.XPATH, f"{self._xpath_commodities_details}//button", "Commodities Details: Vehicle Accordion [Button]")
        accordion_text = (By.XPATH, f"{self._xpath_commodities_details}//button//span", "Commodities Details: Vehicle Accordion [Text]")
        label_accordion = self.get_text().set_locator(accordion_text).by_text()

        logger.info(f"Commodities: {label_accordion}")
        self.click().set_locator(accordion).single_click()
        self.scroll().set_locator(accordion).to_element(-100)

        return self

    def click_commercial_container_details(self):
        accordion = (By.XPATH, f"{self._xpath_commercial_container_details}//button", "Commodities Details: Vehicle Accordion [Button]")
        accordion_text = (By.XPATH, f"{self._xpath_commercial_container_details}//button//span", "Commodities Details: Vehicle Accordion [Text]")
        label_accordion = self.get_text().set_locator(accordion_text).by_text()

        logger.info(f"Commercial Container Details: {label_accordion}")
        self.click().set_locator(accordion).single_click()
        self.scroll().set_locator(accordion).to_element(-100)

        return self

    def get_commercial_container_summary_title(self, index):
        locator = (By.XPATH, f"({self._xpath_commercial_container_details}/section/div/h2//span)[{index}]", f"Commercial Container Summary Title[{index}]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_commodity_vehicle_details_rating_commodity_category(self):
        locator = (By.XPATH,
                   f"{self._xpath_commodities_details}//span[contains(text(),'RATING COMMODITY CATEGORY')]/..//div/span",
                   "Commercial Vehicle Details: RATING COMMODITY CATEGORY [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()
