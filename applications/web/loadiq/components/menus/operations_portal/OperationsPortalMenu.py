import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('OperationsPortalMenu')


class OperationsPortalMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the OperationsPortalMenu instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/list"
        # Locator definitions
        self._title = (By.XPATH, "//nav[contains(@aria-label, 'breadcrumb')]//a[contains(@class,'last-breadcrumb')]", "Page Title")
        self.__nav_my_loads = (By.XPATH, "//a/span[@class='nav-text' and text()='My Loads']",  "My Loads [Menu Option]")
        self.__nav_my_board = (By.XPATH, "//a/span[@class='nav-text' and text()='My Board']", "My Board [Menu Option]")
        self.__nav_shipment_creation = (By.XPATH, "//a/span[@class='nav-text' and text()='Shipment Creation']", "Shipment Creation [Menu Option]")
        self.__nav_ltl_quote = (By.XPATH, "//a/span[@class='nav-text' and text()='LTL Quote']", "LTL Quote [Menu Option]")
        self.__nav_user_profile_menu = (By.XPATH, "//a[@id='navbarDropdown']", "User Profile Menu [Menu Option]")
        self.__nav_user_profile_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'User Profile')]","User Profile [Dropdown Option]")
        self.__nav_logout_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'Log Out')]", "Log Out [Dropdown Option]")
        self.__lbl_sign_in = (By.XPATH, "//h2", "Page Title")
        self.__nav_shipment_tracking = (By.XPATH, "//a/span[@class='nav-text' and text()='Shipment Tracking']", "Shipment Tracking [Menu Option]")

    def _load_page(self, locator, pause):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)
        return self

    @allure.step("Open My Loads")
    def menu_my_loads(self, pause: int = 2):
        self.element().set_locator(self.__nav_my_loads, self._name)
        self.element().is_present(self.__nav_my_loads)
        self.click().set_locator(self.__nav_my_loads, self._name).single_click().pause(pause)

        self.element().set_locator(self._title, self._name)
        self.element().is_present(self._title)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("My Loads").by_text()
        assert title == "My Loads", f"Page Incorrect, current title {title}"
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

    @allure.step("Open LTL Quote")
    def menu_ltl_quote(self, pause: int = 0):
        self.click().set_locator(self.__nav_ltl_quote, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("LTL Quote").by_text()
        assert title == "LTL Quote", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Open User Profile")
    def menu_user_profile(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(pause)
        self.click().set_locator(self.__nav_user_profile_link, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self._title, self._name).by_text()
        assert title == "User Profile", "Page Incorrect"
        return self

    @allure.step("Log Out")
    def menu_log_out(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(pause)
        self.click().set_locator(self.__nav_logout_link, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self.__lbl_sign_in, self._name).by_text()
        assert title == "Sign In", "Page Incorrect"
        return self

    @allure.step("Shipment Tracking")
    def menu_shipment_tracking(self, pause: int = 0):
        self._load_page(self.__nav_shipment_tracking, pause)
        current_url = self.navigation().get_current_url()
        assert "/shipment/list" in current_url, "Page Incorrect"
        return self


