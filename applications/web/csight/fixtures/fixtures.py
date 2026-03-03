import pytest
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.login.SignInSSOPage import SignInSSOPage
from applications.web.loadiq.config.sub_application import CustomerAccounts
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest, user
from core.data.UserDTO import UserDTO

logger = setup_logger('Running Fixture')


@pytest.fixture
def csight_get_instance():
    page = LoginPage.get_instance()
    page.load_page()
    return page


@pytest.fixture(scope='function')
def csight_login(user):
    login = LoginPage.get_instance()
    if not login.is_login_successful():
        login.load_page().login_user(user).is_login_successful()


@pytest.fixture(scope='function')
def salesforce_login(user):
    LoginPage.get_instance().load_page().login_user(user).load_salesforce().is_login_successful()


@pytest.fixture(scope='function')
def singleSignOn():
    user = UserDTO(user_name="cm9zYWJqbw==", user_password="VGVsZXRyYWJham8wMw==")
    LoginPage.get_instance().load_page().click_sign_in_single_sign_on(pause=3).sign_in_with_sso(user).is_login_successful()


