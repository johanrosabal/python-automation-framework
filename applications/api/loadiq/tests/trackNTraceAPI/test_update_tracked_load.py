from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.TrackNTraceAPI.update_tracked_load_endpoint import UpdateTrackedLoadEndpoint
import pytest

logger = setup_logger('UpdateTrackedLoadTest')

@loadiq_trackntrace
class TestUpdateTrackedLoadAPI(LoadIQBaseTest):
    update_api = UpdateTrackedLoadEndpoint()

    @test(test_case_id='CT-UT-001', test_description='Update tracked load - happy path')
    def test_update_tracked_load_success(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-001")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        # Provide realistic update fields
        edition = 1
        tractor = "TR-1234"
        chassis = "CH-5678"
        genset = "GS-000"
        trailer = "TRLR-1"
        driverCell = "555-1234"

        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber=load_number, edition=edition, tractor=tractor, chassis=chassis, genset=genset, trailer=trailer, driverCell=driverCell)

        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        res_body = response.json()
        assert res_body.get("success", False) is True, f"API reported failure: {res_body}"

    @test(test_case_id='CT-UT-002', test_description='Update tracked load with invalid trackedLoadId returns error')
    def test_update_tracked_load_invalid_id(self, record_property):
        record_property("test_key", "CT-UT-002")
        invalid_tracked_id = 0
        load_number = "100000000"

        response = self.update_api.post_update_tracked_load(trackedloadid=invalid_tracked_id, loadNumber=load_number, edition=1, tractor="t", chassis="c", genset="g", trailer="r", driverCell="123")

        assert 400 <= response.status_code < 500, f"Expected 4xx for invalid tracked id but got {response.status_code}"
        try:
            res_body = response.json()
            assert res_body.get("success", True) is False
        except Exception:
            logger.warning("Non-JSON response for invalid id test")

    @test(test_case_id='CT-UT-003', test_description='Update tracked load missing required fields returns validation error')
    def test_update_tracked_load_missing_fields(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-003")
        load_data = api_precondition_search_tracked_load_id
        tracked_load_id = load_data["trackedLoadId"]

        # Intentionally omit loadNumber (pass empty) to trigger validation error
        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber="", edition=1, tractor="", chassis="", genset="", trailer="", driverCell="")

        assert 400 <= response.status_code < 500, f"Expected 4xx for missing fields but got {response.status_code}"
        try:
            res_body = response.json()
            assert res_body.get("success", True) is False
        except Exception:
            logger.warning("Non-JSON response for missing fields test")

    @test(test_case_id='CT-UT-004', test_description='Update tracked load with only tractor provided')
    def test_update_tracked_load_only_tractor(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-004")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber=load_number, edition=1, tractor="TR-ONLY-1", chassis="", genset="", trailer="", driverCell="")

        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        res_body = response.json()
        assert res_body.get("success", False) is True, f"API reported failure: {res_body}"

    @test(test_case_id='CT-UT-005', test_description='Update tracked load with only chassis provided')
    def test_update_tracked_load_only_chassis(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-005")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber=load_number, edition=1, tractor="", chassis="CH-ONLY-1", genset="", trailer="", driverCell="")

        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        res_body = response.json()
        assert res_body.get("success", False) is True, f"API reported failure: {res_body}"

    @test(test_case_id='CT-UT-006', test_description='Update tracked load with only genset provided')
    def test_update_tracked_load_only_genset(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-006")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber=load_number, edition=1, tractor="", chassis="", genset="GS-ONLY-1", trailer="", driverCell="")

        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        res_body = response.json()
        assert res_body.get("success", False) is True, f"API reported failure: {res_body}"

    @test(test_case_id='CT-UT-007', test_description='Update tracked load with only trailer provided')
    def test_update_tracked_load_only_trailer(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-007")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber=load_number, edition=1, tractor="", chassis="", genset="", trailer="TRLR-ONLY-1", driverCell="")

        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        res_body = response.json()
        assert res_body.get("success", False) is True, f"API reported failure: {res_body}"

    @test(test_case_id='CT-UT-008', test_description='Update tracked load with only driverCell provided (formatted)')
    def test_update_tracked_load_only_driver_cell(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-UT-008")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        # Driver cell must follow the format (222) 222-2222
        driver_cell_formatted = "(222) 222-2222"

        response = self.update_api.post_update_tracked_load(trackedloadid=tracked_load_id, loadNumber=load_number, edition=1, tractor="", chassis="", genset="", trailer="", driverCell=driver_cell_formatted)

        assert response.status_code == 200, f"Expected 200 but got {response.status_code}: {response.text}"
        res_body = response.json()
        assert res_body.get("success", False) is True, f"API reported failure: {res_body}"

    @test(test_case_id='CT-UT-009', test_description='Update tracked load forced-exception scenario returns forced failure payload')
    def test_update_tracked_load_forced_exception(self, record_property):
        record_property("test_key", "CT-UT-009")
        # Use the exact payload requested
        trackedloadid = 3108
        loadNumber = "BY_91030049125"
        edition = 1
        tractor = "testfailed"
        chassis = "testfailed"
        genset = "testfailed"
        trailer = "testfailed"
        driverCell = "(123) 456-7890"

        response = self.update_api.post_update_tracked_load(
            trackedloadid=trackedloadid,
            loadNumber=loadNumber,
            edition=edition,
            tractor=tractor,
            chassis=chassis,
            genset=genset,
            trailer=trailer,
            driverCell=driverCell
        )

        # Validate server returns the forced exception payload
        try:
            res_body = response.json()
        except Exception:
            pytest.fail(f"Response is not JSON: status={response.status_code} text={getattr(response, 'text', None)}")

        expected = {
            "statusCode": 0,
            "success": False,
            "message": "Forced exception for testing Update Failed."
        }

        assert res_body.get("statusCode") == expected["statusCode"], f"Unexpected statusCode: {res_body}"
        assert res_body.get("success") is expected["success"], f"Unexpected success flag: {res_body}"
        assert res_body.get("message") == expected["message"], f"Unexpected message: {res_body}"
