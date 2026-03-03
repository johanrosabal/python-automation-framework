import allure
from applications.web.softship.pages.masterdata.financial.account.AccountPage import AccountPage
from core.config.logger_config import setup_logger

logger = setup_logger('AccountPageFlow')


class AccountPageFlow:
    """
    Fluent Pattern class for Account Page operations.
    Allows chaining methods to fill the Account form in a readable way.
    
    Example usage:
        AccountPageFlow() \\
            .load() \\
            .with_account_number("ACC001") \\
            .with_sub_account_number("SUB001") \\
            .with_ship_owner("CROWLEY") \\
            .with_account_name("Test Account") \\
            .with_disbursement_account(True) \\
            .with_payment(True) \\
            .with_bookkeeping_number("BK001") \\
            .with_type_bookkeeping("EXPENSE") \\
            .with_type_account("REVENUE") \\
            .save()
    """

    def __init__(self):
        """Initialize the Account Page Flow."""
        self._page = AccountPage.get_instance()
        self._name = self.__class__.__name__

    # ==========================================================================
    # Navigation
    # ==========================================================================
    @allure.step("Load Account Page")
    def load(self, pause: int = 2):
        """Load the Account page."""
        logger.info(f"{self._name}: Loading Account Page")
        self._page.load_page(pause=pause)
        return self

    # ==========================================================================
    # ACCOUNT SECTION - Fluent Methods
    # ==========================================================================
    @allure.step("Set Account Number: {account_number}")
    def with_account_number(self, account_number: str):
        """Set the Account Number field."""
        logger.info(f"{self._name}: Setting Account Number to '{account_number}'")
        self._page.enter_account_number(account_number)
        return self

    @allure.step("Set Sub Account Number: {sub_account_number}")
    def with_sub_account_number(self, sub_account_number: str):
        """Set the Sub Account Number field."""
        logger.info(f"{self._name}: Setting Sub Account Number to '{sub_account_number}'")
        self._page.enter_sub_account_number(sub_account_number)
        return self

    @allure.step("Set Ship Owner: {ship_owner}")
    def with_ship_owner(self, ship_owner: str):
        """Set the Ship Owner autocomplete field."""
        logger.info(f"{self._name}: Setting Ship Owner to '{ship_owner}'")
        self._page.select_ship_owner(ship_owner)
        return self

    @allure.step("Set Vessel Code: {vessel_code}")
    def with_vessel_code(self, vessel_code: str):
        """Set the Vessel Code autocomplete field."""
        logger.info(f"{self._name}: Setting Vessel Code to '{vessel_code}'")
        self._page.select_vessel_code(vessel_code)
        return self

    @allure.step("Set Account Name: {account_name}")
    def with_account_name(self, account_name: str):
        """Set the Account Name field."""
        logger.info(f"{self._name}: Setting Account Name to '{account_name}'")
        self._page.enter_account_name(account_name)
        return self

    # ==========================================================================
    # SETTINGS SECTION - Fluent Methods
    # ==========================================================================
    @allure.step("Set Disbursement Account: {checked}")
    def with_disbursement_account(self, checked: bool = True):
        """Set the Disbursement Account checkbox."""
        logger.info(f"{self._name}: Setting Disbursement Account to '{checked}'")
        if checked:
            self._page.check_disbursement_account()
        else:
            self._page.uncheck_disbursement_account()
        return self

    @allure.step("Set Payment: {checked}")
    def with_payment(self, checked: bool = True):
        """Set the Payment checkbox."""
        logger.info(f"{self._name}: Setting Payment to '{checked}'")
        if checked:
            self._page.check_payment()
        else:
            self._page.uncheck_payment()
        return self

    @allure.step("Set Protect Account: {checked}")
    def with_protect_account(self, checked: bool = True):
        """Set the Protect this Account checkbox."""
        logger.info(f"{self._name}: Setting Protect Account to '{checked}'")
        if checked:
            self._page.check_protect_account()
        else:
            self._page.uncheck_protect_account()
        return self

    @allure.step("Set Delete in Reorganization: {checked}")
    def with_delete_reorganization(self, checked: bool = True):
        """Set the Delete in next reorganization checkbox."""
        logger.info(f"{self._name}: Setting Delete Reorganization to '{checked}'")
        if checked:
            self._page.check_delete_reorganization()
        else:
            self._page.uncheck_delete_reorganization()
        return self

    @allure.step("Set Status WDL: {status_wdl}")
    def with_status_wdl(self, status_wdl: str):
        """Set the Status WDL field."""
        logger.info(f"{self._name}: Setting Status WDL to '{status_wdl}'")
        self._page.enter_status_wdl(status_wdl)
        return self

    # ==========================================================================
    # BOOKKEEPING SECTION - Fluent Methods
    # ==========================================================================
    @allure.step("Set Bookkeeping Number: {bookkeeping_number}")
    def with_bookkeeping_number(self, bookkeeping_number: str):
        """Set the Bookkeeping Number field."""
        logger.info(f"{self._name}: Setting Bookkeeping Number to '{bookkeeping_number}'")
        self._page.enter_bookkeeping_number(bookkeeping_number)
        return self

    @allure.step("Set Bookkeeping Sub Number: {bookkeeping_sub_number}")
    def with_bookkeeping_sub_number(self, bookkeeping_sub_number: str):
        """Set the Bookkeeping Sub Number field."""
        logger.info(f"{self._name}: Setting Bookkeeping Sub Number to '{bookkeeping_sub_number}'")
        self._page.enter_bookkeeping_sub_number(bookkeeping_sub_number)
        return self

    @allure.step("Set Type in Bookkeeping: {type_bookkeeping}")
    def with_type_bookkeeping(self, type_bookkeeping: str):
        """Set the Type in Bookkeeping autocomplete field."""
        logger.info(f"{self._name}: Setting Type in Bookkeeping to '{type_bookkeeping}'")
        self._page.select_type_bookkeeping(type_bookkeeping)
        return self

    @allure.step("Set Type of Account: {type_account}")
    def with_type_account(self, type_account: str):
        """Set the Type of Account autocomplete field."""
        logger.info(f"{self._name}: Setting Type of Account to '{type_account}'")
        self._page.select_type_account(type_account)
        return self

    # ==========================================================================
    # TRAMP SECTION - Fluent Methods
    # ==========================================================================
    @allure.step("Set Tramp: {checked}")
    def with_tramp(self, checked: bool = True):
        """Set the Tramp checkbox."""
        logger.info(f"{self._name}: Setting Tramp to '{checked}'")
        if checked:
            self._page.check_tramp()
        else:
            self._page.uncheck_tramp()
        return self

    @allure.step("Set Tramp SO: {tramp_so}")
    def with_tramp_so(self, tramp_so: str):
        """Set the Tramp SO autocomplete field."""
        logger.info(f"{self._name}: Setting Tramp SO to '{tramp_so}'")
        self._page.select_tramp_so(tramp_so)
        return self

    @allure.step("Set Text Field 1: {text_field_1}")
    def with_text_field_1(self, text_field_1: str):
        """Set the Text Field 1."""
        logger.info(f"{self._name}: Setting Text Field 1 to '{text_field_1}'")
        self._page.enter_text_field_1(text_field_1)
        return self

    @allure.step("Set Text Field 2: {text_field_2}")
    def with_text_field_2(self, text_field_2: str):
        """Set the Text Field 2."""
        logger.info(f"{self._name}: Setting Text Field 2 to '{text_field_2}'")
        self._page.enter_text_field_2(text_field_2)
        return self

    # ==========================================================================
    # REMARK SECTION - Fluent Methods
    # ==========================================================================
    @allure.step("Set Remark: {remark}")
    def with_remark(self, remark: str):
        """Set the Remark textarea."""
        logger.info(f"{self._name}: Setting Remark to '{remark}'")
        self._page.enter_remark(remark)
        return self

    # ==========================================================================
    # Action Methods (Terminal Operations)
    # ==========================================================================
    @allure.step("Save Account")
    def save(self, pause: int = 2):
        """Click the Save button."""
        logger.info(f"{self._name}: Clicking Save button")
        self._page.click_save(pause=pause)
        return self

    @allure.step("Save and Close Account")
    def save_and_close(self, pause: int = 2):
        """Click the Save and Close button."""
        logger.info(f"{self._name}: Clicking Save and Close button")
        self._page.click_save_and_close(pause=pause)
        return self

    @allure.step("Close Account Page")
    def close(self, pause: int = 2):
        """Click the Close button."""
        logger.info(f"{self._name}: Clicking Close button")
        self._page.click_close(pause=pause)
        return self

    @allure.step("Confirm Yes")
    def confirm_yes(self, pause: int = 2):
        """Click Yes on confirmation dialog."""
        logger.info(f"{self._name}: Clicking Confirm Yes")
        self._page.click_confirm_yes(pause=pause)
        return self

    @allure.step("Confirm No")
    def confirm_no(self, pause: int = 2):
        """Click No on confirmation dialog."""
        logger.info(f"{self._name}: Clicking Confirm No")
        self._page.click_confirm_no(pause=pause)
        return self

    # ==========================================================================
    # Validation Methods
    # ==========================================================================
    @allure.step("Verify Page is Loaded")
    def verify_page_loaded(self):
        """Verify the Account page is loaded."""
        logger.info(f"{self._name}: Verifying page is loaded")
        self._page.verify_page_is_loaded()
        return self

    # ==========================================================================
    # Bulk Fill Method using Dictionary
    # ==========================================================================
    @allure.step("Fill Account Form with Data")
    def fill_form(self, data: dict):
        """
        Fill the Account form using a dictionary.
        
        Args:
            data: Dictionary with field names as keys and values to fill.
            
        Example:
            data = {
                "account_number": "ACC001",
                "sub_account_number": "SUB001",
                "ship_owner": "CROWLEY",
                "account_name": "Test Account",
                "disbursement_account": True,
                "payment": True,
                "protect_account": False,
                "delete_reorganization": False,
                "status_wdl": "1",
                "bookkeeping_number": "BK001",
                "bookkeeping_sub_number": "BKSUB001",
                "type_bookkeeping": "EXPENSE",
                "type_account": "REVENUE",
                "tramp": False,
                "tramp_so": "TRAMP001",
                "text_field_1": "Custom Text 1",
                "text_field_2": "Custom Text 2",
                "remark": "Test remark"
            }
            AccountPageFlow().load().fill_form(data).save()
        """
        logger.info(f"{self._name}: Filling form with data: {data}")

        # Map dictionary keys to fluent methods
        field_mapping = {
            "account_number": self.with_account_number,
            "sub_account_number": self.with_sub_account_number,
            "ship_owner": self.with_ship_owner,
            "vessel_code": self.with_vessel_code,
            "account_name": self.with_account_name,
            "disbursement_account": self.with_disbursement_account,
            "payment": self.with_payment,
            "protect_account": self.with_protect_account,
            "delete_reorganization": self.with_delete_reorganization,
            "status_wdl": self.with_status_wdl,
            "bookkeeping_number": self.with_bookkeeping_number,
            "bookkeeping_sub_number": self.with_bookkeeping_sub_number,
            "type_bookkeeping": self.with_type_bookkeeping,
            "type_account": self.with_type_account,
            "tramp": self.with_tramp,
            "tramp_so": self.with_tramp_so,
            "text_field_1": self.with_text_field_1,
            "text_field_2": self.with_text_field_2,
            "remark": self.with_remark,
        }

        for field, value in data.items():
            if field in field_mapping and value is not None:
                field_mapping[field](value)

        return self

    # ==========================================================================
    # Get Page Instance
    # ==========================================================================
    def get_page(self) -> AccountPage:
        """Return the underlying AccountPage instance for direct access."""
        return self._page
