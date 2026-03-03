import allure
from Cython.Compiler.Naming import self_cname
from selenium.webdriver.common.by import By
from core.asserts.AssertCollector import AssertCollector
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage

logger = setup_logger('RequestAccessorials')


class RequestAccessorialsPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the FreightDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/list"

        self._form = "(//div[contains(@id, 'request-accessorials-dialog')])"
        # Locator definitions
        self._input_hour = (By.XPATH, f"{self._form}//input[contains(@formcontrolname, 'hours')]", "Hour data [Input]")
        self._input_rate = (By.XPATH, f"{self._form}//input[contains(@formcontrolname, 'totalCharge')]", "Rate data [Input]")
        self._input_hour_rate = (By.XPATH, f"{self._form}//input[contains(@formcontrolname, 'hourlyRate')]", "Hour rate data [Input]")
        self._input_flat_rate_rate = (By.XPATH, f"{self._form}//input[contains(@formcontrolname, 'totalCharge')]", "Flat rate data [Input]")
        self._input_comments = (By.XPATH, f"{self._form}//textarea[contains(@formcontrolname, 'comment')]", "Comment data [Input]")
        self._dropdown_equipment=(By.XPATH, f"{self._form}//mat-select[@placeholder='Select Accessorial']", "Equipment dropdown [Input]")
        self._click_accessorials = (By.XPATH, "//button[span[contains(text(), 'Request Accessorials')]]", "Accessorials data [Button]")
        self._click_per_hour = (By.XPATH, "//label[contains(text(), 'Per Hour')]", "Per hour data [Button]")
        self._click_flat_rate = (By.XPATH, "//label[contains(text(), 'Flat Rate')]", "Flat Rate data [Button]")
        self._click_submit = (By.XPATH, "//*[@id='request-accessorials-dialog']/div/div/form/div[2]/button", "Submit [Button]")
        self._click_popup_ok = (By.XPATH, "//button[contains(@class, 'iq-btn') and span[normalize-space(text())='OK']]", "PopUp ok [Button]")
        self._button_upload=(By.XPATH, "//div[@class='col-sm-8 text-sm-end']//span[contains(text(), 'Upload Document')]", "Upload doc [Button]")
        self._click_finance_details=(By.XPATH, "//a[text()='Finance Details']", "Finance details tab [Button]")
        self._all_loads=(By.XPATH, "//div[contains(@class,'row')]//div[contains(@class,'load-list')]","Load list [Select]")

        #UPLOAD MODAL
        self._upload_modal=(By.XPATH, "//*[@id='request-accessorials-dialog']//div[@class='modal-content']", "Modal [Select]")
        self._button_add_file = (By.XPATH, "//div[@id='mCSB_10_container']//label/span/a", "Add file- modal [Button]")
        self._input_add_file = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//input[@type='file']", "Input file- modal [Input]")
        self._button_upload_file_modal = (By.XPATH, "//span[text()='Upload File']", "Upload file- modal [Button]")
        self._button_delete_file=(By.XPATH,"//*[@id='mCSB_5_container']//button", "Delete file- modal [Button]")
        self._input_description_modal = (By.XPATH, "//input[contains(@placeholder, 'Description')]", "Input description- modal [Input]")
        self._button_delete_yes = (By.XPATH, "//span[text()='Yes, Delete']", "Delete file- modal-verification [Button]")
        self._button_cancel_no = (By.XPATH, "//span[text()='No, Cancel']", "Delete avoid file- modal [Button]")

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = RequestAccessorialsPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def _enter_hour(self, hour):
        self.send_keys().set_locator(self._input_hour, self._name).clear().set_text(hour)
        return self

    def _enter_hour_rate(self, hour_rate):
        self.send_keys().set_locator(self._input_hour_rate, self._name).clear().set_text(hour_rate)
        return self

    def _enter_rate(self, rate):
        self.send_keys().set_locator(self._input_rate, self._name).clear().set_text(rate)
        return self

    def _enter_comments(self, comments):
        self.send_keys().set_locator(self._input_comments, self._name).clear().set_text(comments)
        return self


    def _enter_flat_rate_rate(self, hour_rate):
        self.send_keys().set_locator(self._input_flat_rate_rate, self._name).clear().set_text(hour_rate)
        return self

    def _select_equipment(self, dropdown):
        self.click().set_locator(self._dropdown_equipment).single_click()
        locator = (By.XPATH, f"//div[contains(@class, 'cdk-overlay-pane')]//span[contains(text(), '{dropdown}')]")
        self.click().set_locator(locator).single_click()

    def enter_accessorials_items(self, hour, hour_rate, comments,dropdown):
        self._enter_hour(hour)
        self._enter_hour_rate(hour_rate)
        self._enter_comments(comments)
        self._select_equipment(dropdown)
        return self


    def enter_accessorials_items_flat(self,rates,comments,dropdown):
        self._enter_flat_rate_rate(rates)
        self._enter_comments(comments)
        self._select_equipment(dropdown)
        return self

    @allure.step("Click Accessorials")
    def click_generate_accessorial(self):
        self.click().set_locator(self._click_accessorials, self._name).single_click().pause(2)
        return self

    @allure.step("Click ok")
    def click_popup_ok(self):
        self.click().set_locator(self._click_popup_ok, self._name).single_click().pause(2)
        return self

    @allure.step("Click Submit")
    def click_submit(self):
        self.click().set_locator(self._click_submit, self._name).single_click().pause(2)
        return self

    @allure.step("Click Perhour")
    def click_per_hour(self):
        self.click().set_locator(self._click_per_hour, self._name).single_click().pause(2)
        return self

    @allure.step("Click Flat")
    def click_flat_rate(self):
        self.click().set_locator(self._click_flat_rate, self._name).single_click().pause(2)
        return self

    @allure.step("Click Flat")
    def click_flat_rate(self):
        self.click().set_locator(self._click_flat_rate, self._name).single_click().pause(2)
        return self

    @allure.step("Click upload")
    def click_upload(self):
        self.click().set_locator(self._button_upload, self._name).single_click().pause(60)
        return self

    @allure.step("Click ok")
    def click_popup_ok(self):
        self.click().set_locator(self._click_popup_ok, self._name).single_click().pause(2)
        return self

    @allure.step("Click ok")
    def click_finance_details(self):
        self.click().set_locator(self._click_finance_details, self._name).single_click().pause(2)
        return self


    def get_all_loads(self, index: int):
        xpath = f"({self._all_loads}//span[@class='text-primary fw-medium fnt-12 d-block'])[{str(index)}]"
        locator = (By.XPATH, xpath, "All loads")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def get_text_results(self, expected_text= "Sorry, we couldn't find any results."):
        result_elements1 = self.driver.find_elements(By.XPATH,)

        return any(expected_text in el.text for el in result_elements1)

    def get_text_results1(self, expected_text=" No records found "):
        result_elements1 = self.driver.find_elements(By.XPATH,'//*[@id="cdk-drop-list-0"]/tbody/tr/td')

        return any(expected_text in el.text for el in result_elements1)

    def click_add_file(self, file_name: str, description: str):

        # Wait For Modal Should be visible
        self.element().wait_for_element(self.driver, self._upload_modal)

        # Display Temporarily Input Chosen File
        self.element().set_css_property(self._input_add_file, "display: block;")

        # Send Path File
        # self.click().set_locator(self._button_add_file, self._name).single_click().pause(2) # Avoid to Click the "Add File" to not display the dialog box for search the file
        self.upload_file().set_locator(self._input_add_file, self._name).set_file_name(file_name).upload().pause(1)

        # Hidden Temporarily Input Chosen File
        self.element().set_css_property(self._input_add_file, "display: none;")

        # Add some Description to the upload File
        self.send_keys().set_locator(self._input_description_modal, self._name).clear().set_text(description)

        # Click to Upload Current File
        self.click().set_locator(self._button_upload_file_modal, self._name).single_click().pause()


