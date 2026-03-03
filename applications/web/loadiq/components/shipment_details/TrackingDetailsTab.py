from selenium.webdriver.common.by import By

from applications.web.loadiq.pages.my_loads.AllUpdatesModalPage import AllUpdatesModalPage
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('TrackingDetailsTab')


class TrackingDetailsTab(BasePage):

    def __init__(self, driver):
        """
        Initialize the TrackingDetailsTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/my_loads/list"
        # Locator definitions
        # Locator Summary Card
        self._text_current_status = (By.XPATH, "(//span[contains(text(),'Current Status')]/../../div/span)[2]", "Current Status [Summary Card: Text]")
        self._text_last_location = (By.XPATH, "(//span[contains(text(),'Last Location')]/../../div/span)[2]", "Last Location [Summary Card: Text]")
        self._text_last_update = (By.XPATH, "(//span[contains(text(),'Last Update')]/../../div/span)[2]", "Last Update [Summary Card: Text]")
        self._text_distance_remaining = (By.XPATH, "(//span[contains(text(),'Distance Remaining')]/../../div/span)[2]", "Last Update [Summary Card: Text]")
        self._text_total_updates = (By.XPATH, "(//span[contains(text(),'Total Updates')]/../../div/span)[2]", "Last Update [Summary Card: Text]")
        self._link_total_updates_view_all = (By.XPATH, "(//span[contains(text(),'Total Updates')]/../../div/span)[3]/a", "Last Update View All [Summary Card: Link]")

        # Modal
        self.modal_all_updates = AllUpdatesModalPage.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = TrackingDetailsTab(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self, tracking_number: str):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        # Click on Tracking Number
        xpath = f"//div[contains(@class,'listingSide')]//span[contains(@class,'text-primary') and contains(text(),'{tracking_number}')]"
        locator = (By.XPATH, xpath, f"Click on Tracking Number: {tracking_number}")
        self.click().set_locator(locator, self._name).single_click()
        return self

    # Summary Card -----------------------------------------------------------------------------------------------------
    def get_current_status(self):
        return self.get_text().set_locator(self._text_current_status, self._name).by_text()

    def get_last_location(self):
        return self.get_text().set_locator(self._text_last_location, self._name).by_text()

    def get_last_update(self):
        return self.get_text().set_locator(self._text_last_update, self._name).by_text()

    def get_distance_remaining(self):
        return self.get_text().set_locator(self._text_distance_remaining, self._name).by_text()

    def get_total_updates(self):
        return self.get_text().set_locator(self._text_total_updates, self._name).by_text()

    def click_total_updates_view_all(self):
        self.click().set_locator(self._link_total_updates_view_all, self._name).single_click()
        return self

    # Milestone Card ---------------------------------------------------------------------------------------------------
    def get_milestones_stop_1_label(self):
        locator = (By.XPATH, "(//span[contains(text(),'Stop 1')]/../../div)[1]/span", "Stop 1: Label [Milestone Card: Text]")
        self.scroll().set_locator(locator).to_element()
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_milestones_stop_2_label(self):
        locator = (By.XPATH, "(//span[contains(text(),'Stop 2')]/../../div)[1]/span", "Stop 2: Label [Milestone Card: Text]")
        self.scroll().set_locator(locator).to_element()
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_milestones_stop_1_arrived(self):
        locator = (By.XPATH, "(//span[contains(text(),'Stop 1')]/../../div)[3]", "Stop 1: Arrived [Milestone Card: Text]")
        self.scroll().set_locator(locator).to_element()
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_milestones_stop_1_departed(self):
        locator = (By.XPATH, "(//span[contains(text(),'Stop 1')]/../../div)[5]", "Stop 1: Departed [Milestone Card: Text]")
        self.scroll().set_locator(locator).to_element()
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_milestone_stop_2_arrived(self):
        locator = (By.XPATH, "(//span[contains(text(),'Stop 2')]/../../div)[3]", "Stop 2: Arrived [Milestone Card: Text]")
        self.scroll().set_locator(locator).to_element()
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_milestones_stop_2_departed(self):
        locator = (By.XPATH, "(//span[contains(text(),'Stop 2')]/../../div)[5]", "Stop 2: Departed [Milestone Card: Text]")
        self.scroll().set_locator(locator).to_element(pixels=-200)
        return self.get_text().set_locator(locator, self._name).by_text()
