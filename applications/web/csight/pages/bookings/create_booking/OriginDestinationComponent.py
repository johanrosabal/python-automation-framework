from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from applications.web.csight.components.loadings.Loadings import Loadings
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('OriginDestinationPage')


class OriginDestinationComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the OriginDestinationPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Locators
        self._tab_origin_destination = (By.XPATH, "//div[@data-label='Origin Destination']", "Origin-Destination Tab")
        # Booking Party -----------------------------------------------------------------------------------------------
        self._xpath_booking_account = "//label[contains(text(),'Booking Account')]"
        self._xpath_booking_address = "(//label[contains(text(),'Address')])[1]"
        self._xpath_booking_party_contact_name = "(//label[contains(text(),'Contact Name')])[1]"
        self._xpath_modal = "(//div[contains(@class,'modal__content')])[1]"

        self._input_booking_party_phone_number = (By.XPATH, "(//label[contains(text(),'Phone No.')]/..//input)[1]", "Booking Party: Phone No. Input")
        self._input_booking_party_email_id = (By.XPATH, "(//label[contains(text(),'Email ID')]/..//input)[1]", "Booking Party: Email ID Input")
        # Bill to Party -----------------------------------------------------------------------------------------------
        self._checkbox_bill_to_party_same_as_booking_party = (By.XPATH, "(//span[contains(text(),'Same as Booking Party')]/../..//input)[1]/..//label", "Bill to Party: Same as Booking Party")

        self._xpath_bill_to_party_bill_to_account = "(//label[contains(text(),'Bill To Account')])[1]"
        self._xpath_bill_to_party_address = "(//label[contains(text(),'Address')])[2]"
        self._xpath_bill_to_party_contact_name = "(//label[contains(text(),'Contact Name')])[2]"
        self._xpath_bill_to_party_party_type = "//label/span[contains(text(),'Bill To Party Type :')]"

        self._input_bill_to_party_phone_number = (By.XPATH, "(//label[contains(text(),'Phone No.')]/..//input)[2]", "Booking Party: Phone No. Input")
        self._input_bill_to_party_email_id = (By.XPATH, "(//label[contains(text(),'Email ID')]/..//input)[2]", "Booking Party: Email ID Input")
        # Shipping Details  --------------------------------------------------------------------------------------------
        self._input_shipping_details_cargo_ready = (By.XPATH, "//label[contains(text(),'Cargo Ready')]/..//input", "Cargo Ready For Transport Input")
        # Account  Details  --------------------------------------------------------------------------------------------
        self._checkbox_account_details_same_as_booking_party = (By.XPATH, "(//span[contains(text(),'Same as Booking Party')]/../..//input)[2]/..//label/span[@part='indicator']", "Account Details: Same as Booking Party Radio")
        self._checkbox_account_details_same_as_bill_to_party = (By.XPATH, "(//span[contains(text(),'Same as Bill To Party')]/../..//input)[1]/..//label/span[@part='indicator']", "Account Details: Same as Bill to Party Radio")
        self._radio_account_details_search_using_account_name = (By.XPATH, "//span[contains(text(),'Search using Account Name')]/../../..//input", "Account Details: Search using Account Name CheckBox")
        self._radio_account_details_search_using_contract_number = (By.XPATH, "//span[contains(text(),'Search using Contract Number')]/../../..//input", "Account Details: Search using Contract Number CheckBox")

        self._xpath_account_details_account_name = "//label[contains(text(),'Account Name')]"
        self._xpath_account_details_address = "(//label[contains(text(),'Address')])[3]"
        self._xpath_account_details_contact_name = "(//label[contains(text(),'Contact Name')])[3]"

        self._input_account_details_phone = (By.XPATH, "(//label[contains(text(),'Phone')]/..//input)[3]", "Account Details: Phone Input")
        self._input_account_details_email = (By.XPATH, "(//label[contains(text(),'Email ID')]/..//input)[3]", "Account Details: Email Input")

        # PickUp Address  --------------------------------------------------------------------------------------------
        self._input_origin_details = "(//label[contains(text(),'Origin')])[1]"
        self._input_origin_country_cargo = "//label[contains(text(),'Origin Country of Cargo')]"
        self._input_origin_sublocation = "//label/span[contains(text(),'Origin Sublocation')]"
        self._input_destination_details = "//label[contains(text(),'Final Destination')]"
        self._checkbox_crowley_trucking_for_pickup = (By.XPATH, "//span[contains(text(),'Crowley Trucking for Pickup')]/../../label//span[@part='indicator']", "Account Details: Crowley Trucking for Pick Up Checkbox")
        self._checkbox_crowley_trucking_for_delivery = (By.XPATH, "//span[contains(text(),'Crowley Trucking for Delivery')]/../../label//span[@part='indicator']", "Account Details: Crowley Trucking for Delivery Checkbox")

        self._input_origin_pick_up_location_account_name = "(//label[contains(text(),'Pick Up Location - Account Name')])[1]"
        self._input_origin_pick_up_location_address = "(//label[contains(text(),'Address')])[4]"
        self._input_origin_pick_up_location_contact_name = "(//label[contains(text(),'Contact Name')])[4]"

        self._input_final_delivery_location_account_name = "(//label[contains(text(),'Final Delivery Location - Account Name')])[1]"
        self._input_final_delivery_location_address = "(//label[contains(text(),'Address')])[5]"
        self._input_final_delivery_location_contact_name = "(//label[contains(text(),'Contact Name')])[5]"

        # Sub-Components
        self.loadings = Loadings.get_instance()

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
        self.click().set_locator(self._tab_origin_destination, self._name).single_click()
        return self

    # Booking Party -----------------------------------------------------------------------------------------------

    def enter_booking_party_booking_account(self, booking_account):
        locator = (By.XPATH, f"{self._xpath_booking_account}/..//input", "Booking Party: Booking Account Input")
        self.send_keys().set_locator(locator, self._name).set_text(booking_account).pause(2)
        return self

    def select_booking_party_booking_account(self, booking_account):
        xpath_list = f"{self._xpath_booking_account}/../../../../../../../following-sibling::div"
        xpath_item = f"//ul//li//span[contains(text(),'{booking_account}')]"
        locator_item = (By.XPATH, f"{xpath_list}{xpath_item}", "Booking Party: Booking Account List")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def enter_booking_party_address(self, address):
        locator = (By.XPATH, f"{self._xpath_booking_address}/..//input", "Booking Party: Address Input")
        self.send_keys().set_locator(locator, self._name).set_text(address)
        return self

    def select_booking_party_address(self, address):
        xpath_item = f"{self._xpath_booking_address}/../../../../..//ul//li//span[contains(text(),'{address}')]"
        locator_item = (By.XPATH, f"{xpath_item}", "Booking Party: Booking Address List")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def get_booking_party_contact_name(self):
        locator = (By.XPATH, f"{self._xpath_booking_party_contact_name}/..//input", "Booking Party: Contact Input")
        return self.get_text().set_locator(locator).by_attribute("value")

    def enter_booking_party_contact_name(self, contact_name):
        locator = (By.XPATH, f"{self._xpath_booking_party_contact_name}/..//input", "Booking Party: Contact Input")
        self.send_keys().set_locator(locator, self._name).set_text(contact_name)
        self.loadings.is_not_visible_spinner()
        return self

    def select_booking_party_contact(self, contact_name):
        xpath_item = f"{self._xpath_booking_party_contact_name}/../../../../..//ul//li//span[contains(text(),'{contact_name}')]"
        locator_item = (By.XPATH, f"{xpath_item}", "Booking Party: Booking Contact List")
        self.click().set_locator(locator_item).highlight().single_click()
        locator = (By.XPATH, f"{self._xpath_booking_party_contact_name}/..//input", "Booking Party: Contact Input")
        self.send_keys().set_locator(locator, self._name).set_text_with_javascript(contact_name)
        return self

    def enter_booking_party_phone_number(self, phone):
        self.send_keys().set_locator(self._input_booking_party_phone_number, self._name).clear().highlight().set_text(phone).press_tab()
        return self

    def enter_booking_party_email_id(self, email):
        self.send_keys().set_locator(self._input_booking_party_email_id, self._name).clear().highlight().set_text(email).press_enter()
        return self

    def click_modal_replace_no(self):
        locator = (By.XPATH, f"{self._xpath_modal}//button[text()='NO']", "Modal Replace")
        if self.element().is_present(locator, 10):
            self.click().set_locator(locator).highlight().single_click()
        return self

    def click_modal_replace_replace(self):
        locator = (By.XPATH, f"{self._xpath_modal}//button[text()='REPLACE']", "Modal Replace")
        if self.element().is_present(locator, 10):
            self.click().set_locator(locator).highlight().single_click()
        return self

    def fill_booking_party(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        booking_party = booking_data['tests']['data']['booking']['origin_destination']['booking_party']
        # Input Search + List
        self.enter_booking_party_booking_account(booking_party["booking_account"])
        self.select_booking_party_booking_account(booking_party["booking_account"])
        # Input Search + List
        self.enter_booking_party_address(booking_party["address"])
        self.select_booking_party_address(booking_party["address"])

        # Input Search + List

        self.enter_booking_party_contact_name(booking_party["contact_name"])
        self.select_booking_party_contact(booking_party["contact_name"])

        contact_name = self.get_booking_party_contact_name()

        self.pause(1)
        if booking_party["replace_contact_info"]:
            # Input + Modal
            self.enter_booking_party_phone_number(booking_party["phone_number"])
            self.click_modal_replace_replace()

            # Input + Modal
            self.enter_booking_party_email_id(booking_party["email"])
            self.click_modal_replace_replace()
        return self

    # Bill to Party -----------------------------------------------------------------------------------------------

    def click_checkbox_bill_to_party_same_as_booking_party(self, same_as_booking_party):
        if same_as_booking_party:
            self.scroll().set_locator(self._checkbox_bill_to_party_same_as_booking_party).to_element(-100)
            self.click().set_locator(self._checkbox_bill_to_party_same_as_booking_party, self._name).highlight().single_click().pause(1)
        return self

    def enter_bill_to_party_bill_to_account(self, bill_to_account):
        locator = (By.XPATH, f"{self._xpath_bill_to_party_bill_to_account}/..//input", "Bill To Party: Bill to Account Input")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(bill_to_account).pause(2)
        return self

    def select_bill_to_party_bill_to_account(self, bill_to_account):
        xpath_list = f"{self._xpath_bill_to_party_bill_to_account}/../../../../../../../following-sibling::div"
        xpath_item = f"//ul//li//span[contains(text(),'{bill_to_account}')]"
        locator_item = (By.XPATH, f"{xpath_list}{xpath_item}", "Bill To Party: Bill to Account List")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def enter_bill_to_party_address(self, address):
        locator = (By.XPATH, f"{self._xpath_bill_to_party_address}/..//input", "Bill To Party: Bill to Account Input")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(address)
        return self

    def select_bill_to_party_address(self, address):
        xpath_list = f"{self._xpath_bill_to_party_address}/../../../../../../../following-sibling::div"
        xpath_item = f"//ul//li//span[contains(text(),'{address}')]"
        locator_list = (By.XPATH, f"{xpath_list}{xpath_item}", "Bill To Party: Address List")
        self.click().set_locator(locator_list).highlight().single_click()
        return self

    def enter_bill_to_party_contact_name(self, contact_name):
        locator = (By.XPATH, f"{self._xpath_bill_to_party_contact_name}/..//input", "Bill To Party: Contact name Input")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(contact_name)
        return self

    def select_bill_to_party_contact_name(self, contact_name):
        xpath_item = f"{self._xpath_bill_to_party_contact_name}/../../../../..//ul//li//span[contains(text(),'{contact_name}')]"
        locator_item = (By.XPATH, f"{xpath_item}", "Booking Party: Booking Contact List")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def select_bill_to_party_bill_to_party_type(self, party_type):
        locator = (By.XPATH, f"{self._xpath_bill_to_party_party_type}/../..//select")
        self.dropdown().set_locator(locator).highlight().by_text(party_type)
        return self

    def enter_bill_to_party_phone(self, phone):
        self.send_keys().set_locator(self._input_bill_to_party_phone_number, self._name).clear().highlight().set_text(phone).press_tab()
        return self

    def enter_bill_to_email_id(self, email):
        self.send_keys().set_locator(self._input_bill_to_party_email_id, self._name).clear().highlight().set_text(email).press_tab()
        return self

    def fill_bill_to_party(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data
        # Get JSON Data
        bill_to_party = booking_data['tests']['data']['booking']['origin_destination']['bill_to_party']

        if bill_to_party["same_as_booking_party"] is not True:
            # Input Search + List
            self.enter_bill_to_party_bill_to_account(bill_to_party["bill_to_account"])
            self.select_bill_to_party_bill_to_account(bill_to_party["bill_to_account"])
            # Input Search + List
            self.enter_bill_to_party_address(bill_to_party["address"])
            self.select_bill_to_party_address(bill_to_party["address"])
            # Input Search + List
            self.enter_bill_to_party_contact_name(bill_to_party["contact_name"])
            self.select_bill_to_party_contact_name(bill_to_party["contact_name"])

            if bill_to_party["replace_contact_info"]:
                # Input + Modal
                self.enter_bill_to_party_phone(bill_to_party["phone_number"])
                self.click_modal_replace_replace()
                # Input + Modal
                self.enter_bill_to_email_id(bill_to_party["email"])
                self.click_modal_replace_replace()
        else:
            # Checkbox
            self.click_checkbox_bill_to_party_same_as_booking_party(bill_to_party["same_as_booking_party"])

        # Dropdown
        self.select_bill_to_party_bill_to_party_type(bill_to_party["bill_to_party_type"])

        return self

    # Shipping Details  --------------------------------------------------------------------------------------------
    def enter_cargo_ready_for_transport(self, booking_data):
        date = booking_data['tests']['data']['booking']['origin_destination']['shipping_details']["cargo_ready_for_transport"]
        self.scroll().set_locator(self._input_shipping_details_cargo_ready).to_element(pixels=100)
        self.send_keys().set_locator(self._input_shipping_details_cargo_ready, self._name).highlight().set_text(date)
        self.pause(2)
        return self

    def fill_shipping_details(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        self.enter_cargo_ready_for_transport(booking_data=booking_data)
        return self

    # Account  Details  --------------------------------------------------------------------------------------------

    def click_checkbox_account_details_same_as_booking_party(self, value):
        if value:
            self.click().set_locator(self._checkbox_account_details_same_as_booking_party, self._name).highlight().single_click()
            self.loadings.is_not_visible_spinner()
        return self

    def click_checkbox_account_details_same_as_bill_to_party(self, value):
        if value:
            self.click().set_locator(self._checkbox_account_details_same_as_bill_to_party, self._name).highlight().single_click().pause(2)
            self.loadings.is_not_visible_spinner()
        return self

    def click_radio_account_details_search_using_account_name(self, value):
        if value:
            self.radio().set_locator(self._radio_account_details_search_using_account_name, self._name).highlight().set_value(value).pause(1)
        return self

    def click_radio_account_details_search_using_contract_number(self, value):
        if value:
            self.radio().set_locator(self._radio_account_details_search_using_contract_number, self._name).highlight().set_value(value).pause(1)
        return self

    def enter_account_details_account_name(self, account_name):
        locator = (By.XPATH, f"{self._xpath_account_details_account_name}/..//input", "Account Details: Account Name")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(account_name)
        return self

    def select_account_details_account_name(self, account_name):
        xpath_list = f"{self._xpath_account_details_account_name}/../../../../../../../following-sibling::div"
        xpath_item = f"//ul//li//span[contains(text(),'{account_name}')]"
        locator_item = (By.XPATH, f"{xpath_list}{xpath_item}", "Account Details: Account Name List")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def enter_account_details_address(self, address):
        locator = (By.XPATH, f"{self._xpath_account_details_address}/..//input", "Account Details: Address")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(address)
        return self

    def select_account_details_address(self, address):
        xpath_item = f"{self._xpath_account_details_address}/../../../../..//ul//li//span[contains(text(),'{address}')]"
        locator_item = (By.XPATH, f"{xpath_item}", "Account Details: Address")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def enter_account_details_contact_name(self, contact_name):
        locator = (By.XPATH, f"{self._xpath_account_details_contact_name}/..//input", "Account Details: Contact Name")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(contact_name)
        return self

    def select_account_details_contact_name(self, contact_name):
        xpath_item = f"{self._xpath_account_details_contact_name}/../../../../..//ul//li//span[contains(text(),'{contact_name}')]"
        locator_item = (By.XPATH, f"{xpath_item}", "Account Details: Contact Name")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def enter_account_details_enter_phone(self, phone):
        self.send_keys().set_locator(self._input_account_details_phone, self._name).clear().highlight().set_text(phone).press_tab()
        return self

    def enter_account_details_enter_email(self, email):
        self.send_keys().set_locator(self._input_account_details_email, self._name).clear().highlight().set_text(email).press_tab()
        return self

    def select_account_details_enter_contract_number(self, contract_number):
        locator = (By.XPATH, "//label/span[contains(text(),'Contract Number')]/../..//select", "Account Details: Contract Number")
        self.dropdown().set_locator(locator, self._name).highlight().by_text(contract_number)
        return self

    def fill_account_details(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data
        # Get JSON Data
        account_details = booking_data['tests']['data']['booking']['origin_destination']['account_details']

        if (account_details["same_as_booking_party"] or account_details["same_as_bill_to_party"]) is not True:
            # Input Search + List
            self.enter_account_details_account_name(account_details["account_name"])
            self.select_account_details_account_name(account_details["account_name"])
            # Input Search + List
            self.enter_account_details_address(account_details["address"])
            self.select_account_details_address(account_details["address"])
            # Input Search + List
            self.enter_account_details_contact_name(account_details["contact_name"])
            self.select_account_details_contact_name(account_details["contact_name"])

            if account_details["replace_contact_info"]:
                # Input + Modal
                self.enter_account_details_enter_phone(account_details["phone_number"])
                self.click_modal_replace_replace()
                # Input + Modal
                self.enter_account_details_enter_email(account_details["email"])
                self.click_modal_replace_replace()
        else:
            # Checkbox
            self.click_checkbox_account_details_same_as_booking_party(account_details["same_as_booking_party"])
            self.click_checkbox_account_details_same_as_bill_to_party(account_details["same_as_bill_to_party"])
            # Radio Buttons
            self.click_radio_account_details_search_using_account_name(account_details["search_using_account_name"])
            self.click_radio_account_details_search_using_contract_number(account_details["search_using_contract_number"])

        # Input
        self.select_account_details_enter_contract_number(account_details["contract_number"])
        return self

    def enter_origin_details(self, text):
        locator = (By.XPATH, f"{self._input_origin_details}/..//input", "Origin Details: Origin")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text)
        return self

    def select_origin_details(self, text):
        xpath_list = f"{self._input_origin_details}/../../../../../../../following-sibling::div"
        import re
        converted = re.sub(r" - | \(|\)", "\n", text)
        xpath_block_item = (By.XPATH, f"(//label[contains(text(),'Origin')])[1]/../../../../../..//ul//li//div[@class='block-view']", "Origin Block List")

        block = self.get_text().set_locator(xpath_block_item).highlight().by_text()
        # This condition handle the Text Argument to be equal to the Block Div That Contains the exact Match
        if converted.rstrip("\n").replace("\n", " ") == block.replace("\n", " "):
            self.click().set_locator(xpath_block_item).highlight().single_click()
        else:
            logger.error(f"Text Option not found {text}")
        return self

    def select_cleared_customs_at_first_us_port_entry(self, text: str = "No"):
        locator = (By.XPATH, f"//legend[text()='Cleared Customs at first US Port of Entry']/..//span[text()='{text}']", "Cleared Customs at first US Port of Entry [Select Radio Button]")
        if self.element().is_present(locator, timeout=2):
            self.click().set_locator(locator, self._name).single_click()
        return self

    def enter_origin_country_cargo(self, text):
        locator = (By.XPATH, f"{self._input_origin_country_cargo}/..//input", "Origin Details: Origin")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text)
        return self

    def select_origin_country_cargo(self, text):
        xpath_list = f"{self._input_origin_country_cargo}/../../../../../../../following-sibling::div"
        xpath_item = f"//ul//li//span//div[contains(text(),'{text}')]"
        locator_item = (By.XPATH, f"{xpath_list}{xpath_item}", "Origin Details: Origin Country Cargo List")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    def select_origin_sublocation(self, text):
        locator = (By.XPATH, f"{self._input_origin_sublocation}/../..//select", "Origin SubLocation")
        self.dropdown().set_locator(locator).by_text_contains(str(text))
        return self

    def enter_destination_details(self, text):
        locator = (By.XPATH, f"{self._input_destination_details}/..//input", "Destination Details: Final Destination")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text)
        return self

    def select_destination_details(self, text):
        xpath_list = f"{self._input_destination_details}/../../../../../../../following-sibling::div"
        import re
        converted = re.sub(r" - | \(|\)", "\n", text)
        xpath_block_item = (By.XPATH, f"{xpath_list}//ul//li//div[@class='block-view']", "Destination Block List")
        block = self.get_text().set_locator(xpath_block_item).highlight().by_text()
        # This condition handle the Text Argument to be equal to the Block Div That Contains the exact Match
        if converted.rstrip("\n").replace("\n"," ") == block.replace("\n"," "):
            self.click().set_locator(xpath_block_item).highlight().single_click()
        else:
            logger.error(f"Text Option not found {text}")
        return self

    def click_checkbox_crowley_trucking_for_pick_up(self, value):
        self.radio().set_locator(self._checkbox_crowley_trucking_for_pickup, self._name).highlight().set_value(value)
        return self

    def click_checkbox_crowley_trucking_for_delivery(self, value):
        self.radio().set_locator(self._checkbox_crowley_trucking_for_delivery, self._name).highlight().set_value(value)
        return self

    # Hidden Field
    def select_pre_carriage_mode(self, value):
        locator = (By.XPATH, "//label/span[contains(text(),'Pre-carriage Mode')]/../..//select", "Pre-carriage Mode [Select Options]")
        self.element().is_present(locator, timeout=5)
        self.dropdown().set_locator(locator).by_text(value)
        return self

    # Hidden Field
    def select_origin_drayage_options(self, value):
        locator = (By.XPATH, "(//label/span[contains(text(),'Drayage Options')]/../..//select)[1]", "Drayage Options [Select Options]")
        self.element().is_present(locator, timeout=5)
        self.dropdown().set_locator(locator).by_text(value)
        return self

    # Hidden Field
    def enter_origin_special_instruction(self, value):
        locator = (By.XPATH, "(//label[contains(text(),'Special Instructions')]/../..//input[@type='text'])[1]", "Origin: Special Instructions [Origin Input Field]")
        self.send_keys().set_locator(locator).set_text(value)
        return self

    # Hidden Field
    def enter_pick_up_location_account_name(self, text):
        locator = (By.XPATH, f"{self._input_origin_pick_up_location_account_name}/..//input", "Origin Details: Pick Up Location - Account Name")
        self.element().wait(locator=locator, timeout=10)
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text).pause(2)

        locator_item = (By.XPATH, f"{self._input_origin_pick_up_location_account_name}/../../../../../../../..//ul[@role='listbox']//span[text()='{text}']","")
        self.click().set_locator(locator_item).highlight().single_click()
        return self

    # Hidden Field
    def enter_pick_up_location_address(self, text, index=1):
        locator = (By.XPATH, f"(//div[contains(@class,'origin-stops-container')]/div[1]//label[text()='Address']/..//input)[{index}]", "Origin Details: Pick Up Location - Address")
        self.element().wait(locator=locator, timeout=10)
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text).pause(2)

        locator_option = (By.XPATH, f"(//div[contains(@class,'origin-stops-container')]/div[1]//label[text()='Address']/../../../../..//ul[@role='listbox']//span[text()='{text}'])[{index}]", "Origin ")
        self.click().set_locator(locator_option).highlight().single_click()
        return self

    # Hidden Field
    def enter_pick_up_location_contact(self, account_name=None,  text=None, index=1):
        locator_input = (By.XPATH, f"(//div[contains(@class,'origin-stops-container')]/div[1]//label[text()='Contact Name']/..//input)[{index}]", "Origin Details: Pick Up Location - Contact")
        self.element().wait(locator=locator_input, timeout=10)

        if account_name is None:
            self.send_keys().set_locator(locator_input, self._name).clear().highlight().set_text(text).pause(3)
        else:
            self.send_keys().set_locator(locator_input, self._name).clear().highlight().set_text(account_name).pause(3)

        locator_item = (By.XPATH, f"(//div[contains(@class,'origin-stops-container')]/div[1]//label[text()='Contact Name']/../../../../..//ul[@role='listbox']//span[text()='{text}'])[{index}]","")

        self.click().set_locator(locator_item).highlight().single_click().pause(2)

        # TODO Temporal Fix to UI Problem is deleting after selecting the contact name
        self.send_keys().set_locator(locator_input, self._name).highlight().set_text(text).pause(3)
        return self

    # Hidden Field
    def enter_pick_up_phone_number(self, text):
        locator = (By.XPATH, "(//label[contains(text(),'Phone No')])[4]/..//input", "Origin  - Pick Up Phone Number [Input Field]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def fill_origin_details(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data
        # Get JSON Data
        origin_details_pick_up_address = booking_data['tests']['data']['booking']['origin_destination']['origin_details_pick_up_address']

        # Input Search + List
        self.enter_origin_details(origin_details_pick_up_address["origin"])
        self.select_origin_details(origin_details_pick_up_address["origin"])

        self.loadings.is_not_visible_spinner()
        self.scroll().to_bottom()
        # Input Search + List
        self.enter_origin_country_cargo(origin_details_pick_up_address["origin_country_cargo"])
        self.select_origin_country_cargo(origin_details_pick_up_address["origin_country_cargo"])

        if origin_details_pick_up_address["cleared_customs_at_first_us_port_of_entry"] != "":
            self.select_cleared_customs_at_first_us_port_entry(text=origin_details_pick_up_address["cleared_customs_at_first_us_port_of_entry"])

        # Checkbox
        if origin_details_pick_up_address["crowley_trucking_pickup"]:
            self.click_checkbox_crowley_trucking_for_pick_up(origin_details_pick_up_address["crowley_trucking_pickup"])

        sub_loc = origin_details_pick_up_address["origin_sublocation"]
        if sub_loc not in ("--None--", ""):
            self.select_origin_sublocation(sub_loc)

        self.scroll().to_bottom()

        if origin_details_pick_up_address["pre_carriage_mode"] != "":
            self.select_pre_carriage_mode(origin_details_pick_up_address["pre_carriage_mode"])

        if origin_details_pick_up_address["drayage_options"] != "":
            self.select_origin_drayage_options(origin_details_pick_up_address["drayage_options"])

        if origin_details_pick_up_address["special_instructions"] != "":
            self.enter_origin_special_instruction( origin_details_pick_up_address["special_instructions"])

        if origin_details_pick_up_address["pick_up_location_account_name"] != "":
            self.enter_pick_up_location_account_name(origin_details_pick_up_address["pick_up_location_account_name"])

        if origin_details_pick_up_address["pick_up_location_address"] != "":
            self.enter_pick_up_location_address(
                text=origin_details_pick_up_address["pick_up_location_address"]
            )

        if origin_details_pick_up_address["pick_up_location_contact_name"] != "":
            self.enter_pick_up_location_contact(
                text=origin_details_pick_up_address["pick_up_location_contact_name"]
            )

        if origin_details_pick_up_address["pick_up_location_phone_number"] != "":
            self.enter_pick_up_phone_number(origin_details_pick_up_address["pick_up_location_phone_number"])

        return self

    def fill_stops(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data
        # Get JSON Data
        origin_details_pick_up_address = booking_data['tests']['data']['booking']['origin_destination']['origin_details_pick_up_address']

        if origin_details_pick_up_address["enable-stops"] and len(origin_details_pick_up_address["stops"]) > 0:
            # Add First All Stops Fields
            for stop in origin_details_pick_up_address["stops"]:
                logger.info(f"Added Intermediate [{stop}]")
                self.click_add_stop()

            self.pause(5)

            for stops_index, stop in enumerate(origin_details_pick_up_address["stops"]):
                s_index = stops_index + 1
                if stop["stop_location_account_name"] != "":
                    self.enter_stop_location_account_name(index=s_index, text=stop["stop_location_account_name"])
                if stop["stop_location_address"] != "":
                    self.enter_stop_address(index=s_index, text=stop["stop_location_address"])
                if stop["stop_location_contact_name"] != "":
                    self.enter_stop_contact_name(index=s_index, text=stop["stop_location_contact_name"])
                if stop["stop_location_phone_number"] != "":
                    self.enter_stop_phone_number(index=s_index, text=stop["stop_location_phone_number"])

            # if origin_details_pick_up_address["pick_up_location_contact_name"] != "":
            #     self.enter_pick_up_location_contact(
            #         account_name=origin_details_pick_up_address["pick_up_location_account_name"],
            #         text=origin_details_pick_up_address["pick_up_location_contact_name"]
            #     )

        return self

    def select_on_carriage_mode(self, value):
        locator = (By.XPATH, "//label/span[contains(text(),'On-carriage Mode')]/../..//select", "On-carriage Mode [Select Options]")
        self.element().is_present(locator, timeout=5)
        self.dropdown().set_locator(locator).by_text(value)
        return self

    # Hidden Field
    def select_destination_drayage_options(self, value):
        locator = (By.XPATH, "(//label/span[contains(text(),'Drayage Options')]/../..//select)[2]", "Destination Drayage Options [Select Options]")
        self.element().is_present(locator, timeout=5)
        self.dropdown().set_locator(locator).by_text(value)
        return self

    def enter_destination_special_instruction(self, value):
        locator = (By.XPATH, "(//label[contains(text(),'Special Instructions')]/../..//input[@type='text'])[2]", "DestinationL: Special Instructions [Origin Input Field]")
        self.send_keys().set_locator(locator).set_text(value)
        return self

    def enter_final_delivery_location_account_name(self, text):
        locator = (By.XPATH, f"(//div[contains(@class,'OriginDestStopsCmp')])[2]//label[text()='Final Delivery Location - Account Name']/..//input", "Final Delivery: Account Name")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text).pause(2)

        locator = (By.XPATH, f"(//div[contains(@class,'OriginDestStopsCmp')])[2]//label[text()='Final Delivery Location - Account Name']/../../../../..//ul[@role='listbox']//span[text()='{text}']", "Location Account Name List Options")
        self.element().wait(locator=locator, timeout=10)
        self.click().set_locator(locator).highlight().single_click()
        return self

    def enter_final_delivery_location_address(self, text):
        locator = (By.XPATH, f"(//div[contains(@class,'OriginDestStopsCmp')])[2]//label[text()='Address']/..//input", "Final Delivery Details: Pick Up Location - Address")
        self.send_keys().set_locator(locator, self._name).highlight().set_text(text).pause(2)

        locator = (By.XPATH, f"(//div[contains(@class,'OriginDestStopsCmp')])[2]//label[text()='Address']/../../../../..//ul[@role='listbox']//span[text()='{text}']", "Address List Options")
        self.element().wait(locator=locator, timeout=10)
        self.click().set_locator(locator).highlight().single_click()
        return self

    # Hidden Field
    def enter_final_delivery_location_contact(self, text):
        locator_input = (By.XPATH, f"(//div[contains(@class,'OriginDestStopsCmp')])[2]//label[text()='Contact Name']/..//input", "Final Delivery Location - Contact Name")
        self.element().wait(locator=locator_input, timeout=10)
        self.send_keys().set_locator(locator_input, self._name).highlight().set_text(text).pause(2)

        locator_item = (By.XPATH, f"(//div[contains(@class,'OriginDestStopsCmp')])[2]//label[text()='Contact Name']/../../../../..//ul[@role='listbox']//span[text()='{text}']", "Contact Name List Options")
        self.click().set_locator(locator_item).highlight().single_click()

        # TODO Temporal Fix to UI Problem is deleting after selecting the contact name
        self.send_keys().set_locator(locator_input, self._name).highlight().set_text(text).pause(3)
        return self

    # Hidden Field
    def enter_final_delivery_phone_number(self, text):
        locator = (By.XPATH, "(//label[contains(text(),'Phone No')])[5]/..//input", "Final Delivery - Final Delivery Phone Number [Input Field]")
        self.send_keys().set_locator(locator).set_text(text)
        return self

    def fill_destination_details(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data
        # Get JSON Data
        destination_details_final_delivery_address = booking_data['tests']['data']['booking']['origin_destination']['destination_details_final_delivery_address']

        # Input Search + List
        self.enter_destination_details(destination_details_final_delivery_address["final_destination"])
        self.select_destination_details(destination_details_final_delivery_address["final_destination"])

        self.loadings.is_not_visible_spinner()
        self.scroll().to_bottom()

        # Checkbox
        if destination_details_final_delivery_address["crowley_trucking_pickup"]:
            self.click_checkbox_crowley_trucking_for_delivery(destination_details_final_delivery_address["crowley_trucking_pickup"])

        if destination_details_final_delivery_address["on_carriage_mode"] != "":
            self.select_on_carriage_mode(destination_details_final_delivery_address["on_carriage_mode"])

        if destination_details_final_delivery_address["drayage_options"] != "":
            self.select_destination_drayage_options(destination_details_final_delivery_address["drayage_options"])

        if destination_details_final_delivery_address["special_instructions"] != "":
            self.enter_destination_special_instruction(destination_details_final_delivery_address["special_instructions"])

        if destination_details_final_delivery_address["final_delivery_location_account_name"] != "":
            self.enter_final_delivery_location_account_name(destination_details_final_delivery_address["final_delivery_location_account_name"])

        if destination_details_final_delivery_address["address"] != "":
            self.enter_final_delivery_location_address(destination_details_final_delivery_address["address"])

        if destination_details_final_delivery_address["contact_name"] != "":
            self.enter_final_delivery_location_contact(destination_details_final_delivery_address["contact_name"])

        if destination_details_final_delivery_address["relace_phone_number"] and destination_details_final_delivery_address["phone_number"] != "":
            self.enter_final_delivery_phone_number(destination_details_final_delivery_address["phone_number"])
            self.click_modal_replace_replace()

        return self

    def fill_stops_intermediate(self, booking_data=None):
        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data
        # Get JSON Data
        destination_details_final_delivery_address = booking_data['tests']['data']['booking']['origin_destination']['destination_details_final_delivery_address']

        if destination_details_final_delivery_address["enable-stops"] and len(destination_details_final_delivery_address["stops_intermediate"]) > 0:
            # Add First All Stops Fields
            for stop in destination_details_final_delivery_address["stops_intermediate"]:
                logger.info(f"Added Intermediate [{stop}]")
                self.click_add_stop_intermediate()

            self.pause(5)

            for stops_index, stop in enumerate(destination_details_final_delivery_address["stops_intermediate"]):
                s_index = stops_index + 1
                if stop["stop_location_account_name"] != "":
                    self.enter_stop_intermediate_location_account_name(index=s_index, text=stop["stop_location_account_name"])
                if stop["stop_location_address"] != "":
                    self.enter_stop_intermediate_address(index=s_index, text=stop["stop_location_address"])
                if stop["stop_location_contact_name"] != "":
                    self.enter_stop_intermediate_contact_name(index=s_index, text=stop["stop_location_contact_name"])
                if stop["stop_location_phone_number"] != "":
                    self.enter_stop_intermediate_phone_number(index=s_index, text=stop["stop_location_phone_number"])

        return self

    # STOPS -----------------------------------------------------------------------------------------------
    def click_add_stop(self):
        locator = (By.XPATH,"//button[text()='Add Stop']","Add Stop [Button]")
        self.click().set_locator(locator).single_click()
        return self

    def click_add_stop_intermediate(self):
        locator = (By.XPATH, "//button[text()='Add Intermediary Stop']", "Add Intermediary Stop [Button]")
        self.click().set_locator(locator).single_click()
        return self

    def enter_stop_location_account_name(self, index=None, text=None):
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[1])//label[text()='Stop Location - Account Name']/..//input)[{index}]", "Stop Location Account Name")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    def enter_stop_address(self, index=None, text=None):
        xindex = index + 1
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[1])//label[text()='Address']/..//input)[{xindex}]", "Stop Address")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    def enter_stop_contact_name(self, index=None, text=None):
        xindex = index + 1
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[1])//label[text()='Contact Name']/..//input)[{xindex}]", "Stop Contact Name")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    def enter_stop_phone_number(self, index=None, text=None):
        xindex = index + 1
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[1])//label[text()='Phone No.']/..//input)[{xindex}]", "Stop Phone No.")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    # INTERMEDIATE STOPS -----------------------------------------------------------------------------------------------

    def enter_stop_intermediate_location_account_name(self, index=None, text=None):
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[2])//label[text()='Stop Location - Account Name']/..//input)[{index}]", "Stop Location Account Name")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    def enter_stop_intermediate_address(self, index=None, text=None):
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[2])//label[text()='Address']/..//input)[{index}]", "Stop Address")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    def enter_stop_intermediate_contact_name(self, index=None, text=None):
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[2])//label[text()='Contact Name']/..//input)[{index}]", "Stop Contact Name")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self

    def enter_stop_intermediate_phone_number(self, index=None, text=None):
        location = (By.XPATH, f"(((//div[contains(@class,'origin-stops-container')])[2])//label[text()='Phone No.']/..//input)[{index}]", "Stop Phone No.")
        self.send_keys().set_locator(location).set_text_with_javascript(text).pause(2)
        return self



