import pytest
from applications.web.demo.pages.LoginPage import LoginPage
from applications.web.loadiq.config.sub_application import CustomerAccounts
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest, user

logger = setup_logger('Running Fixture')


@pytest.fixture
def demo_get_instance():
    page = LoginPage.get_instance()
    page.load_page()
    return page


@pytest.fixture(scope='function')
def demo_login(user):
    def login():
        page = LoginPage.get_instance()
        page.load_page()
        page.login_user(user)

        page.verify_user_is_logged("/web/index.php/dashboard/index")
    return login
