import os

import pytest
import yaml
import shutil
from pathlib import Path
from core.config.logger_config import setup_logger
from core.config.config_cmd import get_profile, get_app_name, get_app_type, get_app_endpoint, get_app_module
from core.config.config_loader import load_api_config, load_iq_api_config, load_web_softship_config
from core.utils.table_formatter import TableFormatter

from core.ui.driver.DriverManager import DriverManager
from applications.web.loadiq.pages.login.LoginPage import LoginPage
from applications.web.loadiq.config.sub_application import CustomerAccounts
from core.api.common.BaseApi import BaseApi
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('conftest')

# Global variable to store test results for final summary
test_results_summary = []


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == 'call':
        outcome = 'PASSED' if call.excinfo is None else 'FAILED'

        # Extract test case information
        test_case_id = getattr(item.function, 'test_case_id', 'No ID')
        test_description = getattr(item.function, 'test_description', 'No Description')

        # Store test result for summary
        test_results_summary.append({
            'test_name': item.name,
            'test_case_id': test_case_id,
            'description': test_description,
            'result': outcome,
            'duration': call.duration if hasattr(call, 'duration') else 0
        })

        logger.info(
            f"\n****************************************************************************************************" +
            f"\n\tTest Result: {item.name} -> " + str(outcome) +
            f"\n\tTest Case ID: {test_case_id}" +
            f"\n\tDescription: {test_description}" +
            f"\n----------------------------------------------------------------------------------------------------"
        )
        for handler in logger.handlers:
            handler.flush()  # Ensure logs are flushed to the output


