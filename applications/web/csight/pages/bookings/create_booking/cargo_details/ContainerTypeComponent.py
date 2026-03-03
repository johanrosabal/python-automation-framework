from selenium.webdriver.common.by import By
from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.pages.bookings.create_booking.cargo_details.hazardous_details.HazardousDetailsComponent import HazardousDetailsComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('ContainerTypeComponent')


class ContainerTypeComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the ContainerTypeComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Container Items Count
        self.quantity = 0
        # Locator definitions
        self._xpath_containers_list = "(//div[@id='containerId']//div[contains(@class,'containers-col')]//div[contains(@class,'content')])"
        # Sub-Components
        self.loadings = Loadings.get_instance()
        self.hazardous_details = HazardousDetailsComponent.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def set_booking_data(self, data=None):
        """ Set Booking Data and share with all fill methods """
        self.booking_data = data
        # Pass JSON Data to Hazardous Component
        self.hazardous_details.set_booking_data(data)
        return self

    def set_quantity(self, number: int):
        """ Set the Number of Container Items Found on JSON Data """
        self.quantity = number
        return self

    # Cargo Item  -----------------------------------------------------------------------------------------------
    def select_size_type(self, index, text):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Size / Type").by_text(text=text)
        self.loadings.wait_until_loading_not_present()
        return self

    # Reefer Details
    def enter_temperature(self, index, text):
        """
        Reefer temperature range should be between -34C and +38C
        """
        locator = (By.XPATH, f"(//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Temperature']/..//input", "Enter Temperature [Input]")
        self.send_keys().set_locator(locator).set_text(str(text))
        return self

    def select_scale(self, index, text):
        locator = (By.XPATH,
                   f"((//div[@id='containerId']/div/div[2]/div)[{str(index)}]//label[text()='Temperature']/following::select[@class='slds-select'])[1]",
                   "Option Temperature Scale [Select]")
        self.dropdown().set_locator(locator, self._name).by_text_contains(text)
        return self

    def select_vent_settings(self, index, text):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Vent Settings").by_text(text=text)
        return self

    # -----------------------------------------------------------------------------------------------
    def enter_quantity(self, container_index, quantity):
        # Read the number of containers list
        # data = json.loads(quantity)
        size = len(quantity)

        # Input Quantity Amount
        locator = (By.XPATH, f"(//div[@id='containerId']/div/div[2]/div)[{container_index}]//label[text()='Quantity']/..//input", "Enter Quantity [Input]")
        self.send_keys().set_locator(locator).set_text(str(size))
        self.loadings.is_not_visible_spinner()

        # Loop for JSON Quantity values to Fill Up Containers List Section (Accordion List)
        for index, container in enumerate(quantity):
            xpath_index = index + 1
            self.enter_request_container(
                container_index=container_index,
                quantity_index=xpath_index,
                search_container=container['request_container']
            )

            self.enter_assigned_container(
                container_index=container_index,
                quantity_index=xpath_index,
                assigned_container=container['assigned_container']
            )

            self.enter_seaboard_booking_number(
                container_index=container_index,
                quantity_index=xpath_index,
                seaboard_booking_number=container['seaboard_booking_number']
            )

        return self

    # CONTAINERS LIST according to QUANTITY  ---------------------------------------------------------------------------
    def enter_request_container(self, container_index=1, quantity_index=1, search_container=None):
        # If search_container has value
        if search_container not in (None, ""):
            # Root Container XPATH
            xpath_container = f"((//div[@id='containerId']//div[contains(@class,'containers-col')])[{container_index}]//div[contains(@class,'content')])[{quantity_index}]"
            # Root Section XPath
            xpath_label = "//label[text()='Requested Container']"
            # Input Field
            input_locator = (By.XPATH, f"{xpath_container}{xpath_label}/..//input")
            self.scroll().set_locator(input_locator).to_element(pixels=-100)
            self.send_keys().set_locator(input_locator, self._name).set_text(search_container).pause(2)

            list_item_locator = (By.XPATH, f"{xpath_container}{xpath_label}/../../../../../../../..//div[@id='lookup']//li//span[contains(@class,'location-name') and text()='{search_container}']")
            self.click().set_locator(list_item_locator, self._name).single_click()

        return self

    def enter_assigned_container(self, container_index=1, quantity_index=1, assigned_container=None):
        if assigned_container not in (None, ""):
            # Root Container XPATH
            xpath_container = f"((//div[@id='containerId']//div[contains(@class,'containers-col')])[{container_index}]//div[contains(@class,'content')])[{quantity_index}]"
            # Root Section XPath
            xpath_label = "//label[text()='Assigned Container']"
            # Input Field
            input_locator = (By.XPATH, f"{xpath_container}{xpath_label}/..//input")
            self.scroll().set_locator(input_locator).to_element(pixels=-100)
            self.send_keys().set_locator(input_locator, self._name).set_text(assigned_container)
        return self

    # END CONTAINERS LIST according to QUANTITY  -----------------------------------------------------------------------
    def enter_seaboard_booking_number(self, container_index=1, quantity_index=1, seaboard_booking_number=None):
        if seaboard_booking_number not in (None, ""):
            # Root Container XPATH
            xpath_container = f"((//div[@id='containerId']//div[contains(@class,'containers-col')])[{container_index}]//div[contains(@class,'content')])[{quantity_index}]"
            # Root Section XPath
            xpath_label = "//label[text()='Seaboard Booking Number']"
            # Input Field
            input_locator = (By.XPATH, f"{xpath_container}{xpath_label}/..//input")
            self.scroll().set_locator(input_locator).to_element(pixels=-100)
            self.send_keys().set_locator(input_locator, self._name).set_text(seaboard_booking_number)
        return self

    def enter_cargo_wt_per_container(self, index=1, text=None):
        self.send_keys_with_index().set_locator(index=index, label="Cargo Wt. Per Container").by_text(text=text)
        return self

    def select_weight_container(self, index, text):
        locator = (By.XPATH,
                   f"(//label[contains(text(), 'Cargo Wt. Per Container')]/../..//select[@class='slds-select'])[{str(index)}]",
                   "Option Weight Container [Select]")
        self.dropdown().set_locator(locator, self._name).by_text_contains(text)
        return self

    def select_rating_commodity_category(self, index, text):
        self.dropdown_autocomplete().set_locator_by_label(index=index, label="Rating Commodity Category").by_text(text=text)
        self.loadings.is_not_visible_spinner()
        return self

    def select_radio_hazardous_booking(self, index, text: str):

        match text.lower():
            case "yes":
                self.radio_with_index().set_locator(index=index, label="Hazardous Booking").set_yes()
            case "no":
                self.radio_with_index().set_locator(index=index, label="Hazardous Booking").set_no()
            case _:
                logger.error(f"Option not available: [{text}]")

        return self

    def select_radio_hazardous_details_entered(self, index, text: str):

        match text.lower():
            case "yes":
                self.radio_with_index().set_locator(index=index, label="Hazardous Details Entered").set_yes()
            case "no":
                self.radio_with_index().set_locator(index=index, label="Hazardous Details Entered").set_no()
            case _:
                logger.error(f"Option not available: [{text}]")

        return self

    def select_radio_waste(self, index, text: str):

        match text.lower():
            case "yes":
                self.radio_with_index().set_locator(index=index, label="Waste").set_yes()
            case "no":
                self.radio_with_index().set_locator(index=index, label="Waste").set_no()
            case _:
                logger.error(f"Option not available: [{text}]")

        return self

    def select_radio_RCRA(self, index=1, text: str = None):

        match text.lower():
            case "yes":
                self.radio_with_index().set_locator(index=index, label="RCRA").set_yes()
            case "no":
                self.radio_with_index().set_locator(index=index, label="RCRA").set_no()
            case _:
                logger.error(f"Option not available: [{text}]")

        return self

    def select_toggle_shipper_owned(self, index=1):
        locator = (By.XPATH, f"(//label[text()='Shipper Owned'])[{str(index)}]/..//lightning-input", "toggle button")
        self.click().set_locator(locator, self._name).single_click()
        self.loadings.wait_until_loading_not_present()
        return self

    def select_toggle_NOR(self, index=1):
        """ Only available when Reefer Containers"""
        locator = (By.XPATH, f"(//label[contains(text(),'NOR')])[{str(index)}]/..//lightning-input", "toggle button")
        self.click().set_locator(locator, self._name).single_click()
        return self

    def enter_HTS_number(self, index=1, text=None):
        input_locator = (By.XPATH, f"(//label[contains(text(), 'HTS Number')])[{index}]/..//input", "Input HTS Text")
        self.send_keys().set_locator(input_locator, self._name).set_text(text).pause(1)
        self.loadings.is_not_visible_spinner_medium()
        # List of HTS Numbers Displayed after text entered
        list_items_locator = (By.XPATH, f"(//label[contains(text(), 'HTS Number')])[{index}]/..//div[contains(@id,'lookup')]//li//span[contains(@class,'location-name') and contains(text(),'{text}')]", "HTS LIST Displayed")
        self.click().set_locator(list_items_locator, self._name).single_click()
        return self

    def enter_actual_cargo_description(self, index=1, text=None):
        """ If HTS has va numeric value found on the list displayed, it automatically write it text on this field"""
        self.send_keys_with_index().set_locator(index=index, label="Actual Cargo Description").clear().by_text(text=text)
        return self

    def enter_declared_value_of_cargo_USD(self, index=1, text=None):
        self.send_keys_with_index().set_locator(index=index, label="Declared Value of Cargo (USD)").by_text(text=text)
        return self

    # FLAT RACK FIELDS -----------------------------------------------------------------------------
    def select_specialized_equipment_fasteners(self, index=1, option=None):
        locator = (By.XPATH,
                   f"(//div[@id='containerId']/div/div[2]/div)[{index}]//label[contains(text(), 'Specialized Equipment Fasteners ')]/../..//select",
                   "Specialized Equipment Fasteners Options [Select]")
        self.dropdown().set_locator(locator, self._name).by_text_contains(option)
        return self

    def enter_dimensions(self, index=1, length=None, width=None, height=None, weight=None, unit_measure=None):

        locator_length_1 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Length']/../../../../../div[1])//input", "Length ft [Input Field]")
        locator_length_2 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Length']/../../../../../div[2])//input", "Length in [Input Field]")

        locator_width_1 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Width']/../../../../../div[3])//input", "Width ft [Input Field]")
        locator_width_2 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Width']/../../../../../div[4])//input", "Width in [Input Field]")

        locator_height_1 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Height']/../../../../../div[5])//input", "Height ft [Input Field]")
        locator_height_2 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Height']/../../../../../div[6])//input", "Height in [Input Field]")

        locator_weight_1 = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Weight']/../../../../../div[7])//input", "Weight in [Input Field]")

        locator_unit_lb_ft = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Weight']/../../../../../div[8])/div/button[1]", "Lb/Ft [Button]")
        locator_unit_kg_m = (By.XPATH, f"((//div[@id='containerId']/div/div[2]/div)[{index}]//label[text()='Weight']/../../../../../div[8])/div/button[2]", "Kg/M [Button]")

        if unit_measure["lb_ft"]:
            self.click().set_locator(locator_unit_lb_ft).single_click()

        if unit_measure["kg_m"]:
            self.click().set_locator(locator_unit_kg_m).single_click()

        # LENGTH
        if length["ft_m"] > 0:
            self.send_keys().set_locator(locator_length_1).set_text(str(length["ft_m"]))

        if length["in_cm"] > 0:
            self.send_keys().set_locator(locator_length_2).set_text(str(length["in_cm"]))

        # WIDTH
        if width["ft_m"] > 0:
            self.send_keys().set_locator(locator_width_1).set_text(str(width["ft_m"]))
        if width["in_cm"] > 0:
            self.send_keys().set_locator(locator_width_2).set_text(str(width["in_cm"]))

        # HEIGHT
        if height["ft_m"] > 0:
            self.send_keys().set_locator(locator_height_1).set_text(str(height["ft_m"]))
        if height["in_cm"] > 0:
            self.send_keys().set_locator(locator_height_2).set_text(str(height["in_cm"]))

        # WEIGHT
        if weight["lb_kg"] > 0:
            self.send_keys().set_locator(locator_weight_1).set_text(str(weight["lb_kg"]))

        return self

    # GENERAL CONTAINER INFORMATION FIELDS -----------------------------------------------------------------------------
    def get_container_title(self, index=1):
        locator = (By.XPATH, f"//div[@id='containerId']/div[{index}]//h6", " Container Title")
        return self.get_text().set_locator(locator).by_text()

    def scroll_to_container_item(self, index=1):
        locator = (By.XPATH, f"//div[@id='containerId']/div[{index}]//h6/../../div[2]/div", " Container Title")
        self.scroll().set_locator(locator).to_element(pixels=-100)
        return self

    def fill_container_general_information(self, booking_data=None):

        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        containers = self.booking_data['tests']['data']['booking']['cargo_details']['container']

        for index, container in enumerate(containers):

            container = booking_data['tests']['data']['booking']['cargo_details']['container'][index]
            xpath_index = index + 1

            # Scroll to Container Section
            self.loadings.is_not_visible_spinner()
            self.scroll_to_container_item(index=xpath_index)
            # Fill Container Fields

            # Row 1 --------------------------------------------------------------------------------------------------------
            self.select_size_type(index=xpath_index, text=container['size_type'])
            self.enter_quantity(container_index=xpath_index, quantity=container['quantity'])
            self.enter_cargo_wt_per_container(index=xpath_index, text=container['cargo_wt_per_container'])
            self.select_weight_container(index=xpath_index, text=container['weight_type'])
            self.select_rating_commodity_category(index=xpath_index, text=container['rating_commodity_category'])

            # Row 2 --------------------------------------------------------------------------------------------------------
            self.select_radio_hazardous_booking(index=xpath_index, text=container['hazardous_booking'])
            self.select_radio_waste(index=xpath_index, text=container['waste'])
            self.select_radio_RCRA(index=xpath_index, text=container['RCRA'])

            # Check Shipper Owned
            container['shipper_owned'] and self.select_toggle_shipper_owned(index=xpath_index)

            # Row 3 --------------------------------------------------------------------------------------------------------

            # HTS If text is found
            container['HTS_number'] != "" and self.enter_HTS_number(index=xpath_index, text=container['HTS_number'])

            # If the HTS value is Blank, can write text on Actual Cargo
            container['HTS_number'] == "" and self.enter_actual_cargo_description(index=xpath_index, text=container['actual_cargo_description'])

            # Row 4 --------------------------------------------------------------------------------------------------------
            self.enter_declared_value_of_cargo_USD(index=xpath_index, text=str(container['declared_value_of_cargo']))

            # For Containers Flat should fill hidden fields
            if "flat" in str(container['size_type']).lower():
                self.select_specialized_equipment_fasteners(index=xpath_index, option=container['specialized_equipment_fasteners'])
                # Dimensions
                self.enter_dimensions(
                    index=xpath_index,
                    unit_measure=container['dimensions']['unit_measure'],
                    length=container['dimensions']['length'],
                    width=container['dimensions']['width'],
                    height=container['dimensions']['height'],
                    weight=container['dimensions']['weight']
                )

            # Row 5 --------------------------------------------------------------------------------------------------------
            # If the Word 'Reefer' is present in Type of Container
            if "Reefer" in container['size_type']:

                if container["NOR"]:
                    self.select_toggle_NOR(index=xpath_index)
                else:
                    temperature = container['temperature']
                    self.enter_temperature(index=xpath_index, text=str(temperature['amount']))
                    self.select_scale(index=xpath_index, text=temperature['scale'])  # F or C
                    self.select_vent_settings(index=xpath_index, text=str(temperature['vent_settings']))  # Number Between 0 and 100

            # If Hazardous is YES UI Display another Radio Button Option
            if str(container['hazardous_booking']).lower() == "yes":
                self.select_radio_hazardous_details_entered(index=xpath_index, text=container['hazardous_details_entered'])

        # Fill All Hazardous Details Info Indicated in the JSON File
        self.hazardous_details.fill_hazardous_details()

        return self
