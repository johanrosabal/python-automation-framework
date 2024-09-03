import pytest
import os
from core.config.logger_config import setup_logger
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp
from core.ui.driver.DriverManager import DriverManager
from core.utils.table_formatter import TableFormatter
from core.config.config_cmd import get_profile, get_browser
from core.config.config_loader import load_web_config

logger = setup_logger('BaseTest')


@pytest.fixture
def user(config):
    user_dto = UserDTO(
        user_name=config.get('user', {}).get('username'),
        user_password=config.get('user', {}).get('password')
    )
    logger.info("USER DTO: " + user_dto.__str__())
    return user_dto


class BaseTest(BaseApp):

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self):
        # Load Profile Execution
        profile = get_profile()
        browser = get_browser()
        if not profile:
            profile = "qa"  # Default Value

        # Load Profile Configurations
        config_yaml = load_web_config(f"../config/{profile}_config.yaml")

        if not browser:
            browser = config_yaml.web.browser

        base_url = config_yaml.web.base_url
        driver = DriverManager(browser).initialize()
        BaseApp.set_base_url(base_url)
        BaseApp.set_driver(driver)

        # Logging Configurations
        config_dict = {
            "application_name": config_yaml.name,
            "base_url": config_yaml.web.base_url,
            "browser": browser,
            "profile" : profile,
            "username": config_yaml.user.username,
            "password": config_yaml.user.password
        }

        TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()

        yield

        BaseApp.quit_driver()

