import os
import time
import inspect
from threading import local
from core.config.logger_config import setup_logger

logger = setup_logger('BaseApp')

# Map ThreadLocal for WebDriver
_driver = local()


class BaseApp:
    # Static Variables
    project_root = os.getcwd()
    main_resources_path = os.path.join(project_root, 'resources')
    base_url_var = ""

    SEPARATOR = "\n**************************************************************************************************" \
                "************************************* "
    SEPARATOR_DASH = "\n---------------------------------------------------------------------------------------------" \
                     "------------------------------------------ "

    @classmethod
    def set_base_url(cls, value):
        cls.base_url_var = value

    @classmethod
    def get_base_url(cls):
        return cls.base_url_var

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
        logger.info("Pause: " + str(seconds))

        time.sleep(seconds)

    @staticmethod
    def get_back():
        BaseApp.get_driver().back()

    @staticmethod
    def get_forward():
        BaseApp.get_driver().forward()

    @staticmethod
    def get_refresh():
        BaseApp.get_driver().refresh()

    def go(self, base_url, url):
        driver = self.get_driver()
        if driver:
            url = str(base_url) + str(url)
            driver.get(url)
            logger.debug(f"Go: {url}")
        else:
            logger.error("Driver is not set.")

    @staticmethod
    def get_title():
        return BaseApp.get_driver().title

    @staticmethod
    def get_current_url():
        return BaseApp.get_driver().current_url

    @staticmethod
    def method_name():
        current_method_name = inspect.currentframe().f_back.f_code.co_name
        return current_method_name

    @staticmethod
    def build_path(path):
        return os.path.join(BaseApp.project_root, path)

    @staticmethod
    def main_resources(file_name):
        return os.path.join(BaseApp.main_resources_path, file_name)
