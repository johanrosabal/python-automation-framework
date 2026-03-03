import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('FinancialMenu')


class FinancialMenu(BasePage):

    def __init__(self, driver):
        """
        Initialize the Financial Manu instance.
        """
        super().__init__(driver)
        # Relative URL
        self.relative = "/Home/Index?selectedMenuItemIndex=4"
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Locator definitions
        self.__link_account = (By.XPATH, "//a[text()='Account']", "Account Link")
        self.__link_general_ledger_account = (By.XPATH, "//a[text()='General Ledger Account']",
                                              "General Ledger Account Link")
        self.__link_calculation_base = (By.XPATH, "//a[text()='Calculation Base']", "Calculation Base Link")
        self.__link_calculation_rule_template = (By.XPATH, "//a[text()='Calculation Rule Template']",
                                                 "Calculation Rule Template Link")
        self.__link_cost_centre = (By.XPATH, "//a[text()='Cost Centre']", "Cost Centre Link")
        self.__link_cost_revenue_code = (By.XPATH, "//a[text()='Cost/Revenue Code']", "Cost/Revenue Code Link")
        self.__link_cost_revenue_group = (By.XPATH, "//a[text()='Cost/Revenue Group']", "Cost/Revenue Group Link")
        self.__link_equipment_C_R_code_assignment = (By.XPATH, "//a[text()='Equipment C/R Code Assignment']",
                                                     "Equipment C/R Code Assignment Link")
        self.__link_internal_cost_revenue_code = (By.XPATH, "//a[text()='Internal Cost/Revenue Code']",
                                                  "Internal Cost/Revenue Code Link")
        self.__link_logistics_C_R_code_assignment = (By.XPATH, "//a[text()='Logistics C/R Code Assignment']",
                                                     "Logistics C/R Code Assignment Link")
        self.__link_surcharge_costcode_assignment = (By.XPATH, "//a[text()='Surcharge/Costcode Assignment']",
                                                     "Surcharge/Costcode Assignment Link")
        self.__link_currency = (By.XPATH, "//a[text()='Currency']", "Currency Link")
        self.__link_exchange_rate = (By.XPATH, "//a[text()='Exchange Rate']", "Exchange Rate Link")
        self.__link_period_definition = (By.XPATH, "//a[text()='Period Definition']", "Period Definition Link")
        self.__link_purchase_tariff_criteria = (By.XPATH, "//a[text()='Purchase Tariff Criteria']",
                                                "Purchase Tariff Criteria Link")
        self.__link_surcharge = (By.XPATH, "//a[text()='Surcharge']", "Surcharge Link")
        self.__link_term_of_payment = (By.XPATH, "//a[text()='Term of Payment']", "Term of Payment Link")
        self.__link_vat = (By.XPATH, "//a[text()='VAT']", "VAT Link")
        self.__link_sales_tariff_criteria = (By.XPATH, "//a[text()='Sales Tariff Criteria']",
                                             "Sales Tariff Criteria Link")
        self.__link_sof_validation = (By.XPATH, "//a[text()='SOF Validation']", "SOF Validation Link")
        self.__link_short_form_remarks = (By.XPATH, "//a[text()='Short Form Remarks']", "Short Form Remarks Link")

    @allure.step("Load Financial Page")
    def _load_page(self, locator, pause):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative)
        self.click().set_locator(locator, self._name).single_click().pause(pause)

    @allure.step("Link Account")
    def link_account(self, pause: int = 0):
        self._load_page(self.__link_account, pause)
        return self

    @allure.step("Link General Ledger Account")
    def link_general_ledger_account(self, pause: int = 0):
        self._load_page(self.__link_general_ledger_account, pause)
        return self

    @allure.step("Link Calculation Base")
    def link_calculation_base(self, pause: int = 0):
        self._load_page(self.__link_calculation_base, pause)
        return self

    @allure.step("Link Calculation Rule Template")
    def link_calculation_rule_template(self, pause: int = 0):
        self._load_page(self.__link_calculation_rule_template, pause)
        return self

    @allure.step("Link Cost Centre")
    def link_cost_centre(self, pause: int = 0):
        self._load_page(self.__link_cost_centre, pause)
        return self

    @allure.step("Link Cost/Revenue Code")
    def link_cost_revenue_code(self, pause: int = 0):
        self._load_page(self.__link_cost_revenue_code, pause)
        return self

    @allure.step("Link Cost/Revenue Group")
    def link_cost_revenue_group(self, pause: int = 0):
        self._load_page(self.__link_cost_revenue_group, pause)
        return self

    @allure.step("Link Equipment C/R Code Assignment")
    def link_equipment_c_r_code_assignment(self, pause: int = 0):
        self._load_page(self.__link_equipment_C_R_code_assignment, pause)
        return self

    @allure.step("Link Internal Cost/Revenue Code")
    def link_internal_cost_revenue_code(self, pause: int = 0):
        self._load_page(self.__link_internal_cost_revenue_code, pause)
        return self

    @allure.step("Link Logistics C/R Code Assignment")
    def link_logistics_c_r_code_assignment(self, pause: int = 0):
        self._load_page(self.__link_logistics_C_R_code_assignment, pause)
        return self

    @allure.step("Link Surcharge/Costcode Assignment")
    def link_surcharge_costcode_assignment(self, pause: int = 0):
        self._load_page(self.__link_surcharge_costcode_assignment, pause)
        return self

    @allure.step("Link Currency")
    def link_currency(self, pause: int = 0):
        self._load_page(self.__link_currency, pause)
        return self

    @allure.step("Link Exchange Rate")
    def link_exchange_rate(self, pause: int = 0):
        self._load_page(self.__link_exchange_rate, pause)
        return self

    @allure.step("Link Period Definition")
    def link_period_definition(self, pause: int = 0):
        self._load_page(self.__link_period_definition, pause)
        return self

    @allure.step("Link Purchase Tariff Criteria")
    def link_purchase_tariff_criteria(self, pause: int = 0):
        self._load_page(self.__link_purchase_tariff_criteria, pause)
        return self

    @allure.step("Link Surcharge")
    def link_surcharge(self, pause: int = 0):
        self._load_page(self.__link_surcharge, pause)
        return self

    @allure.step("Link Term of Payment")
    def link_term_of_payment(self, pause: int = 0):
        self._load_page(self.__link_term_of_payment, pause)
        return self

    @allure.step("Link VAT")
    def link_vat(self, pause: int = 0):
        self._load_page(self.__link_vat, pause)
        return self

    @allure.step("Link Sales Tariff Criteria")
    def link_sales_tariff_criteria(self, pause: int = 0):
        self._load_page(self.__link_sales_tariff_criteria, pause)
        return self

    @allure.step("Link SOF Validation")
    def link_sof_validation(self, pause: int = 0):
        self._load_page(self.__link_sof_validation, pause)
        return self

    @allure.step("Link Short Form Remarks")
    def link_short_form_remarks(self, pause: int = 0):
        self._load_page(self.__link_short_form_remarks, pause)
        return self
