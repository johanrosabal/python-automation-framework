import pytest
import yaml
from pathlib import Path
from core.config.logger_config import setup_logger
from core.config.config_cmd import get_profile, get_app_name, get_app_type
from core.config.config_loader import load_api_config, load_web_config, load_desktop_config
from core.ui.common.BaseApp import BaseApp
from core.utils.table_formatter import TableFormatter
from core.api.common.BaseApi import BaseApi

logger = setup_logger('BaseTest')


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == 'call':
        outcome = 'PASSED' if call.excinfo is None else 'FAILED'
        test_case_id = getattr(item.function, 'test_case_id', 'No ID')
        test_description = getattr(item.function, 'test_description', 'No Description')
        logger.info(
            f"\n****************************************************************************************************" +
            f"\n\tTest Result: {item.name} -> " + str(outcome) +
            f"\n----------------------------------------------------------------------------------------------------"
        )
        for handler in logger.handlers:
            handler.flush()  # Ensure logs are flushed to the output


def pytest_runtest_protocol(item, nextitem):
    logger.info("\n" + "=" * 50)  # Line Decoration
    test_case_id = getattr(item.function, 'test_case_id', 'No ID')
    test_description = getattr(item.function, 'test_description', 'No Description')
    logger.info(
        f"\n****************************************************************************************************" +
        "\n\t\tTest Name:" + str(item.name) +
        "\n----------------------------------------------------------------------------------------------------" +
        "\n\t\tTest Case ID: " + str(test_case_id) +
        "\n\t\tDescription: " + str(test_description) +
        "\n----------------------------------------------------------------------------------------------------"
    )
    return None


def pytest_addoption(parser):
    parser.addoption("--profile", action="store", default="qa", choices=("dev", "qa", "uat", "prod"),
                     help="Profile to use (e.g. dev, qa, uat, prod)")
    parser.addoption("--app-name", action="store", default="demo", help="Application name (e.g. demo)")
    parser.addoption("--app-type", action="store", default="web", choices=("web", "desktop", "api"),
                     help="Profile to use (e.g. web, desktop, api)")
    parser.addoption("--browser", action="store", default="chrome", choices=("firefox", "edge", "chrome"),
                     help="Browser to use (e.g. firefox, chrome, edge)")
    parser.addoption("--headless", action="store", default="False", choices=("True", "False"),
                     help="Headlesss to use (e.g. True, False)")


@pytest.fixture(scope='class')
def config(request):
    # Defaults from CLI or class attributes
    profile = request.config.getoption("--profile")
    app_name = request.config.getoption("--app-name")
    app_type = request.config.getoption("--app-type")


    # Try to get values from the class decorator
    test_class = getattr(request.node, 'cls', None)
    if test_class:
        profile = getattr(test_class, "profile", profile)
        app_name = getattr(test_class, "app_name", app_name)
        app_type = getattr(test_class, "app_type", app_type)

    # Fallback defaults
    profile = profile or "qa"
    app_name = app_name or "demo"
    app_type = app_type or "web"

    # Root Project
    project_root = Path(__file__).resolve().parent
    print(f"{project_root}")

    # Define the path based on the application and profile
    config_path = project_root / f'applications/{app_type}/{app_name}/config/{profile}_config.yaml'
    print(f"Config path: {config_path}")

    if not config_path.exists():
        raise FileNotFoundError(f"The config file {config_path} does not exist.")

    # Read the YAML file
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Return the configuration for use in tests
    return config_data


@pytest.fixture(scope='class')
def load_yaml_config(request):
    # Defaults from CLI or class attributes
    profile = get_profile()
    app_name = get_app_name()
    app_type = get_app_type()

    # Try to get values from the class decorator
    test_class = getattr(request.node, 'cls', None)
    if test_class:
        profile = getattr(test_class, "profile", profile)
        app_name = getattr(test_class, "app_name", app_name)
        app_type = getattr(test_class, "app_type", app_type)


    # Fallback defaults
    profile = profile or "qa"
    app_name = app_name or "demo"
    app_type = app_type or "web"

    # Root Project
    project_root = Path(__file__).resolve().parent

    # Define the path based on the application and profile
    config_path = f"{project_root}/applications/{app_type}/{app_name}/config/{profile}_config.yaml"

    # Load Profile Configurations
    config_yaml = load_api_config(config_path)

    # Logging Configurations
    config_dict = {
        "application_name": config_yaml.name,
        "base_url": config_yaml.api.base_url,
        "base_token_url": config_yaml.api.base_token_url,
        "grant_type": config_yaml.api.grant_type,
        "client_id": config_yaml.api.client_id,
        "client_secret": config_yaml.api.client_secret,
        "username": config_yaml.user.username,
        "password": config_yaml.user.password
    }
    BaseApi.set_base_url(config_yaml.api.base_url)
    TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()
    yield config_dict
