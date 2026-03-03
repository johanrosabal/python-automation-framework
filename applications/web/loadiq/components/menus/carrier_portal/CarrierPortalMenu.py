import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('CarrierPortalMenu')


class CarrierPortalMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the CarrierPortalMenu instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/my_loads/load-board"
        # Locator definitions
        self._title = (By.XPATH, "//nav[contains(@aria-label, 'breadcrumb')]//a[contains(@class,'last-breadcrumb')]", "Page Title")
        self.__nav_load_board = (By.XPATH, "//a/span[@class='nav-text' and text()='Load Board']",  "Load Board [Menu Option]")
        self.__nav_my_offers = (By.XPATH, "//a/span[@class='nav-text' and text()='My Offers']", "My Offers [Menu Option]")
        self.__nav_my_loads = (By.XPATH, "//a/span[@class='nav-text' and text()='My Loads']", "My Loads [Menu Option]")
        self.__nav_my_payments = (By.XPATH, "//a/span[@class='nav-text' and text()='My Payments']", "My Payments [Menu Option]")
        self.__nav_user_profile_menu = (By.XPATH, "//a[@id='navbarDropdown']", "User Profile Menu [Menu Option]")
        self.__nav_user_profile_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'User Profile')]","User Profile [Dropdown Option]")
        self.__nav_logout_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'Log Out')]", "Log Out [Dropdown Option]")
        self.__lbl_sign_in = (By.XPATH, "//h2", "Page Title")

    def _load_page(self, locator, pause):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Open Load Board")
    def menu_load_board(self, pause: int = 0):
        self.click().set_locator(self.__nav_load_board, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("Load Board").by_text()
        assert title == "Load Board", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Open My Offers")
    def menu_my_offers(self, pause: int = 0):
        self.element().set_locator(self.__nav_my_offers, self._name)
        self.element().is_present(self.__nav_my_offers)
        self.click().set_locator(self.__nav_my_offers, self._name).single_click().pause(pause)

        self.element().set_locator(self._title, self._name)
        self.element().is_present(self._title)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("My Offers").by_text()
        assert title == "My Offers", f"Page Incorrect, current title {title}"
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

    @allure.step("Open My Payments")
    def menu_my_payments(self, pause: int = 0):
        self.click().set_locator(self.__nav_my_payments, self._name).single_click().pause(2)
        title = self.get_text().set_locator(self._title, self._name).wait_for_text("My Payments").by_text()
        assert title == "My Payments", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Open User Profile")
    def menu_user_profile(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(pause)
        self.click().set_locator(self.__nav_user_profile_link, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self._title, self._name).by_text()
        assert title == "User Profile", f"Page Incorrect, current title {title}"
        return self

    @allure.step("Log Out")
    def menu_log_out(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(pause)
        self.click().set_locator(self.__nav_logout_link, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self.__lbl_sign_in, self._name).by_text()
        assert title == "Sign In", f"Page Incorrect, current title {title}"
        return self
