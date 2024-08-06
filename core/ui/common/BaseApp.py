import os
from threading import local

from core.config.logger_config import setup_logger

logger = setup_logger('BaseApp')

# Map ThreadLocal for WebDriver
_driver = local()


class BaseApp:
    # Static Variables
    base_url = None
    application = None
    project_root = os.getcwd()
    main_resources_path = os.path.join(project_root, 'resources')

    SEPARATOR = "\n**************************************************************************************************" \
                "************************************* "
    SEPARATOR_DASH = "\n---------------------------------------------------------------------------------------------" \
                     "------------------------------------------ "

    @property
    def driver(self):
        return _driver.instance

    @driver.setter
    def driver(self, driver):
        _driver.instance = driver

    @staticmethod
    def get_driver():
        return getattr(_driver, 'instance', None)

    @staticmethod
    def set_driver(driver):
        _driver.instance = driver

    @staticmethod
    def pause(seconds):
        logger.info("Pause")
        import time
        time.sleep(seconds)

    @staticmethod
    def back():
        _driver.back()

    @staticmethod
    def forward():
        BaseApp.get_driver().forward()

    @staticmethod
    def refresh():
        BaseApp.get_driver().refresh()

    def go(self, url):
        driver = self.get_driver()
        if driver:
            driver.get(url)
            logger.info(f"Going to {url}")
        else:
            logger.error("Driver is not set.")

    @staticmethod
    def build_path(path):
        return os.path.join(BaseApp.project_root, path)

    @staticmethod
    def main_resources(file_name):
        return os.path.join(BaseApp.main_resources_path, file_name)

    # @staticmethod
    # def token():
    #     # Implementar la clase Token si es necesario
    #     return Token(BaseApp.get_driver())

    @staticmethod
    def get_title():
        return BaseApp.get_driver().title

    @staticmethod
    def get_application():
        return BaseApp.application

    # @staticmethod
    # def screenshots():
    #     logger.debug("Screenshots")
    #     return Screenshots(BaseApp.get_driver())
    @classmethod
    def check_logs_messages(cls):
        logger.info("This is an info message")
        logger.debug("This is a debug message")
        logger.error("This is an error message")
