import allure
from selenium.webdriver.common.by import By
from applications.web.softship.common.SoftshipPage import SoftshipPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from selenium.common.exceptions import NoSuchElementException

logger = setup_logger('BookingsHomePage')


class BookingsHomePage(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/booking-home"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_booking_query = (By.XPATH, "//a[text()='Booking Query']", "Link Booking Query")
        self.__link_container_query = (By.XPATH, "//a[text()='Container Query']", "Link Container Query")
        self.__link_roro_query = (By.XPATH, "//a[text()='RoRo Query']", "Link RoRo Query")
        self.__link_rebooking = (By.XPATH, "//a[text()='Rebooking']", "Link Rebooking")

        self.__btn_create = (By.XPATH, "//a[text()='Create']", "Create Button")
        self.__btn_find = (By.XPATH, "//button[text()='Find']", "Find Button")
        self.__input_searching_for = (By.XPATH, "//input[@placeholder='What are you searching for?']",
                                      "Searching For Input Box")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["booking"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    @allure.step("Link Booking Query")
    def link_booking_query(self, pause: int = 0):
        self.click().set_locator(self.__link_booking_query, self._name).single_click().pause()
        return self

    @allure.step("Link Container Query")
    def link_container_query(self, pause: int = 0):
        self.click().set_locator(self.__link_container_query, self._name).single_click().pause()
        return self

    @allure.step("Link RoRo Query")
    def link_roro_query(self, pause: int = 0):
        self.click().set_locator(self.__link_roro_query, self._name).single_click().pause()
        return self

    @allure.step("Link Rebooking")
    def link_rebooking(self, pause: int = 0):
        self.click().set_locator(self.__link_rebooking, self._name).single_click().pause()
        return self

    @allure.step("Click Create Button")
    def click_create(self, pause: int = 5):
        self.click().set_locator(self.__btn_create, self._name).single_click().pause(pause)
        return self

    @allure.step("Enter searching for")
    def enter_searching_for(self, search: str, pause: int = 0):
        self.send_keys().set_locator(self.__input_searching_for, self._name).set_text(search)
        self.click().set_locator(self.__btn_find, self._name).single_click().pause(pause)
        return self

    @allure.step("Link My Queries")
    def menu_my_queries(self, query_text: str, pause: int = 0):
        locator = (By.XPATH, f"//a[text()='{query_text}']", "Link My Queries:{query_text}")
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Validate presence of all locators on the page")
    def validate_locators(self):
        """
        Validate that all specified locators are present on the page.
        """

        with allure.step("Validating Link booking query"):
            self.highlight_element().set_locator(self.__link_booking_query, self._name)
        with allure.step("Validating Link container query"):
            self.highlight_element().set_locator(self.__link_container_query, self._name)
        with allure.step("Validating Link roro query"):
            self.highlight_element().set_locator(self.__link_roro_query, self._name)
        with allure.step("Validating Link rebooking"):
            self.highlight_element().set_locator(self.__link_rebooking, self._name)
        with allure.step("Validating the create button"):
            self.highlight_element().set_locator(self.__btn_create, self._name)
        with allure.step("Validating the searching input presence"):
            self.highlight_element().set_locator(self.__input_searching_for, self._name)
            self.send_keys().set_locator(self.__input_searching_for, self._name).set_text("test")
        with allure.step("Validating Link the find button"):
            self.highlight_element().set_locator(self.__btn_find, self._name)
        with allure.step("Validating the searching input presence"):
            self.highlight_element().set_locator(self.__input_searching_for, self._name)

