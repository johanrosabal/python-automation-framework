from selenium import webdriver
from selenium.webdriver.edge.options import Options
from pathlib import Path
from appium.options.windows import WindowsOptions
from appium import webdriver as appium_webdriver
from core.config.logger_config import setup_logger
from core.ui.driver.DriversEnum import DriversEnum
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.webdriver.edge.service import Service

logger = setup_logger('BasePage')

appium_server_url = 'http://localhost:4723'


class DriverManager:
    defaultBrowser = DriversEnum.CHROME.value
    time_out = ""
    download = ""
    browser = None
    driver = None
    project_root = Path(__file__).parent.parent.parent.parent

    # Constructor
    def __init__(self, browser, headless=False):

        if browser:
            self.browser = browser
        else:
            self.browser = self.defaultBrowser

        self.headless = headless
        self.downloads = f"{self.project_root}\\downloads"

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
        logger.info("Setting Edge Driver...")
        logger.info(f"Download Folder:{self.downloads}")

        options = Options()
        if bool(self.headless):
            logger.debug("Adding --headless argument")
            options.add_argument("--headless")  # Headless mode
        # options.add_argument("--disable-gpu")  # Disabled GPU (recommended for headless)
        options.add_argument("--disable-dev-shm-usage")  # Shared memory for avoid issues
        options.add_argument("----start-maximized")  #
        # Set the default zoom level to 80%
        options.add_argument("--force-device-scale-factor=0.8")
        options.add_argument("--zoom=0.8")  # This may not work directly; use CDP instead
        options.add_argument("--no-sandbox")  # Restricted mode for avoid errors
        # options.add_argument("--disable-notifications")  # Disable Browser Notifications
        options.add_argument("--disable-extensions")  # Disable Extensions Notifications
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument("--disable-popup-blocking")
        # options.add_argument("--auto-open-devtools-for-tabs")

        prefs = {
            "download.default_directory": self.downloads,  # Download Path
            "download.prompt_for_download": False,  # Disable confirmation window
            "download.directory_upgrade": True,  # Update route if it exists
            "notifications.enabled": True,  # Enable Notifications
            "profile.default_content_setting_values.notifications": 1,  # 1 to allow, 2 to block
            "profile.default_content_setting_values.popups": 0,
            "safebrowsing.enabled": True,  # Enable safe browsing
            "profile.default_content_setting_values.geolocation": 1,  # 1 to allow, 2 to block
            "profile.default_content_setting_values.cookies": 1,
            "profile.default_content_setting_values.javascript": 1,
            "profile.default_content_setting_values.protocol_handlers": 1,
            "profile.default_content_setting_values.images": 1,
            "profile.default_content_setting_values.plugins": 1,
            "profile.default_content_setting_values.clipboard": 1
        }
        options.add_experimental_option("prefs", prefs)

        service = Service(service_args=["--verbose", "--log-path=edge.log"])

        driver = webdriver.Edge(service=service, options=options)
        driver.maximize_window()
        driver.delete_all_cookies()
        logger.info("Return Edge Driver..........................")
        return driver

    def firefox_driver(self):
        logger.info("Setting Firefox Driver...")
        options = ffOptions()
        if bool(self.headless):
            logger.debug("Adding --headless argument")
            options.add_argument("--headless")  # Headless mode
            options.add_argument("--disable-notifications")  # Disable Browser Notifications
            options.add_argument("--disable-extensions")  # Disable Extensions Notifications
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-insecure-localhost')

        profile = {
            "browser.download.folderList": 2,
            "browser.download.dir": self.downloads,
            "browser.helperApps.neverAsk.saveToDisk": "application/pdf,application/octet-stream",
            "browser.download.manager.showWhenStarting": False,
            "pdfjs.disabled": True,  # Disable PDF preview,
            "profile.default_content_setting_values.notifications": 1  # 1 to allow, 2 to block
        }

        for key, value in profile.items():
            options.set_preference(key, value)

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        driver.delete_all_cookies()
        return driver

    def chrome_driver(self):
        logger.info("Setting Chrome Driver...")
        options = Options()
        if bool(self.headless):
            logger.debug("Adding --headless argument")
            options.add_argument("--headless")  # Headless mode
        # options.add_argument("--disable-gpu")  # Disabled GPU (recommended for headless)
        options.add_argument("--disable-dev-shm-usage")  # Shared memory for avoid issues
        options.add_argument("----start-maximized")  #
        # Set the default zoom level to 80%
        options.add_argument("--force-device-scale-factor=0.8")
        options.add_argument("--zoom=0.8")  # This may not work directly; use CDP instead
        options.add_argument("--no-sandbox")  # Restricted mode for avoid errors
        # options.add_argument("--disable-notifications")  # Disable Browser Notifications
        options.add_argument("--disable-extensions")  # Disable Extensions Notifications
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')

        prefs = {
            "download.default_directory": self.downloads,  # Download Path
            "download.prompt_for_download": False,  # Disable confirmation window
            "download.directory_upgrade": True,  # Update route if it exists
            "notifications.enabled": True,  # Enable Notifications
            "safebrowsing.enabled": True,  # Enable safe browsing
            "profile.default_content_setting_values.geolocation": 1,  # 1 to allow, 2 to block
            "profile.default_content_setting_values.notifications": 1,  # 1 to allow, 2 to block
            "profile.default_content_setting_values.popups": 0,
            "profile.default_content_setting_values.cookies": 1,
            "profile.default_content_setting_values.javascript": 1,
            "profile.default_content_setting_values.protocol_handlers": 1,
            "profile.default_content_setting_values.images": 1,
            "profile.default_content_setting_values.plugins": 1,
            "profile.default_content_setting_values.clipboard": 1
        }
        options.add_experimental_option("prefs", prefs)
        service = Service(service_args=["--verbose", "--log-path=edge.log"])
        driver = webdriver.Chrome(service=service, options=options)

        driver.maximize_window()
        driver.delete_all_cookies()
        logger.info("Return Chrome Driver..........................")
        return driver

    @classmethod
    def windows_pc(cls, app: str):
        logger.info("Setting Windows PC...")

        # Driver Capabilities
        windows_options = WindowsOptions()
        windows_options.platform_name = 'Windows'
        windows_options.device_name = 'WindowsPC'
        windows_options.app = app

        logger.debug("APPLICATION: " + app)
        return appium_webdriver.Remote(appium_server_url, options=windows_options)
