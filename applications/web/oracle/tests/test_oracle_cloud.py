import allure
import pytest

from applications.web.oracle.config.decorators import oracle
from applications.web.oracle.pages.LoginPage import LoginPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest, user
from core.utils.decorator import test

logger = setup_logger('TestSoftship')


@pytest.mark.web
@oracle
class TestOracleCloud(BaseTest):
    # Init App
    oracle_login_page = LoginPage.get_instance()

    @test(test_case_id="ORC-0001", test_description="Oracle Cloud Login valid user.")
    def test_oracle_cloud_login_valid_user(self, user):
        # 01. Load Login Page
        self.oracle_login_page.load_page()
        # 02. Enter user credentials
        self.oracle_login_page.login_user(user)
        # 03. Validate user is logged
        self.oracle_login_page.verify_welcome_title()
