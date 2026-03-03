from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('HazardousSearch')


class HazardousSearch(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the HazardousSearch instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookings"
        # String Base XPaths
        self._xpath_hazardous_booking = "//label[contains(text(),'Hazardous Booking')]/.."
        self._xpath_waste = "//label[contains(text(),'Waste')]/.."
        self._xpath_rcra = "//label[contains(text(),'RCRA')]/.."
        self._xpath_haz_qty_pkg_missing = "//label[contains(text(),'Haz Qty/Pkg Missing')]/.."
        self._xpath_final_imo_received = "//label[contains(text(),'Final IMO Received')]/.."
        self._xpath_secondary_approval_status = "//label[contains(text(),'Secondary Approval Status')]/.."
        self._xpath_hazardous_primary_class_materials = "//label[contains(text(),'Hazardous Primary Class Materials')]/.."
        self._xpath_hazardous_secondary_class_materials = "//label[contains(text(),'Hazardous Secondary Class Materials')]/.."

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

    # HIDE/SHOW PANEL --------------------------------------------------------------------------------------------------
    def open(self):
        self.toggle_accordion().set_locator_with_label('Hazardous').open()
        return self

    def close(self):
        self.toggle_accordion().set_locator_with_label('Hazardous').close()
        return self

    # Search Fields ----------------------------------------------------------------------------------------------------
    def select_radio_hazardous_booking(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_hazardous_booking}//span[text()='Yes']", f"Search: Hazardous Booking [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_hazardous_booking}//span[text()='No']", f"Search: Hazardous Booking [No][{value}][Input]")
            case _:
                logger.warning(f"Hazardous Booking not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_waste(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_waste}//span[text()='Yes']", f"Search: Wasted [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_waste}//span[text()='No']", f"Search: Wasted [No][{value}][Input]")
            case _:
                logger.warning(f"Waste not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_rcra(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_rcra}//span[text()='Yes']", f"Search: RCRA [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_rcra}//span[text()='No']", f"Search: RCRA [No][{value}][Input]")
            case _:
                logger.warning(f"RCRA not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_haz_qty_pkg_missing(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_haz_qty_pkg_missing}//span[text()='Yes']", f"Search: Haz Qty/Pkg Missing [Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_haz_qty_pkg_missing}//span[text()='No']", f"Search: Haz Qty/Pkg Missing [No][{value}][Input]")
            case _:
                logger.warning(f"Haz Qty/Pkg Missing not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_radio_final_imo_received(self, value):
        locator_item = None

        match value:
            case "Yes":
                locator_item = (By.XPATH, f"{self._xpath_final_imo_received}//span[text()='Yes']", f"Search: Final IMO Received[Yes][{value}][Input]")
            case "No":
                locator_item = (By.XPATH, f"{self._xpath_final_imo_received}//span[text()='No']", f"Search: Final IMO Received [No][{value}][Input]")
            case _:
                logger.warning(f"Final IMO Received not found [{value}]")

        if locator_item is not None:
            self.click().set_locator(locator_item).single_click()
        return self

    def select_secondary_approval_status(self, option):
        locator_select = (By.XPATH, f"{self._xpath_secondary_approval_status}//select", f"Search: Secondary Approval Status [{option}][Select]")
        self.dropdown().set_locator(locator_select).by_text(option)
        return self

    def select_multiple_hazardous_primary_class_materials(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_hazardous_primary_class_materials}//input[@type='text']/..",
                         f"Search: Hazardous Primary Class Materials [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_hazardous_primary_class_materials}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: Hazardous Primary Class Materials [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    def select_multiple_hazardous_secondary_class_materials(self, search_text, pause=1):
        # First Click InputBox to Open Options List
        locator_input = (By.XPATH, f"{self._xpath_hazardous_secondary_class_materials}//input[@type='text']/..",
                         f"Search: Hazardous Secondary Class Materials [{search_text}] [Input]")
        self.click().set_locator(locator_input).single_click()
        # Click Option Checkbox Displayed
        locator_check = (By.XPATH,
                         f"{self._xpath_hazardous_secondary_class_materials}//span[contains(@class,'checkbox')]//span/label/span[text()=\"{search_text}\"]/..",
                         f"Search Checkbox List: Hazardous Secondary Class Materials [{search_text}] [Input]")
        self.click().set_locator(locator_check).single_click()
        # Click Input box to lose focus on vertical list, Double Click to Hide List Box
        self.click().set_locator(locator_input).double_click().pause(pause)
        return self

    # Remove Pills Criteria --------------------------------------------------------------------------------------------
    def pill_remove_hazardous_primary_class_materials(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_hazardous_primary_class_materials}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Hazardous Primary Class Materials [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self

    def pill_remove_hazardous_secondary_class_materials(self, search, pause=0):
        locator_pill = (By.XPATH,
                        f"{self._xpath_hazardous_secondary_class_materials}//span[contains(@class,'pill')]//span[text()='{search}']/..//button",
                        f"Pill: Hazardous Secondary Class Materials [{search}][Remove Pill]")
        self.click().set_locator(locator_pill).single_click().pause(pause)
        return self
