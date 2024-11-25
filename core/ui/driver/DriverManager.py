from selenium import webdriver
from selenium.webdriver.edge.options import Options
from pathlib import Path

from core.config.logger_config import setup_logger
from core.ui.driver.DriversEnum import DriversEnum

logger = setup_logger('BasePage')
from appium.options.windows import WindowsOptions
from appium import webdriver as appium_webdriver

appium_server_url = 'http://localhost:4723'


class DriverManager:
    defaultBrowser = DriversEnum.CHROME.value
    time_out = ""
    download = ""
    browser = None
    driver = None
    project_root = Path(__file__).parent.parent

    # Constructor
    def __init__(self, browser, headless=False):

        if browser:
            self.browser = browser
        else:
            self.browser = self.defaultBrowser

        self.headless = headless

    def initialize(self):
        logger.debug("Initialize Web Driver...")
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
        logger.debug("Setting Edge Driver...")

        options = Options()
        if bool(self.headless):
            logger.debug("Adding --headless argument")
            options.add_argument("--headless")  # Headless mode
        # options.add_argument("--disable-gpu")  # Disabled GPU (recommended for headless)
        options.add_argument("--disable-dev-shm-usage")  # Shared memory for avoid issues
        options.add_argument("--no-sandbox")  # Restricted mode for avoid errors

        driver = webdriver.Edge(options=options)
        driver.maximize_window()
        return driver

    def firefox_driver(self):
        logger.debug("Setting Firefox Driver...")
        options = Options()
        if bool(self.headless):
            logger.debug("Adding --headless argument")
            options.add_argument("--headless")  # Headless mode

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        return driver

    def chrome_driver(self):
        logger.debug("Setting Chrome Driver...")
        options = Options()
        if bool(self.headless):
            logger.debug("Adding --headless argument")
            options.add_argument("--headless")  # Headless mode
        # options.add_argument("--disable-gpu")  # Disabled GPU (recommended for headless)
        options.add_argument("--disable-dev-shm-usage")  # Shared memory for avoid issues
        options.add_argument("--no-sandbox")  # Restricted mode for avoid errors

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    @classmethod
    def windows_pc(cls, app: str):
        logger.debug("Setting Windows PC...")

        # Driver Capabilities
        windows_options = WindowsOptions()
        windows_options.platform_name = 'Windows'
        windows_options.device_name = 'WindowsPC'
        windows_options.app = app

        logger.debug("APPLICATION: " + app)
        return appium_webdriver.Remote(appium_server_url, options=windows_options)
