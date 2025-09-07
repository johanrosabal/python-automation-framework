from selenium.webdriver.common.by import By

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('ModelosPage')

class ModelosPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        # Driver
        self.driver = driver
        # Relative URL
        self.relative = "/dashboard/models"
        # Locator definitions
        self._button_add_model_button = (By.XPATH, "//button[@id='add-model-button']", "Agregar Modelo [Button]")
        self._page_content = (By.ID, "models-page", "Main Page: Modelos")

        # Modal
        self._modal_div = (By.XPATH,"//div[@role='dialog']","Modal Visible")
        self._modal_brand = (By.XPATH,"//button[@role='combobox' and text()='Selecciona una marca']","Marca [Button]")
        self._modal_input_brand = (By.XPATH, "//input[@role='combobox' and @placeholder='Buscar marca...']", "Marca [TextBox]")

        self._modal_category = (By.XPATH,"//button[@role='combobox' and text()='Filtrar por Categoría...']","Category [Button]")
        self._modal_input_category = (By.XPATH,"//input[@role='combobox' and @placeholder='Buscar categoría...']","Category [TextBox]")

        self._modal_vehicle_type = (By.XPATH,"//input[@id='vehicle-type-search-input']","Tipo de Vehiculo [InputBox]")
        self._modal_model = (By.XPATH,"//input[@id='model-name-input']","Modelo [InputBox]")

        self._model_start_year = (By.XPATH,"//input[@id='start-year-input']","Ano Inicio [InputBox]")
        self._model_end_year = (By.XPATH, "//input[@id='end-year-input']", "Ano Fin [InputBox]")
        self._model_end_year_check = (By.XPATH,"//button[@id='has-end-year-checkbox']","Tiene ano Finalizacion [Checkbox]")

        self._model_save = (By.XPATH,"//button[@id='submit-model-button']","Guardar Datos [Button]")
        self._model_cancel = (By.XPATH, "//button[@id='cancel-model-button']", "Cancelar Registro [Button]")


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

    def click_agregar_modelo(self):
        self.click().set_locator(self._button_add_model_button).single_click()
        return self

    def click_marca(self):
        self.click().set_locator(self._modal_brand).single_click()
        return self

    def enter_marca(self, marca):
        self.send_keys().set_locator(self._modal_input_brand).set_text(marca)
        return self

    def select_marca(self, marca):
        combobox = (By.XPATH, f"//div[contains(@data-value,\"{marca}\")]",f"Seleccionar Marca [{marca}]")
        self.click().set_locator(combobox).single_click()
        return self

    def click_categoria(self):
        self.click().set_locator(self._modal_category).single_click()
        return self

    def enter_categoria(self, categoria):
        self.send_keys().set_locator(self._modal_input_category).set_text(categoria)
        return self

    def select_categoria(self, categoria):
        combobox = (By.XPATH, f"//div[@data-value=\"{categoria}\"]",f"Seleccionar Categoria [{categoria}]")
        self.click().set_locator(combobox).single_click().pause(1)
        return self

    def enter_tipo_de_vehiculo(self, tipo_de_vehiculo):
        self.send_keys().set_locator(self._modal_vehicle_type).set_text(tipo_de_vehiculo).pause(1)
        return self

    def select_tipo_de_vehiculo(self, tipo_de_vehiculo):
        combobox = (By.XPATH, f"//label[text()='{tipo_de_vehiculo}']", f"Seleccionar Tipo de Vehiculo [{tipo_de_vehiculo}]")
        self.click().set_locator(combobox).highlight().pause(1).single_click()
        return self

    def enter_model(self, modelo):
        self.send_keys().set_locator(self._modal_model).set_text(modelo)
        return self

    def enter_inicio(self, inicio):
        self.send_keys().set_locator(self._model_start_year).clear().clear().set_text(inicio)
        return self

    def enter_finalizacion(self, finalizacion):
        self.send_keys().set_locator(self._model_end_year).set_text(finalizacion)
        return self

    def click_finalizacion(self):
        self.click().set_locator(self._model_end_year_check).single_click().pause(1)
        return self

    def click_guardar(self):
        self.click().set_locator(self._model_save).single_click()
        return self

    def click_cancelar(self):
        self.click().set_locator(self._model_cancel).single_click()
        return self

    def is_visible_agregar_modelo(self):
        self.element().set_locator(self._modal_div).is_visible()
        return self

    def is_modal_displayed(self):
        return self.element().set_locator(self._modal_div).is_visible()

    def add_model(self, marca, categoria, tipo,modelo, inicio, fin ):

        self.click_marca()
        self.enter_marca(marca)
        self.select_marca(marca)

        self.click_categoria()
        self.enter_categoria(categoria)
        self.select_categoria(categoria)

        self.enter_tipo_de_vehiculo(tipo)
        self.select_tipo_de_vehiculo(tipo)

        self.enter_model(modelo)

        self.enter_inicio(str(inicio))

        if fin != "Presente":
            self.click_finalizacion()
            self.enter_finalizacion(str(fin))

        self.click_guardar()

        return self




