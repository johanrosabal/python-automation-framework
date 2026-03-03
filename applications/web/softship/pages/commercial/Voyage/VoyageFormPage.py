import allure
from selenium.webdriver.common.by import By

from applications.web.softship.common.SoftshipPage import SoftshipPage
from applications.web.softship.components.buttons.Buttons import Buttons
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('VoyageFormPage')


def _xpath_port_call_container(index):
    return f"(//div[contains(@id,'portcall_')])[{index}]"


class VoyageFormPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the VoyageFormPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/voyage/0/header?taskHandlerId=VoyageAdvanced"
        # Locator definitions
        self._buttons = Buttons(self._driver)
        self._link_add_port_call = (By.XPATH, "//a[@title='Add Port Call']", "Add Port Call [Link action]")
        self._link_connect_child_port_call = (By.XPATH, "//a[@title='Connect child port call']", "Connect child port call [Link action]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["commercial"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    def click_save(self, pause: int = 1):
        self._buttons.click_save(pause)
        return self

    def click_save_and_close(self, pause: int = 2):
        self._buttons.click_save_and_close(pause)
        return self

    def click_close(self, pause: int = 1):
        self._buttons.click_close(pause)
        return self

    def click_calculate_cut_off(self, pause: int = 1):
        self._buttons.click_calculate_cut_off(pause)
        return self

    @allure.step("Select Service: {service}")
    def select_service(self, service: str):
        self.dropdown_autocomplete().set_locator_by_label_span("Service").by_text(text=service, column=2)
        return self

    @allure.step("Select Vessel: {vessel}")
    def select_vessel(self, vessel: str):
        self.dropdown_autocomplete().set_locator_by_label_span("Vessel").by_text(text=vessel, column=2)
        return self

    @allure.step("Select Vessel Owner: {vessel_owner}")
    def select_vessel_owner(self, vessel_owner: str):
        self.dropdown_autocomplete().set_locator_by_label_span("Vessel Owner").by_text(text=vessel_owner, column=2)
        return self

    @allure.step("Select Voyage Owner: {number}")
    def enter_voyage_number(self, number):
        locator = (By.XPATH, "//label/span[text()='Voyage Number']/../../following-sibling::div//input", "Voyage Number [Input Box]")
        self.send_keys().set_locator(locator, self._name).set_text(number)
        return self

    @allure.step("Select Voyage Number: {number}")
    def enter_second_voyage_number(self, number):
        locator = (By.XPATH, "//label/span[text()='Second Voyage Number']/../../following-sibling::div//input", "Voyage Number [Input Box]")
        self.send_keys().set_locator(locator, self._name).set_text(number)
        return self

    @allure.step("Select Customs Declaration Number: {number}")
    def enter_customs_declaration_number(self, number):
        locator = (By.XPATH, "//label/span[text()='Customs Declaration Number']/../../following-sibling::div//input", "Voyage Number [Input Box]")
        self.send_keys().set_locator(locator, self._name).set_text(number)
        return self

    @allure.step("Select Financial voyage period: {date}")
    def enter_financial_voyage_period(self, date):
        locator = (By.XPATH, "//label/span[text()='Financial voyage period']/../../following-sibling::div//input", "Voyage Number [Input Box]")
        self.send_keys().set_locator(locator, self._name).set_text(date)
        return self

    @allure.step("Select Operator: {operator}")
    def select_operator(self, operator: str):
        self.dropdown_autocomplete().set_locator_by_label_span_2("Operator").by_text(text=operator, column=1)
        return self

    @allure.step("Select Transport Mode: {transport_mode}")
    def select_transport_mode(self, transport_mode: str):
        self.dropdown_autocomplete().set_locator_by_label_span_2("Transport mode").by_text(text=transport_mode, column=2)
        return self

    @allure.step("Select Commercial Service: {commercial_service}")
    def select_commercial_service(self, commercial_service: str):
        self.dropdown_autocomplete().set_locator_by_label_span_2("Commercial service").by_text(text=commercial_service, column=2)
        return self

    @allure.step("Enter Offhire Days: {number}")
    def enter_offhire_days(self, number:int):
        locator = (By.XPATH, "//label/span[text()='Offhire Days']/../../following-sibling::div//input", "Offhire Days [Input Box]")
        self.send_keys().set_locator(locator, self._name).clear().set_text(str(number))
        return self

    @allure.step("Click Publish Voyage")
    def click_publish_voyage(self):
        locator = (By.XPATH, "//label/span[text()='Publish Voyage']/../../following-sibling::div//div[contains(@class,'checkbox-box')]", "Publish Voyage [Input Box]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    @allure.step("Enter Remarks: {text}")
    def enter_remarks(self, text):
        locator = (By.XPATH, "//label/span[text()='Remarks']/../../following-sibling::div//textarea", "Remarks [Input Box]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    @allure.step("Enter Carrier's agent ECS: {agent}")
    def select_carriers_agent_ecs(self, agent):
        self.dropdown_autocomplete().set_locator_by_label_span("Carrier's agent ECS").by_text(text=agent, column=2)
        return self

    def click_toggle_details(self, show=True, pause=0):
        locator = (By.XPATH, "//a[@data-toggle='collapse']", " Show/Hide Details")

        title_attribute = self.element().set_locator(locator, self._name).get_attribute("title")

        # Define the states based on the class attribute values
        is_hidden = "Show" in title_attribute
        is_visible = "Hide" in title_attribute

        # If we want the search option to be shown
        if show and is_hidden:
            self.click().set_locator(locator, self._name).single_click()
            logger.info("Show Details")

        # If we want the search option to be hidden
        elif not show and is_visible:
            self.click().set_locator(locator, self._name).single_click()
            logger.info("Hide Details")

        self.pause(pause)

    def fill_out_voyage_information(self, service, vessel, vessel_owner, voyage_number, second_voyage_number,
                                    customs_declarations_number, financial_voyage_period, operator, transport_mode,
                                    commercial_service):

        self.select_service(service)
        self.select_vessel(vessel)
        self.select_vessel_owner(vessel_owner)
        self.enter_voyage_number(voyage_number)
        self.enter_second_voyage_number(second_voyage_number)
        self.enter_customs_declaration_number(customs_declarations_number)
        self.enter_financial_voyage_period(financial_voyage_period)
        self.select_operator(operator)
        self.select_transport_mode(transport_mode)
        self.select_commercial_service(commercial_service)
        return self

    def fill_out_details_information(self, toggle_details=True, offshore_days=0, publish_voyage=True, remarks="", carriers_agent_ecs=""):
        # Show Details Fields, by Default True
        self.click_toggle_details(show=toggle_details, pause=1)
        # Enter Offhire Days, by Default 0
        self.enter_offhire_days(offshore_days)
        # Check True by Default
        if publish_voyage:
            self.click_publish_voyage()

        if remarks != "":
            self.enter_remarks(remarks)

        if carriers_agent_ecs != "":
            self.select_carriers_agent_ecs(carriers_agent_ecs)

        return self

    def click_add_port_call(self):
        self.click().set_locator(self._link_add_port_call, self._name).single_click()
        return self

    def click_connect_child_port_call(self):
        self.click().set_locator(self._link_connect_child_port_call, self._name).single_click()
        return self

    # Port Calls Inputs
    def enter_port_calls_port(self, index, port : str):
        root_xpath = _xpath_port_call_container(index)
        self.dropdown_autocomplete().set_locator_by_label_span(label="Port", root_xpath=root_xpath).by_text(text=port, column=2)
        locator = (By.XPATH, root_xpath, "Main Container [Scroll To Element]")
        self.scroll().set_locator(locator).to_element(100)
        return self

    def enter_port_calls_eta(self, index, date: str):
        xpath = f"{_xpath_port_call_container(index)}//label/span[text()='ETA *']/../../following-sibling::div//input"
        locator = (By.XPATH, xpath, "ETA * [Input Date]")
        self.send_keys().set_locator(locator, self._name).set_text(date).press_enter()
        return self

    def enter_port_calls_ets(self, index, date: str):
        xpath = f"{_xpath_port_call_container(index)}//label/span[text()='ETS *']/../../following-sibling::div//input"
        locator = (By.XPATH, xpath, "ETS * [Input Date]")
        self.send_keys().set_locator(locator, self._name).set_text(date).press_enter()
        return self

    def enter_port_calls_status(self, index, status: str):

        xpath = f"{_xpath_port_call_container(index)}//label[text()='Status']/../div/button[text()='PP']"

        match status:
            case "PP":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Status']/../div/button[text()='PP']"
                logger.info(f"Port Calls Status: AA index [{str(index)}]")
            case "AP":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Status']/../div/button[text()='AP']"
                logger.info(f"Port Calls Status: AP index [{str(index)}]")
            case "AA":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Status']/../div/button[text()='AA']"
                logger.info(f"Port Calls Status: AA index [{str(index)}]")
            case _:
                logger.info(f"Port Calls Status by Default: AA index [{str(index)}]")

        locator = (By.XPATH, xpath, f"Port Call [Status : {status}| Button]")
        self.click().set_locator(locator, self._name).single_click()

        return self

    def enter_port_calls_type(self, index, port_type: str):

        xpath = f"{_xpath_port_call_container(index)}//label[text()='Type']/../div/button[text()='Load']"

        match port_type:
            case "Load":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Type']/../div/button[text()='Load']"
                logger.info(f"Port Calls Type: Load index [{str(index)}]")
            case "Both":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Type']/../div/button[text()='Both']"
                logger.info(f"Port Calls Type: AP Both [{str(index)}]")
            case "Discharge":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Type']/../div/button[text()='Discharge']"
                logger.info(f"Port Calls Type: Discharge index [{str(index)}]")
            case "None":
                xpath = f"{_xpath_port_call_container(index)}//label[text()='Type']/../div/button[text()='None']"
                logger.info(f"Port Calls Type: None index [{str(index)}]")
            case _:
                logger.info(f"Port Calls by Default: Load index [{str(index)}]")

        locator = (By.XPATH, xpath, f"Status [Status : {port_type}| Button]")
        self.click().set_locator(locator, self._name).single_click()

        return self

    def select_port_call_option_delete_port_call(self, index):
        locator_dropdown = (By.XPATH, f"{_xpath_port_call_container(index)}//button[@data-toggle='dropdown']", "Dropdown (...) Multiple Options Select")
        self.click().set_locator(locator_dropdown, self._name).single_click().pause(1)

        xpath = (By.XPATH, f"{_xpath_port_call_container(index)}//button[@data-toggle='dropdown']/..//ul/li/a[contains(text(),'Delete Port Call')]", "Select Delete Port Call")
        self.click().set_locator(xpath, self._name).single_click()

        root_xpath = _xpath_port_call_container(index)
        locator = (By.XPATH, root_xpath, "Port Call Container Div")
        self.scroll().set_locator(locator).to_element(pixels=900)

        return self

    def select_port_call_option_add_port_call_bellow(self, index):
        locator_dropdown = (By.XPATH, f"{_xpath_port_call_container(index)}//button[@data-toggle='dropdown']", "Dropdown (...) Multiple Options Select")
        self.click().set_locator(locator_dropdown, self._name).single_click().pause(1)

        xpath = (By.XPATH, f"{_xpath_port_call_container(index)}//button[@data-toggle='dropdown']/..//ul/li/a[contains(text(),'Add Port Call below')]", "Select Add Port Call below")
        self.click().set_locator(xpath, self._name).single_click()

        root_xpath = _xpath_port_call_container(index)
        locator = (By.XPATH, root_xpath, "Port Call Container Div")
        self.scroll().set_locator(locator).to_element(pixels=900)
        return self

    def select_port_call_option_add_bert_call_in_port(self, index):
        locator_dropdown = (By.XPATH, f"{_xpath_port_call_container(index)}//button[@data-toggle='dropdown']", "Dropdown (...) Multiple Options Select")
        self.click().set_locator(locator_dropdown, self._name).single_click().pause(1)

        xpath = (By.XPATH, f"{_xpath_port_call_container(index)}//button[@data-toggle='dropdown']/..//ul/li/a[contains(text(),'Add Berth Call in Port')]", "Select Add Berth Call in Port")
        self.click().set_locator(xpath, self._name).single_click()

        root_xpath = _xpath_port_call_container(index)
        locator = (By.XPATH, root_xpath, "Port Call Container Div")
        self.scroll().set_locator(locator).to_element(pixels=900)
        return self

    def enter_single_ports(self, index, port, eta, ets, status, port_ype):
        self.enter_port_calls_port(index, port)
        self.enter_port_calls_eta(index, eta)
        self.enter_port_calls_ets(index, ets)
        self.enter_port_calls_status(index, status)
        self.enter_port_calls_type(index, port_ype)
        self.select_port_call_option_add_bert_call_in_port(index)
        return self

    def scroll_to_buttons(self):
        header = (By.XPATH, "//div[contains(@class,'action-bar-buttons-container')]", "Header")
        self.scroll().set_locator(header).to_element(1)
        return self

    def enter_multiple_ports(self, port_calls):

        for index, query in enumerate(port_calls, start=1):
            # This is the Index From the List receive on port_call argument
            index_data = index-1
            if index > 1:
                self.click_add_port_call()

            self.enter_single_ports(
                index=index,
                port=port_calls[index_data]["port"],
                eta=port_calls[index_data]["eta"],
                ets=port_calls[index_data]["ets"],
                status=port_calls[index_data]["status"],
                port_ype=port_calls[index_data]["type"]
            )
            self.scroll_to_buttons()
        return self












