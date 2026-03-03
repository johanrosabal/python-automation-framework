from applications.web.csight.actions.RadioWithIndex import RadioWithIndex
from applications.web.csight.actions.CheckboxWithIndex import CheckboxWithIndex
from applications.web.csight.actions.SendKeysWithIndex import SendKeysWithIndex
from applications.web.csight.actions.ToggleAccordion import ToggleAccordion
from core.ui.common.BasePage import BasePage
from core.config.logger_config import setup_logger
from applications.web.csight.actions.DropdownAutocomplete import DropdownAutocomplete
logger = setup_logger('CSightBasePage')


class CSightBasePage(BasePage):

    def __init__(self, driver=None):
        super().__init__()
        if driver:
            self._driver = driver

    def dropdown_autocomplete(self):
        return DropdownAutocomplete(self.get_driver())

    def send_keys_with_index(self):
        return SendKeysWithIndex(self.get_driver())

    def radio_with_index(self):
        return RadioWithIndex(self.get_driver())

    def checkbox_with_index(self):
        return CheckboxWithIndex(self.get_driver())

    def toggle_accordion(self):
        return ToggleAccordion(self.get_driver())

