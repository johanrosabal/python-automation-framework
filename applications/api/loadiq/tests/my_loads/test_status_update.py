import pytest
import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from core.asserts.AssertCollector import AssertCollector
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.TrackNTraceAPI.save_multi_status_event_endpoint import SaveMultiStatusEventEndpoint
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint

logger = setup_logger('StatusUpdateTest')

@loadiq_trackntrace
class TestStatusUpdateAPI(LoadIQBaseTest):
    save_multi_status_event = SaveMultiStatusEventEndpoint()

    @test(test_case_id= 'CT-5865', test_description= 'Change Load Status to Arrived at PickUp')
    def test_change_load_status_to_arrived_at_pickup(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-5865")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        eventLocalDatetime = self.save_multi_status_event.get_the_day_of_last_month(day=1)

        response = self.save_multi_status_event.post_save_multi_status_event(tracked_load_id=tracked_load_id, statusEventType="arrive_at_pickup", 
        statusEventSubType="null", statusEventSubTypeDV="null", statusEventTypeDV="Arrive at Pickup", statusStopType="origin", 
        statusLocation="null", eventLocalDatetime=eventLocalDatetime, comments="null", eventLatitude="null", eventLongitude="null", 
        notOnTimeReason="null", customerNumber="landtrans", tmsLoadId=load_number, tmsInstance="blue_yonder", stopSequenceNumber=1, isArrivalDate=True)

        assert response.status_code == 200, f"Error updating status: {response.text}"
        self.add_report(test_data=self.save_multi_status_event, status_code=200, response=response)

    @test(test_case_id= 'CT-5866', test_description= 'Change Load Status to Departed at PickUp')
    def test_change_load_status_to_departed_at_pickup(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-5866")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        eventLocalDatetime = self.save_multi_status_event.get_the_day_of_last_month(day=2)

        response = self.save_multi_status_event.post_save_multi_status_event(tracked_load_id=tracked_load_id, statusEventType="depart_pickup", 
        statusEventSubType="null", statusEventSubTypeDV="null", statusEventTypeDV="Departed Pickup", statusStopType="origin", 
        statusLocation="null", eventLocalDatetime=eventLocalDatetime, comments="null", eventLatitude="null", eventLongitude="null", 
        notOnTimeReason="null", customerNumber="landtrans", tmsLoadId=load_number, tmsInstance="blue_yonder", stopSequenceNumber=1, isArrivalDate=False)

        assert response.status_code == 200, f"Error updating status: {response.text}"
        self.add_report(test_data=self.save_multi_status_event, status_code=200, response=response)

    @test(test_case_id= 'CT-5867', test_description= 'Change Load Status to Arrived at delivery')
    def test_change_load_status_to_arrived_at_delivery(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-5867")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        eventLocalDatetime = self.save_multi_status_event.get_the_day_of_last_month(day=3)

        response = self.save_multi_status_event.post_save_multi_status_event(tracked_load_id=tracked_load_id, statusEventType="arrive_at_delivery", 
        statusEventSubType="null", statusEventSubTypeDV="null", statusEventTypeDV="Arrive at Delivery", statusStopType="destination", 
        statusLocation="null", eventLocalDatetime=eventLocalDatetime, comments="null", eventLatitude="null", eventLongitude="null", 
        notOnTimeReason="null", customerNumber="landtrans", tmsLoadId=load_number, tmsInstance="blue_yonder", stopSequenceNumber=2, isArrivalDate=True)

        assert response.status_code == 200, f"Error updating status: {response.text}"
        self.add_report(test_data=self.save_multi_status_event, status_code=200, response=response)

    @test(test_case_id= 'CT-5868', test_description= 'Change Load Status to Delivered')
    def test_change_load_status_to_delivered(self, record_property, api_precondition_search_tracked_load_id):
        record_property("test_key", "CT-5868")
        load_data = api_precondition_search_tracked_load_id
        load_number = load_data["loadNumber"].replace("BY_", "")
        tracked_load_id = load_data["trackedLoadId"]

        eventLocalDatetime = self.save_multi_status_event.get_the_day_of_last_month(day=4)

        response = self.save_multi_status_event.post_save_multi_status_event(tracked_load_id=tracked_load_id, statusEventType="delivered", 
        statusEventSubType="null", statusEventSubTypeDV="null", statusEventTypeDV="Delivered", statusStopType="destination", 
        statusLocation="null", eventLocalDatetime=eventLocalDatetime, comments="null", eventLatitude="null", eventLongitude="null", 
        notOnTimeReason="null", customerNumber="landtrans", tmsLoadId=load_number, tmsInstance="blue_yonder", stopSequenceNumber=2, isArrivalDate=False)

        assert response.status_code == 200, f"Error updating status: {response.text}"
        self.add_report(test_data=self.save_multi_status_event, status_code=200, response=response)