def pytest_sessionfinish(session, exitstatus):
    """Hook that runs at the end of the entire test session"""
    logger.info("\n" + "=" * 120)
    logger.info("                                    TEST EXECUTION SUMMARY")
    logger.info("=" * 120)

    total_tests = len(test_results_summary)
    passed_tests = len([t for t in test_results_summary if t['result'] == 'PASSED'])
    failed_tests = len([t for t in test_results_summary if t['result'] == 'FAILED'])

    logger.info(f"Total Tests Executed: {total_tests}")
    logger.info(f"Passed: {passed_tests}")
    logger.info(f"Failed: {failed_tests}")
    logger.info(f"Success Rate: {(passed_tests / total_tests * 100):.2f}%" if total_tests > 0 else "0%")
    logger.info("=" * 120)

    # Create a formatted table with all test results
    if test_results_summary:
        # Prepare data for table formatting
        table_data = []
        for test_result in test_results_summary:
            status_symbol = "✓" if test_result['result'] == 'PASSED' else "✗"
            table_data.append({
                'Status': status_symbol,
                'Test Case ID': test_result['test_case_id'],
                'Test Name': test_result['test_name'],
                'Description': test_result['description'],
                'Result': test_result['result'],
                'Duration (s)': f"{test_result['duration']:.2f}"
            })

        # Use TableFormatter to create a formatted table
        table_formatter = TableFormatter()
        table_formatter.prepare_list(table_data)

        logger.info("\n" + "=" * 120)
        logger.info("                                    DETAILED TEST RESULTS")
        logger.info("=" * 120)
        logger.info(f"  {table_formatter.to_pretty()}")
        logger.info("=" * 120)

    """# Individual test results summary
    logger.info("\n" + "=" * 120)
    logger.info("                                  INDIVIDUAL TEST RESULTS")
    logger.info("=" * 120)

    for test_result in test_results_summary:
        status_symbol = "✓" if test_result['result'] == 'PASSED' else "✗"
        logger.info(
            f"{status_symbol} [{test_result['test_case_id']}] {test_result['test_name']}"
        )
        logger.info(f"   Description: {test_result['description']}")
        logger.info(f"   Result: {test_result['result']}")
        logger.info(f"   Duration: {test_result['duration']:.2f}s")
        logger.info("-" * 120)
    
    logger.info("=" * 120)
    logger.info("                                   END OF TEST EXECUTION")
    logger.info("=" * 120)"""


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

    parser.addoption("--endpoint", action="store", default="web", choices=("loadboard", "trackntrace", "user_management",
                                                                           "location", "tmsexchange", "web"),
                     help="Endpoint to use (e.g. loadboard, user_management....)")

    parser.addoption("--module", action="store", default="finance", choices=("True", "False"),
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


@pytest.fixture(scope='class')
def softship_yaml_config(request):
    # Defaults from CLI or class attributes
    profile = get_profile()
    app_name = get_app_name()
    app_type = get_app_type()
    app_module = get_app_module()

    # Try to get values from the class decorator
    test_class = getattr(request.node, 'cls', None)
    if test_class:
        profile = getattr(test_class, "profile", profile)
        app_name = getattr(test_class, "app_name", app_name)
        app_type = getattr(test_class, "app_type", app_type)
        app_module = getattr(test_class, "app_module", app_type)

    # Fallback defaults
    profile = profile or "qa"
    app_name = app_name or "demo"
    app_type = app_type or "web"
    app_module = app_module or "configuration"

    # Root Project
    project_root = Path(__file__).resolve().parent

    # Define the path based on the application and profile
    config_path = f"{project_root}/applications/{app_type}/{app_name}/config/{profile}_config.yaml"

    # Load Profile Configurations
    config_yaml = load_web_softship_config(config_path)

    # Logging Configurations
    config_dict = {
        "application_name": config_yaml.name,
        "base_url": config_yaml.web.base_url,
        "username": config_yaml.user.username,
        "password": config_yaml.user.password
    }

    modules = {}
    modules_base_url = None
    if app_module == "contracts":
        modules_base_url = config_yaml.modules.contracts
    elif app_module == "finance":
        modules_base_url = config_yaml.modules.finance
    elif app_module == "commercial":
        modules_base_url = config_yaml.modules.commercial
    elif app_module == "configuration":
        modules_base_url = config_yaml.modules.configuration
    elif app_module == "booking":
        modules_base_url = config_yaml.modules.booking
    elif app_module == "sof":
        modules_base_url = config_yaml.modules.sof
    elif app_module == "master_data":
        modules_base_url = config_yaml.master_data.sof
    else:
        app_module = "Intermodule"

    if app_module is None:
        logger.error("Module Not Defined")
    else:
        # Base URL for Endpoint Execution
        config_dict["module"] = app_module
        # Set Environment Modules
        modules["contracts"] = config_yaml.modules.contracts
        modules["finance"] = config_yaml.modules.finance
        modules["commercial"] = config_yaml.modules.commercial
        modules["configuration"] = config_yaml.modules.configuration
        modules["booking"] = config_yaml.modules.booking
        modules["sof"] = config_yaml.modules.sof
        modules["master_data"] = config_yaml.modules.master_data

        # Set Global Environments
        BaseApp.set_modules(modules)

    BaseApp.set_base_url(modules_base_url)
    TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()

    yield config_dict


''''
 Custom Fixture for LoadIQ API Project, to Read the Endpoint Configuration File or Terminal Commands Specifications.
 By Default Loads 'loadboard' endpoint from configuration file
'''


@pytest.fixture(scope='class')
def load_iq_yaml_config(request):
    # Defaults from CLI or class attributes
    profile = get_profile()
    app_name = get_app_name()
    app_type = get_app_type()
    app_endpoint = get_app_endpoint()
    login_account = None

    # Try to get values from the class decorator
    test_class = getattr(request.node, 'cls', None)
    if test_class:
        profile = getattr(test_class, "profile", profile)
        app_name = getattr(test_class, "app_name", app_name)
        app_type = getattr(test_class, "app_type", app_type)
        app_endpoint = getattr(test_class, "app_endpoint", app_endpoint)
        login_account = getattr(test_class, "login_account", None)

    # Fallback defaults
    profile = profile or "qa"
    app_name = app_name or "demo"
    app_type = app_type or "web"
    app_endpoint = app_endpoint or "loadboard"
    login_account = login_account or CustomerAccounts.TEST_07

    # Root Project
    project_root = Path(__file__).resolve().parent

    # Define the path based on the application and profile
    config_path = f"{project_root}/applications/{app_type}/{app_name}/config/{profile}_config.yaml"

    # Load Profile Configurations
    config_yaml = load_iq_api_config(config_path)

    # Logging Configurations
    config_dict = {
        "application_name": config_yaml.name,
        "base_url": config_yaml.api.base_url,
        "base_token_url": config_yaml.api.base_token_url,
        "grant_type": config_yaml.api.grant_type,
        "client_id": config_yaml.api.client_id,
        "client_secret": config_yaml.api.client_secret,
        "username": config_yaml.user.username,
        "password": config_yaml.user.password,
    }

    # Endpoints Dictionary, this will be pass to BaseAPI class to share this values with the 'Endpoint' child classes
    endpoints = {}

    endpoint_base_url = None
    if app_endpoint == "loadboard":
        endpoint_base_url = config_yaml.endpoints.loadboard
    elif app_endpoint == "trackntrace":
        endpoint_base_url = config_yaml.endpoints.trackntrace
    elif app_endpoint == "user_management":
        endpoint_base_url = config_yaml.endpoints.user_management
    elif app_endpoint == "location":
        endpoint_base_url = config_yaml.endpoints.location
    elif app_endpoint == "tmsexchange":
        endpoint_base_url = config_yaml.endpoints.tmsexchange
    else:
        endpoint_base_url = None

    if endpoint_base_url is None:
        logger.error("Endpoint Not Defined")
    else:
        # Base URL for Endpoint Execution
        config_dict["endpoint"] = endpoint_base_url
        # Set Environment Variable
        endpoints["loadboard"] = config_yaml.endpoints.loadboard
        endpoints["trackntrace"] = config_yaml.endpoints.trackntrace
        endpoints["user_management"] = config_yaml.endpoints.user_management
        endpoints["location"] = config_yaml.endpoints.location
        endpoints["tmsexchange"] = config_yaml.endpoints.tmsexchange
        endpoints["web"] = config_yaml.api.base_url
        # Set Global Environments
        BaseApi.set_endpoints(endpoints)

    BaseApi.set_base_url(endpoint_base_url)
    TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()
    # Initialize Driver Manager to obtain the JWT Token and Custom Token from local storage, running on headless mode
    driver = DriverManager("edge", True).initialize()
    base_url = config_yaml.api.base_url
    # ReUse Login Class From Load IQ Login Page with a New Custom Method 'load_page_with_base_url'
    LoginPage(driver) \
        .load_page_with_base_url(base_url) \
        .login_user(login_account) \
        .is_login_successful()
    # After making the user login verification Extract 'jwt_access_token' and 'customtoken'
    custom_token = driver.execute_script("return window.localStorage.getItem('customtoken');")
    BaseApi.set_custom_token(custom_token)

    jwt_access_token = driver.execute_script("return window.localStorage.getItem('jwt_access_token');")
    BaseApi.set_jwt_access_token("Bearer " + jwt_access_token)

    logger.info(f"Bear Token:{jwt_access_token}")
    logger.info(f"Custom Token:{custom_token}")

    driver.quit()

    yield config_dict


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))

