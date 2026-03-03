from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.components.modals.ModalComponent import ModalComponent
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage


class EquipmentEventsPage(BasePage):

    def __init__(self, driver=None):
        """
        Initialize the EquipmentEventsPage instance.
        """
        super().__init__(driver)

        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/equipmentevents"
        # Locator definitions
        self._popup_success_message = (By.XPATH, "//h5[contains(text(), 'Equipment Event has been successfully created.')]", "Success Message [Popup]")

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
        # reuse navigation helper from BasePage
        self.navigation().go(base_url, self.relative)
        return self

    def get_equipment_events_link(self):
        equipment_event_url = BaseApp.get_base_url() + self.relative
        return equipment_event_url

    def get_navigation(self):
        return self.navigation().get_current_url()

    def click_create_equipment_events(self):
        self.buttons.click_button_with_label("CREATE EQUIPMENT EVENTS")
        self.loadings.is_not_visible_spinner()
        return self
