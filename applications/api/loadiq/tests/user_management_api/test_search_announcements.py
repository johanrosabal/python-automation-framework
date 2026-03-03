import pytest
from datetime import datetime, timezone
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.AnnouncementAPI.search_announcements import SearchAnnouncementsEndpoint

logger = setup_logger('SearchAnnouncementsTest')

@loadiq_user_management
class TestSearchAnnouncements(LoadIQBaseTest):
    search_announcements = SearchAnnouncementsEndpoint.get_instance()

    @test(test_case_id="CT-4001", test_description="Test search announcements with basic parameters")
    def test_search_announcements_basic(self, record_property):
        record_property("test_key", "CT-4001")

        # Execute search with basic parameters
        response = self.search_announcements.search_announcements(
            search_terms="string",
            sort_descending=True,
            exclude_expired=False
        )

        # Validate response structure and status
        assert response is not None, "Response should not be None"
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        # Validate response data
        data = response.json()
        assert isinstance(data, dict), "Response should be a dictionary"
        assert "statusCode" in data, "Response should contain statusCode"
        assert "success" in data, "Response should contain success"
        assert "data" in data, "Response should contain data"

        # Validate data type of each field
        assert isinstance(data["statusCode"], int), "statusCode should be an integer"
        assert isinstance(data["success"], bool), "success should be a boolean"
        assert isinstance(data["data"], list), "data should be a list"

        # If there are any announcements, validate their structure
        if data["data"]:
            announcement = data["data"][0]
            assert isinstance(announcement["announcementid"], int), "announcementid should be an integer"
            assert isinstance(announcement["content"], str), "content should be a string"
            assert isinstance(announcement["dateCreated"], str), "dateCreated should be a string"
            assert isinstance(announcement["createdByUserNumber"], str), "createdByUserNumber should be a string"
            assert isinstance(announcement["isDeleted"], bool), "isDeleted should be a boolean"
            assert isinstance(announcement["isCurrentlyActive"], bool), "isCurrentlyActive should be a boolean"

    @test(test_case_id="CT-4002", test_description="Test search announcements with search conditions")
    def test_search_announcements_with_conditions(self, record_property):
        record_property("test_key", "CT-4002")

        search_conditions = [
            {
                "fieldName": "content",  # Changed from title to content since that's the actual field
                "fieldType": "string",
                "operator": "contains",
                "value": "test",
                "value2": None
            }
        ]

        response = self.search_announcements.search_announcements(
            search_conditions=search_conditions,
            sort_by="dateCreated",
            sort_descending=True,
            rows_per_page=10,
            page_number=1
        )

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()

        # Validate that we got results
        assert data["success"] is True, "Expected success to be True"
        assert isinstance(data["data"], list), "Expected data to be a list"

        # Validate that search condition is working
        if data["data"]:
            for announcement in data["data"]:
                assert "test" in announcement["content"].lower(), "Search results should contain 'test' in content"

    @test(test_case_id="CT-4003", test_description="Test search announcements with date range")
    def test_search_announcements_date_range(self, record_property):
        record_property("test_key", "CT-4003")

        current_date = datetime.now(timezone.utc).isoformat()

        search_conditions = [
            {
                "fieldName": "startDate",
                "fieldType": "date",
                "operator": "lessThanOrEqual",
                "value": current_date
            }
        ]

        response = self.search_announcements.search_announcements(
            search_conditions=search_conditions,
            exclude_expired=True
        )

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()

        # Validate that all returned announcements are active
        if data["data"]:
            for announcement in data["data"]:
                assert announcement["isCurrentlyActive"], "All announcements should be currently active"
