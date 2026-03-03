import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SupportPortalMenu')

class SupportPortalMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the SupportPortalMenu.
        """
        super().__init__(driver)
        #Driver
        self._Driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/add-user"
        #Locator definitions
        self._title = (By.XPATH, "//header//nav//span[@class='white-text header-page-title']", "Page Title")
        self.__nav_mirror = (By.XPATH, "//a/span[@class='nav-text' and text()='Mirror']", "Mirror [Menu Option]")
        self.__nav_create_user = (By.XPATH, "//a/span[@class='nav-text' and text()='Create User']", "Create User [Menu Option]")
        self.__nav_reports = (By.XPATH, "//a/span[@class='nav-text' and text()='Reports']", "Reports [Menu Option]")
        self.__nav_user_management = (By.XPATH, "//a/span[@class='nav-text' and text()='User Management']", "User Management [Menu Option]")
        self.__nav_user_profile_menu = (By.XPATH, "//a[@id='navbarDropdown']", "User Profile Menu [Menu Option]")
        self.__nav_announcements_menu = (By.XPATH, "//a/span[@class='nav-text' and text()='Announcements']", "Announcements [Menu Option]")
        self.__nav_user_profile_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'User Profile')]","User Profile [Dropdown Option]")
        self.__nav_logout_link = (By.XPATH, "//div[@aria-labelledby='navbarDropdown']/a[contains(text(),'Log Out')]", "Log Out [Dropdown Option]")
        self.__lbl_sign_in = (By.XPATH, "//h2", "Page Title")
        self.__lbl_title_announcements = (By.XPATH, "//nav[contains(@aria-label,'breadcrumb')]//a[contains(text(),'Announcements')]", "Page Title Announcements")

    def _load_page(self, locator, pause):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)
        return self

    @allure.step("Open Mirror")
    def menu_mirror(self, pause: int = 0):
        self.click().set_locator(self.__nav_mirror, self._name).single_click().pause(pause)
        current_url = self.navigation().get_current_url()
        assert "/add-user" in current_url, "Page Incorrect"
        return self

    @allure.step("Open Create User")
    def menu_create_user(self, pause: int = 0):
        self.click().set_locator(self.__nav_create_user, self._name).single_click().pause(pause)
        current_url = self.navigation().get_current_url()
        assert "/add-user" in current_url, "Page Incorrect"
        return self

    @allure.step("Open Reports")
    def menu_reports(self, pause: int = 0):
        self.click().set_locator(self.__nav_reports, self._name).single_click().pause(pause)
        current_url = self.navigation().get_current_url()
        assert "/activity-report" in current_url, "Page Incorrect"
        return self

    @allure.step("Open User Management")
    def menu_user_management(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_management, self._name).single_click().pause(5)
        current_url = self.navigation().get_current_url()
        assert "/user-manage" in current_url, "Page Incorrect"
        return self

    @allure.step("Open User Profile")
    def menu_user_profile(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(pause)
        self.click().set_locator(self.__nav_user_profile_link, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self._title, self._name).by_text()
        assert title == "User Profile", "Page Incorrect"
        return self

    @allure.step("Open Announcements")
    def menu_announcements(self, pause: int = 0):
        self.click().set_locator(self.__nav_announcements_menu, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self.__lbl_title_announcements, self._name).by_text()
        assert title == "Announcements", "Page Incorrect"
        return self

    @allure.step("Log Out")
    def menu_log_out(self, pause: int = 0):
        self.click().set_locator(self.__nav_user_profile_menu, self._name).single_click().pause(pause)
        self.click().set_locator(self.__nav_logout_link, self._name).single_click().pause(pause)
        title = self.get_text().set_locator(self.__lbl_sign_in, self._name).by_text()
        assert title == "Sign In", "Page Incorrect"
        return self
