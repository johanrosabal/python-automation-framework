import pytest

from core.api.common.BaseTest import BaseTest
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from core.utils import helpers
from core.data.sources.JSON_reader import JSONReader
from applications.api.mock.config.decoratos import mock
from applications.api.mock.endpoints.users_endpoint import UsersEndpoint

logger = setup_logger('TestUsers')


@pytest.fixture(scope="session")
def reports():
    return "applications\\api\\mock\\tests"


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.fixture(scope="session")
def test_data():
    # Import Json Data
    path = "../../mock/data/users.json"
    data = JSONReader.import_json(path)
    return parse_dynamic_dates_values(data)


@pytest.mark.api
@mock
class TestUsers(BaseTest):

    users = UsersEndpoint.get_instance()

    @test(test_case_id="CT-1234", test_description="Create an user", skip=False)
    def test_create_an_user(self, reports, shared_data, test_data):
        # Import Json Data
        # path = "../../mock/data/users.json"
        # data = JSONReader.import_json(path)
        # data = parse_dynamic_dates_values(data)
        json = test_data['tests'][0]['data']

        # Send Post Request
        response = self.users.create_user(json)

        # Verify Information Response
        helpers.save_request_and_response(base_path=reports, response=response, filename_prefix="CT-1234_create_an_user")

        # Save Request & Response Files
        self.add_report(test_data=self.test_create_an_user, status_code=201, response=response)

        # Parce Text Response Raw Data to Json Object
        user = JSONReader.text_to_dict(response.text)

        # Share information with others scenarios
        shared_data["id"] = user["id"]

        # Optional Logs some values
        logger.info(f"User ID: {shared_data["id"]}")

        # Assert user ID is not Null
        assert (user["id"] is not None), "User id required"

    @test(test_case_id="CT-1234", test_description="Edit an User", skip=False)
    def test_edit_user(self, reports, shared_data, test_data):
        # Import Json Data
        json = test_data['tests'][1]['data']

        # Send Post Request
        response = self.users.edit_user_information(id_user=shared_data["id"], json=json)

        # Verify Information Response
        helpers.save_request_and_response(base_path=reports, response=response,filename_prefix="CT-1234_edit_an_user")

        # Save Request & Response Files
        self.add_report(test_data=self.test_edit_user, status_code=200, response=response)

        # Parce Text Response Raw Data to Json Object
        user = JSONReader.text_to_dict(response.text)

        # Assert user ID is not Null
        assert (user["age"] == 25), "Age not match"

    @test(test_case_id="CT-1234", test_description="Get User Information", skip=False)
    def test_get_user_information(self, reports, shared_data):
        # Send Get
        response = self.users.get_user_information(id_user=shared_data["id"])

        # Verify Information Response
        helpers.save_request_and_response(base_path=reports, response=response, filename_prefix="CT-1234_get_user_information")

        # Save Request & Response Files
        self.add_report(test_data=self.test_get_user_information, status_code=200, response=response)

        # Parce Text Response Raw Data to Json Object
        user = JSONReader.text_to_dict(response.text)

        msg = f"User {user.get('username', 'N/A')} has null values"
        assert user["id"] is not None, msg
        assert user["username"] is not None, msg
        assert user["email"] is not None, msg
        assert user["full_name"] is not None, msg
        assert user["age"] is not None, msg

    @test(test_case_id="CT-1234", test_description="Get Users Information", skip=False)
    def test_get_users_information(self, reports, shared_data):

        # Send Get
        response = self.users.get_users_information()

        # Verify Information Response
        helpers.save_request_and_response(base_path=reports, response=response, filename_prefix="CT-1234_get_users_information")

        # Save Request & Response Files
        self.add_report(test_data=self.test_get_users_information, status_code=200, response=response)

        # Parce Text Response Raw Data to Json Object
        users = JSONReader.text_to_dict(response.text)

        for user in users:
            msg = f"User {user.get('username', 'N/A')} has null values"
            assert user["id"] is not None, msg
            assert user["username"] is not None, msg
            assert user["email"] is not None, msg
            assert user["full_name"] is not None, msg
            assert user["age"] is not None, msg

    @test(test_case_id="CT-1234", test_description="Delete User Information", skip=False)
    def test_delete_user_information(self, reports, shared_data):
        # Send Get
        response = self.users.delete_user_information(id_user=shared_data["id"])

        # Verify Information Response
        helpers.save_request_and_response(base_path=reports, response=response, filename_prefix="CT-1234_delete_user_information")

        # Save Request & Response Files
        self.add_report(test_data=self.test_get_user_information, status_code=204, response=response)

        # Parce Text Response Raw Data to Json Object
        user = JSONReader.text_to_dict(response.text)

        assert (user is None), "User should not be present"