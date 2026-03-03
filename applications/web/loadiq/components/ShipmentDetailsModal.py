from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ShipmentDetailsModal')


class ShipmentDetailsModal(BasePage):

    def __init__(self, driver):
        """
        Initialize the ShipmentDetailsModal instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/my_loads/list"
        # Locator definitions
        # Origin
        self._text_load_number = (By.XPATH, "//div[@class='load-number-text']", "Load Number [Text]")
        self._text_origin_address_line_1 = (By.XPATH, "(//div[contains(@class,'address-column')])[1]/div/p/span[1]", "Origin Address Line 1 [Text Span]")
        self._text_origin_address_line_2 = (By.XPATH, "(//div[contains(@class,'address-column')])[1]/div/p/span[2]", "Origin Address Line 2 [Text Span]")
        self._text_origin_address_line_3 = (By.XPATH, "(//div[contains(@class,'address-column')])[1]/div/p/span[3]", "Origin Address Line 3 [Text Span]")
        self._icon_origin_contact_information = (By.XPATH, "(//div[contains(@class,'address-column')])[1]/div/div[1]", "Origin Contact Information [Icon]")
        self._icon_origin_street_view = (By.XPATH, "(//div[contains(@class,'address-column')])[1]/div/div[2]", "Origin Street View [Icon]")
        self._text_origin_address_date_delivered = (By.XPATH, "((//div[contains(@class,'address-column')])[1]//div[contains(@class,'star-inserted')]/div)[2]/div/div/div/div", "Origin Address Date: Delivered [Text]")
        self._text_origin_address_date = (By.XPATH, "((//div[contains(@class,'address-column')])[1]//div[contains(@class,'star-inserted')]/div)[2]/div/div[2]", "Origin Address Date: Delivered [Text]")
        # Destination
        self._text_destination_address_line_1 = (By.XPATH, "(//div[contains(@class,'address-column')])[2]/div/p/span[1]", "Destination Address Line 1 [Text Span]")
        self._text_destination_address_line_2 = (By.XPATH, "(//div[contains(@class,'address-column')])[2]/div/p/span[2]", "Destination Address Line 2 [Text Span]")
        self._text_destination_address_line_3 = (By.XPATH, "(//div[contains(@class,'address-column')])[2]/div/p/span[3]", "Destination Address Line 3 [Text Span]")
        self._icon_destination_contact_information = (By.XPATH, "(//div[contains(@class,'address-column')])[2]/div/div[1]", "Destination Contact Information [Icon]")
        self._icon_destination_street_view = (By.XPATH, "(//div[contains(@class,'address-column')])[2]/div/div[2]", "DestinationStreet View [Icon]")
        self._text_destination_address_date_delivered = (By.XPATH, "((//div[contains(@class,'address-column')])[2]//div[contains(@class,'star-inserted')]/div)[2]/div/div/div/div", "Destination Address Date [Text]")
        # Buttons
        self._button_complete_delivery = (By.XPATH, "//button[contains(text(),'Complete Delivery')]", "Complete Delivery [Button]")
        self._button_request_accessorials = (By.XPATH, "//button/span[contains(text(),'Request Accessorials')]", "Request Accessorials [Button]")
        self._button_update_load_info = (By.XPATH, "//button/span[contains(text(),'Update Load Info')]", "Update Load Info [Button]")
        self._button_status_update = (By.XPATH, "//button/span[contains(text(),'Status Update')]", "Update Load Info [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = ShipmentDetailsModal(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def get_load_number(self):
        return self.get_text().set_locator(self._text_load_number, self._name).highlight().by_text()

    # Origin Info  -----------------------------------------------------------------------------------------------------
    def get_origin_address_line_1(self):
        return self.get_text().set_locator(self._text_origin_address_line_1, self._name).highlight().by_text()

    def get_origin_address_line_2(self):
        return self.get_text().set_locator(self._text_origin_address_line_2, self._name).highlight().by_text()

    def get_origin_address_line_3(self):
        return self.get_text().set_locator(self._text_origin_address_line_3, self._name).highlight().by_text()

    def get_origin_date(self):
        return self.get_text().set_locator(self._text_origin_address_date_delivered, self._name).highlight().by_text()

    def click_origin_contact_information(self):
        self.click().set_locator(self._icon_origin_contact_information, self._name).single_click()
        return self

    def click_origin_street_view(self):
        self.click().set_locator(self._icon_origin_street_view, self._name).single_click()
        return self

    def get_origin_information(self):
        origin = {
            "address_line_1": self.get_origin_address_line_1(),
            "address_line_2": self.get_origin_address_line_1(),
            "address_line_3": self.get_origin_address_line_1(),
            "date": self.get_origin_date()
        }
        return origin

    # Destination Info  ------------------------------------------------------------------------------------------------
    def get_destination_address_line_1(self):
        return self.get_text().set_locator(self._text_destination_address_line_1, self._name).highlight().by_text()

    def get_destination_address_line_2(self):
        return self.get_text().set_locator(self._text_destination_address_line_2, self._name).highlight().by_text()

    def get_destination_address_line_3(self):
        return self.get_text().set_locator(self._text_destination_address_line_3, self._name).highlight().by_text()

    def get_destination_date(self):
        return self.get_text().set_locator(self._text_destination_address_date_delivered, self._name).highlight().by_text()

    def click_destination_contact_information(self):
        self.click().set_locator(self._icon_destination_contact_information, self._name).single_click()
        return self

    def click_destination_street_view(self):
        self.click().set_locator(self._icon_destination_street_view, self._name).single_click()
        return self

    # Buttons  ---------------------------------------------------------------------------------------------------------
    def click_complete_delivery(self):
        self.click().set_locator(self._button_complete_delivery, self._name).single_click()
        return self

    def click_request_accessorials(self):
        self.click().set_locator(self._button_request_accessorials, self._name).single_click()
        return self

    def click_update_load_info(self):
        self.click().set_locator(self._button_update_load_info, self._name).single_click()
        return self

    def click_status_update(self):
        self.click().set_locator(self._button_status_update, self._name).single_click()
        return self
