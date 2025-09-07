import csv
import pytest
from pathlib import Path
from applications.web.automarket.config.decorators import automarket
from applications.web.automarket.pages.login.LoginPage import LoginPage
from applications.web.automarket.pages.admin.dashboard.DashboardPage import DashboardPage
from applications.web.automarket.pages.admin.tipos_de_vehiculos.TiposDeVehiculosPage import TiposDeVehiculosPage
from applications.web.automarket.pages.admin.modelos.ModelosPage import ModelosPage
from applications.web.automarket.data.source_mapping import TiposDeVehiculos,ModelosDeVehiculos
from core.config.logger_config import setup_logger
from core.data.sources.EXCEL_reader import EXCELReader
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test

logger = setup_logger('TestLogin')


@pytest.mark.web
@automarket
class TestLogin(BaseTest):
    LoginPage = LoginPage.get_instance()
    DashboardPage = DashboardPage.get_instance()
    TiposDeVehiculosPage = TiposDeVehiculosPage.get_instance()
    ModelosPage = ModelosPage.get_instance()

    @test(test_case_id="AUTO-001", test_description="Login Page Automarket", skip=False)
    def test_login(self):
        # 01. Interact with page elements
        self.LoginPage.load_page()
        # 02. Validations
        self.LoginPage.login("johan.manuel.rosabal@gmail.com","Snap1234!")
        assert  self.DashboardPage.is_displayed(), "Dashboard pagina no cargo"

    @test(test_case_id="AUTO-002", test_description="Entrar pagina Tipo de Vehiculo",skip=True)
    def test_tipos_de_vehiculo(self):
        # 01. Cargar la Pagina de Tipos de Vehiculo
        self.TiposDeVehiculosPage.load_page()
        assert self.TiposDeVehiculosPage.is_displayed(), "Tipos de Vehiculo pagina no cargo"

    @test(test_case_id="AUTO-003", test_description="Agregar un tipo de vehiculo", skip=True)
    def test_agregar_un_tipo_de_vehiculo(self):
        # Importar Datos
        path = "../../data/tipos_vehiculos_2.csv"
        # 02. Specifying the Sheet Name to map UserInformation values
        tipos_vehiculos = EXCELReader().set_file_path(path).read_file(
            object_class=TiposDeVehiculos
        )

        # 03. Verifica que se leyeron datos
        assert len(tipos_vehiculos) > 0, "No se cargaron datos del CSV"

        logger.info(tipos_vehiculos)

        # 04. Procesa cada registro
        for tipo in tipos_vehiculos:
            self.TiposDeVehiculosPage.click_anadir_tipo_de_vehiculo()
            assert self.TiposDeVehiculosPage.is_modal_displayed(), "Modal no es visible"

            self.TiposDeVehiculosPage.add_vehicule_type(
                nombre=tipo.VehicleLevel3,
                descripcion=tipo.VehicleLevel3,
                categoria=tipo.VehicleLevel1,
                sub_categorias=tipo.VehicleLevel2
            )

    @test(test_case_id="AUTO-004", test_description="Agregar Modelos", skip=False)
    def test_agregar_modelos_de_vehiculo(self):

        # Importar Datos
        path = "../../data/modelos_vehiculos_2.csv"
        # 02. Specifying the Sheet Name to map UserInformation values
        modelos_vehiculos = EXCELReader().set_file_path(path).read_file(
            object_class=ModelosDeVehiculos
        )

        # Cargar Pagina de Modelos
        self.ModelosPage.load_page()

        # 04. Procesa cada registro
        for modelo in modelos_vehiculos:

            self.ModelosPage.click_agregar_modelo()
            self.ModelosPage.is_visible_agregar_modelo()

            line = "[RECORD] " + str(modelo.marca) + " - " + str(modelo.categoria)  + " - "+ str(modelo.tipo)  + " - "+ str(modelo.modelo)  + " - "+ str(modelo.inicio)  + " - "+ str(modelo.fin)
            logger.info(line)

            self.ModelosPage.add_model(
                marca=modelo.marca,
                categoria=modelo.categoria,
                tipo=modelo.tipo,
                modelo=modelo.modelo,
                inicio=modelo.inicio,
                fin=modelo.fin
            )






