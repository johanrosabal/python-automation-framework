import allure
import json
import os
from pathlib import Path
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint
from applications.api.loadiq.endpoints.loadboard.search_my_offers_endpoint import SearchMyOffersEndpoint
from applications.web.loadiq.config.sub_application import CarrierAccounts

from core.utils import helpers
from core.utils.helpers import parse_dynamic_dates_values


logger = setup_logger('SearchAnnouncementsTest')

@loadiq_loadboard
class TestLoadBlueYonderLifeCycle(LoadIQBaseTest):

    # Define which user account to use for login - this will be used by the load_iq_yaml_config fixture
    # If not specified, defaults to CustomerAccounts.TEST_07
    # Use CarrierAccounts for users with carrier permissions (required for SearchMyOffers endpoint)
    login_account = CarrierAccounts.TEST_20
    test_path = "applications\\api\\loadiq\\tests\\loadboard"

    submit_load_endpoint = SubmitLoadEndpoint.get_instance()
    search_my_offers_endpoint = SearchMyOffersEndpoint.get_instance()

    @allure.title('Verify search_offers_with_a_valid_loadNumber')
    @allure.description(
                'Verify that the endpoint returns the correct offer(s) when a valid load number is provided.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-5254", name="Jira")
    @allure.testcase("CT-5254")
    @allure.feature("My Offers")
    @test(test_case_id="CT-5254", test_description="Verify search_offers_with_a_valid_loadNumber",
          feature="MyOffersSearch", skip=False)
    def test_search_offers_with_a_valid_loadNumber(self, record_property):
        record_property("test_key", "CT-5254")

        project_root = Path(__file__).parent.parent.parent.parent.parent
        xml_path = project_root / "applications/api/loadiq/data/loadAccepted/2506223047118_LoadTendered_1352155.LoadTendered.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        load_number = response_dict['data']['loadNumber']
        assert result.status_code == 200

        response = self.search_my_offers_endpoint.search_my_offers(
            is_draft=False,
            search_terms=load_number,
            rows_per_page=10,
            page_number=1,
            sort_by="OfferPriority",
            sort_descending=True,
            search_conditions=[]
        )
        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-5254_verify_search_offers_with_a_valid_loadNumber"
        )
        self.add_report(
            test_data="CT-5254 | Verify search offers with a valid loadNumber",
            status_code=response.status_code,
            response=response
        )
        # Validate the response
        assert response.status_code == 200
        response_json = response.json() if hasattr(response, 'json') else json.loads(response.text)
        assert 'data' in response_json
        assert any(offer.get('loadNumber') == load_number for offer in response_json['data'])

    @allure.title('Verify search_offers_with_non_existent_loadNumber')
    @allure.description(
        'Ensure the endpoint handles searches for non-existent load numbers gracefully.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-5255", name="Jira")
    @allure.testcase("CT-5255")
    @allure.feature("My Offers")
    @test(test_case_id="CT-5255", test_description="Verify search_offers_with_non_existent_loadNumber",
          feature="MyOffersSearch", skip=False)
    def test_search_offers_with_non_existent_loadNumber(self, record_property):
        record_property("test_key", "CT-5255")
        # Set non-existent load number
        non_existent_load_number = "NO_EXIST_123"

        response = self.search_my_offers_endpoint.search_my_offers(
            is_draft=False,
            search_terms=non_existent_load_number,
            rows_per_page=10,
            page_number=1,
            sort_by="OfferPriority",
            sort_descending=True,
            search_conditions=[]
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-5255_verify_search_offers_with_non_existent_loadNumber"
        )
        self.add_report(
            test_data="CT-5255 | Verify search offers with non existent loadNumber",
            status_code=response.status_code,
            response=response
        )

        # Validate the response
        assert response.status_code == 200
        response_json = response.json() if hasattr(response, 'json') else json.loads(response.text)
        # Validate that success is true and message indicates no results found
        assert response_json['success'] == True, "Expected success to be true"
        assert response_json['message'] == "No results found", f"Expected 'No results found' message, but got '{response_json.get('message')}'"
        assert response_json['statusCode'] == 0, "Expected statusCode to be 0"
        assert response_json['loadNumber'] == "", "Expected empty loadNumber"

    @allure.title('Verify search_offers_without_defining_loadNumber')
    @allure.description(
        'Check the endpoint behavior when no load number is provided.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-5256", name="Jira")
    @allure.testcase("CT-5256")
    @allure.feature("My Offers")
    @test(test_case_id="CT-5256", test_description="Verify search_offers_without_defining_loadNumber",
          feature="MyOffersSearch", skip=False)
    def test_search_offers_without_defining_loadNumber(self, record_property):
        record_property("test_key", "CT-5256")
        # Leave search_terms empty
        response = self.search_my_offers_endpoint.search_my_offers(
            is_draft=False,
            search_terms="",
            rows_per_page=10,
            page_number=1,
            sort_by="OfferPriority",
            sort_descending=True,
            search_conditions=[]
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-5256_verify_search_offers_without_defining_loadNumber"
        )
        self.add_report(
            test_data="CT-5256 | Verify search offers without defining loadNumber",
            status_code=response.status_code,
            response=response
        )

        # Validate the response
        assert response.status_code == 200
        response_json = response.json() if hasattr(response, 'json') else json.loads(response.text)

        # Validate response structure
        assert response_json['success'] == True, "Expected success to be true"
        assert response_json['statusCode'] == 0, "Expected statusCode to be 0"
        assert 'data' in response_json, "Expected 'data' field in response"
        assert 'message' in response_json, "Expected 'message' field in response"

        # Validate message format "NResults: X" where X is the number of results
        assert response_json['message'].startswith("NResults:"), f"Expected message to start with 'NResults:', but got '{response_json['message']}'"

        # Validate data array (can contain offers or be empty)
        assert isinstance(response_json['data'], list), "Expected 'data' to be a list"

        # If there are results, validate basic structure of first offer
        if len(response_json['data']) > 0:
            first_offer = response_json['data'][0]
            assert 'loadNumber' in first_offer, "Expected 'loadNumber' in offer"
            assert 'loadBoardStatus' in first_offer, "Expected 'loadBoardStatus' in offer"
            assert 'offerPriority' in first_offer, "Expected 'offerPriority' in offer"

    @allure.title('Verify search_offers_including_closed_loads')
    @allure.description(
        'Validate that closed loads are included in the response when requested.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-5257", name="Jira")
    @allure.testcase("CT-5257")
    @allure.feature("My Offers")
    @test(test_case_id="CT-5257", test_description="Verify search_offers_including_closed_loads",
          feature="MyOffersSearch", skip=False)
    def test_search_offers_including_closed_loads(self, record_property):
        record_property("test_key", "CT-5257")

        response = self.search_my_offers_endpoint.search_my_offers(
            is_draft=False,
            search_terms="",
            rows_per_page=10,
            page_number=1,
            sort_by="OfferPriority",
            sort_descending=True,
            search_conditions=[],
            include_closed_loads=True
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-5257_verify_search_offers_including_closed_loads"
        )
        self.add_report(
            test_data="CT-5257 | Verify search offers including closed loads",
            status_code=response.status_code,
            response=response
        )

        # Validate the response
        assert response.status_code == 200
        response_json = response.json() if hasattr(response, 'json') else json.loads(response.text)

        # Validate response structure
        assert response_json['success'] == True, "Expected success to be true"
        assert response_json['statusCode'] == 0, "Expected statusCode to be 0"
        assert 'data' in response_json, "Expected 'data' field in response"

    @allure.title('Verify validate_pagination')
    @allure.description(
        'Confirm that pagination works correctly and returns the expected number of results per page.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-5258", name="Jira")
    @allure.testcase("CT-5258")
    @allure.feature("My Offers")
    @test(test_case_id="CT-5258", test_description="Verify validate_pagination",
          feature="MyOffersSearch", skip=False)
    def test_validate_pagination(self, record_property):
        record_property("test_key", "CT-5258")
        # First page
        response_page1 = self.search_my_offers_endpoint.search_my_offers(
            is_draft=False,
            search_terms="",
            rows_per_page=5,
            page_number=1,
            sort_by="OfferPriority",
            sort_descending=False,
            search_conditions=[]
        )

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response_page1,
            filename_prefix="CT-5258_validate_pagination_page1"
        )
        self.add_report(
            test_data="CT-5258 | Verify validate pagination - Page 1",
            status_code=response_page1.status_code,
            response=response_page1
        )

        # Validate first page response
        assert response_page1.status_code == 200
        response_json_page1 = response_page1.json() if hasattr(response_page1, 'json') else json.loads(response_page1.text)
        assert 'data' in response_json_page1
        page1_data = response_json_page1['data']

        # If there are results, validate pagination
        if len(page1_data) > 0:
            assert len(page1_data) <= 5, "Expected at most 5 results per page"

            # Second page
            response_page2 = self.search_my_offers_endpoint.search_my_offers(
                is_draft=False,
                search_terms="",
                rows_per_page=5,
                page_number=2,
                sort_by="OfferPriority",
                sort_descending=False,
                search_conditions=[]
            )

            helpers.save_request_and_response(
                base_path=self.test_path,
                response=response_page2,
                filename_prefix="CT-5258_validate_pagination_page2"
            )
            self.add_report(
                test_data="CT-5258 | Verify validate pagination - Page 2",
                status_code=response_page2.status_code,
                response=response_page2
            )

            # Validate second page response
            assert response_page2.status_code == 200
            response_json_page2 = response_page2.json() if hasattr(response_page2, 'json') else json.loads(response_page2.text)
            assert 'data' in response_json_page2
            page2_data = response_json_page2['data']
            assert len(page2_data) <= 5, "Expected at most 5 results per page"

    @allure.title('Verify response_with_invalid_token')
    @allure.description(
        'Ensure the endpoint returns an authentication error when an invalid or expired token is used.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-5259", name="Jira")
    @allure.testcase("CT-5259")
    @allure.feature("My Offers")
    @test(test_case_id="CT-5259", test_description="Verify response_with_invalid_token",
          feature="MyOffersSearch", skip=False)
    def test_response_with_invalid_token(self, record_property):
        record_property("test_key", "CT-5259")
        # Save original tokens
        original_jwt_token = self.search_my_offers_endpoint.jwt_access_token
        original_custom_token = self.search_my_offers_endpoint.custom_token

        try:
            # Set invalid tokens
            self.search_my_offers_endpoint.jwt_access_token = "invalid_token_12345"
            self.search_my_offers_endpoint.custom_token = "invalid_custom_token_12345"

            response = self.search_my_offers_endpoint.search_my_offers(
                is_draft=False,
                search_terms="",
                rows_per_page=10,
                page_number=1,
                sort_by="OfferPriority",
                sort_descending=True,
                search_conditions=[]
            )

            helpers.save_request_and_response(
                base_path=self.test_path,
                response=response,
                filename_prefix="CT-5259_response_with_invalid_token"
            )
            self.add_report(
                test_data="CT-5259 | Verify response with invalid token",
                status_code=response.status_code,
                response=response
            )

            # Validate the response - should return 401 or 403
            assert response.status_code in [500], f"Expected 500, but got {response.status_code}"

        finally:
            # Restore original tokens
            self.search_my_offers_endpoint.jwt_access_token = original_jwt_token
            self.search_my_offers_endpoint.custom_token = original_custom_token