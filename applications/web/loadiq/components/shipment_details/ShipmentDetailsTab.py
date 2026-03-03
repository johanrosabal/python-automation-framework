from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ShipmentDetailsTab')


class ShipmentDetailsTab(BasePage):

    def __init__(self, driver):
        """
        Initialize the ShipmentDetailsTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/my_loads/list"
        # Locator definitions
        self._tab_shipment_details = (By.XPATH, "//a[contains(text(),'Shipment Details')]", "Shipment Details [Tab]")
        # Locator: Summary Card
        self._text_equipment = (By.XPATH, "//div[@class='summary-card']//div[text()='Equipment']/../div[2]/span", "Equipment [Text: Summary Card]")
        self._text_equipment_sub = (By.XPATH, "//div[@class='summary-card']//div[text()='Equipment Sub']/../div[2]/span", "Equipment Sub [Text: Summary Card]")
        self._text_total = (By.XPATH, "//div[@class='summary-card']//div[text()='Total ']/../div[2]/span", "Total [Text: Summary Card]")
        self._text_total_weight = (By.XPATH, "//div[@class='summary-card']//div[text()='Total Weight']/../div[2]/span", "Total Weight [Text: Summary Card]")
        self._text_load_value = (By.XPATH, "//div[@class='summary-card']//div[text()='Load Value']/../div[2]/span", "Load Value [Text: Summary Card]")
        self._text_hazmat = (By.XPATH, "//div[@class='summary-card']//div[text()='Hazmat']/../div[2]/span", "Hazmat [Text: Summary Card]")

        self._text_tractor_cont = (By.XPATH, "//div[@class='summary-card']//span[text()='Trailer/Cont.']/../div[2]/span", "Tractor [Text: Summary Card]")

        self._text_tractor = (By.XPATH, "//div[@class='summary-card']//div[text()='Tractor']/../div[2]/span", "Tractor [Text: Summary Card]")
        self._text_driver_cell = (By.XPATH, "//div[@class='summary-card']//div[text()='Driver Cell']/../div[2]/span", "Driver Cell [Text: Summary Card]")

        self._text_genset = (By.XPATH, "//div[@class='summary-card']//div[text()='Genset']/../div[2]/span", "Genset Cell [Text: Summary Card]")
        self._text_chassis = (By.XPATH, "//div[@class='summary-card']//div[text()='Chassis']/../div[2]/span", "Chassis Cell [Text: Summary Card]")

        # Locator: Reference Numbers
        self._text_load_number = (By.XPATH, "//div[@class='summary-card']//div[text()='Load #']/../div[2]/span", "Load # [Text: Reference Numbers]")
        self._text_p_o = (By.XPATH, "//div[@class='summary-card']//div[text()='PO #']/../div[2]/span", "PO # [Text: Reference Numbers]")
        self._text_b_o_l = (By.XPATH, "//div[@class='summary-card']//div[text()='BOL #']/../div[2]/span", "BOL # [Text: Reference Numbers]")
        self._text_booking_number = (By.XPATH, "//div[@class='summary-card']//div[text()='Booking #']/../div[2]/span", "Booking #[Text: Summary Card]")
        self._text_pick_up_number_1 = (By.XPATH, "(//div[@class='summary-card']//div[text()='Pickup #']/../div[2]/span)[1]", "Pickup # (1)[Text: Reference Numbers]")
        self._text_pick_up_number_2 = (By.XPATH, "(//div[@class='summary-card']//div[text()='Pickup #']/../div[2]/span)[2]", "Pickup # (2)[Text: Reference Numbers]")
        self._icon_edit_pick_up_number_2 = (By.XPATH, "(//div[@class='summary-card']//div[text()='Pickup #']/../div[2]/span)[3]", "Pickup # (2)[Icon: Edit Pickup Icon]")
        # Locator: Shipment Instructions
        self._header_instructions = (By.XPATH, "//div[@class='summary-card']/div[3]/h4", "Shipment Instructions [Header]")
        self._text_instructions = (By.XPATH, "//div[@class='summary-card']/div[3]/p", "Instructions [Shipment Instructions Text]")
        # Locator: Table Shipment Items
        self._table_shipment_items = "//table[contains(@class,'table')]"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = ShipmentDetailsTab(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self, tracking_number: str):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        # Click on Tracking Number
        xpath = f"//div[contains(@class,'listingSide')]//span[contains(@class,'text-primary') and contains(text(),'{tracking_number}')]"
        locator = (By.XPATH, xpath, f"Click on Tracking Number: {tracking_number}")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_shipment_details(self):
        self.click().set_locator(self._tab_shipment_details, self._name).single_click()
        return self

    # Summary Card -----------------------------------------------------------------------------------------------------

    def get_equipment(self):
        return self.get_text().set_locator(self._text_equipment, self._name).by_text()
    
    def over_equipment(self):
        self.click().set_locator(self._text_equipment).mouse_over()
        locator = (By.XPATH, "//div[@class='cdk-overlay-container']", "Tool Tip Hidden")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_equipment_sub(self):
        return self.get_text().set_locator(self._text_equipment_sub, self._name).by_text()

    def get_total(self):
        return self.get_text().set_locator(self._text_total, self._name).by_text()

    def get_total_weight(self):
        return self.get_text().set_locator(self._text_total_weight, self._name).by_text()

    def get_load_value(self):
        return self.get_text().set_locator(self._text_load_value, self._name).by_text()

    def get_hazmat(self):
        return self.get_text().set_locator(self._text_hazmat, self._name).by_text()

    def get_trailer_cont(self):
        return self.get_text().set_locator(self._text_tractor_cont, self._name).by_text()

    def get_tractor(self):
        return self.get_text().set_locator(self._text_tractor, self._name).by_text()

    def get_driver_cell(self):
        return self.get_text().set_locator(self._text_driver_cell, self._name).by_text()

    def get_genset(self):
        self.scroll().set_locator(self._text_chassis, self._name).to_element(pixels=-100)
        return self.get_text().set_locator(self._text_genset, self._name).by_text()

    def get_chassis(self):
        self.scroll().set_locator(self._text_chassis, self._name).to_element(pixels=-100)
        return self.get_text().set_locator(self._text_chassis, self._name).by_text()

    # Reference Numbers ------------------------------------------------------------------------------------------------

    def get_load_number(self):
        return self.get_text().set_locator(self._text_load_number, self._name).by_text()

    def get_po_number(self):
        return self.get_text().set_locator(self._text_p_o, self._name).by_text()

    def get_bol_number(self):
        return self.get_text().set_locator(self._text_b_o_l, self._name).by_text()

    def get_booking_number(self):
        return self.get_text().set_locator(self._text_booking_number, self._name).by_text()

    def over_booking_number(self):
        self.click().set_locator(self._text_booking_number).mouse_over()
        locator = (By.XPATH, "//div[@class='cdk-overlay-container']", "Tool Tip Hidden")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_pick_up_number_1(self):
        return self.get_text().set_locator(self._text_pick_up_number_1, self._name).by_text()

    def get_pick_up_number_2(self):
        return self.get_text().set_locator(self._text_pick_up_number_2, self._name).by_text()

    def click_edit_pickup_number(self):
        self.click().set_locator(self._icon_edit_pick_up_number_2, self._name).single_click()
        return self

    # Shipment Instructions --------------------------------------------------------------------------------------------

    def get_header_shipment_instructions(self):
        return self.get_text().set_locator(self._header_instructions, self._name).by_text()

    def get_shipment_instructions(self):
        return self.get_text().set_locator(self._text_instructions, self._name).by_text()

    # Table: Shipment Items --------------------------------------------------------------------------------------------
    def get_table_part_name(self, index: int):
        xpath = f"{self._table_shipment_items}/tbody/tr[{index}]/td[1]"
        locator = (By.XPATH, xpath, "Part Name [Table Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_quantity(self, index: int):
        xpath = f"{self._table_shipment_items}/tbody/tr[{index}]/td[2]"
        locator = (By.XPATH, xpath, "Quantity [Table Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_handling_unit(self, index: int):
        xpath = f"{self._table_shipment_items}/tbody/tr[{index}]/td[3]"
        locator = (By.XPATH, xpath, "Handling Unit [Table Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_dimensions(self, index: int):
        xpath = f"{self._table_shipment_items}/tbody/tr[{index}]/td[4]"
        locator = (By.XPATH, xpath, "Dimensions [Table Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_weight_per_hu_lb(self, index: int):
        xpath = f"{self._table_shipment_items}/tbody/tr[{index}]/td[5]"
        locator = (By.XPATH, xpath, "Weight per HU (Lb) [Table Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_total_weight_lb(self, index: int):
        xpath = f"{self._table_shipment_items}/tbody/tr[{index}]/td[6]"
        locator = (By.XPATH, xpath, "Total Weight (Lb) [Table Cell]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_table_shipment_items(self, index: int):
        row = {
            "part_name": self.get_table_part_name(index),
            "quantity": self.get_table_quantity(index),
            "handling_unit": self.get_table_handling_unit(index),
            "dimensions": self.get_table_dimensions(index),
            "weight_per_hu_lb": self.get_table_weight_per_hu_lb(index),
            "total_weight_lb": self.get_table_total_weight_lb(index)
        }

        return row

    def get_table_total(self):
        locator = (By.XPATH, "//table[contains(@class,'table')]/tbody/tr[@class='last']/td[2]", "Table Total [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()
