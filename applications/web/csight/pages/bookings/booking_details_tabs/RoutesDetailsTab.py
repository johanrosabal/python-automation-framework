from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from applications.web.csight.common.CSightBasePage import CSightBasePage

logger = setup_logger('RoutesDetailsTab')


class RoutesDetailsTab(CSightBasePage):

    def __init__(self, driver):
        """
        Initialize the RoutesDetailsTab instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "Employees/s/bookingDetail?id={ID}"
        # xPath Containers
        self._xpath_commercial_route = "//h6[text()='COMMERCIAL ROUTE']/../.."
        self._xpath_operational_route = "//h6[text()='OPERATIONAL ROUTE']/../.."

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

    def get_commercial_route_empty_pick_up(self):
        # Read Elements
        line_1 = (By.XPATH, f"({self._xpath_commercial_route}//div[contains(@class,'booking-list-data-row')]/div/div/span[2])[1]", "Commercial Route Pick Up [Text]")
        line_2 = (By.XPATH, f"({self._xpath_commercial_route}//div[contains(@class,'booking-list-data-row')]/div[2]/span[1])[1]", "Commercial Route Pick Up [Text]")
        line_3 = (By.XPATH, f"({self._xpath_commercial_route}//div[contains(@class,'booking-list-data-row')]/div[2]/span[2])[1]", "Commercial Route Pick Up [Text]")

        # Return Dictionary with values
        data = {
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "line_2": self.get_text().set_locator(line_2, self._name).by_text(),
            "line_3": self.get_text().set_locator(line_3, self._name).by_text()
        }
        return data

    def get_commercial_route_port_origin(self):
        # Read Elements
        port = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[1]/div/span[2]", "Commercial Route Port [Text]")
        voyage = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[1]/div[2]/div[1]/span[2]", "Commercial Route Voyage [Text]")
        vessel = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[1]/div[2]/div[2]/span[2]", "Commercial Route Vessel [Text]")

        line_1 = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[2]/div/span[1]", "Commercial Route Port: Line 1 [Text]")
        line_2 = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[2]//span/span[1]", "Commercial Route Port: Line 2 [Text]")

        booked_date = (By.XPATH, f"(((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2])/div[3]//span)[1]", "Commercial Route Port: Booked Sail Date [Text]")
        date = (By.XPATH, f"(((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2])/div[3]//span)[2]", "Commercial Route Port: Date [Text]")

        # Return Dictionary with values
        data = {
            "port": self.get_text().set_locator(port, self._name).by_text(),
            "voyage": self.get_text().set_locator(voyage, self._name).by_text(),
            "vessel": self.get_text().set_locator(vessel, self._name).by_text(),
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "line_2": self.get_text().set_locator(line_2, self._name).by_text(),
            "booked_date": self.get_text().set_locator(booked_date, self._name).by_text(),
            "date": self.get_text().set_locator(date, self._name).by_text(),
        }
        return data

    def get_commercial_route_port_destination(self):
        port = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[2]/div[1]/div/span)[1]", "Commercial Route Port [Text]")
        line_1 = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[2]/div[1]/div/span)[2]", "Commercial Route Port [Text]")

        booked_date = (By.XPATH, f"(//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[3]/div/span", "Commercial Route Port: Booked Sail Date [Text]")
        date = (By.XPATH, f"(//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[3]/div/div/span", "Commercial Route Port: Date [Text]")

        # Return Dictionary with values
        data = {
            "port": self.get_text().set_locator(port, self._name).by_text(),
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "booked_date": self.get_text().set_locator(booked_date, self._name).by_text(),
            "date": self.get_text().set_locator(date, self._name).by_text(),
        }
        return data

    def get_commercial_route_empty_return(self):
        empty_return = (By.XPATH, f"(//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[4]/div[1]//span[2]", "Commercial Route Empty Return [Text]")
        line_1 = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[4]/div[2]//span)[1]", "Commercial Route Line 1 [Text]")
        line_2 = (By.XPATH, f"((//h6[text()='COMMERCIAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[4]/div[2]//span)[2]", "Commercial Route Line 2 [Text]")

        data = {
            "empty_return": self.get_text().set_locator(empty_return, self._name).by_text(),
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "line_2": self.get_text().set_locator(line_2, self._name).by_text(),
        }
        return data

    def get_commercial_route(self):
        commercial_route = {
            "empty_pick_up": self.get_commercial_route_empty_pick_up(),
            "port_origin": self.get_commercial_route_port_origin(),
            "port_destination": self.get_commercial_route_port_destination(),
            "empty_return": self.get_commercial_route_empty_return()
        }
        return commercial_route

    def get_operational_route_empty_pick_up(self):
        # Read Elements
        line_1 = (By.XPATH, f"({self._xpath_operational_route}//div[contains(@class,'booking-list-data-row')]/div/div/span[2])[1]", "Commercial Route Pick Up [Text]")
        line_2 = (By.XPATH, f"({self._xpath_operational_route}//div[contains(@class,'booking-list-data-row')]/div[2]/span[1])[1]", "Commercial Route Pick Up [Text]")
        line_3 = (By.XPATH, f"({self._xpath_operational_route}//div[contains(@class,'booking-list-data-row')]/div[2]/span[2])[1]", "Commercial Route Pick Up [Text]")

        # Return Dictionary with values
        data = {
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "line_2": self.get_text().set_locator(line_2, self._name).by_text(),
            "line_3": self.get_text().set_locator(line_3, self._name).by_text()
        }
        return data

    def get_operational_route_port_origin(self):
        # Read Elements
        port = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[1]/div/span[2]", "Commercial Route Port [Text]")
        voyage = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[1]/div[2]/div[1]/span[2]", "Commercial Route Voyage [Text]")
        vessel = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[1]/div[2]/div[2]/span[2]", "Commercial Route Vessel [Text]")

        line_1 = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[2]/div/span[1]", "Commercial Route Port: Line 1 [Text]")
        line_2 = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2]/div/div)[2]//span/span[1]", "Commercial Route Port: Line 2 [Text]")

        booked_date = (By.XPATH, f"(((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2])/div[3]//span)[1]", "Commercial Route Port: Booked Sail Date [Text]")
        date = (By.XPATH, f"(((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[2])/div[3]//span)[2]", "Commercial Route Port: Date [Text]")

        # Return Dictionary with values
        data = {
            "port": self.get_text().set_locator(port, self._name).by_text(),
            "voyage": self.get_text().set_locator(voyage, self._name).by_text(),
            "vessel": self.get_text().set_locator(vessel, self._name).by_text(),
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "line_2": self.get_text().set_locator(line_2, self._name).by_text(),
            "booked_date": self.get_text().set_locator(booked_date, self._name).by_text(),
            "date": self.get_text().set_locator(date, self._name).by_text(),
        }
        return data

    def get_operational_route_port_destination(self):
        port = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[2]/div[1]/div/span)[1]", "Commercial Route Port [Text]")
        line_1 = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[2]/div[1]/div/span)[2]", "Commercial Route Port [Text]")

        booked_date = (By.XPATH, f"(//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[3]/div/span", "Commercial Route Port: Booked Sail Date [Text]")
        date = (By.XPATH, f"(//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[3]/div[3]/div/div/span", "Commercial Route Port: Date [Text]")

        # Return Dictionary with values
        data = {
            "port": self.get_text().set_locator(port, self._name).by_text(),
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "booked_date": self.get_text().set_locator(booked_date, self._name).by_text(),
            "date": self.get_text().set_locator(date, self._name).by_text(),
        }
        return data

    def get_operational_route_empty_return(self):
        empty_return = (By.XPATH, f"(//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[4]/div[1]//span[2]", "Commercial Route Empty Return [Text]")
        line_1 = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[4]/div[2]//span)[1]", "Commercial Route Line 1 [Text]")
        line_2 = (By.XPATH, f"((//h6[text()='OPERATIONAL ROUTE']/../..//div[contains(@class,'booking-list-data-row')])[4]/div[2]//span)[2]", "Commercial Route Line 2 [Text]")

        data = {
            "empty_return": self.get_text().set_locator(empty_return, self._name).by_text(),
            "line_1": self.get_text().set_locator(line_1, self._name).by_text(),
            "line_2": self.get_text().set_locator(line_2, self._name).by_text(),
        }
        return data

    def get_operational_route(self):
        operational_route = {
            "empty_pick_up": self.get_operational_route_empty_pick_up(),
            "port_origin": self.get_operational_route_port_origin(),
            "port_destination": self.get_operational_route_port_destination(),
            "empty_return": self.get_operational_route_empty_return()
        }
        return operational_route
