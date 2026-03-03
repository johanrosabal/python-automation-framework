import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('LoadInformationUpdatePage')


class LoadInformationUpdatePage(BasePage):

    def __init__(self, driver):
        """
        Initialize the LoadInformationUpdatePage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__

        # ====================================================================
        # LOCATOR DEFINITIONS - Using label text pattern:
        # //label[contains(text(),'LABEL_TEXT')]/..//input
        # ====================================================================
        self._input_trailer_container = (
            By.XPATH,
            "//label[contains(text(),'Trailer/Container')]/..//input",
            "Trailer/Container Input"
        )

        self._input_tractor = (
            By.XPATH,
            "//label[contains(text(),'Tractor')]/..//input",
            "Tractor Input"
        )
        self._input_driver_cellphone = (
            By.XPATH,
            "//label[contains(text(),'Driver Cellphone')]/..//input",
            "Driver Cellphone Input"
        )
        self._input_chassis = (
            By.XPATH,
            "//label[contains(text(),'Chassis')]/..//input",
            "Chassis Input"
        )
        self._input_genset = (
            By.XPATH,
            "//label[contains(text(),'GenSet')]/..//input",
            "GenSet Input"
        )

        self._label_trailer_container = (
            By.XPATH,
            "//label[contains(text(),'Trailer/Container')]",
            "Trailer/Container Input"
        )
        self._label_tractor = (
            By.XPATH,
            "//label[contains(text(),'Tractor')]",
            "Tractor Input"
        )
        self._label_driver_cellphone = (
            By.XPATH,
            "//label[contains(text(),'Driver Cellphone')]",
            "Driver Cellphone Input"
        )
        self._label_chassis = (
            By.XPATH,
            "//label[contains(text(),'Chassis')]",
            "Chassis Input"
        )
        self._label_genset = (
            By.XPATH,
            "//label[contains(text(),'GenSet')]",
            "GenSet Input"
        )

        self._btn_update = (
            By.XPATH,
            "//button/span[text()='Update']",
            "Update [Button]"
        )

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    # ====================================================================
    # METHODS - Fluent interface pattern
    # ====================================================================

    @allure.step("Enter Trailer/Container: {text}")
    def enter_trailer_container(self, text: str = None):
        """
        Enters text into the Trailer/Container input field.

        Args:
            text (str): Text to enter (e.g., "TRL123456")
        """
        self.send_keys() \
            .set_locator(self._input_trailer_container, self._name) \
            .clear() \
            .set_text(text) \
            .press_tab()
        return self

    @allure.step("Enter Tractor: {text}")
    def enter_tractor(self, text: str = None):
        """
        Enters text into the Tractor input field.

        Args:
            text (str): Text to enter (e.g., "TRC789012")
        """
        self.send_keys() \
            .set_locator(self._input_tractor, self._name) \
            .clear() \
            .set_text(text)
        return self

    @allure.step("Enter Driver Cellphone: {text}")
    def enter_driver_cellphone(self, text: str = None):
        """
        Enters text into the Driver Cellphone input field.
        Note: Field has phone mask pattern: (XXX) XXX-XXXX

        Args:
            text (str): Phone number to enter (e.g., "(555) 123-4567")
        """
        self.send_keys() \
            .set_locator(self._input_driver_cellphone, self._name) \
            .clear() \
            .set_text(text)
        return self

    @allure.step("Enter Chassis: {text}")
    def enter_chassis(self, text: str = None):
        """
        Enters text into the Chassis input field.

        Args:
            text (str): Text to enter (e.g., "CHS456789")
        """
        self.send_keys() \
            .set_locator(self._input_chassis, self._name) \
            .clear() \
            .set_text(text)
        return self

    @allure.step("Clear Chassis")
    def clear_chassis(self):
        """
        Enters text into the Chassis input field.
        """
        self.send_keys() \
            .set_locator(self._input_chassis, self._name) \
            .clear_input_with_events()
        return self

    @allure.step("Enter GenSet: {text}")
    def enter_genset(self, text: str = None):
        """
        Enters text into the GenSet input field.

        Args:
            text (str): Text to enter (e.g., "GEN321654")
        """
        self.send_keys() \
            .set_locator(self._input_genset, self._name) \
            .clear() \
            .set_text(text)
        return self

    @allure.step("Clear GenSet")
    def clear_genset(self):
        """
        Enters text into the GenSet input field.
        """
        self.send_keys() \
            .set_locator(self._input_genset, self._name) \
            .clear_input_with_events()
        return self

    def click_enter(self):
        self.send_keys() \
            .set_locator(self._input_genset, self._name) \
            .press_enter()

        self.element().wait_for_save_api_response(timeout=10)
        return self

    # ====================================================================
    # ERROR MESSAGE VALIDATION
    # ====================================================================
    def get_error_message_trailer_container(self) -> str:
        """Gets the current value of the Trailer/Container field."""
        locator = (By.XPATH, "//label[contains(text(),'Trailer/Container')]/../div/p", "Error Message Validation Trailer Container")
        self.element().is_present(locator=locator, timeout=10)
        return self.get_text().set_locator(locator).by_text()

    # ====================================================================
    # GETTER METHODS - For validation
    # ====================================================================

    def get_trailer_container_value(self) -> str:
        """Gets the current value of the Trailer/Container field."""
        return self.get_text().set_locator(self._input_trailer_container).by_attribute("value")

    def get_tractor_value(self) -> str:
        """Gets the current value of the Tractor field."""
        return self.get_text().set_locator(self._input_tractor).by_attribute("value")

    def get_driver_cellphone_value(self) -> str:
        """Gets the current value of the Driver Cellphone field."""
        return self.get_text().set_locator(self._input_driver_cellphone).by_attribute("value")

    def get_chassis_value(self) -> str:
        """Gets the current value of the Chassis field."""
        return self.get_text().set_locator(self._input_chassis).by_attribute("value")

    def get_genset_value(self) -> str:
        """Gets the current value of the GenSet field."""
        return self.get_text().set_locator(self._input_genset).by_attribute("value")

    # ====================================================================
    # LABELS TEXT METHODS
    # ====================================================================
    def get_label_trailer_container(self) -> str:
        """Gets the current label of the Trailer/Container field."""
        return self.get_text().set_locator(self._label_trailer_container).by_text()

    def get_label_tractor(self) -> str:
        """Gets the current label of the Tractor field."""
        return self.get_text().set_locator(self._label_tractor).by_text()

    def get_label_driver_cellphone(self) -> str:
        """Gets the current label of the Driver Cellphone field."""
        return self.get_text().set_locator(self._label_driver_cellphone).by_text()

    def get_label_chassis(self) -> str:
        """Gets the current label of the Chassis field."""
        return self.get_text().set_locator(self._label_chassis).by_text()

    def get_label_genset(self) -> str:
        """Gets the current label of the GenSet field."""
        return self.get_text().set_locator(self._label_genset).by_text()

    # ====================================================================
    # UTILITY METHODS
    # ====================================================================

    @allure.step("Fill all load information")
    def fill_upload_load_information(
            self,
            trailer: str = None,
            tractor: str = None,
            driver_cell: str = None,
            chassis: str = None,
            genset: str = None
    ):
        """
        Fills all available fields in the load information form.

        Args:
            trailer (str, optional): Trailer/Container value
            tractor (str, optional): Tractor value
            driver_cell (str, optional): Driver cellphone value
            chassis (str, optional): Chassis value
            genset (str, optional): GenSet value
        """
        if trailer:
            self.enter_trailer_container(trailer)
        if tractor:
            self.enter_tractor(tractor)
        if driver_cell:
            self.enter_driver_cellphone(driver_cell)
        if chassis:
            self.enter_chassis(chassis)
        if genset:
            self.enter_genset(genset)
        return self

    @allure.step("Clear all load information fields")
    def clear_all_fields(self):
        """Clears all input fields in the form."""
        for locator in [
            self._input_trailer_container,
            self._input_tractor,
            self._input_driver_cellphone,
            self._input_chassis,
            self._input_genset
        ]:
            self.send_keys().set_locator(locator=locator).clear()
        return self

    @allure.step("Click Update Button")
    def click_update(self):
        self.screenshot().attach_to_allure(name="Load Information Update Modal")
        self.click().set_locator(self._btn_update, self._name).single_click()
        return self

    @allure.step("Click Update Enable/Disabled")
    def is_enable_update(self):
        self.screenshot().attach_to_allure(name="Load Information Update Modal")
        return self.element().is_enabled_js(locator=self._btn_update, timeout=5, debug=False)
