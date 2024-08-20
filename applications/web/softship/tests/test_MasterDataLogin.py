from applications.web.softship.pages.LoginPage import LoginPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest, user
from core.utils.decorator import test
from core.asserts.AssertCollector import AssertCollector

logger = setup_logger('TestMasterDataLogin')


class TestMasterDataLogin(BaseTest):
    LoginPage = LoginPage.get_instance()

    @test(test_case_id="MDS-0001", test_description="Master Data Login page 1.")
    def test_login_valid_user(self, user):
        logger.info("Validating Valid User...")
        # loginPage = LoginPage.get_instance()
        # (self.loginPage
        #  .load_page()
        #  .login_user_with_agency(user, "Crowley HQ")
        #  .verify_title("MasterData QA")
        #  )

        self.LoginPage.load_page()
        self.LoginPage.login_user(user)
        self.LoginPage.select_agency("Crowley HQ")
        self.LoginPage.verify_title("MasterData QA")
