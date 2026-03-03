import allure
from core.config.logger_config import setup_logger
from core.ui.common.BasePage import BasePage
from selenium.webdriver.common.by import By
logger = setup_logger('BasicMenu')


class Buttons(BasePage):

    def __init__(self, driver):
        """
        Initialize the Buttons class.
        """
        super().__init__(driver)
        # Name
        self._name = self.__class__.__name__
        # Locator definitions
        # Buttons
        self.__btn_select = (By.XPATH, "//button/span[text()='Select'] | //button[contains(text(),'Select')]", "Select [Button]")
        self.__btn_select_toggle = (By.XPATH, "//span[contains(@class,'pi-angle')] | //span[contains(@class,'fa-caret')]", "Select ^ [Toggle]")
        self.__btn_new = (By.XPATH, "//button/span[text()='New'] | //button[@id='btnNew'] | //button[contains(text(),'New')]", "New [Button]")
        self.__btn_copy = (By.XPATH, "//button/span[text()='Copy'] | //button[@id='btnCopy'] | //button[contains(text(),'Copy')]", "Copy [Button]")
        self.__btn_delete = (By.XPATH, "//button/span[text()='Delete'] | //button[@id='btnDelete']", "Delete  [Button]")
        self.__btn_excel_export = (By.XPATH, "//button/span[text()='Excel Export'] | //button[@id='btnExportQuery']", "Excel Export [Button]")
        self.__btn_add_to_schedule = (By.XPATH, "//button/span[text()='Add to Schedule']", "Add to Schedule [Button]")
        self.__btn_unlock_position = (By.XPATH, "//button/span[text()='Unlock Position']", "Unlock Position [Button]")
        self.__btn_remove = (By.XPATH, "//button/span[text()='Remove']", "Remove [Button]")
        self.__btn_edit = (By.XPATH, "//button[@id='btnDetails']", "Edit [Button]")
        self.__btn_save = (By.XPATH, "//button[@id='btnSave'] | //button[@title='Save']", "Save [Button]")
        self.__btn_save_and_close = (By.XPATH, "//button[@title='Save and Close'] | //button[@id='btnSaveAndClose']", "Save And Close Button")
        self.__btn_close = (By.XPATH, "//button[@id='btnClose'] | //button[@title='Close']", "Close Button")
        self.__btn_cancel = (By.XPATH, "//button[@id='btnCancel']", "Cancel [Button]")
        self.__btn_customize_screen = (By.XPATH, "//button[@id='btnCustomizeScreen']", "Customize Screen [Button]")
        self.__btn_sql_info = (By.XPATH, "//button[@id='btnSqlInfo']", "Sql Info {Button}")
        self.__btn_excel_export_with = (By.XPATH, "//button[@id='btnExportWithMetaData']", "Excel Export+ [Button]")
        self.__btn_import_excel = (By.XPATH, "//button[@id='btnImportExcel']", "Import Excel [Button]")
        self.__btn_close_selected_accounts = (By.XPATH, "//button/span[text()='Close Selected Accounts']", "Close Selected Accounts [Button]")
        self.__btn_confirm_yes = (By.XPATH, "//button[contains(@class,'confirm-button-yes')]", "Conform Yes Button")
        self.__btn_confirm_no = (By.XPATH, "//button[contains(@class,'confirm-button-no')]", "Conform No Button")
        self.__btn_multi_update_details = (By.XPATH, "//button[@id='btnMultiUpdateDetails']", "Multi Update Details [Button]")
        self.__btn_expire_and_copy = (By.XPATH, "//button[contains(text(),'Expire & Copy')]", "Expire & Copy [Button]")
        self.__btn_export_changes = (By.XPATH, "//button[contains(text(),'Export Charges')]", "Export Changes [Button]")
        self.__btn_tariff_export = (By.XPATH, "//button[contains(text(),'Tariff Export')]", "Tariff Export [Button]")
        self.__btn_change_history = (By.XPATH, "//button[contains(text(),'Change History')]", "Change History [Button]")

        # Buttons From Commercial https://softship-qa.crowley.com/Commercial/Query/Index/VoyageAdvanced
        self.__btn_calculate_cut_off = (By.XPATH, "//button/span[contains(text(),'Calculate Cut-Off')]", "Calculate Cut-Off [Button]")
        self.__btn_create_new_voyage_from_template = (By.XPATH, "//button/span[contains(text(),'Create new voyage from template')]", "Create new voyage from template [Button]")
        self.__btn_create_new_voyage_from_selected_voyage = (By.XPATH, "//button/span[contains(text(),'Create new voyage from selected voyage')]", "Create new voyage from selected voyage [Button]")

        # Buttons from Container QueryPage https://softship-qa.crowley.com/Booking/Query/Index/BookingAdvancedContainer
        self.__btn_multi_update = (By.XPATH, "//button[@id='multiUpdateButtonId'] | //button[@id='btnMultiUpdate']", "Multi Update [Button]")
        self.__btn_create_events = (By.XPATH, "//button[@id='createEventsButtonId']", "Create Events [Button]")
        self.__btn_manage_doc_only_bookings = (By.XPATH, "//button[@id='manageDobButtonId']", "Manage Docs Bookings [Button]")
        self.__btn_copy_booking = (By.XPATH, "//button[@id='copyButtonId']", "Copy Booking [Button]")

        # Buttons from Roro Query Page https://softship-qa.crowley.com/Booking/Query/Index/BookingAdvancedRoRo
        self.__btn_vin_insert = (By.XPATH, "//button[@id='vinImportButtonId']", "VIN Insert [Button]")
        self.__btn_update_vin = (By.XPATH, "//button[@id='squishVinIButtonId']", "Update VIN [Button]")
        self.__btn_update_vin = (By.XPATH, "//button[@id='squishVinIButtonId']", "Update VIN [Button]")

        # Buttons from Rebooking Query Page https://softship-qa.crowley.com/Booking/Query/Index/RebookingLegBasis
        self.__btn_rebook = (By.XPATH, "//button[@id='rebookButtonId']", "Rebook [Button]")
        self.__btn_godsnumber = (By.XPATH, "//button[@id='godsnumberButtonId']", "Godsnumber [Button]")

        # Buttons from Create Booking https://softship-qa.crowley.com/Booking/booking/{bookingNumber}/main/summary
        self.__btn_return_to_pending = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderReturnToPending')]", "Return to Pending [Button]")
        self.__btn_confirm_booking =  (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderConfirmBooking')]", "Confirm Booking [Button]")
        self.__btn_auto_b_l = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderAutoBL')]", "Auto B/L [Button]")
        self.__link_b_l = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderLinkAutoBL')]", "Link B/L [Button]")
        self.__unlink_b_l = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderUnlinkAutoBL')]", "Unlink B/L [Button]")
        self.__match_clauses = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderMatchClauses')]", "Match Clauses [Button]")
        self.__match_revenues = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderMatchRevenues')]", "Match Revenues [Button]")
        self.__match_costs = (By.XPATH, "//button[contains(@sshcustomizable, 'HeaderMatchCosts')]", "Match Costs [Button]")
        self.__create_report = (By.XPATH, "//button[contains(@sshcustomizable, 'CreateReport')]", "Create Report [Button]")
        self.__assign_lcl = (By.XPATH, "//button[contains(@sshcustomizable, 'AssignLcl')]", "Assign LCL [Button]")
        self.__manage_dobs = (By.XPATH, "//button[contains(@sshcustomizable, 'ManageDob')]", "Manage DOBs [Button]")

    @allure.step("Click Select Button")
    def click_select(self, pause: int = 0):
        self.click().set_locator(self.__btn_select, self._name).single_click().pause(pause)
        return self

    # @allure.step("Click Select Toggle Button")
    # def click_select_toggle(self, pause: int = 0):
    #     self.click().set_locator(self.__btn_select_toggle, self._name).single_click().pause(pause)
    #     return self

    @allure.step("Click Select Toggle Button")
    def click_select_toggle(self, show=True, pause=0):
        """
           Ensure the search button is in the desired state (shown or hidden).

           :param pause: Pause seconds
           :param show: If True, ensures the search option is visible ('up').
                        If False, ensures the search option is hidden ('down').
           """
        class_attribute = self.element().set_locator(self.__btn_select_toggle, self._name).get_attribute("class")

        # Define the states based on the class attribute values
        is_hidden = "down" in class_attribute
        is_visible = "up" in class_attribute

        # If we want the search option to be shown
        if show and is_hidden:
            self.click().set_locator(self.__btn_select_toggle, self._name).single_click()
            logger.info("Show: Search Button")

        # If we want the search option to be hidden
        elif not show and is_visible:
            self.click().set_locator(self.__btn_select_toggle, self._name).single_click()
            logger.info("Hide: Search Button")

        self.pause(pause)

    @allure.step("Click New Button")
    def click_new(self, pause: int = 0):
        self.click().set_locator(self.__btn_new, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Copy Button")
    def click_copy(self, pause: int = 0):
        self.click().set_locator(self.__btn_copy, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Delete Button")
    def click_delete(self, pause: int = 0):
        self.click().set_locator(self.__btn_delete, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Excel Export Button")
    def click_excel_export(self, pause: int = 0):
        self.click().set_locator(self.__btn_excel_export, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Add to schedule Button")
    def click_add_to_schedule(self, pause: int = 0):
        self.click().set_locator(self.__btn_add_to_schedule, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Unlock Position Button")
    def click_unlock_position(self, pause: int = 0):
        self.click().set_locator(self.__btn_unlock_position, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Remove Button")
    def click_remove(self, pause: int = 0):
        self.click().set_locator(self.__btn_remove, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Edit Button")
    def click_edit(self, pause: int = 0):
        self.click().set_locator(self.__btn_edit, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Save Button")
    def click_save(self, pause: int = 0):
        self.click().set_locator(self.__btn_save, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Save and Close Button")
    def click_save_and_close(self, pause: int = 0):
        self.click().set_locator(self.__btn_save_and_close, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Close Button")
    def click_close(self, pause: int = 0):
        self.click().set_locator(self.__btn_close, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Cancel Button")
    def click_cancel(self, pause: int = 0):
        self.click().set_locator(self.__btn_cancel, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Customize Screen Button")
    def click_customize_screen(self, pause: int = 0):
        self.click().set_locator(self.__btn_customize_screen, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Sql Info Button")
    def click_sql_info(self, pause: int = 0):
        self.click().set_locator(self.__btn_sql_info, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Excel Export With Button")
    def click_excel_export_with(self, pause: int = 0):
        self.click().set_locator(self.__btn_excel_export_with, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Excel Import Button")
    def click_excel_import(self, pause: int = 0):
        self.click().set_locator(self.__btn_import_excel, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Close Selected Accounts Button")
    def click_close_selected_accounts(self, pause: int = 0):
        self.click().set_locator(self.__btn_close_selected_accounts, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Confirm Yes Button")
    def click_confirm_yes(self, pause: int = 2):
        self.click().set_locator(self.__btn_confirm_yes, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Confirm No Button")
    def click_confirm_no(self, pause: int = 5):
        self.click().set_locator(self.__btn_confirm_no, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Multi Update Button")
    def click_multi_update(self, pause: int = 0):
        self.click().set_locator(self.__btn_multi_update, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Multi Update Details Button")
    def click_multi_update_details(self, pause: int = 0):
        self.click().set_locator(self.__btn_multi_update_details, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Create Events Button")
    def click_create_events(self, pause: int = 0):
        self.click().set_locator(self.__btn_create_events, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Manage Documentation only Bookings Button")
    def click_manage_doc_only_bookings(self, pause: int = 0):
        self.click().set_locator(self.__btn_manage_doc_only_bookings, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Copy Booking Button")
    def click_copy_booking(self, pause: int = 0):
        self.click().set_locator(self.__btn_copy_booking, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Expire & Copy Button")
    def click_expire_and_copy(self, pause: int = 0):
        self.click().set_locator(self.__btn_expire_and_copy, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Export Changes Button")
    def click_export_changes(self, pause: int = 0):
        self.click().set_locator(self.__btn_export_changes, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Tariff Export Button")
    def click_tariff_export(self, pause: int = 0):
        self.click().set_locator(self.__btn_tariff_export, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Change History Button")
    def click_change_history(self, pause: int = 0):
        self.click().set_locator(self.__btn_change_history, self._name).single_click().pause(pause)
        return self

    @allure.step("Click VIN Insert Button")
    def click_vin_insert(self, pause: int = 0):
        self.click().set_locator(self.__btn_vin_insert, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Update VIN Button")
    def click_update_vin(self, pause: int = 0):
        self.click().set_locator(self.__btn_update_vin, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Rebooking Button")
    def click_rebooking(self, pause: int = 0):
        self.click().set_locator(self.__btn_rebook, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Godsnumber Button")
    def click_godsnumber(self, pause: int = 0):
        self.click().set_locator(self.__btn_godsnumber, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Calculate Cut-Off Button")
    def click_calculate_cut_off(self, pause: int = 0):
        self.click().set_locator(self.__btn_calculate_cut_off, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Create new Voyage from template Button")
    def click_create_new_voyage_from_template(self, pause: int = 0):
        self.click().set_locator(self.__btn_create_new_voyage_from_template, self._name).single_click().pause(pause)
        return self

    @allure.step("Click Create new Voyage from selected voyage Button")
    def click_create_new_voyage_from_selected_voyage(self, pause: int = 0):
        self.click().set_locator(self.__btn_create_new_voyage_from_selected_voyage, self._name).single_click().pause(pause)
        return self
