from selenium.webdriver.common.by import By

from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.data import UserDTO

logger = setup_logger('AdminMenuPage')

class AdminMenuPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/login"
        # Locator definitions
        self._menu_panel_control = (By.ID, "nav-link-panel-de control", "Menu Panel de Control")
        self._menu_gestionar = (By.ID, "nav-link-gestionar-usuarios", "Menu Gestionar Usuarios")
        self._menu_geografia = (By.ID, "geography-menu", "Menu Geografia")
        self._menu_config_vehicle = (By.ID, "vehicle-config-menu", "Menu Configuracion Vehiculos")
        self._menu_config_anuncios = (By.ID, "listing-config-menu", "Menu Config. Anuncios")
        self._menu_finanzas = (By.ID, "finance-menu", "Menu Finanzas")
        self._option_tipos_de_vehiculos = (By.ID,"nav-link-tipos-de-vehículo","Option Tipos de Vehiculos")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls.name = __class__.__name__
        return cls._instance

    def click_menu_panel_de_control(self):
        self.click().set_locator(self._menu_panel_control).single_click()
        return self

    def click_menu_gestionar_usarios(self):
        self.click().set_locator(self._menu_gestionar).single_click()
        return self

    def click_menu_geografia(self):
        self.click().set_locator(self._menu_geografia).single_click()
        return self

    def click_menu_config_vehicules(self):
        self.click().set_locator(self._menu_config_vehicle).single_click()
        return self

    def click_menu_config_tipos_de_vehiculos(self):
        self.click().set_locator(self._option_tipos_de_vehiculos).single_click()
        return self

    def click_menu_config_anuncios(self):
        self.click().set_locator(self._menu_config_anuncios).single_click()
        return self

    def click_menu_config_finanzas(self):
        self.click().set_locator(self._menu_finanzas).single_click()
        return self