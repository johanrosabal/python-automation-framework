from selenium.webdriver.common.by import By

from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.modals.ModalComponent import ModalComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('OtherDetailsPage')


class OtherDetailsComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the OtherDetailsPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Locator definitions
        self._tab_other_details = (By.XPATH, "//div[@data-label='Other Details']", "Other Details [Tab]")
        # Root Locator definitions
        self._xpath_booking_party = "//h6[text()='Booking Party Details']/../.."
        self._xpath_bill_to_party = "//h6[text()='Bill To Party Details']/../.."
        self._xpath_customer_details = "//h6[text()='Customer Details']/../.."
        self._xpath_cargo_release_details = "//h6[text()='Cargo Release Details']/../.."
        self._xpath_consignee_details = "//h6[text()='Consignee Details']/../.."
        self._xpath_other_party_details = "//h6[text()='Other Party Details']/../.."
        self._xpath_booking_remarks = "//h6[text()='Booking Remarks']/../.."
        self._xpath_vsa_booking_ref_numbers = "//h6[text()='VSA Booking Ref Numbers']/../.."
        # Sub-Components
        self.modal = ModalComponent.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def set_booking_data(self, data=None):
        """ Set Booking Data and share with all fill methods """
        self.booking_data = data
        return self

    def load_tab(self):
        self.click().set_locator(self._tab_other_details, self._name).single_click()
        return self

    # Booking Party Details --------------------------------------------------------------------------------------------
    def get_booking_party_details_account(self):
        locator = (By.XPATH, f"{self._xpath_booking_party}//span[contains(text(),'Account')]/following-sibling::span[1]", "Booking Party Details: Account [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_booking_party_details_address(self):
        locator = (By.XPATH, f"{self._xpath_booking_party}//span[contains(text(),'Address')]/..", "Booking Party Details: Address [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[-1]
        return address

    def get_booking_party_details_contact_name(self):
        locator = (By.XPATH, f"{self._xpath_booking_party}//span[contains(text(),'Contact Name')]/..", "Booking Party Details: Contact Name [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[0]
        return address

    def get_booking_party_details_phone_number(self):
        locator = (By.XPATH, f"{self._xpath_booking_party}//span[contains(text(),'Phone Number:')]/..", "Booking Party Details: Phone Number [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        phone = lines[1]
        return phone

    def get_booking_party_details_email(self):
        locator = (By.XPATH, f"{self._xpath_booking_party}//span[contains(text(),'Email ID:')]/..", "Booking Party Details: Email ID [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        email = lines[2]
        return email

    # Bill To Party Details --------------------------------------------------------------------------------------------
    def get_bill_to_party_details_account(self):
        locator = (By.XPATH, f"{self._xpath_bill_to_party}//span[contains(text(),'Account')]/following-sibling::span[1]", "Bill To Party Details: Account [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_bill_to_party_details_address(self):
        locator = (By.XPATH, f"{self._xpath_bill_to_party}//span[contains(text(),'Address')]/..", "Bill To Party Details: Address [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[-1]
        return address

    def get_bill_to_party_details_contact_name(self):
        locator = (By.XPATH, f"{self._xpath_bill_to_party}//span[contains(text(),'Contact Name')]/..", "Booking Party Details: Contact Name [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[0]
        return address

    def get_bill_to_party_details_phone_number(self):
        locator = (By.XPATH, f"{self._xpath_bill_to_party}//span[contains(text(),'Phone Number:')]/..", "Booking Party Details: Phone Number [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        phone = lines[1]
        return phone

    def get_bill_to_party_details_email(self):
        locator = (By.XPATH, f"{self._xpath_bill_to_party}//span[contains(text(),'Email ID:')]/..", "Booking Party Details: Email ID [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        email = lines[2]
        return email

    # Customer Details Details -----------------------------------------------------------------------------------------
    def get_customer_details_account(self):
        locator = (By.XPATH, f"{self._xpath_customer_details}//span[contains(text(),'Account')]/following-sibling::span[1]", "Customer Details: Account [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def get_customer_details_address(self):
        locator = (By.XPATH, f"{self._xpath_customer_details}//span[contains(text(),'Address')]/..", "Bill To Party Details: Address [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[-1]
        return address

    def get_customer_details_contract_name(self):
        locator = (By.XPATH, f"{self._xpath_customer_details}//span[contains(text(),'Contract')]/..", "Customer Details: Contract [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[0]
        return address

    def get_customer_details_contact_name(self):
        locator = (By.XPATH, f"{self._xpath_customer_details}//span[contains(text(),'Contact Name')]/..", "Customer Details: Contact Name [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        address = lines[0]
        return address

    def get_customer_details_phone_number(self):
        locator = (By.XPATH, f"{self._xpath_customer_details}//span[contains(text(),'Phone Number:')]/..", "Customer Details: Phone Number [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        phone = lines[1]
        return phone

    def get_customer_details_email(self):
        locator = (By.XPATH, f"{self._xpath_customer_details}//span[contains(text(),'Email ID:')]/..", "Customer Details: Email ID [Text]")
        lines = self.get_text().set_locator(locator, self._name).by_text().split("\n")
        email = lines[2]
        return email

    def select_customer_details_payment_terms(self, option):
        locator = (By.XPATH, f"{self._xpath_customer_details}//label[contains(text(),'Payment Terms')]/..//select")
        self.dropdown().set_locator(locator, self._name).by_text(option)
        return self

    # Cargo Release Details --------------------------------------------------------------------------------------------

    def select_cargo_release_details_customs_clearence_location(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_cargo_release_details}//label[contains(text(),'Customs Clearence Location')]", "Cargo Release Details: Customs Clearence Location [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[contains(text(),'{option_location}')]/..", f"Cargo Release Details: : Customs Clearence Location List Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_cargo_release_details_customs_clearence_sublocation(self, option_sublocation):
        locator = (By.XPATH, f"{self._xpath_cargo_release_details}//span[contains(text(),'Customs Clearence Sublocation')]/../../..//select", "Cargo Release Details: Customs Clearence Sublocation [Select Dropdown]")
        self.dropdown().set_locator(locator, self._name).by_text(option_sublocation).pause(1)
        return self

    def select_cargo_release_details_cargo_release_location(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_cargo_release_details}//label[contains(text(),'Cargo Release Location')]", "Cargo Release Details: Cargo Release Location [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[contains(text(),'{option_location}')]/..", f"Cargo Release Details: : Cargo Release Location List Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_cargo_release_details_cargo_release_sublocation(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_cargo_release_details}//label[contains(text(),'Cargo Release Sublocation')]", "Cargo Release Details: Cargo Release Sublocation [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[contains(text(),'{option_location}')]/..", f"Cargo Release Details: : Cargo Release Sublocation List Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    # Shipper Details --------------------------------------------------------------------------------------------------
    # These fields are disable on UI

    # Consignee Details ------------------------------------------------------------------------------------------------
    def click_checkbox_consignee_details_same_as_booking_party(self):
        locator = (By.XPATH, f"{self._xpath_consignee_details}//label/span[contains(text(),'Same as Booking Party')]/../..//input[@type='checkbox']/..//span[@part='indicator']", "Consignee Details: Same as Booking Party [Checkbox]")
        self.scroll().set_locator(locator).to_element(pixels=-100)
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_checkbox_consignee_details_same_as_customer(self):
        locator = (By.XPATH, f"{self._xpath_consignee_details}//label/span[contains(text(),'Same as Customer')]/../..//input[@type='checkbox']/..//span[@part='indicator']", "Consignee Details: Same as Customer [Checkbox]")
        self.scroll().set_locator(locator).to_element(pixels=-100)
        self.click().set_locator(locator, self._name).single_click()
        return self

    def select_consignee_details_consignee_account(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_consignee_details}//label[contains(text(),'Consignee Account')]/../..//input[@type='search']", "Consignee Details: Consignee Account [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[text()='{option_location}']/..", f"Consignee Details: Consignee Account List Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_consignee_details_address(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_consignee_details}/following-sibling::div[1]//label[contains(text(),'Address')]/../..//input[@type='search']", "Consignee Details: Address [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[text()='{option_location}']/..", f"Consignee Details: Address List Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_consignee_details_contact_name(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_consignee_details}/following-sibling::div[1]//label[contains(text(),'Contact Name')]/../..//input[@type='search']", "Consignee Details: Contact Name [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[text()='{option_location}']/..", f"Consignee Details: Contact Name Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_consignee_details_phone_no(self, option_location):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_consignee_details}/following-sibling::div[1]//label[contains(text(),'Phone No.')]/../..//input[@type='text']", "Consignee Details: Phone No. [Search Dropdown]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(option_location).pause(1)
        # After List Values will be displayed, search Text Option on it and click on it
        list_search_values = (By.XPATH, f"{self._xpath_cargo_release_details}//div[@id='lookup']//li//span[text()='{option_location}']/..", f"Consignee Details: Phone No. Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def enter_consignee_details_email_id(self, email):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_consignee_details}/following-sibling::div[3]//label[contains(text(),'Email ID')]/../..//input[@type='text']", "Consignee Details: Email ID [Input]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(email).pause(1)
        return self

    def enter_consignee_details_reference_number(self, email):
        # First Enter text on Input Box
        input_search_locator = (By.XPATH, f"{self._xpath_consignee_details}/following-sibling::div[3]//label[contains(text(),'Reference Number')]/../..//input[@type='text']", "Consignee Details: Email ID [Input]")
        self.send_keys().set_locator(input_search_locator, self._name).set_text(email).pause(1)
        return self

    def fill_consignee_details(self, booking_data=None):
        # Set Up Booking Data if Argument is None
        if self.booking_data:
            booking_data = self.booking_data

        consignee_details = booking_data['tests']['data']['booking']['other_details']['consignee_details']

        if consignee_details['same_as_booking_party']:
            self.click_checkbox_consignee_details_same_as_booking_party()

        if consignee_details['same_as_customer']:
            self.click_checkbox_consignee_details_same_as_customer()

        if consignee_details['shipper_account'] != "":
            self.select_consignee_details_consignee_account(consignee_details['shipper_account'])

        if consignee_details['address'] != "":
            self.select_consignee_details_address(consignee_details['address'])

        if consignee_details['contact_name'] != "":
            self.select_consignee_details_contact_name(consignee_details['contact_name'])

        if consignee_details['phone_number'] != "":
            self.select_consignee_details_phone_no(consignee_details['phone_number'])

        if consignee_details['email_id'] != "":
            self.enter_consignee_details_email_id(consignee_details['email_id'])

        if consignee_details['reference_number'] != "":
            self.enter_consignee_details_reference_number(consignee_details['reference_number'])

        return self

    # Other Party Details ----------------------------------------------------------------------------------------------
    # These fields are disable by default
    def select_other_party_details_party_type(self, index, option):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label/span[text()='Party Type']/../..//select)[{str(index)}]", f"Other Party Details: Party Type [{str(index)}][Select]")
        self.dropdown().set_locator(locator, self._name).by_text(option)
        return self

    def click_checkbox_other_party_details_same_as_customer(self, index):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label/span[text()='Same as Customer']/../..//input[@type='checkbox']/..//span[@part='indicator'])[{str(index)}]", f"Other Party Details: Same as Customer [{str(index)}][Checkbox]")
        self.click().set_locator(locator, self._name).single_click().pause(1)
        return self

    def click_checkbox_other_party_details_same_as_booking_party(self, index):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label/span[text()='Same as Booking Party']/../..//input[@type='checkbox']/..//span[@part='indicator'])[{str(index)}]", f"Other Party Details: Same as Booking Party [{str(index)}][Checkbox]")
        self.click().set_locator(locator, self._name).single_click().pause(1)
        return self

    def click_checkbox_other_party_details_same_as_shipper(self, index):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label/span[text()='Same as Shipper']/../..//input[@type='checkbox']/..//span[@part='indicator'])[{str(index)}]", f"Other Party Details: Same as Shipper [{str(index)}][Checkbox]")
        self.click().set_locator(locator, self._name).single_click().pause(1)
        return self

    def select_other_party_details_account(self, index, option_location):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label[text()='Account']/../..//input[@type='search'])[{str(index)}]", f"Other Party Details: Account [{str(index)}][Select]")
        self.send_keys().set_locator(locator, self._name).set_text(option_location).pause(1)

        list_search_values = (By.XPATH, f"{self._xpath_other_party_details}//div[@id='lookup']//li//span[text()='{option_location}']/..", f"Other Party Details: Account Item {option_location} [Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_other_party_details_contact_name(self, index, option_location):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label[text()='Contact Name']/../..//input[@type='search'])[{str(index)}]", f"Other Party Details: Contact Name [{str(index)}][Select]")
        self.send_keys().set_locator(locator, self._name).set_text(option_location).pause(1)

        list_search_values = (By.XPATH, f"{self._xpath_other_party_details}//div[@id='lookup']//li//span[text()='{option_location}']/..", f"Other Party Details: Contact Name Item {option_location} [{str(index)}][Click]")
        self.click().set_locator(list_search_values, self._name).highlight(1).single_click().pause(1)
        return self

    def select_other_party_details_phone_no(self, index, text):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label[text()='Phone No.']/../..//input[@type='text'])[{str(index)}]", f"Other Party Details: Contact Name [{str(index)}][Select]")
        self.send_keys().set_locator(locator, self._name).set_text(text).pause(1)
        return self

    def enter_other_party_details_email_id(self, index, text):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label[text()='Email ID']/../..//input[@type='text'])[{str(index)}]", f"Other Party Details: Email ID [{str(index)}][Select]")
        self.send_keys().set_locator(locator, self._name).set_text(text).pause(1)
        return self

    def enter_other_party_details_reference_number(self, index, text):
        locator = (By.XPATH, f"({self._xpath_other_party_details}//label[text()='Reference Number']/../..//input[@type='text'])[[{str(index)}]]", f"Other Party Details: Email ID [{str(index)}][Select]")
        self.send_keys().set_locator(locator, self._name).set_text(text).pause(1)
        return self

    def click_other_party_details_add_more(self):
        locator = (By.XPATH, f"{self._xpath_other_party_details}//button[@title='Add More +']", "Other Party Details: Add More+ [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def click_other_party_details_remove(self, index):
        locator = (By.XPATH, f"{self._xpath_other_party_details}//a[text()='- Remove'])[{str(index)}]", f"Other Party Details: Remove {index} [Select]")
        self.click().set_locator(locator, self._name).single_click().pause(1)
        return self

    # Booking Remarks --------------------------------------------------------------------------------------------------
    def enter_booking_remarks_remark(self, booking_data=None):
        # Set Up Booking Data if Argument is None
        if self.booking_data:
            booking_data = self.booking_data

        items = booking_data['tests']['data']['booking']['other_details']['booking_remarks']

        for index, item in enumerate(items):

            xpath_index = index + 1

            # Click on ADD Remarks
            if index > 0:
                self.click_booking_remarks_add_more()

            locator = (By.XPATH, f"{self._xpath_booking_remarks}//label[text()='Remark {xpath_index}']/../..//input[@type='text']", f"Booking Remarks [{xpath_index}][Input]")
            self.send_keys().set_locator(locator, self._name).set_text(item)
        return self

    def click_booking_remarks_remove(self, index):
        locator = (By.XPATH, f"{self._xpath_booking_remarks}//a[text()='- Remove'])[{str(index)}]", f"Other Party Details: Remove {index} [Select]")
        self.click().set_locator(locator, self._name).single_click().pause(1)
        return self

    def click_booking_remarks_add_more(self):
        locator = (By.XPATH, f"{self._xpath_booking_remarks}//button[@title='Add More +']", "Booking Remarks: Add More+ [Button]")
        self.click().set_locator(locator, self._name).single_click()
        return self
    # ------------------------------------------------------------------------------------------------------------------

    def enter_itn_number(self, booking_data=None):
        # Set Up Booking Data if Argument is None
        if self.booking_data:
            booking_data = self.booking_data

        items = booking_data['tests']['data']['booking']['other_details']['ITN_Number']

        add_itn_locator = (By.XPATH, "//span[text()='+ Add ITN Numbers']/..", "[Add ITN Numbers]")

        for index, item in enumerate(items):

            xpath_index = index+1

            # Click on ADD ITN Numbers
            if index > 0:
                self.click().set_locator(add_itn_locator).single_click().pause(1)

            locator = (By.XPATH, f"(//label[contains(text(),'ITN Number')]/..//input[@type='text'])[{str(xpath_index)}]", f"ITN Number [{item}][{str(xpath_index)}][Input]")
            self.send_keys().set_locator(locator, self._name).set_text(item)

        return self

    def click_itn_Number_remove(self, index, text):
        locator = (By.XPATH, f"(//label[contains(text(),'ITN Number')]/span/i)[{str(index)}]", f"ITN Number Remove [{str(index)}][Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def select_exemption_clause(self, option):
        locator = (By.XPATH, f"(//label[contains(text(),'Exemption Clause')]/..//select)", f"Exemption Clause [Select]")
        self.dropdown().set_locator(locator, self._name).by_text(option)
        return self

    def enter_post_departure_date(self, index, text):
        locator = (By.XPATH, f"//label[contains(text(),'Postdeparture Date')]/..//input[@type='text']", f"Postdeparture Date [{str(index)}][Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def select_booking_pending_reasons(self, option):
        locator_input = (By.XPATH, f"//label[contains(text(),'Booking Pending Reasons')]/..//input[@type='text']", f"Booking Pending Reasons [Select Multiple]")
        self.click().set_locator(locator_input, self._name).single_click().pause(1)
        locator_option = (By.XPATH, f"//span[contains(@class,'checkboxGroup')]//span[contains(text(),'{option}')]/..", f"Booking Pending Reasons [Check Option]")
        self.click().set_locator(locator_option, self._name).single_click().pause(1)
        return self

    def remove_booking_pending_reason(self, option):
        locator_input = (By.XPATH, f"//lightning-pill//span[contains(text(),'{option}')]/following-sibling::lightning-button-icon[1]/button", f"Remove Booking Pending Reasons [Select Multiple]")
        self.click().set_locator(locator_input, self._name).single_click().pause(1)
        return self

    # VSA Booking Ref Numbers --------------------------------------------------------------------------------------------------
    def enter_vsa_booking_ref_numbers_dry(self, text):
        locator = (By.XPATH, f"{self._xpath_vsa_booking_ref_numbers}//label[contains(text(),'Dry')]/..//input[@type='text']", f"VSA Booking Ref Numbers: Dry [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def enter_vsa_booking_ref_numbers_reefer(self, text):
        locator = (By.XPATH, f"{self._xpath_vsa_booking_ref_numbers}//label[contains(text(),'Reefer')]/..//input[@type='text']", f"VSA Booking Ref Numbers: Reefer [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def enter_vsa_booking_ref_numbers_hazardous(self, text):
        locator = (By.XPATH, f"{self._xpath_vsa_booking_ref_numbers}//label[contains(text(),'Hazardous')]/..//input[@type='text']", f"VSA Booking Ref Numbers: Hazardous [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def enter_vsa_booking_ref_numbers_vehicle(self, text):
        locator = (By.XPATH, f"{self._xpath_vsa_booking_ref_numbers}//label[contains(text(),'Vehicle')]/..//input[@type='text']", f"VSA Booking Ref Numbers: Vehicle [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def enter_vsa_booking_ref_numbers_cargo_not_in_a_container(self, text):
        locator = (By.XPATH, f"{self._xpath_vsa_booking_ref_numbers}//label[contains(text(),'Cargo Not in a Container')]/..//input[@type='text']", f"VSA Booking Ref Numbers: Cargo Not in a Container [Input]")
        self.send_keys().set_locator(locator, self._name).set_text(text)
        return self

    def fill_vsa_booking_ref_numbers(self, dry, reefer, hazardous, vehicle, cargo_not_in_a_container):
        self.enter_vsa_booking_ref_numbers_dry(dry)
        self.enter_vsa_booking_ref_numbers_reefer(reefer)
        self.enter_vsa_booking_ref_numbers_hazardous(hazardous)
        self.enter_vsa_booking_ref_numbers_vehicle(vehicle)
        self.enter_vsa_booking_ref_numbers_cargo_not_in_a_container(cargo_not_in_a_container)
        return self

    def close_modal_hazardous_validation(self, booking_data=None):
        locator = (By.XPATH, f"//div[contains(@class, 'modal__content') or contains(@class, 'modalContent')]//span[contains(text(),'Hazardous validation')] | //div[contains(@class, 'modal__content') or contains(@class, 'modalContent')]//span/b[contains(.,'Hazardous validaton')]", "Hazardous Modal Validation")
        # If Modal with Hazardous is Present click on Close
        if self.element().is_present(locator, timeout=5):
            proceed_btn = (By.XPATH, "//div[contains(@class, 'modal__content') or contains(@class, 'modalContent')]//button[@title='PROCEED']", "Proceed [ Button]")
            if self.element().is_present(proceed_btn, timeout=2):
                self.click().set_locator(proceed_btn).single_click()
                logger.info("Proceed button clicked on Modal Hazardous Validation")
            else:
                self.modal.click_close()

        return self
