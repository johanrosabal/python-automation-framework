import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from core.asserts.AssertCollector import AssertCollector # Add this import
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.TrackNTraceAPI.search_tracker_loads_endpoint import SearchTrackerLoadsEndpoint

logger = setup_logger('SearchMyPaymentsTest')

@loadiq_trackntrace

class TestSearchMyPaymentsAPI(LoadIQBaseTest):

    search_loads = SearchTrackerLoadsEndpoint()

    @test(test_case_id= 'CT-5865', test_description= 'Successful Load Search by Specific Term')
    def test_search_loads_by_load_number(self, record_property):
        record_property("test_key", "CT-5865")
        target_load = "MC_118134"

        # 1 Send request and get response
        response = self.search_loads.post_search_loads(includeClosedLoads=True, searchType="LoadSearch", searchTerms=target_load, rowsPerPage=25, pageNumber=1, sortBy="PickupLocalDatetime", sortDescending=False, searchConditions=[])

        res_body = response.json()

        # Validate success response
        assert res_body["success"] is True, "API returns success: false"

        # Validate that response return at less 1 result ("NResults: 1")
        assert len(res_body["data"]) > 0, "Data list is empty"

        # Validate that the loadnumber in the first element is the expected
        actual_load = res_body["data"][0]["loadNumber"]
        assert actual_load == target_load, f"Waited {target_load} but get {actual_load}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_loads, status_code=200, response=response)

    @test(test_case_id= 'CT-5866', test_description= 'Successful with no matching Terms')
    def test_search_loads_by_non_existing_load_number(self, record_property):
        record_property("test_key", "CT-5866")
        target_load = "Nonexist_123456"

        # 1 Send request and get response
        response = self.search_loads.post_search_loads(includeClosedLoads=True, searchType="LoadSearch", searchTerms=target_load, rowsPerPage=25, pageNumber=1, sortBy="PickupLocalDatetime", sortDescending=False, searchConditions=[])

        res_body = response.json()

        # Validate response fields
        assert res_body["success"] is True, f"Expected success: true, but got {res_body.get('success')}"
        assert res_body["statusCode"] == 0, f"Expected statusCode: 0, but got {res_body.get('statusCode')}"
        assert res_body["message"] == "No results found", f"Expected message: 'No results found', but got {res_body.get('message')}"
        
        expected_hidden_message = '[{"usercwroleid":9,"isdeleted":false,"IsDefault":true,"RoleType":"shipper","TradingPartnerNumber":"landtrans"}]'
        assert res_body["hiddenMessage"] == expected_hidden_message, f"Hidden message mismatch. Got: {res_body.get('hiddenMessage')}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_loads, status_code=200, response=response)

    @test(test_case_id= 'CT-5867', test_description= 'Successful search without any term')
    def test_search_loads_by_empty_load_number(self, record_property):
        record_property("test_key", "CT-5867")
        target_load = ""

        # 1 Send request and get response
        response = self.search_loads.post_search_loads(includeClosedLoads=True, searchType="LoadSearch", searchTerms=target_load, rowsPerPage=25, pageNumber=1, sortBy="PickupLocalDatetime", sortDescending=False, searchConditions=[])

        res_body = response.json()

        # Validate response fields
        assert res_body["success"] is True, f"Expected success: true, but got {res_body.get('success')}"
        assert len(res_body["data"]) == 25, f"Expected 25 loads, but got {len(res_body.get('data', []))}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_loads, status_code=200, response=response)


    @test(test_case_id= 'CT-5868', test_description= 'Search results sorted by PickupLocalDatetime')
    def test_search_loads_sorting_by_pickup_date(self, record_property):
        record_property("test_key", "CT-5868")
        
        # 1 Send request with sorting
        response = self.search_loads.post_search_loads(includeClosedLoads=True, searchType="LoadSearch", searchTerms="", rowsPerPage=25, pageNumber=1, sortBy="PickupLocalDatetime", sortDescending=False, searchConditions=[])
        
        res_body = response.json()
        assert res_body["success"] is True, f"API returns success: false. Response: {res_body}"
        
        data = res_body.get("data", [])
        assert len(data) > 1, "Not enough data to validate sorting"
        
        # Extract pickup dates
        pickup_dates = [item["pickupLocalDatetime"] for item in data if item.get("pickupLocalDatetime")]
        
        # Validate sorting (ascending)
        # We compare adjacent elements
        for i in range(len(pickup_dates) - 1):
            assert pickup_dates[i] <= pickup_dates[i+1], f"Data is not sorted. {pickup_dates[i]} > {pickup_dates[i+1]} at index {i}"
        
        # 2 Validate Standard Response
        self.add_report(test_data=self.search_loads, status_code=200, response=response)

    @test(test_case_id= 'CT-5869', test_description= 'Search results sorted by PickupLocalDatetime descending')
    def test_search_loads_sorting_by_pickup_date_descending(self, record_property):
        record_property("test_key", "CT-5869")
        
        # 1 Send request with sorting descending
        response = self.search_loads.post_search_loads(includeClosedLoads=True, searchType="LoadSearch", searchTerms="", rowsPerPage=25, pageNumber=1, sortBy="PickupLocalDatetime", sortDescending=True, searchConditions=[])
        
        res_body = response.json()
        assert res_body["success"] is True, f"API returns success: false. Response: {res_body}"
        
        data = res_body.get("data", [])
        assert len(data) > 1, "Not enough data to validate sorting"
        
        # Extract pickup dates
        pickup_dates = [item["pickupLocalDatetime"] for item in data if item.get("pickupLocalDatetime")]
        
        # Validate sorting (descending)
        for i in range(len(pickup_dates) - 1):
            assert pickup_dates[i] >= pickup_dates[i+1], f"Data is not sorted descending. {pickup_dates[i]} < {pickup_dates[i+1]} at index {i}"
        
        # 2 Validate Standard Response
        self.add_report(test_data=self.search_loads, status_code=200, response=response)

    @test(test_case_id= 'CT-5870', test_description= 'Validate includeClosedLoads behavior')
    def test_search_loads_by_closed_status(self, record_property):
        record_property("test_key", "CT-5870")
        
        # Iteration 1: includeClosedLoads=True (Should return Completed loads)
        response_true = self.search_loads.post_search_loads(includeClosedLoads=True, searchType="LoadSearch", searchTerms="", rowsPerPage=0, pageNumber=0, sortBy="PickupLocalDatetime", sortDescending=False, searchConditions=[])
        res_body_true = response_true.json()
        assert res_body_true["success"] is True, f"Failed with includeClosedLoads=True. Response: {res_body_true}"
        
        data_true = res_body_true.get("data", [])
        tracking_statuses_true = [item["trackingStatus"] for item in data_true if "trackingStatus" in item]
        has_completed = "completed" in tracking_statuses_true
        assert has_completed is True, "Expected to find 'Completed' loads when includeClosedLoads=True"
        
        # Iteration 2: includeClosedLoads=False (Should NOT return Completed loads)
        response_false = self.search_loads.post_search_loads(includeClosedLoads=False, searchType="LoadSearch", searchTerms="", rowsPerPage=0, pageNumber=0, sortBy="PickupLocalDatetime", sortDescending=False, searchConditions=[])
        res_body_false = response_false.json()
        assert res_body_false["success"] is True, f"Failed with includeClosedLoads=False. Response: {res_body_false}"
        
        data_false = res_body_false.get("data", [])
        tracking_statuses_false = [item["trackingStatus"] for item in data_false if "trackingStatus" in item]
        has_completed_false = "completed" in tracking_statuses_false
        assert has_completed_false is False, "Expected NO 'Completed' loads when includeClosedLoads=False"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_loads, status_code=200, response=response_false)
