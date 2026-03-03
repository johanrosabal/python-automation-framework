import json
from datetime import datetime, timedelta

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('SaveMultiStatusEventEndpoint')

class SaveMultiStatusEventEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "TrackNTraceAPI/SaveMultiStatusEvent"

    def post_save_multi_status_event(self, tracked_load_id: int, statusEventType: str, statusEventSubType: str, statusEventSubTypeDV: str, statusEventTypeDV: str, statusStopType: str, statusLocation: str, eventLocalDatetime: str, comments: str, eventLatitude: str, eventLongitude: str, notOnTimeReason: str, customerNumber: str, tmsLoadId: str, tmsInstance: str, stopSequenceNumber: int, isArrivalDate: bool):

        def handle_null(val):
            return None if val == "null" or val is None else val

        data = {
            "trackedloadid": tracked_load_id,
            "statusEventType": handle_null(statusEventType),
            "statusEventSubType": handle_null(statusEventSubType),
            "statusEventSubTypeDV": handle_null(statusEventSubTypeDV),
            "statusEventTypeDV": handle_null(statusEventTypeDV),
            "statusStopType": handle_null(statusStopType),
            "statusLocation": handle_null(statusLocation),
            "eventLocalDatetime": handle_null(eventLocalDatetime),
            "comments": handle_null(comments),
            "eventLatitude": handle_null(eventLatitude),
            "eventLongitude": handle_null(eventLongitude),
            "notOnTimeReason": handle_null(notOnTimeReason),
            "customerNumber": handle_null(customerNumber),
            "tmsLoadId": handle_null(tmsLoadId),
            "tmsInstance": handle_null(tmsInstance),
            "stopSequenceNumber": stopSequenceNumber,
            "isArrivalDate": isArrivalDate
        }

        payload = [data]

        request = self.post_request() \
            .set_base_url(self.endpoints['trackntrace']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_json(payload) \
            .send()

        return request

    def get_the_day_of_last_month(self, day: int):
        today = datetime.now()
        day_this_month = today.replace(day=1)
        last_day_last_month = day_this_month - timedelta(days=1)
        day_last_month = last_day_last_month.replace(day=day, hour=day, minute=day, second=0)
        return day_last_month.strftime("%Y-%m-%dT%H:%M:%S")
