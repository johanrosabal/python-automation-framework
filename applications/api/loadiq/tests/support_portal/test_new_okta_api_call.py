import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from core.asserts.AssertCollector import AssertCollector # Add this import
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.UserManagementAPI.toggle_user_access_in_okta import ToggleUserAccessInOktaEndpoint

logger = setup_logger('NewOktaApiCallTest')

@loadiq_user_management

class TestNewOktaApiCall(LoadIQBaseTest):

    toggle_user_access = ToggleUserAccessInOktaEndpoint.get_instance()

    @test(test_case_id="CT-3817", test_description="Test successfully disable a user via OKTA API")
    def test_disable_user_via_okta_api(self, record_property):
        record_property("test_key", "CT-3817")
        # 01 Disable User
        response = self.toggle_user_access.toggle_user_access(
            email="Carrier.Test99@crowleyplatforms.com", enable=False)

        assert response is not None, "Response should not be None"
        assert hasattr(response, "status_code"), "Response should have a status_code attribute"
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert hasattr(response, "json"), "Response should have a json() method"
        data = response.json()
        assert data.get("success") is True, f"Expected success True, got {data.get('success')}"
        assert data.get("statusCode") == 1, f"Expected statusCode 1, got {data.get('statusCode')}"
        expected_message = "User Carrier.Test99@crowleyplatforms.com was successfully disabled in Okta."
        assert data.get("message") == expected_message, f"Expected message '{expected_message}', got '{data.get('message')}'"
        assert "data" in data, "Response JSON should contain 'data' key"
        user_data = data["data"]
        assert user_data.get("userName") == "Carrier.Test99@crowleyplatforms.com", "Expected userName to match"
        assert user_data.get("email") == "Carrier.Test99@crowleyplatforms.com", "Expected email to match"



    @test(test_case_id="CT-3818", test_description="Test successfully enable a user via OKTA API")
    def test_enable_user_via_okta_api(self, record_property):
        record_property("test_key", "CT-3818")
        # 01 Enable User
        response = self.toggle_user_access.toggle_user_access(
            email="Carrier.Test99@crowleyplatforms.com", enable=True)

        assert response is not None, "Response should not be None"
        assert hasattr(response, "status_code"), "Response should have a status_code attribute"
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert hasattr(response, "json"), "Response should have a json() method"
        data = response.json()
        assert data.get("success") is True, f"Expected success True, got {data.get('success')}"
        assert data.get("statusCode") == 1, f"Expected statusCode 1, got {data.get('statusCode')}"
        expected_message = "User Carrier.Test99@crowleyplatforms.com was successfully enabled in Okta."
        assert data.get("message") == expected_message, f"Expected message '{expected_message}', got '{data.get('message')}'"
        assert "data" in data, "Response JSON should contain 'data' key"
        user_data = data["data"]
        assert user_data.get("userName") == "Carrier.Test99@crowleyplatforms.com", "Expected userName to match"
        assert user_data.get("email") == "Carrier.Test99@crowleyplatforms.com", "Expected email to match"

    @test(test_case_id="CT-3819", test_description="Test missing email parameter via OKTA API")
    def test_disable_user_missing_email_via_okta_api(self, record_property):
        record_property("test_key", "CT-3819")
        response = self.toggle_user_access.toggle_user_access_without_email(
            enable=False
        )

        assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

        data = response.json()
        assert data.get("title") == "One or more validation errors occurred.", f"Unexpected title: {data.get('title')}"
        assert data.get("status") == 400, f"Expected status 400, got {data.get('status')}"
        assert "errors" in data, "Response JSON should contain 'errors' key"
        assert "email" in data["errors"], "Errors should contain 'email' key"
        assert "The email field is required." in data["errors"]["email"], "Expected email required error message"

    @test(test_case_id="CT-3820", test_description="Test disable non-existent user via OKTA API")
    def test_disable_nonexistent_user_via_okta_api(self, record_property):
        record_property("test_key", "CT-3820")
        response = self.toggle_user_access.toggle_user_access(
            email="Carrier.Test99@gmail.com", enable=False)

        assert response is not None, "Response should not be None"
        assert hasattr(response, "status_code"), "Response should have a status_code attribute"
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert hasattr(response, "json"), "Response should have a json() method"
        data = response.json()
        assert data.get("success") is False, f"Expected success False, got {data.get('success')}"
        assert data.get("statusCode") == 0, f"Expected statusCode 0, got {data.get('statusCode')}"
        expected_message = "User Carrier.Test99@gmail.com is not registered in Okta"
        assert data.get("message") == expected_message, f"Expected message '{expected_message}', got '{data.get('message')}'"

    @test(test_case_id="CT-3821", test_description="Test disable user with invalid email via OKTA API")
    def test_disable_user_with_invalid_email_via_okta_api(self, record_property):
        record_property("test_key", "CT-3821")
        response = self.toggle_user_access.toggle_user_access(
            email="Carrier.Test99@crowleyplatforms", enable=False
        )

        assert response is not None, "Response should not be None"
        assert hasattr(response, "status_code"), "Response should have a status_code attribute"
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert hasattr(response, "json"), "Response should have a json() method"
        data = response.json()
        assert data.get("success") is False, f"Expected success False, got {data.get('success')}"
        assert data.get("statusCode") == 0, f"Expected statusCode 0, got {data.get('statusCode')}"
        expected_message = "User Carrier.Test99@crowleyplatforms is not registered in Okta"
        assert data.get(
            "message") == expected_message, f"Expected message '{expected_message}', got '{data.get('message')}'"