@pytest.fixture(scope='class')
def csight_yaml_config(request):
    # Defaults from CLI or class attributes
    profile = get_profile()
    app_name = get_app_name()
    app_type = get_app_type()
    app_endpoint = get_app_endpoint()

    # Try to get values from the class decorator
    test_class = getattr(request.node, 'cls', None)
    if test_class:
        profile = getattr(test_class, "profile", profile)
        app_name = getattr(test_class, "app_name", app_name)
        app_type = getattr(test_class, "app_type", app_type)
        app_endpoint = getattr(test_class, "app_endpoint", app_endpoint)

    # Fallback defaults
    profile = profile or "qa"
    app_name = app_name or "csight"
    app_type = app_type or "api"

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
        "password": config_yaml.user.password,
    }

    BaseApi.set_base_url(config_dict["base_url"])

    TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()

    BaseApi.set_client_id(config_dict["client_id"])
    BaseApi.set_client_secret(config_dict["client_secret"])

    logger.info(f"Client ID:{BaseApi.get_client_id()}")
    logger.info(f"Client Secret:{BaseApi.get_client_secret()}")

    yield config_dict

# Fixture to load configuration from a YAML file for use in tests
@pytest.fixture(scope='class')
def load_iq_yaml_blueyonder_config(request):
    # Defaults from CLI or class attributes
    profile = get_profile()
    app_name = get_app_name()
    app_type = get_app_type()
    app_endpoint = get_app_endpoint()

    # Try to get values from the class decorator
    test_class = getattr(request.node, 'cls', None)
    if test_class:
        profile = getattr(test_class, "profile", profile)
        app_name = getattr(test_class, "app_name", app_name)
        app_type = getattr(test_class, "app_type", app_type)
        app_endpoint = getattr(test_class, "app_endpoint", app_endpoint)

    # Fallback defaults
    profile = profile or "qa"
    app_name = app_name or "demo"
    app_type = app_type or "web"
    app_endpoint = app_endpoint or "loadboard"

    # Root Project
    project_root = Path(__file__).resolve().parent

    # Define the path based on the application and profile
    config_path = f"{project_root}/applications/{app_type}/{app_name}/config/{profile}_config.yaml"

    # Load Profile Configurations
    config_yaml = load_iq_api_config(config_path)

    # Logging Configurations
    config_dict = {
        "application_name": config_yaml.name,
        "base_url": config_yaml.api.base_url,
        "base_token_url": config_yaml.api.base_token_url,
        "grant_type": config_yaml.api.grant_type,
        "client_id": config_yaml.api.client_id,
        "client_secret": config_yaml.api.client_secret
    }

    # Endpoints Dictionary, this will be pass to BaseAPI class to share this values with the 'Endpoint' child classes
    endpoints = {}

    if app_endpoint == "loadboard":
        endpoint_base_url = config_yaml.endpoints.loadboard
    elif app_endpoint == "trackntrace":
        endpoint_base_url = config_yaml.endpoints.trackntrace
    elif app_endpoint == "user_management":
        endpoint_base_url = config_yaml.endpoints.user_management
    elif app_endpoint == "location":
        endpoint_base_url = config_yaml.endpoints.location
    elif app_endpoint == "tmsexchange":
        endpoint_base_url = config_yaml.endpoints.tmsexchange
    else:
        endpoint_base_url = None

    if endpoint_base_url is None:
        logger.error("Endpoint Not Defined")
    else:
        # Base URL for Endpoint Execution
        config_dict["endpoint"] = endpoint_base_url
        # Set Environment Variable
        endpoints["loadboard"] = config_yaml.endpoints.loadboard
        endpoints["trackntrace"] = config_yaml.endpoints.trackntrace
        endpoints["user_management"] = config_yaml.endpoints.user_management
        endpoints["location"] = config_yaml.endpoints.location
        endpoints["tmsexchange"] = config_yaml.endpoints.tmsexchange
        endpoints["web"] = config_yaml.api.base_url
        # Set Global Environments
        BaseApi.set_endpoints(endpoints)

    BaseApi.set_base_url(config_dict["base_url"])

    TableFormatter().set_dictionary(config_dict).set_headers({"Config Key", "Config Value"}).to_pretty()

    BaseApi.set_client_id(config_dict["client_id"])
    BaseApi.set_client_secret(config_dict["client_secret"])

    logger.info(f"Client ID:{BaseApi.get_client_id()}")
    logger.info(f"Client Secret:{BaseApi.get_client_secret()}")

    yield config_dict


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Runs after pytest configuration but before test collection.
    This is the RIGHT time to clean Allure results.
    """
    config = session.config

    print("\n" + "=" * 80)
    print(f"🔧 pytest_sessionstart: Configuring Allure & Logs")
    print(f"📁 Project root: {config.rootdir}")
    print(f"📁 Current dir: {Path.cwd()}")

    # ========================================================================
    # FORCE PROJECT ROOT
    # ========================================================================
    project_root = Path(config.rootdir)

    # ========================================================================
    # CONFIGURE ALLURE RESULTS DIRECTORY
    # ========================================================================
    allure_dir = project_root / "reports" / "allure-results"

    # Set environment variable (Allure reads this directly)
    os.environ['ALLURE_RESULTS_DIR'] = str(allure_dir.absolute())

    # Override pytest option
    config.option.alluredir = str(allure_dir.absolute())

    # 🔥 CLEAN PREVIOUS RESULTS (with error handling)
    if allure_dir.exists():
        try:
            print(f"🧹 Cleaning previous Allure results: {allure_dir}")
            shutil.rmtree(allure_dir, ignore_errors=False, onerror=remove_readonly)
            print(f"✅ Cleaned: {allure_dir}")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean {allure_dir}: {e}")
            print(f"   Trying alternative method...")
            # Alternative: Delete files one by one
            for file in allure_dir.glob('*'):
                try:
                    if file.is_file():
                        file.unlink()
                    else:
                        shutil.rmtree(file)
                except Exception as inner_e:
                    print(f"   ⚠️  Could not delete {file}: {inner_e}")

    # Create directory
    allure_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {allure_dir.absolute()}")

    # ========================================================================
    # CONFIGURE LOG FILE AT PROJECT ROOT
    # ========================================================================
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "python-framework_pytest-logs.txt"
    config.option.log_file = str(log_file.absolute())

    print(f"📝 Log file: {log_file.absolute()}")

    # ========================================================================
    # PRINT CONFIGURATION SUMMARY
    # ========================================================================
    # print("\n" + "=" * 80)
    # print(f"📁 PROJECT ROOT: {project_root}")
    # print(f"📁 WORKING DIRECTORY: {Path.cwd()}")
    # print(f"📁 ALLURE RESULTS: {allure_dir.absolute()}")
    # print(f"📁 LOG FILE: {log_file.absolute()}")
    # print("=" * 80 + "\n")


def remove_readonly(func, path, excinfo):
    """
    Error handler for shutil.rmtree() on Windows.
    Clears readonly attribute and retries.
    """
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Configure Allure results directory and log file at project root level.
    """
    # ========================================================================
    # FORCE PROJECT ROOT
    # ========================================================================
    project_root = Path(config.rootdir)

    # ========================================================================
    # CONFIGURE ALLURE RESULTS DIRECTORY
    # ========================================================================
    allure_dir = project_root / "reports" / "allure-results"

    # Set environment variable (Allure reads this directly)
    os.environ['ALLURE_RESULTS_DIR'] = str(allure_dir.absolute())
    print(f"🌐 Set env ALLURE_RESULTS_DIR={allure_dir.absolute()}")

    # Override pytest option
    config.option.alluredir = str(allure_dir.absolute())
    print(f"⚙️  Set config.option.alluredir={allure_dir.absolute()}")

    # Clean and create directory
    if allure_dir.exists():
        shutil.rmtree(allure_dir)
        print(f"🧹 Cleaned: {allure_dir}")

    allure_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {allure_dir.absolute()}")

    # ========================================================================
    # CONFIGURE LOG FILE AT PROJECT ROOT
    # ========================================================================
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "python-framework_pytest-logs.txt"
    config.option.log_file = str(log_file.absolute())

    # print(f"📝 Log file: {log_file.absolute()}")

    # ========================================================================
    # PRINT CONFIGURATION SUMMARY
    # ========================================================================
    # print("\n" + "=" * 80)
    # print(f"📁 PROJECT ROOT: {project_root}")
    # print(f"📁 WORKING DIRECTORY: {Path.cwd()}")
    # print(f"📁 ALLURE RESULTS: {allure_dir.absolute()}")
    # print(f"📁 LOG FILE: {log_file.absolute()}")
    # print("=" * 80 + "\n")

