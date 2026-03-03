import allure
import pytest
import json

from applications.api.softship.config.decorators import softship
from core.api.common.BaseTest import BaseTest
from core.config.logger_config import setup_logger
from applications.api.softship.endpoints.account_authenticate import AccountAuthenticate
from applications.api.softship.endpoints.account_select import AccountSelect
from applications.api.softship.endpoints.basic_address import BasicAddress
from core.data.sources.JSON_reader import JSONReader
from core.utils.decorator import test
from core.utils.random_utils import replace_random_value

logger = setup_logger('TestBasicAddress')


@pytest.fixture(scope="session")
def shared_value():
    main_class = TestBasicAddress()
    return main_class


@softship
class TestBasicAddress(BaseTest):
    # Session Cookie
    master_data_session = "Softship.MasterData.Session"
    master_data_session_value = ""
    # Master Data Cookie after selects agency
    master_data = "Softship.MasterData"
    master_data_value = ""

    @test(test_case_id="API-0001", test_description="01. User Authentication Login")
    @pytest.mark.usefixtures("load_yaml_config", "shared_value")
    @allure.feature("User Authentication")
    @allure.title("API-0001 | User Authentication.")
    @pytest.mark.dependency()
    def test_api_01_user_authentication(self, load_yaml_config, shared_value):
        # 01. User Credentials Authentication and Instance Endpoint
        authentication = AccountAuthenticate.get_instance()
        username = load_yaml_config["username"]
        password = load_yaml_config["password"]
        # 02. Setting Authorization and Instance Endpoint
        response = authentication.get_authentication(username=username, password=password)
        # 04. Validate Standard Response
        self.add_report(test_data=self.test_api_01_user_authentication, status_code=200, response=response)
        # 05. Extract Cookies
        cookie_value = response.cookies.get(self.master_data_session)
        if cookie_value:
            shared_value.master_data_session_value = cookie_value  # Save cookie on shared_value
            logger.info(f"Cookie Master Data Session: {cookie_value}")
        else:
            logger.error("Can't get cookie value.")

    @test(test_case_id="API-0002", test_description="02. Select Agency")
    @pytest.mark.dependency(depends=["test_api_01_user_authentication"])
    @pytest.mark.usefixtures("shared_value")
    @allure.feature("Select Agency")
    @allure.title("API-0002 | Select Agency.")
    @pytest.mark.dependency()
    def test_api_02_select_agency(self, shared_value):
        data = JSONReader().set_file_path("../data/account/Api_account_select.json").read_single_structure()

        select_agency = AccountSelect.get_instance()
        response = select_agency.select_agency(shared_value.master_data_session_value, data)

        # 04. Validate Standard Response
        self.add_report(test_data=self.test_api_02_select_agency, status_code=200, response=response)

        # Extract Cookies
        cookie_value = response.cookies.get(self.master_data)
        if cookie_value:
            shared_value.master_data_value = cookie_value  # Save cookie on shared_value after agency selected
            logger.info(f"Cookie Master Data Session: {shared_value.master_data_session_value}")
            logger.info(f"Cookie Master Data : {shared_value.master_data_value}")
        else:
            logger.error("Can't get cookie value.")

    @test(test_case_id="API-0003", test_description="03. Basic | Customer Suppliers | Address | Save")
    @pytest.mark.dependency(depends=["test_api_02_select_agency"])
    @pytest.mark.usefixtures("shared_value")
    @allure.feature("Customer Suppliers New Address")
    @allure.title("API-0003 | Customer Suppliers New Address.")
    @pytest.mark.dependency()
    def test_api_03_basic_customer_suppliers_address_save(self, shared_value):
        # 01. Setting Session Cookies
        basic_address = BasicAddress().get_instance(
            cookie_session=shared_value.master_data_session_value,
            cookie_master_data=shared_value.master_data_value
        )

        # 02. Preparing Set of Data
        payload = JSONReader().set_file_path("../data/basic_address/Api_01_NewAddress.json").read_single_structure()
        # 02.01. Replace "AddressCode":"9999-{Random-6}" with Dynamic Value
        payload["AddressCode"] = replace_random_value(payload["AddressCode"])
        # 03. Format JSon Data
        payload = json.dumps(payload)
        # 04. Sending request to Save Address endpoint
        response = basic_address.save_address(payload)
        # 04. Validate Standard Response
        self.add_report(test_data=self.test_api_03_basic_customer_suppliers_address_save, status_code=200,
                        response=response)

    @test(test_case_id="API-0004", test_description="04. Basic | Customer Suppliers | Address | Fail")
    @pytest.mark.dependency(depends=["test_api_02_select_agency"])
    @pytest.mark.usefixtures("shared_value")
    @allure.feature("Customer Suppliers New Address Fail")
    @allure.title("API-0004 | Customer Suppliers New Address Fail.")
    @pytest.mark.dependency()
    def test_api_04_basic_customer_suppliers_address_save_with_fail(self, shared_value):
        # 01. Setting Session Cookies
        basic_address = BasicAddress().get_instance(
            cookie_session=shared_value.master_data_session_value,
            cookie_master_data=shared_value.master_data_value
        )

        # 02. Preparing Set of Data
        payload = JSONReader().set_file_path("../data/basic_address/Api_01_NewAddress.json").read_single_structure()
        # 02.01. Replace "AddressCode":"9999-{Random-6}" with Dynamic Value
        payload["AddressCode"] = replace_random_value(payload["AddressCode"])
        # 03. Format JSon Data
        payload = json.dumps(payload)
        # 04. Sending request to Save Address endpoint
        response = basic_address.save_address(payload)
        # 04. Validate Standard Response
        self.add_report(test_data=self.test_api_04_basic_customer_suppliers_address_save_with_fail, status_code=201,
                        response=response)
