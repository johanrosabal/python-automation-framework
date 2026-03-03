import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from core.asserts.AssertCollector import AssertCollector # Add this import
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.TrackNTraceAPI.search_payments_endpoint import SearchPaymentsEndpoint

logger = setup_logger('SearchMyPaymentsTest')

@loadiq_trackntrace

class TestSearchMyPaymentsAPI(LoadIQBaseTest):

    search_payments = SearchPaymentsEndpoint()

    @test(test_case_id= 'CT-5811', test_description= 'My Payments Successful search by LoadNumber')
    def test_search_my_payments_by_load_number(self, record_property):
        record_property("test_key", "CT-5811")
        target_load = "BY_10000080001"

        # 1 Send request and get response
        response = self.search_payments.post_search_payment(isDraft=False, searchTerms=target_load, rowsPerPage=25, pageNumber=1, sortDescending=False)

        res_body = response.json()

        # Validate success response
        assert res_body["success"] is True, "API returns success: false"

        # Validate that response return at less 1 result ("NResults: 1")
        assert len(res_body["data"]) > 0, "Data list is empty"

        # Validate that the loadnumber in the first element is the expected
        actual_load = res_body["data"][0]["loadNumber"]
        assert actual_load == target_load, f"Waited {target_load} but get {actual_load}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_payments, status_code=200, response=response)

    @test(test_case_id='CT-5812', test_description='My Payments Successful search by Pro Number')
    def test_search_my_payments_by_pro_number(self, record_property):
        record_property("test_key", "CT-5812")
        pro_number = "PRO2234567"

        # 1 Send request and get response
        response = self.search_payments.post_search_payment(isDraft=False, searchTerms=pro_number, rowsPerPage=25,
                                                            pageNumber=1, sortDescending=False)

        res_body = response.json()

        # Validate success response
        assert res_body["success"] is True, "API returns success: false"

        # Validate that response return at less 1 result ("NResults: 1")
        assert len(res_body["data"]) > 0, "La lista de datos está vacía"

        # Validamos que el LoadNumber en el primer elemento sea el que buscamos
        # Validate that the pronumber in the first element is the expected
        actual_pro_number = res_body["data"][0]["proNumber"]
        assert actual_pro_number == pro_number, f"Waited {pro_number} but get {actual_pro_number}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_payments, status_code=200, response=response)

    @test(test_case_id='CT-5813', test_description='My Payments Successful search by Shipper')
    def test_search_my_payments_by_shipper(self, record_property):
        record_property("test_key", "CT-5813")
        shipper = "Land Transportation"

        # 1 Send request and get response
        response = self.search_payments.post_search_payment(isDraft=False, searchTerms=shipper, rowsPerPage=25,
                                                            pageNumber=1, sortDescending=False)

        res_body = response.json()

        # Validate success response
        assert res_body["success"] is True, "API returns success: false"

        # Validate that response return at less 1 result ("NResults: 1")
        assert len(res_body["data"]) > 10, "La lista de datos está vacía"

        # Validate that the shipper searched is the expected
        #create a for  loop to validate 5 first results
        for i in range(min(5, len(res_body["data"]))):
            actual_shipper = res_body["data"][i]["customerName"]
            assert actual_shipper == shipper, f"Waited {shipper} but get {actual_shipper}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_payments, status_code=200, response=response)

    @test(test_case_id='CT-5814', test_description='My Payments Successful search by Location Name')
    def test_search_my_payments_by_location_name(self, record_property):
        record_property("test_key", "CT-5814")
        location_name = "Miami"

        # 1 Send request and get response
        response = self.search_payments.post_search_payment(isDraft=False, searchTerms=location_name, rowsPerPage=25,
                                                            pageNumber=1, sortDescending=False)

        res_body = response.json()

        # Validate success response
        assert res_body["success"] is True, "API returns success: false"

        # Validate that response return at less 1 result ("NResults: 1")
        assert len(res_body["data"]) > 5, "Datalist is empty"

        # Validate that the location name is the expected
        # create a for  loop to validate 5 first results
        for i in range(min(5, len(res_body["data"]))):
            actual_location_name = res_body["data"][i]["originCity"]
            assert actual_location_name == location_name, f"Waited {location_name} but get {actual_location_name}"

        # 2 Validate Standard Response
        self.add_report(test_data=self.search_payments, status_code=200, response=response)

    @test(test_case_id='CT-5815', test_description='My Payments Successful search by invalid load number')
    def test_search_my_payments_by_invalid_load_number(self, record_property):
        record_property("test_key", "CT-5814")
        invalid_load_number = "inv_123456"

        # 1 Send request and get response
        response = self.search_payments.post_search_payment(isDraft=False, searchTerms=invalid_load_number, rowsPerPage=25,
                                                            pageNumber=1, sortDescending=False)

        res_body = response.json()

        # 2. Validation Suite for "Empty Results" scenario
        # Verify the API processed the request successfully at the application level
        assert res_body["success"] is True, "Expected success to be True even with no results"
        assert res_body["statusCode"] == 0, f"Expected statusCode 0, but got {res_body['statusCode']}"

        # Validate the specific business message for empty searches
        expected_msg = "No results found"
        assert res_body[
                   "message"] == expected_msg, f"Expected message '{expected_msg}', but got '{res_body['message']}'"

        # Ensure the 'data' field is either missing or an empty list
        # This prevents the test from passing if dummy data is returned
        results_data = res_body.get("data", [])
        assert len(results_data) == 0, f"Expected 0 results, but found {len(results_data)} items in data"

        # 3. Add execution details to the final report
        self.add_report(test_data=self.search_payments, status_code=200, response=response)