from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.components.modals.ModalComponent import ModalComponent
from applications.web.csight.pages.bookings.create_booking.cargo_details.hazardous_details.HazardousDetailsComponent import \
    HazardousDetailsComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)
from selenium.webdriver.common.by import By

logger = setup_logger('VehicleTypeComponent')


class VehicleTypeComponent(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the VehicleTypeComponent instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Set Class Data
        self.booking_data = None
        # Locator definitions
        self._xpath_vehicle_list = "(//div[@id='containerId']//div[contains(@class,'containers-col')]//div[contains(@class,'content')])"
        # Sub-Components
        self.loadings = Loadings.get_instance()
        self.modal = ModalComponent.get_instance()
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
        self.hazardous_details.set_booking_data(data)
        return self

    @staticmethod
    def main_content(index):
        text = f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1])"
        return text

    def vehicles_modal_confirmation(self):
        self.modal.click_remove()
        self.loadings.is_not_visible_spinner()
        return self

    def click_first_clickable_ok_button(self):
        buttons = self.get_driver().find_elements(By.XPATH, "//button[@title='OK']")
        logger.info(f"Found {len(buttons)} 'OK' buttons")

        for i, btn in enumerate(buttons):
            logger.info(f"Button {i}:")
            logger.info(f"  displayed: {btn.is_displayed()}")
            logger.info(f"  enabled: {btn.is_enabled()}")
            logger.info(f"  location: {btn.location}")
            logger.info(f"  size: {btn.size}")
            try:
                parent_class = btn.find_element(By.XPATH, '..').get_attribute('class')
            except:
                parent_class = "<not available>"
            logger.info(f"  parent class: {parent_class}")

            # Check basic visibility and enabled state
            if not (btn.is_displayed() and btn.is_enabled()):
                logger.info("  -> Not visible or disabled. Skipping.")
                logger.info("---")
                continue

            # Attempt to click the button
            try:
                btn.click()
                logger.info("  -> Click successful!")
                return  # Exit early if click succeeds
            except (ElementClickInterceptedException, StaleElementReferenceException, WebDriverException) as e:
                logger.warning(f"  -> Click failed: {type(e).__name__}: {e}")
                logger.info("  -> Trying next button...")
            logger.info("---")

        # If we reach this point, no button was clickable
        logger.error("Could not click any 'OK' button")
        # raise Exception("No clickable 'OK' button found")

    def select_type(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label[text()='Type']/..//input | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Type']/..//input",
                        "Type[Input Search]")
        option_locator = (By.XPATH,
                          f"{self.main_content(index)}//label[text()='Type']/..//ul/li/span[contains(text(),'{text}')] | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Type']/..//ul/li/span[contains(text(),'{text}')]",
                          "Type [Option List]")
        self.scroll().set_locator(text_locator).to_element(pixels=-100)
        self.click().set_locator(text_locator).highlight().single_click().pause(3)
        self.click().set_locator(option_locator).highlight().single_click().pause(2)

    def select_rating_commodity_category(self, index=1, text: str = None):

        text_locator = (By.XPATH, f"{self.main_content(index)}//label[contains(text(),'Rating Commodity Category')]/..//input | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[contains(text(),'Rating Commodity Category')]/..//input",
                        "Rating Commodity Category [Input Search]")
        option_locator = (By.XPATH,
                          f"{self.main_content(index)}//label[contains(text(),'Rating Commodity Category')]/..//ul/li/span[contains(text(),'{text}')] | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[contains(text(),'Rating Commodity Category')]/..//ul/li/span[contains(text(),'{text}')]",
                          "Rating Commodity Category [Option List]")

        self.scroll().set_locator(text_locator).to_element(pixels=-200)

        self.click().set_locator(text_locator).highlight().single_click()
        self.click().set_locator(text_locator).highlight().single_click().pause(2)

        visible = self.element().set_locator(option_locator).is_visible()
        logger.info(f"Visible: {visible}")

        self.click().set_locator(option_locator).highlight().double_click().pause(3)

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

    def select_year(self, index=1, text: str = None):

        text_locator = (By.XPATH, f"{self.main_content(index)}//label[contains(text(),'Year')]/..//select", "Year [Input Search]")
        self.dropdown().set_locator(text_locator).by_text(text)
        return self

    def select_manufacturer(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label/span[contains(text(),'Manufacturer')]/../..//select", "Manufacturer [Input Search]")
        self.dropdown().set_locator(text_locator).by_text(text)
        return self

    def select_model(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label/span[contains(text(),'Model')]/../..//select", "Model [Input Search]")
        self.dropdown().set_locator(text_locator).by_text(text)
        return self

    def select_color(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label/span[contains(text(),'Color')]/../..//select", "Color [Input Search]")
        self.dropdown().set_locator(text_locator).by_text(text)
        return self

    def enter_quantity(self, index=1, quantity=None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label[contains(text(),'Quantity')]/..//input | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Quantity']/..//input", "Quantity [Input Search]")

        count = 0
        for item in quantity:
            if "vin_serial_number" in item:
                count += 1

        self.send_keys().set_locator(text_locator).highlight().set_text(str(count)).pause(2)

        # Loop for JSON Quantity values to Fill Up Containers List Section (Accordion List)
        for index_c, quantity_item in enumerate(quantity):
            xpath_index = index_c + 1
            self.enter_vin_serial_number(
                container_index=index,
                quantity_index=xpath_index,
                text=quantity_item["vin_serial_number"],
                units=quantity_item["consolidate_units"]
            )

        return self

    def enter_vin_serial_number(self, container_index=1, quantity_index=1, text: str = None, units: str = None):
        text_locator = (By.XPATH,
                        f"((((//div[@id='vehicle']/div)[{container_index}]/div[2]/div[@class='row'])[3]//div[@class='row'])[{quantity_index}]//label[text()='VIN / Serial Number']/../div/input)[1] | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[6]//div[@class='row'])[{quantity_index}]//label[text()='VIN / Serial Number']/../div/input | (((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[5]//div[@class='row'])[{quantity_index}]//label[text()='VIN / Serial Number']/../div/input",
                        "VIN / Serial Number [Input Box]")

        self.scroll().set_locator(text_locator).to_element(pixels=-100)
        self.send_keys().set_locator(text_locator).set_text(text)

        len_units = len(units)

        if len_units > 0:
            for index, unit in enumerate(units):
                logger.info(f"Adding Consolidate Units: [{unit}]")
                add_consolidate_units_locator = (By.XPATH,
                                                 f"(((//div[@id='vehicle']/div)[{container_index}]/div[2]/div[@class='row'])[3]/div//label[text()='VIN / Serial Number']/../../../../..//a[text()=' + ADD CONSOLIDATED UNITS '])[{quantity_index}] | ((((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[6]//div[@class='row'])[{quantity_index}]//label[text()='VIN / Serial Number']/../../../../..//a[contains(text(),'ADD CONSOLIDATED UNITS')])",
                                                 f"Add Consolidate Units [{quantity_index}]")
                self.click().set_locator(add_consolidate_units_locator).single_click()

            for index_input, unit in enumerate(units):
                index_xpath = index_input + 1
                consolidate_unit_input = (By.XPATH, f"(((((//div[@id='vehicle']/div)[{container_index}]/div[2]/div[@class='row'])[3]//div[@class='row'])[{quantity_index}]//label[text()='VIN / Serial Number']/..)[1]/../../../../div[2]//input)[{index_xpath}] | (((((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{container_index}]/div)[6]//div[@class='row'])[{quantity_index}]//label[text()='VIN / Serial Number']/..)[1]/../../../../div[2]//input)[{index_xpath}]")
                self.send_keys().set_locator(consolidate_unit_input).set_text(unit)

        return self

    def select_propulsion(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label[contains(text(),'Propulsion')]/..//select", "Propulsion [Input Search]")
        self.dropdown().set_locator(text_locator).by_text(text).pause(2)
        okay_locator = (By.XPATH, f"(//section[@role='dialog']//button[text()='Okay'])", "Okay [Dialog Box]")
        if self.element().set_locator(okay_locator).is_visible():
            self.click().set_locator(okay_locator).single_click()
        return self

    def enter_declared_value_of_cargo(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label[text()='Declared Value of Cargo (USD)']/..//input | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Declared Value of Cargo (USD)']/..//input", "Quantity [Input Search]")
        self.send_keys().set_locator(text_locator).highlight().set_text(str(text))
        return self

    def click_checkbox_add_additional_units(self, index=1, value=False):
        locator = (By.XPATH, f"((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div)[3]//label[contains(text(),'Add Additional Units')]/..//span[contains(@part,'indicator')]", "Add Additional Units [Checkbox]")
        if value:
            self.click().set_locator(locator).highlight().single_click()
        return self

    def click_checkbox_add_additional_cargo_in_on_units(self, index=1, value=False):
        locator = (By.XPATH, f"((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div)[3]//label/span[contains(text(),'Add Additional Cargo in/on Units')]/..//span[contains(@part,'indicator')]", "Add Additional Cargo in/on Units [Checkbox]")
        if value:
            self.click().set_locator(locator).highlight().single_click().pause(2)
            self.click_first_clickable_ok_button()
        return self

    def enter_description(self, index=1, text: str = None):
        text_locator = (By.XPATH, f"{self.main_content(index)}//label[text()='Description']/..//textarea | (//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Description']/..//textarea", "Quantity [Input Search]")
        self.scroll().set_locator(text_locator).to_element(pixels=-100)
        self.send_keys().set_locator(text_locator).clear().highlight().set_text(text)
        return self

    def enter_dimensions(self, index=1, length=None, width=None, height=None, weight=None, unit_measure=None, weight_over_write=False):

        locator_length_1 = (By.XPATH,
                            f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[text()='Length']/../../../../../div[1]/..//input)[1] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Length']/../../../../..//input)[1]",
                            "Length ft [Input Field]")
        locator_length_2 = (By.XPATH,
                            f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[text()='Length']/../../../../../div[1]/..//input)[2] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Length']/../../../../..//input)[2]",
                            "Length in [Input Field]")

        locator_width_1 = (By.XPATH,
                           f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[text()='Width']/../../../../../div[1]/..//input)[1] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Width']/../../../../..//input)[1]",
                           "Width ft [Input Field]")
        locator_width_2 = (By.XPATH,
                           f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[text()='Width']/../../../../../div[1]/..//input)[2] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Width']/../../../../..//input)[2]",
                           "Width in [Input Field]")

        locator_height_1 = (By.XPATH,
                            f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[text()='Height']/../../../../../div[1]/..//input)[1] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Height']/../../../../..//input)[1]",
                            "Height ft [Input Field]")
        locator_height_2 = (By.XPATH,
                            f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[text()='Height']/../../../../../div[1]/..//input)[2] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Height']/../../../../..//input)[2]",
                            "Height in [Input Field]")

        locator_weight_1 = (By.XPATH,
                            f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[contains(text(),'Weight Per Unit')]/..//input)[1] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Weight Per Unit']/../../../../..//input)[2]",
                            "Weight in [Input Field]")

        locator_unit_lb_ft = (By.XPATH,
                              f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[contains(text(),'Weight Per Unit')]/../../../../../../div[5])/div/button[1] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Weight Per Unit']/../../../../../../div)[5]/div/button[1]",
                              "Lb/Ft [Button]")
        locator_unit_kg_m = (By.XPATH,
                             f"(((//div[@id='vehicle']/div)[{index}]/div[2]/div[@class='row'])[1]//label[contains(text(),'Weight Per Unit')]/../../../../../../div[5])/div/button[2] | ((//div[@id='vehicle' or @id='breakbulk']/div/div/div[2])[{index}]/div//label[text()='Weight Per Unit']/../../../../../../div)[5]/div/button[2]",
                             "Kg/M [Button]")

        self.scroll().set_locator(locator_unit_lb_ft).to_element(pixels=-100)

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
        if weight_over_write and weight["lb_kg"] > 0:
            self.send_keys().set_locator(locator_weight_1).clear().set_text(str(weight["lb_kg"]))

        return self

    def fill_vehicle_general_information(self, booking_data=None):

        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        vehicles = self.booking_data['tests']['data']['booking']['cargo_details']['vehicle']

        for index, containers in enumerate(vehicles):

            vehicle = booking_data['tests']['data']['booking']['cargo_details']['vehicle'][index]
            xpath_index = index + 1

            # Scroll to Container Section
            # self.loadings.is_not_visible_spinner()

            # Fill Container Fields

            # Row 1 --------------------------------------------------------------------------------------------------------
            if vehicle['rating_commodity_category'] != "":
                self.select_rating_commodity_category(index=xpath_index, text=vehicle['rating_commodity_category'])
                self.click_first_clickable_ok_button()
            if vehicle['year'] != "" and vehicle['rating_commodity_category'] != "Vehicles - Classic/Vintage":
                self.select_year(index=xpath_index, text=vehicle['year'])
            if vehicle['manufacturer'] != "" and vehicle['rating_commodity_category'] != "Vehicles - Classic/Vintage":
                self.select_manufacturer(index=xpath_index, text=vehicle['manufacturer'])
            if vehicle['model'] != "" and vehicle['rating_commodity_category'] != "Vehicles - Classic/Vintage":
                self.select_model(index=xpath_index, text=vehicle['model'])
            if vehicle['color'] != "":
                self.select_color(index=xpath_index, text=vehicle['color'])
            if vehicle['quantity'] != "":
                self.enter_quantity(index=xpath_index, quantity=vehicle['quantity'])

            if vehicle['propulsion'] != "":
                self.select_propulsion(index=xpath_index, text=vehicle['propulsion'])

            if vehicle['manufacturer'] == "Others" or vehicle['rating_commodity_category'] == "Vehicles - Classic/Vintage":

                over_write = False
                if vehicle['rating_commodity_category'] == "Vehicles - Classic/Vintage":
                    over_write = True

                # Dimensions
                self.enter_dimensions(
                    index=xpath_index,
                    unit_measure=vehicle['dimensions']['unit_measure'],
                    length=vehicle['dimensions']['length'],
                    width=vehicle['dimensions']['width'],
                    height=vehicle['dimensions']['height'],
                    weight=vehicle['dimensions']['weight'],
                    weight_over_write=over_write
                )

            # if vehicle['add_additional_cargo_in_on_units'] != "":
            #     self.click_checkbox_add_additional_cargo_in_on_units(index=xpath_index, value=vehicle['add_additional_cargo_in_on_units'])

            if vehicle['description'] != "":
                self.enter_description(index=xpath_index, text=vehicle['description'])

        return self

    def fill_breakbulk_information(self, booking_data=None):

        # Verify if Booking Data was previously set by the user on Create Booking Page
        if self.booking_data:
            booking_data = self.booking_data

        breakbulk = booking_data['tests']['data']['booking']['cargo_details']['cargo_not_in_container']

        for index, breakbulk_cargo in enumerate(breakbulk):
            xpath_index = index + 1
            # Row 1 --------------------------------------------------------------------------------------------------------
            if breakbulk_cargo['type'] != "":
                self.select_type(index=xpath_index, text=breakbulk_cargo['type'])

            if breakbulk_cargo['rating_commodity_category'] != "":
                self.select_rating_commodity_category(index=xpath_index, text=breakbulk_cargo['rating_commodity_category'])

            if breakbulk_cargo['quantity'] != "":
                self.enter_quantity(index=xpath_index, quantity=breakbulk_cargo['quantity'])

            if breakbulk_cargo['hazardous_booking'] != "":
                self.select_radio_hazardous_booking(index=xpath_index, text=breakbulk_cargo['hazardous_booking'])

            if breakbulk_cargo['declared_value_of_cargo'] != "":
                self.enter_declared_value_of_cargo(index=xpath_index, text=breakbulk_cargo['declared_value_of_cargo'])

            if breakbulk_cargo['add_additional_units'] != "":
                self.click_checkbox_add_additional_units(index=xpath_index, value=breakbulk_cargo['add_additional_units'])

            if breakbulk_cargo['add_additional_cargo_in_on_units'] != "":
                self.click_checkbox_add_additional_cargo_in_on_units(index=xpath_index, value=breakbulk_cargo['add_additional_cargo_in_on_units'])

            if breakbulk_cargo['description'] != "":
                self.enter_description(index=xpath_index, text=breakbulk_cargo['description'])

            # Dimensions
            self.enter_dimensions(
                index=xpath_index,
                unit_measure=breakbulk_cargo['dimensions']['unit_measure'],
                length=breakbulk_cargo['dimensions']['length'],
                width=breakbulk_cargo['dimensions']['width'],
                height=breakbulk_cargo['dimensions']['height'],
                weight=breakbulk_cargo['dimensions']['weight'],
                weight_over_write=True
            )

            # If Hazardous is YES UI Display another Radio Button Option
            if str(breakbulk_cargo['hazardous_booking']).lower() == "yes":
                self.select_radio_hazardous_details_entered(index=xpath_index, text=breakbulk_cargo['hazardous_details_entered'])

        # Fill All Hazardous Details Info Indicated in the JSON File
        self.hazardous_details.fill_hazardous_details()

