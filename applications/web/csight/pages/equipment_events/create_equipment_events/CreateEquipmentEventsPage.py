from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.components.modals.ModalComponent import ModalComponent
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CreateEquipmentEventsPage')


class CreateEquipmentEventsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the CeateEquipmentEventsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/create-equipment-event"
        # Locator definitions
        self._input_sublocation = (By.XPATH, "//label[text()='Sublocation']/..//input", "Sublocation [Input]")
        self._input_location = (By.XPATH, "//label[text()='Location']/..//input", "Location [Input]")
        self._input_event_date = (By.XPATH, "//label[text()='Event Date']/..//input", "Event Date [Input]")
        self._input_event_time = (By.XPATH, "//label[text()='EVENT TIME (HH:MM)']/..//input", "Event Time [Input]")
        self._dropdown_movement = (By.XPATH, "//label[text()='Movement']/../..//button", "Movement [Dropdown]")
        # Equipment Events
        self._input_container_id = (By.XPATH, "//label[text()='Container ID']/..//input", "Container ID [Input]")
        self._input_trucker_scac = (By.XPATH, "//label[text()='Trucker SCAC']/..//input", "Trucker SCAC [Input]")

        # Sub-Components
        self.buttons = Buttons.get_instance()
        self.loadings = Loadings.get_instance()
        self.modal = ModalComponent.get_instance()

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

    def get_equipment_events_link(self):
        equipment_event_url = BaseApp.get_base_url() + self.relative
        return equipment_event_url

    def get_navigation(self):
        return self.navigation().get_current_url()

    def verify_all_locators_present(self):

        self.loadings.is_not_visible_spinner()
        self.pause(1)

        locators = [
            self._input_sublocation,
            self._input_location,
            self._input_event_date,
            self._input_event_time,
            self._dropdown_movement
        ]
        return self.verify_locators().verify_page_locators(locators)

    def select_sublocation(self,  search):
        if search != "":
            self.send_keys().set_locator(self._input_sublocation, self._name).set_text(search)
            list_item_locator = (By.XPATH,
                                 f"//label[text()='Sublocation']/../../../../../../..//ul[contains(@role, 'listbox')]//li//span[contains(text(),'{search}')]")
            self.element().wait(list_item_locator)
            self.click().set_locator(list_item_locator, self._name).single_click().pause(2)

        return self

    def get_location(self):
        return self.get_text().set_locator(self._input_location, self._name).by_text()

    def enter_event_date(self, event_date):
        if event_date != "":
            self.send_keys().set_locator(self._input_event_date, self._name).clear().set_text(event_date)
        return self

    def enter_event_time(self, event_time):
        if event_time != "":
            self.send_keys().set_locator(self._input_event_time, self._name).clear().set_text(event_time)
        return self

    def get_event_time(self):
        return self.get_text().set_locator(self._input_event_time, self._name).by_text()

    def select_movement(self, movement):
        if movement != "":
            self.click().set_locator(self._dropdown_movement, self._name).single_click()
            option_item = (By.XPATH,f"//span[normalize-space(text())='{movement}']/../..", f"Movement Option: {movement} [Click Option]")
            self.click().set_locator(option_item, self._name).single_click()
            self.loadings.is_not_visible_spinner()
        return self

    # Equipment Details ------------------------------------------------------------------------------------------------
    def select_radio_manually(self):
        locator = (By.XPATH,"//input[@name='ENTER MANUALLY']","Enter Manually [Click Radio Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def select_radio_upload_bulk(self):
        locator = (By.XPATH,"//input[@name='UPLOAD BULK']","Enter Upload Bulk [Click Radio Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def select_cargo_type(self, type):
        if type != "":
            locator = (By.XPATH, "//button[contains(@name,'CargoType')]", "CargoType [Select Options]")
            self.click().set_locator(locator,self._name).single_click().pause(1)
            option_item = (By.XPATH, f"//span[@title='{type}']", "[Cargo Type Option]")
            self.click().set_locator(option_item, self._name).single_click()
        return self

    def enter_container_id(self, search):
        if search != "":
            self.element().wait(self._input_container_id)
            self.send_keys().set_locator(self._input_container_id, self._name).set_text(search)
            list_item_locator = (By.XPATH, f"//label[text()='Container ID']/../../../../../../..//ul[contains(@role, 'listbox')]//li//span[contains(text(),'{search}')]")
            self.element().wait(list_item_locator)
            self.click().set_locator(list_item_locator, self._name).single_click().pause(2)

    def enter_trucker_scac(self, trucker_scac):
        # Trucker SCAC
        if trucker_scac != "":
            self.send_keys().set_locator(self._input_trucker_scac, self._name).set_text(trucker_scac)
        return self

    def enter_reference_number(self, index=1, reference_number=None):
        locator = (By.XPATH, f"(//input[@name='Reference_Number__c' and @placeholder='Reference Number' and @type='text'])[{index}]", "Booking / ReferenceNumber [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(reference_number)
        return None

    def enter_seal(self,index=1, seal=None):
        locator = (By.XPATH, f"//input[@name='Seal{index}']", f"Seals {index} [Input]")
        # Seals
        if seal != "":
            self.send_keys().set_locator(locator, self._name).set_text(seal)
        return self

    def fill_equipment_information(self, event_equipment_data=None, booking_number=None):

        """Fill the Create Equipment Event form safely using page helpers."""
        event_equipment = event_equipment_data["tests"][0]["data"]
        event_equipment_data["tests"][0]["data"]["equipment_details"]["reference_type_and_number"][0]["reference_number"] = booking_number

        self.select_sublocation(event_equipment["sublocation"])
        self.enter_event_date(event_equipment["event_date"])
        self.enter_event_time(event_equipment["event_time"])
        self.select_movement(event_equipment["movement"])

        # Equipment Details
        # Radio Button
        if event_equipment["equipment_details"]["enter_manually"]:
            self.select_radio_manually()
        # Radio Button
        if event_equipment["equipment_details"]["upload_bulk"]:
            self.select_radio_upload_bulk()
        # Input +  List Option
        self.select_cargo_type(event_equipment["equipment_details"]["cargo_type"])
        # Input
        self.enter_container_id(event_equipment["equipment_details"]["container_id"])
        self.enter_trucker_scac(event_equipment["equipment_details"]["trucker_scac"])

        for index, ref_type in enumerate(event_equipment["equipment_details"]["reference_type_and_number"]):
            xpath_index = index+1
            self.enter_reference_number(index=xpath_index, reference_number=ref_type["reference_number"])

        for index, seal in enumerate(event_equipment["equipment_details"]["seals"]):
            xpath_index = index + 1
            self.enter_seal(index=xpath_index, seal=seal)

        self.scroll().to_bottom()
        return self

    def click_create_equipment_event(self):
        self.scroll().to_bottom()
        self.buttons.click_button_with_label("CREATE EQUIPMENT EVENT")
        return self

    def get_modal_message(self):
        return self.modal.get_title_contains()

    def modal_is_visible(self):
        return self.modal.is_visible()

