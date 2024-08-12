import logging
import pytest

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.driver.DriverManager import DriverManager
from core.ui.driver.DriversEnum import DriversEnum

logger = setup_logger('BaseTest')


class BaseTest(BaseApp):

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self):

        logger.debug("Base Test Execution:" + self.SEPARATOR)

        browser = DriversEnum.CHROME.value
        logger.info("Setting Browser Driver: " + str(browser) + self.SEPARATOR)
        driver = DriverManager(browser).initialize()
        # self.set_driver(driver)
        BaseApp.set_driver(driver)

        yield
        driver.quit()
