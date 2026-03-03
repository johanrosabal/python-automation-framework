import allure
from selenium.webdriver.common.by import By
from applications.web.softship.components.buttons.Buttons import Buttons
from applications.web.softship.common.SoftshipPage import SoftshipPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('AccountPage')


class AccountPage(SoftshipPage):

    def __init__(self, driver):
        """
        Initialize the Account Page instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        self._module_url = None
        # Relative URL
        self.relative = "/MasterData/detail/Account/0/general"
        # Locator definitions
        # Headers Buttons
        self._buttons = Buttons(self._driver)

        # ==================== ACCOUNT SECTION ====================
        # Input Locators - Account Section (using label relationship)
        self._input_account_number = (By.XPATH, "//ssh-labeled-field[@label='Account Number']//input", "Account Number Input")
        self._input_sub_account_number = (By.XPATH, "//ssh-labeled-field[@label='Sub Account Number']//input", "Sub Account Number Input")
        self._input_account_name = (By.XPATH, "//ssh-labeled-field[@label='Account Name']//input", "Account Name Input")

        # Autocomplete Locators - Account Section
        self._autocomplete_ship_owner = (By.XPATH, "//ssh-labeled-field[@label='Ship Owner']//input[@role='combobox']", "Ship Owner Autocomplete")
        self._autocomplete_vessel_code = (By.XPATH, "//ssh-labeled-field[@label='Vessel (Code)']//input[@role='combobox']", "Vessel Code Autocomplete")

        # ==================== SETTINGS SECTION ====================
        # Checkbox Locators - Settings Section (using label relationship)
        self._chk_disbursement_account = (By.XPATH, "//ssh-labeled-field[@label='Disbursement Account']//input[@type='checkbox']", "Disbursement Account Checkbox")
        self._chk_payment = (By.XPATH, "//ssh-labeled-field[@label='Payment']//input[@type='checkbox']", "Payment Checkbox")
        self._chk_protect_account = (By.XPATH, "//ssh-labeled-field[@label='Protect this Account']//input[@type='checkbox']", "Protect this Account Checkbox")
        self._chk_delete_reorganization = (By.XPATH, "//ssh-labeled-field[@label='Delete in next reorganization']//input[@type='checkbox']", "Delete in next reorganization Checkbox")

        # Integer Input Locators - Settings Section
        self._input_status_wdl = (By.XPATH, "//ssh-labeled-field[@label='Status: 1 for WDL']//input", "Status: 1 for WDL Input")

        # ==================== BOOKKEEPING SECTION ====================
        # Input Locators - Bookkeeping Section
        self._input_bookkeeping_number = (By.XPATH, "//ssh-labeled-field[@label='Bookkeeping Number']//input", "Bookkeeping Number Input")
        self._input_bookkeeping_sub_number = (By.XPATH, "//ssh-labeled-field[@label='Bookkeeping Sub Number']//input", "Bookkeeping Sub Number Input")

        # Autocomplete Locators - Bookkeeping Section
        self._autocomplete_type_bookkeeping = (By.XPATH, "//ssh-labeled-field[@label='Type in Bookkeeping']//input[@role='combobox']", "Type in Bookkeeping Autocomplete")
        self._autocomplete_type_account = (By.XPATH, "//ssh-labeled-field[@label='Type of Account']//input[@role='combobox']", "Type of Account Autocomplete")

        # ==================== TRAMP SECTION ====================
        # Checkbox Locators - Tramp Section
        self._chk_tramp = (By.XPATH, "//ssh-labeled-field[@label='Tramp']//input[@type='checkbox']", "Tramp Checkbox")

        # Autocomplete Locators - Tramp Section
        self._autocomplete_tramp_so = (By.XPATH, "//ssh-labeled-field[@label='Tramp SO']//input[@role='combobox']", "Tramp SO Autocomplete")

        # Input Locators - Text Fields
        self._input_text_field_1 = (By.XPATH, "//ssh-labeled-field[@label='Text Field 1']//input", "Text Field 1 Input")
        self._input_text_field_2 = (By.XPATH, "//ssh-labeled-field[@label='Text Field 2']//input", "Text Field 2 Input")

        # ==================== REMARK SECTION ====================
        # Textarea Locators
        self._txt_remark = (By.XPATH, "//ssh-labeled-field[@label='Remark']//textarea", "Remark Textarea")

        # ==================== AUDIT SECTION (Read-Only) ====================
        # Create Date / By
        self._input_create_date = (By.XPATH, "//ssh-labeled-field[@label='Create Date']//input", "Create Date Input")
        self._input_create_date_by = (By.XPATH, "(//ssh-labeled-field[@label='By']//input)[1]", "Create Date By Input")

        # Change Date / By
        self._input_change_date = (By.XPATH, "//ssh-labeled-field[@label='Change']//input", "Change Date Input")
        self._input_change_date_by = (By.XPATH, "(//ssh-labeled-field[@label='By']//input)[2]", "Change Date By Input")

        # ==================== LABEL LOCATORS ====================
        self._lbl_account_number = (By.XPATH, "//ssh-labeled-field[@label='Account Number']//label", "Account Number Label")
        self._lbl_sub_account_number = (By.XPATH, "//ssh-labeled-field[@label='Sub Account Number']//label", "Sub Account Number Label")
        self._lbl_ship_owner = (By.XPATH, "//ssh-labeled-field[@label='Ship Owner']//label", "Ship Owner Label")
        self._lbl_vessel_code = (By.XPATH, "//ssh-labeled-field[@label='Vessel (Code)']//label", "Vessel Code Label")
        self._lbl_account_name = (By.XPATH, "//ssh-labeled-field[@label='Account Name']//label", "Account Name Label")
        self._lbl_disbursement_account = (By.XPATH, "//ssh-labeled-field[@label='Disbursement Account']//label", "Disbursement Account Label")
        self._lbl_payment = (By.XPATH, "//ssh-labeled-field[@label='Payment']//label", "Payment Label")
        self._lbl_protect_account = (By.XPATH, "//ssh-labeled-field[@label='Protect this Account']//label", "Protect this Account Label")
        self._lbl_delete_reorganization = (By.XPATH, "//ssh-labeled-field[@label='Delete in next reorganization']//label", "Delete in next reorganization Label")
        self._lbl_status_wdl = (By.XPATH, "//ssh-labeled-field[@label='Status: 1 for WDL']//label", "Status WDL Label")
        self._lbl_bookkeeping_number = (By.XPATH, "//ssh-labeled-field[@label='Bookkeeping Number']//label", "Bookkeeping Number Label")
        self._lbl_bookkeeping_sub_number = (By.XPATH, "//ssh-labeled-field[@label='Bookkeeping Sub Number']//label", "Bookkeeping Sub Number Label")
        self._lbl_type_bookkeeping = (By.XPATH, "//ssh-labeled-field[@label='Type in Bookkeeping']//label", "Type in Bookkeeping Label")
        self._lbl_type_account = (By.XPATH, "//ssh-labeled-field[@label='Type of Account']//label", "Type of Account Label")
        self._lbl_tramp = (By.XPATH, "//ssh-labeled-field[@label='Tramp']//label", "Tramp Label")
        self._lbl_tramp_so = (By.XPATH, "//ssh-labeled-field[@label='Tramp SO']//label", "Tramp SO Label")
        self._lbl_text_field_1 = (By.XPATH, "//ssh-labeled-field[@label='Text Field 1']//label", "Text Field 1 Label")
        self._lbl_text_field_2 = (By.XPATH, "//ssh-labeled-field[@label='Text Field 2']//label", "Text Field 2 Label")
        self._lbl_remark = (By.XPATH, "//ssh-labeled-field[@label='Remark']//label", "Remark Label")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    @allure.step("Load page")
    def load_page(self, pause=0):
        self._module_url = BaseApp.get_modules()["master_data"]
        logger.info("LOAD PAGE: " + self._module_url + self.relative)
        self.navigation().go(self._module_url, self.relative).pause(pause)
        return self

    # ==========================================================================
    # Button Actions
    # ==========================================================================
    def click_save(self, pause: int = 2):
        self._buttons.click_save(pause=pause)
        return self

    def click_save_and_close(self, pause: int = 2):
        self._buttons.click_save_and_close(pause=pause)
        return self

    def click_close(self, pause: int = 2):
        self._buttons.click_close(pause=pause)
        return self

    def click_confirm_yes(self, pause: int = 2):
        self._buttons.click_confirm_yes(pause=pause)
        return self

    def click_confirm_no(self, pause: int = 5):
        self._buttons.click_confirm_no(pause=pause)
        return self

    # ==========================================================================
    # ACCOUNT SECTION - Input Actions
    # ==========================================================================
    @allure.step("Enter Account Number: {account_number}")
    def enter_account_number(self, account_number: str):
        self.send_keys().set_locator(self._input_account_number, self._name).clear().set_text(account_number)
        return self

    @allure.step("Enter Sub Account Number: {sub_account_number}")
    def enter_sub_account_number(self, sub_account_number: str):
        self.send_keys().set_locator(self._input_sub_account_number, self._name).clear().set_text(sub_account_number)
        return self

    @allure.step("Enter Account Name: {account_name}")
    def enter_account_name(self, account_name: str):
        self.send_keys().set_locator(self._input_account_name, self._name).clear().set_text(account_name)
        return self

    @allure.step("Select Ship Owner: {ship_owner}")
    def select_ship_owner(self, ship_owner: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_ship_owner, self._name) \
            .clear() \
            .by_text(text=ship_owner, column=1)
        return self

    @allure.step("Select Vessel Code: {vessel_code}")
    def select_vessel_code(self, vessel_code: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_vessel_code, self._name) \
            .clear() \
            .by_text(text=vessel_code, column=1)
        return self

    # ==========================================================================
    # SETTINGS SECTION - Checkbox Actions
    # ==========================================================================
    @allure.step("Check Disbursement Account")
    def check_disbursement_account(self):
        self.checkbox().set_locator(self._chk_disbursement_account, self._name).check()
        return self

    @allure.step("Uncheck Disbursement Account")
    def uncheck_disbursement_account(self):
        self.checkbox().set_locator(self._chk_disbursement_account, self._name).uncheck()
        return self

    @allure.step("Check Payment")
    def check_payment(self):
        self.checkbox().set_locator(self._chk_payment, self._name).check()
        return self

    @allure.step("Uncheck Payment")
    def uncheck_payment(self):
        self.checkbox().set_locator(self._chk_payment, self._name).uncheck()
        return self

    @allure.step("Check Protect this Account")
    def check_protect_account(self):
        self.checkbox().set_locator(self._chk_protect_account, self._name).check()
        return self

    @allure.step("Uncheck Protect this Account")
    def uncheck_protect_account(self):
        self.checkbox().set_locator(self._chk_protect_account, self._name).uncheck()
        return self

    @allure.step("Check Delete in next reorganization")
    def check_delete_reorganization(self):
        self.checkbox().set_locator(self._chk_delete_reorganization, self._name).check()
        return self

    @allure.step("Uncheck Delete in next reorganization")
    def uncheck_delete_reorganization(self):
        self.checkbox().set_locator(self._chk_delete_reorganization, self._name).uncheck()
        return self

    @allure.step("Enter Status WDL: {status_wdl}")
    def enter_status_wdl(self, status_wdl: str):
        self.send_keys().set_locator(self._input_status_wdl, self._name).clear().set_text(status_wdl)
        return self

    # ==========================================================================
    # BOOKKEEPING SECTION - Input Actions
    # ==========================================================================
    @allure.step("Enter Bookkeeping Number: {bookkeeping_number}")
    def enter_bookkeeping_number(self, bookkeeping_number: str):
        self.send_keys().set_locator(self._input_bookkeeping_number, self._name).clear().set_text(bookkeeping_number)
        return self

    @allure.step("Enter Bookkeeping Sub Number: {bookkeeping_sub_number}")
    def enter_bookkeeping_sub_number(self, bookkeeping_sub_number: str):
        self.send_keys().set_locator(self._input_bookkeeping_sub_number, self._name).clear().set_text(bookkeeping_sub_number)
        return self

    @allure.step("Select Type in Bookkeeping: {type_bookkeeping}")
    def select_type_bookkeeping(self, type_bookkeeping: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_type_bookkeeping, self._name) \
            .clear() \
            .by_text(text=type_bookkeeping, column=1)
        return self

    @allure.step("Select Type of Account: {type_account}")
    def select_type_account(self, type_account: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_type_account, self._name) \
            .clear() \
            .by_text(text=type_account, column=1)
        return self

    # ==========================================================================
    # TRAMP SECTION - Actions
    # ==========================================================================
    @allure.step("Check Tramp")
    def check_tramp(self):
        self.checkbox().set_locator(self._chk_tramp, self._name).check()
        return self

    @allure.step("Uncheck Tramp")
    def uncheck_tramp(self):
        self.checkbox().set_locator(self._chk_tramp, self._name).uncheck()
        return self

    @allure.step("Select Tramp SO: {tramp_so}")
    def select_tramp_so(self, tramp_so: str):
        self.dropdown_autocomplete() \
            .set_locator(self._autocomplete_tramp_so, self._name) \
            .clear() \
            .by_text(text=tramp_so, column=1)
        return self

    @allure.step("Enter Text Field 1: {text_field_1}")
    def enter_text_field_1(self, text_field_1: str):
        self.send_keys().set_locator(self._input_text_field_1, self._name).clear().set_text(text_field_1)
        return self

    @allure.step("Enter Text Field 2: {text_field_2}")
    def enter_text_field_2(self, text_field_2: str):
        self.send_keys().set_locator(self._input_text_field_2, self._name).clear().set_text(text_field_2)
        return self

    # ==========================================================================
    # REMARK SECTION - Actions
    # ==========================================================================
    @allure.step("Enter Remark: {remark}")
    def enter_remark(self, remark: str):
        self.send_keys().set_locator(self._txt_remark, self._name).clear().set_text(remark)
        return self

    # ==========================================================================
    # Get Values Actions
    # ==========================================================================
    @allure.step("Get Account Number Value")
    def get_account_number_value(self):
        return self.get_attribute().set_locator(self._input_account_number, self._name).get_value()

    @allure.step("Get Sub Account Number Value")
    def get_sub_account_number_value(self):
        return self.get_attribute().set_locator(self._input_sub_account_number, self._name).get_value()

    @allure.step("Get Account Name Value")
    def get_account_name_value(self):
        return self.get_attribute().set_locator(self._input_account_name, self._name).get_value()

    @allure.step("Get Ship Owner Value")
    def get_ship_owner_value(self):
        return self.get_attribute().set_locator(self._autocomplete_ship_owner, self._name).get_value()

    @allure.step("Get Vessel Code Value")
    def get_vessel_code_value(self):
        return self.get_attribute().set_locator(self._autocomplete_vessel_code, self._name).get_value()

    @allure.step("Get Bookkeeping Number Value")
    def get_bookkeeping_number_value(self):
        return self.get_attribute().set_locator(self._input_bookkeeping_number, self._name).get_value()

    @allure.step("Get Bookkeeping Sub Number Value")
    def get_bookkeeping_sub_number_value(self):
        return self.get_attribute().set_locator(self._input_bookkeeping_sub_number, self._name).get_value()

    @allure.step("Get Type in Bookkeeping Value")
    def get_type_bookkeeping_value(self):
        return self.get_attribute().set_locator(self._autocomplete_type_bookkeeping, self._name).get_value()

    @allure.step("Get Type of Account Value")
    def get_type_account_value(self):
        return self.get_attribute().set_locator(self._autocomplete_type_account, self._name).get_value()

    @allure.step("Get Tramp SO Value")
    def get_tramp_so_value(self):
        return self.get_attribute().set_locator(self._autocomplete_tramp_so, self._name).get_value()

    @allure.step("Get Text Field 1 Value")
    def get_text_field_1_value(self):
        return self.get_attribute().set_locator(self._input_text_field_1, self._name).get_value()

    @allure.step("Get Text Field 2 Value")
    def get_text_field_2_value(self):
        return self.get_attribute().set_locator(self._input_text_field_2, self._name).get_value()

    @allure.step("Get Remark Value")
    def get_remark_value(self):
        return self.get_attribute().set_locator(self._txt_remark, self._name).get_value()

    @allure.step("Get Status WDL Value")
    def get_status_wdl_value(self):
        return self.get_attribute().set_locator(self._input_status_wdl, self._name).get_value()

    @allure.step("Get Create Date Value")
    def get_create_date_value(self):
        return self.get_attribute().set_locator(self._input_create_date, self._name).get_value()

    @allure.step("Get Create Date By Value")
    def get_create_date_by_value(self):
        return self.get_attribute().set_locator(self._input_create_date_by, self._name).get_value()

    @allure.step("Get Change Date Value")
    def get_change_date_value(self):
        return self.get_attribute().set_locator(self._input_change_date, self._name).get_value()

    @allure.step("Get Change Date By Value")
    def get_change_date_by_value(self):
        return self.get_attribute().set_locator(self._input_change_date_by, self._name).get_value()

    # ==========================================================================
    # Checkbox State Actions
    # ==========================================================================
    @allure.step("Is Disbursement Account Checked")
    def is_disbursement_account_checked(self):
        return self.checkbox().set_locator(self._chk_disbursement_account, self._name).is_checked()

    @allure.step("Is Payment Checked")
    def is_payment_checked(self):
        return self.checkbox().set_locator(self._chk_payment, self._name).is_checked()

    @allure.step("Is Protect Account Checked")
    def is_protect_account_checked(self):
        return self.checkbox().set_locator(self._chk_protect_account, self._name).is_checked()

    @allure.step("Is Delete Reorganization Checked")
    def is_delete_reorganization_checked(self):
        return self.checkbox().set_locator(self._chk_delete_reorganization, self._name).is_checked()

    @allure.step("Is Tramp Checked")
    def is_tramp_checked(self):
        return self.checkbox().set_locator(self._chk_tramp, self._name).is_checked()

    # ==========================================================================
    # Validation Actions
    # ==========================================================================
    @allure.step("Verify Account Number is displayed")
    def verify_account_number_is_displayed(self):
        return self.element().set_locator(self._input_account_number, self._name).is_visible()

    @allure.step("Verify Sub Account Number is displayed")
    def verify_sub_account_number_is_displayed(self):
        return self.element().set_locator(self._input_sub_account_number, self._name).is_visible()

    @allure.step("Verify Account Name is displayed")
    def verify_account_name_is_displayed(self):
        return self.element().set_locator(self._input_account_name, self._name).is_visible()

    @allure.step("Verify Ship Owner is displayed")
    def verify_ship_owner_is_displayed(self):
        return self.element().set_locator(self._autocomplete_ship_owner, self._name).is_visible()

    @allure.step("Verify Vessel Code is displayed")
    def verify_vessel_code_is_displayed(self):
        return self.element().set_locator(self._autocomplete_vessel_code, self._name).is_visible()

    @allure.step("Verify Disbursement Account is displayed")
    def verify_disbursement_account_is_displayed(self):
        return self.element().set_locator(self._chk_disbursement_account, self._name).is_visible()

    @allure.step("Verify Payment is displayed")
    def verify_payment_is_displayed(self):
        return self.element().set_locator(self._chk_payment, self._name).is_visible()

    @allure.step("Verify page is loaded")
    def verify_page_is_loaded(self):
        return self.verify_account_number_is_displayed()
