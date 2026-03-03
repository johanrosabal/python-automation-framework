from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('FreightDetailsPage')


class FreightDetailsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the FreightDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/create"

        self._form = "(//div[contains(@class,'order-line-items')])"
        # Locator definitions
        self._input_gross_weight = (By.XPATH, f"{self._form}//label[contains(text(),'Gross Weight')]/following-sibling::input", "Gross Weight [Input]")
        self._dropdown_weight = (By.XPATH, f"{self._form}//*[@formcontrolname='grossWeightUOM']", "Weight Type [Select]")
        self._input_handling_unit_count = (By.XPATH, f"{self._form}//label[contains(text(),'Handling Unit Count')]/following-sibling::input", "Handling Unit Count [Input]")
        self._dropdown_handling_unit_type = (By.XPATH, f"{self._form}//*[@formcontrolname='handlingUnitType']", "Handling Unit Type [Select]")
        self._input_commodity_value = (By.XPATH, f"{self._form}//label[contains(text(),'Commodity Value')]/following-sibling::input")
        self._input_length = (By.XPATH, f"{self._form}//label[contains(text(),'Length')]/following-sibling::input")
        self._input_width = (By.XPATH, f"{self._form}//label[contains(text(),'Width')]/following-sibling::input")
        self._input_height = (By.XPATH, f"{self._form}//label[contains(text(),'Height')]/following-sibling::input")
        self._dropdown_uom = (By.XPATH, f"{self._form}//*[@formcontrolname='dimUOM']")
        self._checkbox_hazmat = (By.XPATH, f"{self._form}//span[contains(@class,'mat-checkbox-label')]")
        self._input_commodity_description = (By.XPATH, f"{self._form}//label[contains(text(),'Commodity Description')]/following-sibling::textarea")

        # Locator definitions
        self._button_save_and_add_more_items = (By.XPATH, f"{self._form}//button/span[text()='Save & Add More Items']", "Save & Add More Items [Button]")
        self._button_cancel_edit = (By.XPATH, f"{self._form}//button/span[text()='Cancel Edit']", "Cancel Edit [Button]")

        self._button_cancel = (By.XPATH, f"{self._form}//button/span[text()='Cancel']", "Cancel [Button]")
        self._button_save_for_later = (By.XPATH, f"{self._form}//button/span[text()='Save For Later']", "Save For Later [Button]")
        self._button_save_and_continue = (By.XPATH, f"{self._form}//button/span[text()='Save & Continue']", "Save & Continue [Button]")

        # Locator Hazmat
        self._input_un_na_number = (By.XPATH, f"{self._form}//label[contains(text(),'UN/NA Number')]/following-sibling::input")
        self._input_hazmat_contact_number = (By.XPATH, f"{self._form}//label[contains(text(),'Hazmat Contact Number')]/following-sibling::input")
        self._dropdown_hazmat_class = (By.XPATH, f"{self._form}//*[@ng-reflect-name='hazmatClass']")
        self._dropdown_packing_group = (By.XPATH, f"{self._form}//*[@ng-reflect-name='packingGroup']")
        self._input_proper_shipping_name = (By.XPATH, f"{self._form}//label[contains(text(),'Proper Shipping Name')]/following-sibling::input")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = FreightDetailsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def _enter_gross_weight(self, gross_weight):
        self.send_keys().set_locator(self._input_gross_weight, self._name).clear().set_text(gross_weight)
        return self

    def _select_weight_type(self, weight_type):
        self.click().set_locator(self._dropdown_weight).single_click()
        locator = (By.XPATH, f'//*[@role="option"]/span[contains(text(),"{weight_type}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_handling_unit_count(self, handling_unit_count):
        self.send_keys().set_locator(self._input_handling_unit_count, self._name).clear().set_text(handling_unit_count)
        return self

    def _select_handling_unit_type(self, handling_unit_type):
        self.click().set_locator(self._dropdown_handling_unit_type).single_click()
        locator = (By.XPATH, f'//*[@role="option"]/span[contains(text(),"{handling_unit_type}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_commodity_value(self, commodity_value):
        self.send_keys().set_locator(self._input_commodity_value, self._name).clear().set_text(commodity_value)
        return self

    def _enter_length(self, length):
        self.send_keys().set_locator(self._input_length, self._name).clear().set_text(length).pause(1)
        return self

    def _enter_width(self, width):
        self.send_keys().set_locator(self._input_width, self._name).clear().set_text(width).pause(1)
        return self

    def _enter_height(self, height):
        self.send_keys().set_locator(self._input_height, self._name).clear().set_text(height).pause(1)
        return self

    def _enter_commodity_description(self, text):
        self.send_keys().set_locator(self._input_commodity_description, self._name).clear().set_text(text).pause(1)
        return self

    def _select_uom(self, uom):
        self.click().set_locator(self._dropdown_uom).single_click()
        locator = (By.XPATH, f'//*[@role="option"]/span[contains(text(),"{uom}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _click_hazmat(self):
        self.click().set_locator(self._checkbox_hazmat, self._name).single_click()
        return self

    def _enter_un_na_number(self, un_na_number):
        self.send_keys().set_locator(self._input_un_na_number, self._name).clear().set_text(un_na_number)
        return self

    def _select_hazmat_class(self, hazmat_class):
        self.click().set_locator(self._dropdown_hazmat_class).single_click()
        locator = (By.XPATH, f'//span[@class="mat-option-text" and contains(text(),"{hazmat_class}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_hazmat_contact_number(self, contact_number):
        self.send_keys().set_locator(self._input_hazmat_contact_number, self._name).clear().set_text(contact_number)
        return self

    def _select_packing_group(self, packing_group):
        self.click().set_locator(self._dropdown_packing_group).single_click()
        locator = (By.XPATH, f'//span[@class="mat-option-text" and contains(text(),"{packing_group}")]', "Select Dropdown")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def _enter_proper_shipping_name(self, proper_shipping_name):
        self.send_keys().set_locator(self._input_proper_shipping_name, self._name).clear().set_text(proper_shipping_name)
        return self

    def enter_freight_item(self, gross_weight, weight_type, handling_unit_count, select_handling_unit_type, commodity_value):
        self._enter_gross_weight(gross_weight)
        self._select_weight_type(weight_type)
        self._enter_handling_unit_count(handling_unit_count)
        self._select_handling_unit_type(select_handling_unit_type)
        self._enter_commodity_value(commodity_value)
        return self

    def enter_dimension(self, length, width, height, uom, commodity_description):
        self._enter_length(length)
        self._enter_width(width)
        self._enter_height(height)
        self._select_uom(uom)
        self._enter_commodity_description(commodity_description)
        return self

    def enter_hazmat(self, un_na_number: str, hazmat_class: str, hazmat_contact_number: str, packing_group: str, proper_shipping_name: str):
        self._click_hazmat()
        self._enter_un_na_number(un_na_number)
        self._select_hazmat_class(hazmat_class)
        self._enter_hazmat_contact_number(hazmat_contact_number)
        self._select_packing_group(packing_group)
        self._enter_proper_shipping_name(proper_shipping_name)
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

    def click_save_and_add_more_items(self):
        self.click().set_locator(self._button_save_and_add_more_items, self._name).single_click()
        return self

    def click_cancel_edit(self):
        self.click().set_locator(self._button_cancel_edit, self._name).single_click()
        return self


