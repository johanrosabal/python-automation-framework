
from selenium import webdriver
from pathlib import Path

from core.config.logger_config import setup_logger
from core.ui.driver.DriversEnum import DriversEnum

logger = setup_logger('BasePage')


class DriverManager:

    defaultBrowser = DriversEnum.CHROME.value
    time_out = ""
    download = ""
    browser = None
    driver = None
    project_root = Path(__file__).parent.parent

    # Constructor
    def __init__(self, browser):

        if browser:
            self.browser = browser
        else:
            self.browser = self.defaultBrowser

    def initialize(self):
        logger.info("Initialize Web Driver...")
        if self.browser == "chrome":
            return self.chrome_driver()
        elif self.browser == "edge":
            return self.edge_driver()
        elif self.browser == "firefox":
            return self.firefox_driver()
        else:
            logger.info("Default Web Driver: Chrome")
            return self.chrome_driver()

    def edge_driver(self):
        logger.info("Setting Edge Driver...")
        return webdriver.Edge()

    def firefox_driver(self):
        logger.info("Setting Firefox Driver...")
        return webdriver.Firefox()

    def chrome_driver(self):
        logger.info("Setting Chrome Driver...")
        return webdriver.Chrome()
