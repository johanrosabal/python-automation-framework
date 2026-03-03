import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('SecurityMenu')


class SecurityMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Home Menu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=1"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__nav_menu = (By.XPATH, "//a[text()='Menu']", "Menu Link")
        self.__nav_menu_groups = (By.XPATH, "//a[text()='Menu Groups']", "Menu Groups Link")
        self.__nav_users = (By.XPATH, "//a[text()='Users']", "Users Link")
        self.__nav_users_group = (By.XPATH, "//a[text()='User Groups']", "User Groups Link")
        self.__nav_application = (By.XPATH, "//a[text()='Applications']", "Applications Link")

    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["configuration"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Menu Menu")
    def link_menu(self, pause: int = 0):
        self._load_page(self.__nav_menu, pause)
        return self

    @allure.step("Menu Menu Groups")
    def link_menu_groups(self, pause: int = 0):
        self._load_page(self.__nav_menu_groups, pause)
        return self

    @allure.step("Menu Users")
    def link_users(self, pause: int = 0):
        self._load_page(self.__nav_users, pause)
        return self

    @allure.step("Menu Users Groups")
    def link_users_groups(self, pause: int = 0):
        self._load_page(self.__nav_users_group, pause)
        return self

    @allure.step("Menu Application")
    def link_application(self, pause: int = 0):
        self._load_page(self.__nav_application, pause)
        return self
