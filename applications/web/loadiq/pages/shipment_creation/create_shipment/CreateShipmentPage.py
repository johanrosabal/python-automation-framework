from selenium.webdriver.common.by import By

from applications.web.loadiq.pages.shipment_creation.create_shipment.BidParametersPage import BidParametersPage
from applications.web.loadiq.pages.shipment_creation.create_shipment.DestinationInformationPage import \
    DestinationInformationPage
from applications.web.loadiq.pages.shipment_creation.create_shipment.FreightDetailsPage import FreightDetailsPage
from applications.web.loadiq.pages.shipment_creation.create_shipment.OriginInformationPage import OriginInformationPage
from applications.web.loadiq.pages.shipment_creation.create_shipment.ShipmentDetailsPage import ShipmentDetailsPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CreateShipmentPage')


class CreateShipmentPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the CreateShipmentPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/create"

        # Locators----------------------------------------------------------------------------------------
        self._nav_origin_information = (By.XPATH, "(//div[@class='submit-order-tab']//li)[1]", "Origin Information [Button]")
        self._nav_destination_information = (By.XPATH, "(//div[@class='submit-order-tab']//li)[2]", "Origin Information [Button]")
        self._nav_shipment_details = (By.XPATH, "(//div[@class='submit-order-tab']//li)[3]", "Origin Information [Button]")
        self._nav_freight_items = (By.XPATH, "(//div[@class='submit-order-tab']//li)[4]", "Origin Information [Button]")
        self._nav_bid_parameters = (By.XPATH, "(//div[@class='submit-order-tab']//li)[5]", "Origin Information [Button]")
        self._text_shipment_number = (By.XPATH, "//h4[contains(text(),'Shipment Number')]/span", "Shipment Number [Text]")

        self.tab_origin_information = OriginInformationPage.get_instance()
        self.tab_destination_information = DestinationInformationPage.get_instance()
        self.tab_shipment_details = ShipmentDetailsPage.get_instance()
        self.tab_freight_items = FreightDetailsPage.get_instance()
        self.tab_bid_parameters = BidParametersPage.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = CreateShipmentPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def get_shipment_tracker_number(self):
        return self.get_text().set_locator(self._text_shipment_number, self._name).pause(2).by_text().strip()

    def click_origin_information(self):
        self.scroll().to_top()
        self.click().set_locator(self._nav_origin_information, self._name).single_click()
        return self

    def click_destination_information(self):
        self.scroll().to_top()
        self.click().set_locator(self._nav_destination_information, self._name).single_click()
        return self

    def click_shipment_details(self):
        self.scroll().to_top()
        self.click().set_locator(self._nav_shipment_details, self._name).single_click()
        return self

    def click_freight_items(self):
        self.scroll().to_top()
        self.click().set_locator(self._nav_freight_items, self._name).single_click()
        return

    def click_bid_parameters(self):
        self.scroll().to_top()
        self.click().set_locator(self._nav_bid_parameters, self._name).single_click()
        return self
