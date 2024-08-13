import pytest

from core.config.logger_config import setup_logger
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp
from core.ui.driver.DriverManager import DriverManager
from core.ui.driver.DriversEnum import DriversEnum

logger = setup_logger('BaseTest')


@pytest.fixture
def base_url(config):
    value = config.get('web', {}).get('base_url')
    logger.info("BASE URL: " + value)
    return value


@pytest.fixture
def user(config):
    user_dto = UserDTO(user_name=config.get('user', {}).get('name'),
                       user_password=config.get('user', {}).get('password'))
    logger.info("USER: " + user_dto.__str__())
    return user_dto


class BaseTest(BaseApp):

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self, config):
        logger.debug("Base Test Execution:" + self.SEPARATOR)
        browser = DriversEnum.CHROME.value
        logger.info("Setting Browser Driver: " + str(browser) + self.SEPARATOR)
        driver = DriverManager(browser).initialize()
        value = config.get('web', {}).get('base_url')
        BaseApp.set_base_url(value)
        logger.info("BASE URL: " + BaseApp.get_base_url())

        # self.set_driver(driver)
        BaseApp.set_driver(driver)

        yield

        driver.quit()
