import pytest
from applications.web.softship.common.LoginPage import LoginPage
from applications.web.softship.components.menus.master_data.HomeMenu import HomeMenu
from applications.web.softship.components.menus.master_data.FinancialMenu import FinancialMenu
from applications.web.softship.components.buttons.Buttons import Buttons
from core.data.UserDTO import UserDTO
from core.ui.common.BaseApp import BaseApp


@pytest.fixture(scope="function")
def user(softship_yaml_config):
    """Create UserDTO from softship config"""
    user_dto = UserDTO(
        user_name=str(softship_yaml_config.get('username')),
        user_password=str(softship_yaml_config.get('password'))
    )
    return user_dto


@pytest.fixture(scope="function")
def softship_login_master_data(user):
    """
    Login to Master Data and navigate to Financial > Account > New
    Complete flow: Login > Click Financial Menu > Click Account Link > Click New Button
    """
    # Step 1: Login to Master Data
    LoginPage.get_instance().login_master_data(user)

    # Step 2: Click on Financial menu
    driver = BaseApp.get_driver()
    HomeMenu(driver).menu_financial(pause=2)

    # Step 3: Click on Account link
    FinancialMenu(driver).link_account(pause=2)

    # Step 4: Click on New button
    Buttons(driver).click_new(pause=2)


@pytest.fixture(scope="function")
def softship_login_finance(user):
    LoginPage.get_instance().login_finance(user)


@pytest.fixture(scope="function")
def softship_login_contract(user):
    LoginPage.get_instance().login_contract(user)


@pytest.fixture(scope="function")
def softship_login_commercial(user):
    LoginPage.get_instance().login_commercial(user)


@pytest.fixture(scope="function")
def softship_login_configuration(user):
    LoginPage.get_instance().login_configuration(user)


@pytest.fixture(scope="function")
def softship_login_booking(user):
    LoginPage.get_instance().login_booking(user)


@pytest.fixture(scope="function")
def softship_login_sof(user):
    LoginPage.get_instance().login_sof(user)

