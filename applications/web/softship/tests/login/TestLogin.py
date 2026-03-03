import pytest

from applications.web.softship.components.menus.SoftshipMenu import SoftshipMenu
from applications.web.softship.fixtures.fixtures import *
from applications.web.softship.config.decorators import softship
from applications.web.softship.common.SoftshipBaseTest import SoftshipBaseTest
from core.ui.common.BaseTest import user
from core.config.logger_config import setup_logger
from core.utils.decorator import test

logger = setup_logger('TestMexicoProject')


@pytest.mark.web
@softship
class TestLogin(SoftshipBaseTest):

    menu = SoftshipMenu.get_instance()

    @test(test_case_id="SF-0001", test_description="Login user on Contracts module", feature="Login", skip=False)
    def test_contracts(self, softship_login_contract):
        self.menu.logout()

    @test(test_case_id="SF-0002", test_description="Login user on Finance module", feature="Login", skip=False)
    def test_finance(self, softship_login_finance):
        self.menu.logout()

    @test(test_case_id="SF-0003", test_description="Login user on Commercial module", feature="Login", skip=False)
    def test_commercial(self, softship_login_commercial):
        self.menu.logout()

    @test(test_case_id="SF-0004", test_description="Login user on Configuration module", feature="Login", skip=False)
    def test_configuration(self, softship_login_configuration):
        self.menu.logout()

    @test(test_case_id="SF-0005", test_description="Login user on Booking module", feature="Login", skip=False)
    def test_finance(self, softship_login_booking):
        self.menu.logout()

    @test(test_case_id="SF-0006", test_description="Login user on SOF module", feature="Login", skip=False)
    def test_sof(self, softship_login_sof):
        self.menu.logout()

    @test(test_case_id="SF-0007", test_description="Login user on Master Data module", feature="Login", skip=False)
    def test_master_data(self, softship_login_master_data):
        self.menu.logout()




