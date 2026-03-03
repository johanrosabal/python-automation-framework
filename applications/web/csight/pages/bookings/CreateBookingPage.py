from selenium.webdriver.common.by import By
from applications.web.csight.common.CSightBasePage import CSightBasePage
from applications.web.csight.components.buttons.Buttons import Buttons
from applications.web.csight.components.loadings.Loadings import Loadings
from applications.web.csight.pages.bookings.create_booking.CargoDetailsComponent import CargoDetailsComponent
from applications.web.csight.pages.bookings.create_booking.OriginDestinationComponent import OriginDestinationComponent
from applications.web.csight.pages.bookings.create_booking.OtherDetailsComponent import OtherDetailsComponent
from applications.web.csight.pages.bookings.create_booking.RoutesComponent import RoutesComponent
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp


logger = setup_logger('CreateBookingPage')


class CreateBookingPage(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the CreateBookingPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Data
        self.booking_data = None
        # Relative URL
        self.relative = "Employees/s/create-booking"

        # Pages Components Related
        self.origin_destination = OriginDestinationComponent.get_instance()
        self.cargo_details = CargoDetailsComponent.get_instance()
        self.routes = RoutesComponent.get_instance()
        self.other_details = OtherDetailsComponent.get_instance()

        # Modal
        self._text_modal_update = (By.XPATH, "//section[@aria-modal='true']//div[contains(text(),'update') or contains(text(),'cancelled')]", "Modal Update or Cancel")

        # Sub-Components
        self.buttons = Buttons.get_instance()
        self.loadings = Loadings.get_instance()

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def set_booking_data(self, data=None):
        """ Set Booking Data and share with all fill methods """
        self.booking_data = data

        # Pass Booking Data To Sub-Components
        self.origin_destination.set_booking_data(self.booking_data)
        self.cargo_details.set_booking_data(self.booking_data)
        self.routes.set_booking_data(self.booking_data)
        self.other_details.set_booking_data(self.booking_data)
        return self

    def get_modal_text(self):
        return self.get_text().set_locator(self._text_modal_update).by_text()

    def click_next(self):
        self.buttons.click_next()
        self.loadings.is_not_visible_spinner()
        return self

    def click_back(self):
        self.buttons.click_back()
        return self

    def click_save(self):
        self.buttons.click_save()
        return self

    def click_create(self):
        self.buttons.click_save()
        return self

    def click_proceed(self):
        self.scroll().to_bottom()
        self.buttons.click_proceed()
        self.loadings.is_not_visible_spinner()
        return self

    def click_modal_ok(self):
        self.buttons.click_ok()
        self.loadings.is_not_visible_spinner()
        return self

    def click_cancel_booking(self):
        self.buttons.click_cancel_booking()
        return self

    def click_updated_booking(self):
        self.buttons.click_update_booking()
        return self

    def click_cancel_update(self):
        self.buttons.click_cancel_update()
        return self

    def click_create_booking(self):
        self.buttons.click_create_booking()
        self.loadings.is_not_visible_spinner()
        self.pause(5)
        return self

    def click_continue_update(self):
        self.buttons.click_continue_update()
        self.loadings.is_not_visible_spinner()
        return self

    def click_confirm_cancellation(self):
        self.buttons.click()
        self.loadings.is_not_visible_spinner()
        return self

    def click_close_modal(self):
        self.buttons.click_close_modal()
        return self
