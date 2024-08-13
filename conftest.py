import pytest
import yaml

from pathlib import Path
from core.config.logger_config import setup_logger

logger = setup_logger('BaseTest')


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == 'call':
        outcome = 'PASSED' if call.excinfo is None else 'FAILED'
        test_case_id = getattr(item.function, 'test_case_id', 'No ID')
        test_description = getattr(item.function, 'test_description', 'No Description')
        logger.info(
            "\n****************************************************************************************************" +
            "\n\tTest Name: " + str(item.name) +
            "\n----------------------------------------------------------------------------------------------------" +
            "\n\t\t- Test Case ID: " + str(test_case_id) +
            "\n\t\t- Description: " + str(test_description) +
            "\n\t\t- Result: " + str(outcome) +
            "\n****************************************************************************************************"
        )
        for handler in logger.handlers:
            handler.flush()  # Ensure logs are flushed to the output


def pytest_addoption(parser):
    parser.addoption("--profile", action="store", default="qa", choices=("dev","qa","uat","prod"),
                     help="Profile to use (e.g. dev, qa, uat, prod)")
    parser.addoption("--app-name", action="store", default="demo", help="Application name (e.g. demo)")
    parser.addoption("--app-type", action="store", default="web", choices=("web","desktop","api"),
                     help="Profile to use (e.g. web, desktop, api)")


@pytest.fixture(scope='session')
def config(request):
    profile = request.config.getoption("--profile")
    app_name = request.config.getoption("--app-name")
    app_type = request.config.getoption("--app-type")

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
