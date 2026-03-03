from selenium.webdriver.common.by import By
from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.components.modals.ModalComponent import ModalComponent
from applications.web.csight.pages.bookings.create_booking.cargo_details.BreakBulkTypeComponent import BreakBulkTypeComponent
from applications.web.csight.pages.bookings.create_booking.cargo_details.ContainerTypeComponent import ContainerTypeComponent
from applications.web.csight.pages.bookings.create_booking.vehicles.VehicleTypeComponent import VehicleTypeComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.utils.helpers import safe_get

logger = setup_logger('CargoDetailsPage')


class CargoDetailsComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the CargoDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Locator definitions
        self._tab_cargo_details = (By.XPATH, "//div[@data-label='Cargo Details']", "Cargo Details Tab")
        # Cargo Type -----------------------------------------------------------------------------------------------
        self._checkbox_cargo_type_container = (By.XPATH, "(//span[text()='CONTAINER'])[1]/../..//input", "Cargo Type: CONTAINER [Checkbox]")
        self._checkbox_cargo_type_vehicle = (By.XPATH, "(//span[text()='VEHICLES'])[1]/../..//input/../label/span[@part='indicator']", "Cargo Type: VEHICLE [Checkbox]")
        self._checkbox_cargo_type_cargo_not_in_container = (By.XPATH, "(//span[text()='CARGO NOT IN CONTAINER'])[1]/../..//input/../label/span[@part='indicator']", "Cargo Type: CARGO NOT IN CONTAINER [Checkbox]")
        # Buttons -----------------------------------------------------------------------------------------------
        self._button_add_more = (By.XPATH, "//button[@title='Add More +' or contains(text(),'ADD MORE')]", "ADD MORE [Button]")

        # Sub-Components
        self.loadings = Loadings.get_instance()
        self.container = ContainerTypeComponent.get_instance()
        self.vehicle = VehicleTypeComponent.get_instance()
        self.breakbulk = BreakBulkTypeComponent.get_instance()
        self.modal = ModalComponent.get_instance()

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

    def load_tab(self):
        self.click().set_locator(self._tab_cargo_details, self._name).single_click()
        return self

    def click_add_more(self):
        self.loadings.wait_until_loading_not_present()
        self.scroll().set_locator(self._button_add_more).to_element()
        self.click().set_locator(self._button_add_more, self._name).single_click()
        self.loadings.wait_until_loading_not_present()
        self.scroll().to_top()
        return self

    # Cargo Type -----------------------------------------------------------------------------------------------
    def click_cargo_type_container(self, value):
        current_value = self.element().set_locator(self._checkbox_cargo_type_container).is_selected()
        if current_value is not True:
            self.checkbox().set_locator(self._checkbox_cargo_type_container, self._name).set_value(value)
            self.loadings.wait_until_loading_not_present()
        return self

    def click_cargo_type_vehicle(self, value):
        if value:
            self.click().set_locator(self._checkbox_cargo_type_vehicle).single_click()
            self.vehicle.vehicles_modal_confirmation()
        return self

    def click_cargo_type_cargo_not_in_container(self, value):
        if value:
            self.click().set_locator(self._checkbox_cargo_type_cargo_not_in_container).single_click()
            self.vehicle.vehicles_modal_confirmation()
            self.modal.click_ok()
        return self

    def is_visible_cargo_details(self, result):
        locator = (By.XPATH, "(//div[@id='containerId']//span[text()='CONTAINER'])[1]", "Cargo Details Element")
        visible = self.element().is_present(locator=locator, timeout=5)

        if visible:

            return True
        else:
            result["test_status"] = "FAIL"
            result["booking_message"] = "Origin - Destination Incomplete"
            result["booking_status"] = "NOT CREATED"
            return False

    def process_cargo_type(self, cargo_type=None):
        # Set Up Booking Data if Argument is None
        if self.booking_data:
            cargo_type = self.booking_data['tests']['data']['booking']['cargo_details']['cargo_type']
        # Depending on Cargo Type
        if bool(cargo_type["container"]):
            self.container.set_booking_data(self.booking_data)
            self.scroll().to_top()
            self.click_cargo_type_container(cargo_type["container"])

            containers = self.booking_data['tests']['data']['booking']['cargo_details']['container']

            for index, container in enumerate(containers):
                if index > 0:
                    containerNumber = index+1
                    logger.info(f"Adding Cargo Items: [{containerNumber}]")
                    self.click_add_more()

            self.container.fill_container_general_information()
            self.fill_optional_services_dropdown()
            self.fill_optional_services_with_quantity()
            self.fill_optional_services_only_checkboxes()

        elif bool(cargo_type["vehicles"]):
            self.vehicle.set_booking_data(self.booking_data)
            self.scroll().to_top()
            self.click_cargo_type_vehicle(cargo_type["vehicles"])

            vehicles = self.booking_data['tests']['data']['booking']['cargo_details']['vehicle']

            for index, vehicle in enumerate(vehicles):
                if index > 0:
                    vehicleNumber = index+1
                    logger.info(f"Adding Cargo Items: [{vehicleNumber}]")
                    self.click_add_more()

            self.vehicle.fill_vehicle_general_information()
            self.fill_optional_services_dropdown()
            self.fill_optional_services_with_quantity()
            self.fill_optional_services_only_checkboxes()

        elif bool(cargo_type["cargo_not_in_container"]):
            self.vehicle.set_booking_data(self.booking_data)
            self.scroll().to_top()
            self.click_cargo_type_cargo_not_in_container(cargo_type["cargo_not_in_container"])

            breakbulk = self.booking_data['tests']['data']['booking']['cargo_details']['cargo_not_in_container']

            for index, item in enumerate(breakbulk):
                if index > 0:
                    itemNumber = index+1
                    logger.info(f"Adding Cargo Items: [{itemNumber}]")
                    self.click_add_more()

            self.vehicle.fill_breakbulk_information()
            self.fill_optional_services_dropdown()
            self.fill_optional_services_with_quantity()
            self.fill_optional_services_only_checkboxes()

        else:
            logger.warning("No Cargo Container Selected, please verify the JSON Data Provided!")

        return self

    # OPTIONAL SERVICES -----------------------------------------------------------------------------------------------
    def click_optional_services_accordion(self, index=1):
        locator = (By.XPATH, f"(//div[contains(@class,'OptionalServices')])[{index}]/ul/li/section/div[1]", "Optional Services [Accordion]")
        self.click().set_locator(locator).highlight().single_click()
        return self

    def scroll_to_optional_services_accordion(self, index=1):
        locator = (By.XPATH, f"(//div[contains(@class,'OptionalServices')])[{index}]/ul/li/section/div[1]", "Optional Services [Accordion]")
        self.scroll().set_locator(locator).to_element(pixels=-100)
        return self

    def enter_optional_services_bulkhead(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Bulkhead").by_list_item(text=text)
        return self

    def enter_optional_services_logistic_bar(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Logistic Bar").by_list_item(text=text)
        return self

    def enter_optional_services_protective_covering(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Protective Covering").by_list_item(text=text)
        return self

    def enter_optional_services_EEI_preparation(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="EEI Preparation").by_list_item(text=text)
        return self

    def enter_optional_services_marine_cargo_insurance(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Marine Cargo Insurance").by_list_item_contains(text=text)
        return self

    def enter_optional_services_south_florida_tailgate_government_inspec(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="South Florida Tailgate Government Inspec").by_list_item(text=text)
        return self

    def enter_optional_services_fumigation(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Fumigation").by_list_item(text=text)
        return self

    def enter_optional_services_merchant_haulage(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Merchant Haulage").by_list_item(text=text)
        return self

    def enter_optional_services_team_driver_destination(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Team Driver Destination").by_list_item(text=text)
        return self

    def enter_optional_services_team_driver_origin(self, index=1, text=None):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Team Driver Origin").by_list_item(text=text)
        return self

    def fill_optional_services_dropdown(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        container_type, containers = self.get_cargo_info(booking_data)

        for index, container in enumerate(containers):

            optional_services = booking_data['tests']['data']['booking']['cargo_details'][container_type][index]['optional_services']
            xpath_index = index + 1

            self.scroll_to_optional_services_accordion(index=xpath_index)
            # Row 1 --------------------------------------------------------------------------------------------------------
            if str(optional_services['bulkhead']).lower() != "no":
                self.enter_optional_services_bulkhead(index=xpath_index, text=optional_services['bulkhead'])
            if str(optional_services['EEI_preparation']).lower() != str("EEI Filing").lower():
                self.enter_optional_services_EEI_preparation(index=xpath_index, text=optional_services['EEI_preparation'])
            if str(optional_services['fumigation']).lower() != "no":
                self.enter_optional_services_fumigation(index=xpath_index, text=optional_services['fumigation'])
            # Row 2 --------------------------------------------------------------------------------------------------------
            if str(optional_services['logistic_bar']).lower() != "no":
                self.enter_optional_services_logistic_bar(index=xpath_index, text=optional_services['logistic_bar'])
            if str(optional_services['marine_cargo_insurance']).lower() != str("Up to $50k Cargo Value").lower():
                self.enter_optional_services_marine_cargo_insurance(index=xpath_index, text=optional_services['marine_cargo_insurance'])
            if str(optional_services['merchant_haulage']).lower() != "no":
                self.enter_optional_services_merchant_haulage(index=xpath_index, text=optional_services['merchant_haulage'])
            # Row 3 --------------------------------------------------------------------------------------------------------
            if str(optional_services['protective_covering']).lower() != "no":
                self.enter_optional_services_protective_covering(index=xpath_index, text=optional_services['protective_covering'])
            if str(optional_services['south_florida_tailgate_government_inspec']).lower() != "no":
                self.enter_optional_services_south_florida_tailgate_government_inspec(index=xpath_index, text=optional_services['south_florida_tailgate_government_inspec'])
            if str(optional_services['team_driver_destination']).lower() != "no":
                self.enter_optional_services_team_driver_destination(index=xpath_index, text=optional_services['team_driver_destination'])
            # Row 4 --------------------------------------------------------------------------------------------------------
            if str(optional_services['team_driver_origin']).lower() != "no":
                self.enter_optional_services_team_driver_origin(index=xpath_index, text=optional_services['team_driver_origin'])

        return self

    # OPTIONAL SERVICES: Check with Qty/Price---------------------------------------------------------------------------
    def click_optional_services_additional_bill_of_lading_fee(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Additional Bill of Lading Fee").click().with_text(text=text)
        return self

    def click_optional_services_additional_seals(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Additional Seals").click().with_text(text=text)
        return self

    def click_optional_services_customs_exam(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Customs Exam").click().with_text(text=text)
        return self

    def click_optional_services_multiple_bills_of_lading(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Multiple Bills of Lading").click().with_text(text=text)
        return self

    def click_optional_services_additional_bill_of_lading_fee_return_cargo(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Additional Bill of Lading Fee (Return Cargo)").click().with_text(text=text)
        return self

    def click_optional_services_additional_straps(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Additional Straps").click().with_text(text=text)
        return self

    def click_optional_services_dry_run_false_move_destination(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Dry Run / False Move - Destination").click().with_text(text=text)
        return self

    def click_optional_services_pallets(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Pallets").click().with_text(text=text)
        return self

    def click_optional_services_additional_chains(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Additional Chains").click().with_text(text=text)
        return self

    def click_optional_services_complete_government_inspection(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Complete Government Inspection").click().with_text(text=text)
        return self

    def click_optional_services_dry_run_false_move_origin(self, index=1, text=None):
        self.checkbox_with_index().set_locator(index=index, label="Dry Run / False Move - Origin").click().with_text(text=text)
        return self

    def fill_optional_services_with_quantity(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        # containers = booking_data['tests']['data']['booking']['cargo_details']['container']
        container_type, containers = self.get_cargo_info(booking_data)

        for index, container in enumerate(containers):

            xpath_index = index + 1

            locator = (By.XPATH, f"(//span[text()='Optional Services'])[{xpath_index}]", "Optional Services Accordion")
            self.scroll().set_locator(locator).to_element(pixels=270)

            # Column 1 -------------------------------------------------------------------------------------------------
            if container['optional_services']['additional_bill_of_lading_fee']['checked']:
                self.click_optional_services_additional_bill_of_lading_fee(
                    index=xpath_index,
                    text=str(container['optional_services']['additional_bill_of_lading_fee']['quantity'])
                )

            if container['optional_services']['additional_seals']['checked']:
                self.click_optional_services_additional_seals(
                    index=xpath_index,
                    text=str(container['optional_services']['additional_seals']['quantity'])
                )

            if container['optional_services']['customs_exam']['checked']:
                self.click_optional_services_customs_exam(
                    index=xpath_index,
                    text=str(container['optional_services']['customs_exam']['price'])
                )

            if container['optional_services']['multiple_bills_of_lading']['checked']:
                self.click_optional_services_multiple_bills_of_lading(
                    index=xpath_index,
                    text=str(container['optional_services']['multiple_bills_of_lading']['quantity'])
                )
            # Column 2 -------------------------------------------------------------------------------------------------
            if container['optional_services']['additional_bill_of_lading_fee_return_cargo']['checked']:
                self.click_optional_services_additional_bill_of_lading_fee_return_cargo(
                    index=xpath_index,
                    text=str(container['optional_services']['additional_bill_of_lading_fee_return_cargo']['quantity'])
                )

            if container['optional_services']['additional_straps']['checked']:
                self.click_optional_services_additional_straps(
                    index=xpath_index,
                    text=str(container['optional_services']['additional_straps']['quantity'])
                )

            if container['optional_services']['dry_run_false_move_destination']['checked']:
                self.click_optional_services_dry_run_false_move_destination(
                    index=xpath_index,
                    text=str(container['optional_services']['dry_run_false_move_destination']['price'])
                )

            if container['optional_services']['pallets']['checked']:
                self.click_optional_services_pallets(
                    index=xpath_index,
                    text=str(container['optional_services']['pallets']['quantity'])
                )

            # Column 3 -------------------------------------------------------------------------------------------------
            if container['optional_services']['additional_chains']['checked']:
                self.click_optional_services_additional_chains(
                    index=xpath_index,
                    text=str(container['optional_services']['additional_chains']['quantity'])
                )

            if container['optional_services']['complete_government_inspection']['checked']:
                self.click_optional_services_complete_government_inspection(
                    index=xpath_index,
                    text=str(container['optional_services']['complete_government_inspection']['price'])
                )

            if container['optional_services']['dry_run_false_move_origin']['checked']:
                self.click_optional_services_dry_run_false_move_origin(
                    index=xpath_index,
                    text=str(container['optional_services']['dry_run_false_move_origin']['price'])
                )

        return self

    # OPTIONAL SERVICES: Checks + Quantity -----------------------------------------------------------------------------
    def click_optional_services_additional_cargo_in_on_units(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Additional Cargo in/on Units").click()
        return self

    def click_optional_services_bonded_cargo_document_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Bonded Cargo Document Fee").click()
        return self

    def click_optional_services_customs_clearance_vehicle_wheeled_NIT(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Customs Clearance - Vehicle/Wheeled NIT").click()
        return self

    def click_optional_services_equipment_cleaning(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Equipment Cleaning").click()
        return self

    def click_optional_services_GPS_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="GPS Fee").click()
        return self

    def click_optional_services_late_documentation_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Late Documentation Fee").click()
        return self

    def click_optional_services_shipment_roll_over_charge(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Shipment Roll Over Charge").click()
        return self

    def click_optional_services_WAM_usage(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="WAM Usage").click()
        return self

    def click_optional_services_blocking_bracing_securing_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Blocking / Bracing / Securing Fee").click()
        return self

    def click_optional_services_caricom_invoice_prep_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Caricom Invoice Prep Fee").click()
        return self

    def click_optional_services_diversion_or_reconsignment(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Diversion or Reconsignment").click()
        return self

    def click_optional_services_equipment_repositioning_charge(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Equipment Repositioning Charge").click()
        return self

    def click_optional_services_importer_security_filing(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Importer Security Filing").click()
        return self

    def click_optional_services_late_gate_charge(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Late Gate Charge").click()
        return self

    def click_optional_services_shipper_loaded_flatrack_OOG_cargo_penalty(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Shipper Loaded Flatrack OOG Cargo Penalty").click()
        return self

    def click_optional_services_wire_pick_end_down_charge(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Wire Pick / End Down Charge").click()
        return self

    def click_optional_services_BOL_processing_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="BOL Processing Fee").click()
        return self

    def click_optional_services_custom_brokerage(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Custom Brokerage").click()
        return self

    def click_optional_services_document_change_fee(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Document Change Fee").click()
        return self

    def click_optional_services_excess_fuel_in_vehicles_RO_RO(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="Excess Fuel in Vehicles / RO/RO").click()
        return self

    def click_optional_services_labels_and_placards(self, index=None):
        locator = (By.XPATH, f"(//label[text()='Labels & Placards'] )[{index}]/..//span[@part='indicator']")
        self.click().set_locator(locator).single_click()
        return self

    def click_optional_services_NIT_non_operable(self, index=None):
        self.checkbox_with_index().set_locator(index=index, label="NIT - Non Operable").click()
        return self

    def click_optional_services_VGM_certification(self, index=None):
        locator = (By.XPATH, f"(//label[text()='VGM Certification'] )[{index}]/..//span[@part='indicator']")
        self.click().set_locator(locator).single_click()
        return self

    def fill_optional_services_only_checkboxes(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        # containers = booking_data['tests']['data']['booking']['cargo_details']['container']
        container_type, containers = self.get_cargo_info(booking_data)

        for index, container in enumerate(containers):

            xpath_index = index + 1

            # Column 1 -------------------------------------------------------------------------------------------------
            if container['optional_services']['additional_cargo_in_on_units']:
                self.click_optional_services_additional_cargo_in_on_units(index=xpath_index)

            if container['optional_services']['bonded_cargo_document_fee']:
                self.click_optional_services_bonded_cargo_document_fee(index=xpath_index)

            if container['optional_services']['customs_clearance_vehicle_wheeled_NIT']:
                self.click_optional_services_customs_clearance_vehicle_wheeled_NIT(index=xpath_index)

            if container['optional_services']['equipment_cleaning']:
                self.click_optional_services_equipment_cleaning(index=xpath_index)

            if container['optional_services']['GPS_fee']:
                self.click_optional_services_GPS_fee(index=xpath_index)

            if container['optional_services']['late_documentation_fee']:
                self.click_optional_services_late_documentation_fee(index=xpath_index)

            if container['optional_services']['shipment_roll_over_charge']:
                self.click_optional_services_shipment_roll_over_charge(index=xpath_index)

            if container['optional_services']['WAM_usage']:
                self.click_optional_services_WAM_usage(index=xpath_index)

            # Column 2 -------------------------------------------------------------------------------------------------
            if container['optional_services']['blocking_bracing_securing_fee']:
                self.click_optional_services_blocking_bracing_securing_fee(index=xpath_index)

            if container['optional_services']['caricom_invoice_prep_fee']:
                self.click_optional_services_caricom_invoice_prep_fee(index=xpath_index)

            if container['optional_services']['diversion_or_reconsignment']:
                self.click_optional_services_diversion_or_reconsignment(index=xpath_index)

            if container['optional_services']['equipment_repositioning_charge']:
                self.click_optional_services_equipment_repositioning_charge(index=xpath_index)

            if container['optional_services']['importer_security_filing']:
                self.click_optional_services_importer_security_filing(index=xpath_index)

            if container['optional_services']['late_gate_charge']:
                self.click_optional_services_late_gate_charge(index=xpath_index)

            if container['optional_services']['shipper_loaded_flatrack_OOG_cargo_penalty']:
                self.click_optional_services_shipper_loaded_flatrack_OOG_cargo_penalty(index=xpath_index)

            if container['optional_services']['wire_pick_end_down_charge']:
                self.click_optional_services_wire_pick_end_down_charge(index=xpath_index)

            # Column 3 -------------------------------------------------------------------------------------------------
            if container['optional_services']['BOL_processing_fee']:
                self.click_optional_services_BOL_processing_fee(index=xpath_index)

            if container['optional_services']['custom_brokerage']:
                self.click_optional_services_custom_brokerage(index=xpath_index)

            if container['optional_services']['document_change_fee']:
                self.click_optional_services_document_change_fee(index=xpath_index)

            if container['optional_services']['excess_fuel_in_vehicles_RO_RO']:
                self.click_optional_services_excess_fuel_in_vehicles_RO_RO(index=xpath_index)

            if container['optional_services']['labels_and_placards']:
                self.click_optional_services_labels_and_placards(index=xpath_index)

            if container['optional_services']['NIT_non_operable']:
                self.click_optional_services_NIT_non_operable(index=xpath_index)

            if container['optional_services']['VGM_certification']:
                self.click_optional_services_VGM_certification(index=xpath_index)
        return self

    # OPERATIONAL SERVICES ---------------------------------------------------------------------------------------------
    def select_origin_transfer(self, value):
        locator = (By.XPATH, "//label/span[text()='Origin Transfer']/../..//select", "Origin Transfer [Select Option]")
        self.dropdown().set_locator(locator, self._name).by_text(value)
        return self

    def select_destination_transfer(self, value):
        locator = (By.XPATH, "//label/span[text()='Destination Transfer']/../..//select", "Origin Transfer [Select Option]")
        self.dropdown().set_locator(locator, self._name).by_text(value)
        return self

    def click_checkbox_load_last_hot_hatch(self, value):
        locator = (By.XPATH, "//label/span[text()='Load Last (Hot Hatch)']/../..//span[@part='indicator']", "Load Last (Hot Hatch) [Checkbox]")
        self.checkbox().set_locator(locator, self._name).set_value(value)
        return self

    def click_checkbox_do_not_advance(self, value):
        locator = (By.XPATH, "//label/span[text()='Do not Advance']/../..//span[@part='indicator']", "Do not Advance [Checkbox]")
        self.checkbox().set_locator(locator, self._name).set_value(value)
        return self

    def click_checkbox_do_not_split(self, value):
        locator = (By.XPATH, "//label/span[text()='Do not Split']/../..//span[@part='indicator']", "Do not Split[Checkbox]")
        self.checkbox().set_locator(locator, self._name).set_value(value)
        return self

    def fill_operational_services(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        self.scroll().to_bottom()
        if self.booking_data:
            booking_data = self.booking_data

        operational_services = booking_data['tests']['data']['booking']['cargo_details']['operational_services']

        self.select_origin_transfer(operational_services['origin_transfer'])
        self.select_destination_transfer(operational_services['destination_transfer'])

        self.click_checkbox_load_last_hot_hatch(operational_services['load_last_hot_hatch'])
        self.click_checkbox_do_not_advance(operational_services['do_not_advance'])
        self.click_checkbox_do_not_split(operational_services['do_not_split'])

        return self

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
