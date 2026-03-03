from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ShipmentDetailsPage')


class ShipmentDetailsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the ShipmentDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/create"
        self._form = "(//div[contains(@class,'order-details')])"
        # Locator definitions
        self._input_mode = (By.XPATH, f"{self._form}//label[text()='Mode']/..//input", "Mode [Input]")
        self._button_add_on_service = (By.XPATH, f"{self._form}//label[text()='Mode']/..//button", "Add-On Service [Button]")
        self._dropdown_equipment = (By.XPATH,  "//*[@formcontrolname='equipment']", "Equipment [Dropdown]")
        self._dropdown_freight_class = (By.XPATH, f"{self._form}//*[@formcontrolname='freightClass']", "Freight Class [Dropdown]")
        self._input_low_temperature = (By.XPATH, f"{self._form}//label[contains(text(),'Low Temperature °F')]/..//input")
        self._input_high_temperature = (By.XPATH, f"{self._form}//label[contains(text(),'High Temperature °F')]/..//input")
        self._input_po_number = (By.XPATH, f"{self._form}//label[text()='PO Number']/..//input", "PO Number [Input Box]")
        self._input_bill_of_landing_number = (By.XPATH, f"{self._form}//label[text()='Bill Of Lading Number']/..//input", "Bill Of Lading Number[Input Box]")
        self._input_pick_up_number = (By.XPATH, f"{self._form}//label[text()='Pick Up Number']/..//input", "Pick Up Number [Input Box]")
        self._input_shipment_instruction = (By.XPATH, f"{self._form}//label[text()='Shipment Instructions']/..//textarea", "Shipment Instruction [Input Box]")

        # Locator definitions
        self._button_cancel = (By.XPATH, f"{self._form}//button/span[text()='Cancel']", "Cancel [Button]")
        self._button_save_for_later = (By.XPATH, f"{self._form}//button/span[text()='Save For Later']", "Save For Later [Button]")
        self._button_save_and_continue = (By.XPATH, f"{self._form}//button/span[text()='Save & Continue']", "Save & Continue [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = ShipmentDetailsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def get_mode(self):
        return self.get_text().set_locator(self._input_mode, self._name).by_attribute("value")

    def click_add_on_service(self):
        self.click().set_locator(self._button_add_on_service, self._name).single_click()
        return self

    def _select_equipment(self, equipment):
        self.click().set_locator(self._dropdown_equipment).single_click()
        locator = (By.XPATH, f'//mat-option[@role="option"]/span[contains(text(),"{equipment}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _select_freight_class(self, freight_class):
        self.click().set_locator(self._dropdown_freight_class).single_click()
        locator = (By.XPATH, f'//mat-option[@role="option"]/span[contains(text(),"{freight_class}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_low_temperature(self, temperature: int):
        self.send_keys().set_locator(self._input_low_temperature, self._name).set_text(str(temperature))
        return self

    def _enter_high_temperature(self, temperature: int):
        self.send_keys().set_locator(self._input_high_temperature, self._name).set_text(str(temperature))
        return self

    def _enter_po_number(self, po_number):
        self.send_keys().set_locator(self._input_po_number, self._name).set_text(po_number)
        return self

    def _enter_bill_of_landing_number(self, bill_of_lading_number):
        self.send_keys().set_locator(self._input_bill_of_landing_number, self._name).set_text(bill_of_lading_number)
        return self

    def _enter_pick_up_number(self, bill_of_lading_number):
        self.send_keys().set_locator(self._input_pick_up_number, self._name).set_text(bill_of_lading_number)
        return self

    def _enter_shipment_instructions(self, shipment_instructions):
        self.send_keys().set_locator(self._input_shipment_instruction, self._name).set_text(shipment_instructions)
        return self

    def enter_shipment_details(self, equipment, po_number, bill_of_landing_number, pick_up_number, shipment_instructions, freight_class):
        self._select_equipment(equipment)
        self._select_freight_class(freight_class)
        self._enter_po_number(po_number)
        self._enter_bill_of_landing_number(bill_of_landing_number)
        self._enter_pick_up_number(pick_up_number)
        self._enter_shipment_instructions(shipment_instructions)
        return self

    def enter_shipment_details_with_temperature(self, equipment, low_temperature: int, high_temperature: int, po_number, bill_of_landing_number, pick_up_number, shipment_instructions, freight_class):
        self._select_equipment(equipment)
        self._select_freight_class(freight_class)
        self._enter_po_number(po_number)
        self._enter_bill_of_landing_number(bill_of_landing_number)
        self._enter_pick_up_number(pick_up_number)
        self._enter_shipment_instructions(shipment_instructions)
        self._enter_low_temperature(low_temperature)
        self._enter_high_temperature(high_temperature)
        return self

    def click_cancel(self):
        self.click().set_locator(self._button_cancel, self._name).single_click()
        return self

    def click_save_for_later(self):
        self.click().set_locator(self._button_save_for_later, self._name).single_click()
        return self

    def click_save_and_continue(self):
        self.click().set_locator(self._button_save_and_continue, self._name).single_click().pause()
        return self
