from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.loadings.Loadings import Loadings
from core.config.logger_config import setup_logger
from core.utils.helpers import safe_get
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('HazardousDetailsComponent')


class HazardousDetailsComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the HazardousDetailsComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Sub-Components
        self.loadings = Loadings.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def set_booking_data(self, data=None):
        """ Set Booking Data and share with all fill methods """
        self.booking_data = data
        return self

    def select_toggle_final_IMO_received(self, index=1):
        locator = (By.XPATH, f"(//label[text()='Final IMO Received'])[{str(index)}]/..//lightning-input",
                   "Final IMO Received [Toggle button]")
        if self.element().set_locator(locator).is_enabled():
            self.click().set_locator(locator, self._name).single_click()
            self.loadings.wait_until_loading_not_present()
        else:
            logger.warning("Final IMO Received Element is not enable to be Clickable.")
        return self

    def click_upload_files(self, index=1, file_name=None):
        file_upload = (By.XPATH,
                       f"(//label/strong[text()='Upload IMO Document']/../..//span[@part='button'])[{index}]/../..//input[@type='file']",
                       "Hidden Input File")
        self.upload_file().set_locator(file_upload).set_file_name(file_name).upload().pause(4)

        done_locator = (By.XPATH, "//button/span[text()='Done']", "Done [Button to Confirm Upload File]")
        self.element().set_locator(done_locator).is_visible()
        self.pause(2)
        self.click().set_locator(done_locator).single_click().pause(2)
        return self

    def click_remove_file_uploaded(self, index=1, item=1):
        locator = (
            By.XPATH, f"((//label[text()='Files Uploaded:']/..)[{index}]//a)[{item}]",
            f"Remove File Upload Item: {item}")
        self.click().set_locator(locator, self._name).single_click()
        self.loadings.is_not_visible_spinner()
        return self

    def enter_emergency_contact_name(self, index=1, text=None):
        return self.send_keys_with_index().set_locator(index=index, label="Emergency Contact Name").by_text(text=text)

    def enter_emergency_contact_number(self, index=1, text=None):
        return self.send_keys_with_index().set_locator(index=index, label="Emergency Contact Number").by_text(text=text)

    def enter_haz_contract_number(self, index=1, text=None):
        return self.send_keys_with_index().set_locator(index=index, label="Haz Contract Number").by_text(text=text)

    def select_UN_number(self, container_index=1, un_number_index=1, UN_Number=None, proper_shipping_name=None, group_name=None):

        # Click UN Number on Form
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[text()='UN Number']/..//input[@type='text'])[{un_number_index}] | ((((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5])[1]/div//label[text()='UN Number']/..//input[@type='text'])[{un_number_index}]",
                   "UN Number [Input Box Clickable]")

        element = self.element().wait_for_element_present(self.get_driver(), locator, 5)
        self.scroll().set_element(element).to_element(pixels=-100)

        if element.is_enabled():

            self.element().is_present(locator=locator, timeout=15)
            self.click().set_locator(locator).single_click()

            # Enter UN Number on Modal Window
            locator = (By.XPATH, "//div[contains(@class,'modal__container')]//input[@type='search' or @type='text']", "Select Hazardous Items [Modal Dialog Box]")
            self.element().is_present(locator=locator, timeout=15)
            self.send_keys().set_locator(locator).set_text_with_javascript(UN_Number).pause(3)

            locator_table = (By.XPATH, "//div[contains(@class,'modal__container')]//table", "Table Select Hazardous Items")
            table_size = self.table().set_locator(locator_table).get_row_count()

            for i in range(1, table_size + 1):
                table_proper_shipper_name = (By.XPATH, f"//div[contains(@class,'modal__container')]//table/tbody/tr[{i}]/td[2]", f"Table Row [{i}]")
                table_packing_group = (By.XPATH, f"//div[contains(@class,'modal__container')]//table/tbody/tr[{i}]/td[6]", f"Table Row [{i}]")

                str_proper_shipping_name = self.get_text().set_locator(table_proper_shipper_name).by_text()
                str_packing_group = self.get_text().set_locator(table_packing_group).by_text()

                if str_proper_shipping_name == proper_shipping_name and str_packing_group == group_name:
                    # Select Proper Shipping Name
                    locator = (By.XPATH, f"//div[contains(@class,'modal__container')]//table/tbody/tr[{i}]/td[1]//lightning-primitive-input-radio/div/span")
                    # table_group_name =
                    self.element().is_present(locator=locator, timeout=15)
                    self.click().set_locator(locator).single_click()
                    break

                if str_proper_shipping_name == proper_shipping_name and str_packing_group == "":
                    locator = (By.XPATH, f"//div[contains(@class,'modal__container')]//td[contains(text(),'{proper_shipping_name}')]/..//td[1]//lightning-primitive-input-radio/div/span")
                    # table_group_name =
                    self.element().is_present(locator=locator, timeout=15)
                    self.click().set_locator(locator).highlight().single_click()
                    break

            # Click Confirm Button within modal
            locator = (By.XPATH, "//div[contains(@class,'modal__container')]//button[text()='CONFIRM']", "Confirm [Modal Button]")
            self.click().set_locator(locator).single_click()
            self.pause(1)

        else:
            logger.warning(f"UN Number Field not enable to interact index [{un_number_index}]")

        return self

    def select_content_type(self, container_index=1, content_type_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Content Type')])[{content_type_index}]/..//input[@type='text'] | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Content Type')]/..//input[@type='text'])[{content_type_index}]",
                   "Content Type [Input Search]")

        element = self.element().wait_for_element_present(self.get_driver(), locator, 5)

        if element.is_enabled():
            self.send_keys().set_locator(locator).clear().set_text(text).pause(2)
            item_selected = (By.XPATH, f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Content Type')])[{content_type_index}]/..//ul[@role='menu']/li/span[contains(text(),'{text}')] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Content Type')]/..//ul[@role='menu']/li/span[contains(text(),'{text}')]")
            self.element().is_present(item_selected)
            self.click().set_locator(item_selected).highlight().javascript_click()
        else:
            logger.warning(f"Content Type Field not enable to interact index [{content_type_index}]")
        return self

    def enter_permit_number(self, container_index=1, permit_number_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Permit Number')])[{permit_number_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Permit Number')]/..//input[@type='text'])[{permit_number_index}]",
                   "Permit Number [Input Box]")

        self.scroll().set_locator(locator).to_element(pixels=-100)
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_ex_number(self, container_index=1, ex_number_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Ex Number')])[{ex_number_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Ex Number')]/..//input[@type='text'])[{ex_number_index}]",
                   "Ex Number [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_technical_name(self, container_index=1, technical_name_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Technical Name')])[{technical_name_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Technical Name')]/..//input[@type='text'])[{technical_name_index}]",
                   "Technical Name [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_secondary_emergency_contact_name(self, container_index=1, name_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Secondary Emergency Contact Name')])[{name_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Secondary Emergency Contact Name')]/..//input[@type='text'])[{name_index}]",
                   "Secondary Emergency Contact Name [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_secondary_emergency_contact_number(self, container_index=1, number_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Secondary Emergency Contact Number')])[{number_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Secondary Emergency Contact Number')]/..//input[@type='text'])[{number_index}]",
                   "Secondary Emergency Contact Number [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_secondary_haz_contract_number(self, container_index=1, contract_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Secondary Haz Contract Number')])[{contract_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Secondary Haz Contract Number')]/..//input[@type='text'])[{contract_index}]",
                   "Secondary Haz Contract Number [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_special_provision(self, container_index=1, special_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Special Provision')])[{special_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Special Provision')]/..//input[@type='text'])[{special_index}]",
                   "Special Provision [Input Box]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def enter_special_permit(self, container_index=1, special_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Special Permit')])[{special_index}]/..//input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Special Permit')]/..//input[@type='text'])[{special_index}]",
                   "Special Permit [Select Option]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def select_excepted_quantity(self, container_index=1, excepted_quantity_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label/span[contains(text(),'Excepted Quantity')])[{excepted_quantity_index}]/../..//select | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label/span[contains(text(),'Excepted Quantity')]/../..//select)[{excepted_quantity_index}]",
                   "Excepted Quantity [Select Option]")
        self.dropdown().set_locator(locator).by_text(text)
        return self

    def select_marine_pollutant(self, container_index=1, marine_pollutant_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//span[contains(text(),'Marine Pollutant')])[{marine_pollutant_index}]/../../../../tbody/tr[1]/td[7]//select | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//table/tbody/tr[1]/td[7]//select",
                   "Marine Pollutant [Select Option]")
        self.dropdown().set_locator(locator).by_text(text)
        return self

    def select_max_limited_quantity_in_package(self, container_index=1, quantity_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//span[contains(text(),'Max. Limited Quantity in Package')])[{quantity_index}]/../../../../tbody/tr[1]/td[8]//select | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//table/tbody/tr[1]/td[8]//select",
                   "Marine Pollutant [Select Option]")
        self.dropdown().set_locator(locator).by_text(text)
        return self

    def get_table_proper_shipping_name(self, container_index=1, col_index=1):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//span[contains(text(),'Proper Shipping Name')])[{col_index}]/../../../../tbody/tr[1]/td[1] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//table/tbody/tr[1]/td[1]",
                   "Proper Shipping Name [Table Text Value]")
        self.get_text().set_locator(locator).by_text()
        return self

    def get_table_primary_hazardous(self, container_index=1, col_index=1):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//span[contains(text(),'Primary Hazard')])[{col_index}]/../../../../tbody/tr[1]/td[2] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//table/tbody/tr[1]/td[2]",
                   "Primary Hazard [Table Text Value]")
        self.get_text().set_locator(locator).by_text()
        return self

    def click_table_edit_hazmat_UN_record(self, container_index=1, link_index=1):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//span[contains(text(),'Max. Limited Quantity in Package')])[{link_index}]/../../../../tbody/tr[1]/td[10]//a | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//table/tbody/tr[1]/td[10]/a",
                   "Edit Link Action [Edit Link]")

        self.click().set_locator(locator).single_click()
        return self

    def click_add_hazardous_commodity_button(self, index=None):
        locator = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}])//a[text()='+ Hazardous Commodity Add Button']", "Add Hazardous UN Number")
        self.click().set_locator(locator).single_click()
        return

    def remove_hazardous_commodity(self, index=1, item=1):
        locator = (By.XPATH, f"(((//div[@id='containerId']/div/div[2]/div)[{index}])//a[text()='- Remove'])[{item}]", "Remove Hazardous UN Number")
        self.element().is_present(locator, timeout=5)
        self.click().set_locator(locator).single_click()
        return

    def enter_flash_temperature(self, container_index=1, temperature_index=1, text=None, scale=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Flash Temperature')])[{temperature_index}]/..//input[@type='text'] | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Flash Temperature')]/..//input[@type='text'])[{temperature_index}]",
                   "Flash Temperature [Input Box]")
        self.send_keys().set_locator(locator).set_text(str(text))

        options = (By.XPATH,
                   f"((((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Flash Temperature')])[{temperature_index}]/../../../../..//select) | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Flash Temperature')]/../../../../..//select)[{temperature_index}]",
                   "Flash Temperature [Options]")
        self.element().is_present(locator=options, timeout=10)
        self.dropdown().set_locator(options).by_value(scale)

        return self

    def enter_report_spill_quantity(self, container_index=1, report_spill_index=1, text=None, scale=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Report Spill Quantity')])[{report_spill_index}]/..//input[@type='text'] | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Report Spill Quantity')]/..//input[@type='text'])[{report_spill_index}]",
                   "Report Spill Quantity [Input Box]")
        self.send_keys().set_locator(locator).set_text(str(text))

        options = (By.XPATH,
                   f"((((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Report Spill Quantity')])[{report_spill_index}]/../../../../..//select) | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Report Spill Quantity')]/../../../../..//select)[{report_spill_index}]",
                   "Report Spill Quantity [Options]")
        self.element().is_present(locator=options, timeout=10)

        self.dropdown().set_locator(options).by_text(scale)

        return self

    def enter_quantity(self, container_index=1, quantity_index=1, text=None):
        locator = (By.XPATH,
                   f"((((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[text()='Quantity'])[2]/../../../../../../..//label[text()='Quantity']/..//input)[{quantity_index}] | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[text()='Quantity']/../../..//input)[{quantity_index}]",
                   "UN Number Quantity [Input Box]")
        self.send_keys().set_locator(locator).clear().set_text(str(text))
        return self

    def select_type_of_package(self, container_index=1, content_type_index=1, text=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Type of Package')])[{content_type_index}]/..//input[@type='text'] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Type of Package')]/..//input",
                   "Type of Package [Input Search]")

        if self.element().set_locator(locator).is_enabled():
            self.send_keys().set_locator(locator).clear().set_text(str(text))
            options = (By.XPATH,
                       f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Type of Package')])[{content_type_index}]/..//ul[@role='menu']/li/span[contains(text(),'{text}')]",
                       "Type of Package")
            self.element().is_present(locator=options, timeout=10)
            self.click().set_locator(options).single_click()
        return self

    def enter_weight(self, container_index=1, report_spill_index=1, text=None, scale=None):
        locator = (By.XPATH,
                   f"(((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Weight')])[{report_spill_index}]/..//input[@type='text'] | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Weight')]/..//input)[{report_spill_index}]",
                   "Weight [Input Box]")
        self.send_keys().set_locator(locator).clear().set_text(str(text))

        options = (By.XPATH,
                   f"((((//div[@id='containerId']/div/div[2]/div)[{container_index}])//label[contains(text(),'Weight')])[{report_spill_index}]/../../../../..//select) | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//label[contains(text(),'Weight')]/../../../../..//select)[{report_spill_index}]",
                   "Weight [Options]")
        self.element().is_present(locator=options, timeout=10)
        self.dropdown().set_locator(options).by_text(scale)
        return self

    def fill_hazardous_details(self, booking_data=None):

        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        # containers = booking_data['tests']['data']['booking']['cargo_details']['container']
        container_type, containers = self.get_cargo_info(booking_data)

        for index_c, container in enumerate(containers):
            # Adjusting Index for XPaths
            index = index_c + 1

            if str(containers[index_c]['hazardous_details_entered']).lower() == "yes":
                # Extracting Hazardous Details
                hazardous_details = containers[index_c]['hazardous_details']

                if hazardous_details['final_IMO_received']:
                    self.select_toggle_final_IMO_received(index=index)

                if len(hazardous_details['upload_files']) > 0:
                    for file in hazardous_details['upload_files']:
                        self.click_upload_files(index=index, file_name=file)

                if len(hazardous_details['upload_files_remove']) > 0:
                    for file in hazardous_details['upload_files_remove']:
                        self.click_remove_file_uploaded(index=index, item=file)

                # Second UN Content Field Disable on Form [Break Bulk Cargo Type]
                if container_type == 'cargo_not_in_container' and index_c == 0:
                    if hazardous_details['emergency_contact_name'] != "":
                        self.enter_emergency_contact_name(index=index, text=hazardous_details['emergency_contact_name'])
                    if hazardous_details['emergency_contact_number'] != "":
                        self.enter_emergency_contact_number(index=index, text=hazardous_details['emergency_contact_number'])
                    if hazardous_details['haz_contract_number'] != "":
                        self.enter_haz_contract_number(index=index, text=hazardous_details['haz_contract_number'])

                # Note: Review Container and Vehicles
                if container_type != 'cargo_not_in_container':
                    if hazardous_details['emergency_contact_name'] != "":
                        self.enter_emergency_contact_name(index=index, text=hazardous_details['emergency_contact_name'])
                    if hazardous_details['emergency_contact_number'] != "":
                        self.enter_emergency_contact_number(index=index, text=hazardous_details['emergency_contact_number'])
                    if hazardous_details['haz_contract_number'] != "":
                        self.enter_haz_contract_number(index=index, text=hazardous_details['haz_contract_number'])

                if len(hazardous_details['UN_number']) > 0:

                    for Un_index, UN_Number in enumerate(hazardous_details['UN_number']):
                        # XIndex For XPATH
                        Xindex = Un_index + 1

                        # Click Add has more than 1 hazardous UN Number
                        if Un_index > 0:
                            self.click_add_hazardous_commodity_button(index=index)

                        # Second UN Content Field Disable on Form [Break Bulk Cargo Type]
                        if container_type == 'cargo_not_in_container' and Un_index == 0:
                            if UN_Number['code'] != "":
                                self.select_UN_number(
                                    container_index=index,
                                    un_number_index=Xindex,
                                    UN_Number=UN_Number['code'],
                                    proper_shipping_name=UN_Number['proper_shipping'],
                                    group_name=UN_Number['package_group'],
                                )

                            if UN_Number['content_type'] != "":
                                self.select_content_type(
                                    container_index=index,
                                    content_type_index=Xindex,
                                    text=UN_Number['content_type']
                                )

                        # Note: Review Container and Vehicles
                        if container_type != 'cargo_not_in_container':
                            if UN_Number['code'] != "":
                                self.select_UN_number(
                                    container_index=index,
                                    un_number_index=Xindex,
                                    UN_Number=UN_Number['code'],
                                    proper_shipping_name=UN_Number['proper_shipping'],
                                    group_name=UN_Number['package_group'],
                                )

                            if UN_Number['content_type'] != "":
                                self.select_content_type(
                                    container_index=index,
                                    content_type_index=Xindex,
                                    text=UN_Number['content_type']
                                )

                        if UN_Number['permit_number'] != "":
                            self.enter_permit_number(
                                container_index=index,
                                permit_number_index=Xindex,
                                text=UN_Number['permit_number']
                            )

                        if UN_Number['ex_number'] != "":
                            self.enter_ex_number(
                                container_index=index,
                                ex_number_index=Xindex,
                                text=UN_Number['ex_number']
                            )

                        if UN_Number['technical_name'] != "":
                            self.enter_technical_name(
                                container_index=index,
                                technical_name_index=Xindex,
                                text=UN_Number['technical_name']
                            )

                        if UN_Number['secondary_emergency_contact_name'] != "":
                            self.enter_secondary_emergency_contact_name(
                                container_index=index,
                                name_index=Xindex,
                                text=UN_Number['secondary_emergency_contact_name']
                            )

                        if UN_Number['secondary_emergency_contact_number'] != "":
                            self.enter_secondary_emergency_contact_number(
                                container_index=index,
                                number_index=Xindex,
                                text=UN_Number['secondary_emergency_contact_number']
                            )

                        if UN_Number['secondary_haz_contract_number'] != "":
                            self.enter_secondary_haz_contract_number(
                                container_index=index,
                                contract_index=Xindex,
                                text=UN_Number['secondary_haz_contract_number']
                            )

                        if UN_Number['special_provision'] != "":
                            self.enter_special_provision(
                                container_index=index,
                                special_index=Xindex,
                                text=UN_Number['special_provision']
                            )

                        if UN_Number['special_permit'] != "":
                            self.enter_special_permit(
                                container_index=index,
                                special_index=Xindex,
                                text=UN_Number['special_permit']
                            )

                        if UN_Number['excepted_quantity'] != "Select an option":
                            self.select_excepted_quantity(
                                container_index=index,
                                excepted_quantity_index=Xindex,
                                text=UN_Number['excepted_quantity']
                            )

                        if str(UN_Number['marine_pollutant']).lower() != "no":
                            self.select_marine_pollutant(
                                container_index=index,
                                marine_pollutant_index=Xindex,
                                text=UN_Number['marine_pollutant']
                            )

                        if str(UN_Number['max_limited_quantity_in_package']).lower() != "no":
                            self.select_max_limited_quantity_in_package(
                                container_index=index,
                                quantity_index=Xindex,
                                text=UN_Number['max_limited_quantity_in_package']
                            )

                        if UN_Number['flash_temperature']['amount'] > 0:
                            self.enter_flash_temperature(
                                container_index=index,
                                temperature_index=Xindex,
                                text=UN_Number['flash_temperature']['amount'],
                                scale=UN_Number['flash_temperature']['scale']
                            )

                        if UN_Number['report_spill_quantity']['amount'] > 0:
                            self.enter_report_spill_quantity(
                                container_index=index,
                                report_spill_index=Xindex,
                                text=UN_Number['report_spill_quantity']['amount'],
                                scale=UN_Number['report_spill_quantity']['scale']
                            )

                        if UN_Number['type_of_package'] != "" and container_type != 'cargo_not_in_container':
                            self.select_type_of_package(
                                container_index=index,
                                content_type_index=Xindex,
                                text=UN_Number['type_of_package']
                            )

                        if UN_Number['quantity'] > 0:
                            self.enter_quantity(
                                container_index=index,
                                quantity_index=Xindex,
                                text=UN_Number['quantity']
                            )

                        if UN_Number['weight']['amount'] > 0 and container_type != 'cargo_not_in_container':
                            self.enter_weight(
                                container_index=index,
                                report_spill_index=Xindex,
                                text=UN_Number['weight']['amount'],
                                scale=UN_Number['weight']['scale']
                            )

                if len(hazardous_details['remove_UN_number']) > 0:
                    for Un_index, UN_Number in enumerate(hazardous_details['remove_UN_number']):
                        self.remove_hazardous_commodity(
                            index=index,
                            item=UN_Number
                        )

    @staticmethod
    def get_cargo_info(booking_data=None):
        """
        Extract Type of Cargo Type
        """
        booking = safe_get(booking_data, 'tests', 'data', 'booking')

        if not booking:
            raise ValueError("Booking structure not found")

        cargo_type = booking.get('cargo_details', {}).get('cargo_type', {})
        container_type = None

        if cargo_type.get('container') is True:
            container_type = 'container'
            containers = booking.get('cargo_details', {}).get('container', {})
        elif cargo_type.get('vehicles') is True:
            container_type = 'vehicle'
            containers = booking.get('cargo_details', {}).get('vehicle', {})
        elif cargo_type.get('cargo_not_in_container') is True:
            container_type = 'cargo_not_in_container'
            containers = booking.get('cargo_details', {}).get('cargo_not_in_container', {})
        else:
            containers = None
            logger.error('JSON Not Contain a Valid Cargo Type')

        return container_type, containers
