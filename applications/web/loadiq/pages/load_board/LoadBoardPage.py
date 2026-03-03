import allure
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('LoadBoard')


class LoadBoard(BasePage):

    def __init__(self, driver):
        """
        Initialize the MyLoadsPage instance.
        """
        super().__init__(driver)
        # Driver

        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/load-board"

        # Locator definitions
        self._noload = (By.XPATH, "//app-load-list//h5[contains(text(), 'Sorry')]", "Message [Output]")
        self._input_search_by = (By.XPATH, "//app-load-list//input", "Search by [Input]")
        self._button_search = (By.XPATH, "//app-load-list//button[1]"," Search click [Button]")
        self._txt_expedite_load_value = (By.XPATH, "//*[@id='loadItem21']/td[12]/div/span/input")

        self._checkbox_filter = (By.XPATH, "//app-load-list//button[2]", "Include Closed [Checkbox]")
        self._button_sort_by_ship_date = (By.XPATH, "//div/span[text()='Ship date']", "Sort by ship date  [Button]")
        self._button_sort_by_status = (By.XPATH, "//div/span[text()='Status']", "Sort by status  [Button]")
        self._button_sort_by_origin = (By.XPATH, "//div/span[text()='Origin']", "Sort by origin [Button]")
        self._text_total_records = (By.XPATH, "//span[contains(@class, 'search-result')]", "Total Records [Text]")
        self._list_container = "//div[contains(@class, 'listingSide')]//div[@class='row']/div"
        self._get_ship_date = "////span[normalize-space(.)='Ship date']/following-sibling::span//*[name() = 'svg']"
        self._no_load = (By.XPATH, "//h5[contains(text(), 'Sorry, we couldn't find any results.')]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = LoadBoard(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    # @allure.step("Enter Search By: {search_by}")
    def enter_search_by(self, search_by: str):
        self.send_keys().set_locator(self._input_search_by, self._name).clear().set_text(search_by)

        return self

    @allure.step("Click Search")
    def click_search(self):
        self.click().set_locator(self._button_search, self._name).single_click().pause(2)
        return self

    # Methods for load columns view

    @allure.step("Get Load Value Accessorials details")
    def get_load_expedite_text_value(self):
        return self.get_text().set_locator(self._txt_expedite_load_value, self._name).by_text()

    def is_expedite_true(self):
        try:
            self.driver.find_element(By.XPATH, "//span[@ng-reflect-message='true']")
            return True
        except NoSuchElementException:
            return False

    @allure.step("Click Bid button in details")
    def click_bid_details_button(self):
        self.click().set_locator(self._btn_bid_details, self._name).single_click()
        return self

    @allure.step("Click Book Now button in details")
    def click_book_now_details_button(self):
        self.click().set_locator(self._btn_book_now_details, self._name).single_click()
        return self

    @allure.step("Click Accept Tender button in details")
    def click_accept_tender_details_button(self):
        self.click().set_locator(self._btn_accept_tender_details, self._name).single_click()
        return self

    @allure.step("Click Reject Tender button in details")
    def click_reject_tender_details_button(self):
        self.click().set_locator(self._btn_reject_tender_details, self._name).single_click()
        return self

    # Methods for bid modal interactions
    @allure.step("Get Bid Modal Title")
    def get_bid_modal_title_text(self):
        return self.get_text().set_locator(self._txt_bid_modal_title, self._name).by_text()

    @allure.step("Get Bid Modal Shipment Number")
    def get_bid_modal_shipment_no_text(self):
        return self.get_text().set_locator(self._txt_bid_modal_shipment_no, self._name).by_text()

    @allure.step("Enter Bid Amount: {amount}")
    def enter_bid_amount(self, amount: str):
        self.send_keys().set_locator(self._txt_bid_modal_input_amount, self._name).clear().set_text(amount)
