import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CustomerPortalMenu')


class CustomerPortalMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Customer Portal Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/my_loads/my-board"
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        self._title = (By.XPATH, "//nav[contains(@aria-label, 'breadcrumb')]//a[contains(@class,'last-breadcrumb')]", "Page Title")
        self.__nav_my_board = (By.XPATH, "//a/span[@class='nav-text' and text()='My Board']",  "My Board [Menu Option]")
        self.__nav_shipment_creation = (By.XPATH, "//a/span[@class='nav-text' and text()='Shipment Creation']", "Shipment Creation [Menu Option]")
        self.__nav_shipment_tracking = (By.XPATH, "//a/span[@class='nav-text' and text()='Shipment Tracking']", "Shipment Tracking [Menu Option]")
        self.__nav_user_profile_menu = (By.XPATH, "//a[@id='navbarDropdown']", "User Profile Menu [Menu Option]")
        self.__nav_user_profile_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'User Profile')]","User Profile [Dropdown Option]")
        self.__nav_logout_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'Log Out')]", "Log Out [Dropdown Option]")
        self.__lbl_sign_in = (By.XPATH, "//h2[normalize-space(text())='Sign In']", "Page Title")

    def _load_page(self, locator, pause):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(2)
        return self

    @allure.step("Open My Board")
    def menu_my_board(self, pause: int = 0):
        self.click().set_locator(self.__nav_my_board, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("My Board").by_text()
        assert title == "My Board", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Open Shipment Creation")
    def menu_shipment_creation(self, pause: int = 0):
        self.click().set_locator(self.__nav_shipment_creation, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("Shipment Creation").by_text()
        assert title == "Shipment Creation", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Open Shipment Tracking")
    def menu_shipment_tracking(self, pause: int = 0):
        self.click().set_locator(self.__nav_shipment_tracking, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("Shipment Tracking").by_text()
        assert title == "Shipment Tracking", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Open User Profile")
    def menu_user_profile(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(2)
        self.click().set_locator(self.__nav_user_profile_link, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self._title, self._name).by_text()
        assert title == "User Profile", "Page Incorrect"
        return self

    @allure.step("Log Out")
    def menu_log_out(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(2)
        self.click().set_locator(self.__nav_logout_link, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self.__lbl_sign_in, self._name).by_text()
        assert title == "Sign In", "Page Incorrect"
        return self