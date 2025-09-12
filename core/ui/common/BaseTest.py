import pytest
from pathlib import Path
from core.config.logger_config import setup_logger
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp
from core.ui.driver.DriverManager import DriverManager
from core.utils.table_formatter import TableFormatter
from core.config.config_cmd import get_profile, get_browser, get_app_type, get_app_name, get_headless
from core.config.config_loader import load_web_config
from core.ui.report.WEBTestReport import WEBTestReport
from tabulate import tabulate

logger = setup_logger('BaseTest')


@pytest.fixture
def user(config):
    user_dto = UserDTO(
        user_name=str(config.get('user', {}).get('username')),
        user_password=str(config.get('user', {}).get('password'))
    )
    logger.info("USER DTO: " + user_dto.__str__())
    return user_dto


@pytest.fixture
def downloads():
    project_root = Path(__file__).parent.parent.parent.parent
    downloads = f"{project_root}\\downloads"
    return downloads


class BaseTest(BaseApp):
    report = WEBTestReport()

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self):
        # Use class attributes as defaults
        profile = get_profile() or getattr(self, "profile", None) or "qa"
        app_name = get_app_name() or getattr(self, "app_name", None) or "demo"
        browser = get_browser() or getattr(self, "browser", None) or "chrome"
        app_type = get_app_type() or getattr(self, "app_type", None) or "web"
        # headless = get_headless() or getattr(self, "headless", None) or False
        headless = True

        # Load configurations
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        config_path = f"{project_root}/applications/{app_type}/{app_name}/config/{profile}_config.yaml"
        config_yaml = load_web_config(config_path)

        # Load Default Browser in Yaml File, in case not arguments or project decorator
        if not browser:
            browser = config_yaml.web.browser

        # Setup driver and base URL
        base_url = config_yaml.web.base_url
        driver = DriverManager(browser, headless).initialize()
        # Detect Javascript Console Errors
        for log in driver.get_log('browser'):
            logger.error(log)

        BaseApp.set_base_url(base_url)
        BaseApp.set_driver(driver)

        # Logging Configurations
        config_dict = {
            "application_name": config_yaml.name,
            "base_url": config_yaml.web.base_url,
            "browser": browser,
            "profile": profile,
            "headless": headless,
            "username": config_yaml.user.username,
            "password": config_yaml.user.password
        }

        TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()
        logger.info(f"Running with profile: {profile}, app_name: {app_name}, app_type: {app_type}, browser: {browser}, headless: {headless}")

        yield

        BaseApp.quit_driver()

    @classmethod
    def add_report(cls, test_data, errors=None):
        if errors is None:
            errors = []
        table = []

        result = {
            "Test Case ID": test_data.test_case_id,
            "Test Name": test_data.test_description,
            "Status": "PASS" if len(errors) == 0 else "FAIL",
            "Errors": errors if len(errors) != 0 else "-"
        }

        table.append(result)

        headers = list(table[0].keys())
        formatted_results = [[result[header] for header in headers] for result in table]
        logger.info("\n" + tabulate(formatted_results, headers=headers, tablefmt='pretty'))
        cls.report.add_result(result)
        if errors:
            pytest.fail("\n".join(errors))

    @classmethod
    def teardown_class(cls):
        # Create Report on Console
        cls.report.generate_report()
