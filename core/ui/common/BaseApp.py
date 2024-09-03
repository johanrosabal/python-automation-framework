import os
import time
import inspect
from threading import local
from core.config.logger_config import setup_logger
from core.ui.actions.Navigation import Navigation

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
    def quit_driver():
        if _driver:
            getattr(_driver, 'instance', None).quit()

    @staticmethod
    def pause(seconds):
        logger.info("Pause: " + str(seconds))
        time.sleep(seconds)

    def navigation(self):
        return Navigation(self.get_driver())

    @staticmethod
    def method_name():
        current_method_name = inspect.currentframe().f_back.f_code.co_name
        return current_method_name

    @staticmethod
    def get_project_root():
        return os.path.join(BaseApp.project_root)

    @staticmethod
    def main_resources(file_name):
        return os.path.join(BaseApp.main_resources_path, file_name)
