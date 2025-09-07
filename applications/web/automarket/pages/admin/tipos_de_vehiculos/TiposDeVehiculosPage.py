from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('TiposDeVehiculosPage')

class TiposDeVehiculosPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/dashboard/vehicle-types"
        # Locator definitions
        self._button_add_type_button = (By.ID, "add-type-button", "Agregar Tipo de Vehiculo [Button]")
        self._page_content = (By.ID, "vehicle-types-page", "Main Page: Tipos de Vehiculo")

        # Modal
        self._modal_div = (By.XPATH,"//div[@role='dialog']","Modal Visible")
        self._modal_name = (By.NAME,"name","Nombre [modal]")
        self._modal_order = (By.NAME, "order", "Orden [modal]")
        self._modal_description = (By.XPATH, "//textarea[@name='description']", "Description [modal]")
        self._modal_parent_category = (By.ID,"parent-category-select","Categoria Principal [Button]")
        self._modal_category = (By.XPATH,"//select","Categorias [Dropdown]")
        self._modal_cancel = (By.ID,"cancel-vehicle-type-button","Cancelar [Button]")
        self._modal_save = (By.ID, "submit-vehicle-type-button", "Añadir Tipo de Vehículo [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls.name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def click_anadir_tipo_de_vehiculo(self):
        self.click().set_locator(self._button_add_type_button).single_click()
        return self

    def is_displayed(self):
        self.pause(2)
        return self.element().set_locator(self._page_content).is_visible()

    def is_modal_displayed(self):
        return self.element().set_locator(self._modal_div).is_visible()

    def select_categorias(self, categoria):
        locator = (By.XPATH, f"//label/div/h3[text()='{categoria}']", f"Select Checkbox: {categoria}")
        self.click().set_locator(locator).single_click().pause(2)
        return self

    def select_sub_categoria(self, subcategoria):
        """
        Selecciona una o múltiples subcategorías dadas por el texto de la etiqueta (ej: 'Automóvil').

        :param subcategoria: str o list[str] – Nombre(s) de la(s) subcategoría(s) a seleccionar
        :return: self (para encadenar métodos)
        """
        if isinstance(subcategoria, str):
            subcategorias = [subcategoria]  # Convertir a lista si es un string
        elif isinstance(subcategoria, list):
            subcategorias = subcategoria
        else:
            raise TypeError("El parámetro 'subcategoria' debe ser str o list[str]")

        for sub in subcategorias:
            locator = (By.XPATH, f"//label[text()='{sub}']", f"Select Checkbox: {sub}")
            self.click().set_locator(locator).single_click()

        return self


    def click_cancelar(self):
        self.click().set_locator(self._modal_cancel).single_click()
        return self

    def click_guardar(self):
        self.click().set_locator(self._modal_save).single_click()
        return self

    def add_vehicule_type(self, nombre=None, descripcion=None, categoria=None, sub_categorias=None):
        self.send_keys().set_locator(self._modal_name).set_text(nombre)
        self.send_keys().set_locator(self._modal_description).set_text(descripcion)

        self.select_categorias(categoria)

        self.select_sub_categoria(sub_categorias)

        self.click_guardar()
        return self

