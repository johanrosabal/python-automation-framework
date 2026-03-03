from selenium.webdriver.common.by import By

from applications.web.csight.components.buttons.Buttons import Buttons
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('CargoNotInContainerShippingPage')


class CargoNotInContainerShippingPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the CargoNotInContainerShippingPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/cargonotincontainershipping"
        # String Base XPaths
        self._xpath_origin = "//label[contains(text(),'Origin')]/.."
        self._xpath_destination = "//label[contains(text(),'Booking Number')]/.."
        # Sub-Components
        self.buttons = Buttons.get_instance()

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

    def click_get_instructions(self):
        self.buttons.click_button_with_label("Get Instructions")
        return self

    def select_origin(self, search="", port_type="", location_name="", location_code="", pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_origin}//input[@type='text']/..", f"Search: Origin [{search}] [Input]")
        # Click Search Input
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Displayed Depending on the Port Type or Location Name or Location Code
        xpath_locator_list = f"{self._xpath_origin}/../../../../../../../../..//ul[@role='listbox']"
        # List Options Locators
        locator_type = (By.XPATH, f"{xpath_locator_list}//span[@class='d-r-p-type'][text()='{port_type}']", f"Search List: Origin > Port Type [{port_type}] [List Text]")
        locator_location_name = (By.XPATH, f"{xpath_locator_list}//span[@class='location-name'][text()='{location_name}']", f"Search List: Origin > Location Name [{location_name}] [List Text]")
        locator_location_code = (By.XPATH, f"{xpath_locator_list}//span[@class='location-code'][text()='{location_code}']", f"Search List: Origin > Location Code [{location_code}] [List Text]")

        if port_type != "":
            self.click().set_locator(locator_type).single_click().pause(pause)

        if location_name != "":
            self.click().set_locator(locator_location_name).single_click().pause(pause)

        if location_code != "":
            self.click().set_locator(locator_location_code).single_click().pause(pause)

        return self

    def select_destination(self, search="", port_type="", location_name="", location_code="", pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_destination}//input[@type='text']/..", f"Search: Destination [{search}] [Input]")
        # Click Search Input
        self.click().set_locator(locator_input).single_click()
        # Input Search Text
        self.send_keys().set_locator(locator_input).set_text(search)
        # Click Option Displayed Depending on the Port Type or Location Name or Location Code
        xpath_locator_list = f"{self._xpath_origin}/../../../../../../../../..//ul[@role='listbox']"
        # List Options Locators
        locator_type = (By.XPATH, f"{xpath_locator_list}//span[@class='d-r-p-type'][text()='{port_type}']", f"Search List: Destination > Port Type [{port_type}] [List Text]")
        locator_location_name = (By.XPATH, f"{xpath_locator_list}//span[@class='location-name'][text()='{location_name}']", f"Search List: Destination > Location Name [{location_name}] [List Text]")
        locator_location_code = (By.XPATH, f"{xpath_locator_list}//span[@class='location-code'][text()='{location_code}']", f"Search List: Destination > Location Code [{location_code}] [List Text]")

        if port_type != "":
            self.click().set_locator(locator_type).single_click().pause(pause)

        if location_name != "":
            self.click().set_locator(locator_location_name).single_click().pause(pause)

        if location_code != "":
            self.click().set_locator(locator_location_code).single_click().pause(pause)

        return self
