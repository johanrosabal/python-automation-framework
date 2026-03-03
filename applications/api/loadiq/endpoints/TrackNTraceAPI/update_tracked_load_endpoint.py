import json

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('UpdateTrackedLoadEndpoint')

class UpdateTrackedLoadEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "TrackNTraceAPI/UpdateTrackedLoad"

    def post_update_tracked_load(self, trackedloadid: int, loadNumber: str, edition: int, tractor: str, chassis: str, genset: str, trailer: str, driverCell: str):

        data = {
            "trackedloadid": trackedloadid,
            "loadNumber": loadNumber,
            "edition": edition,
            "tractor": tractor,
            "chassis": chassis,
            "genset": genset,
            "trailer": trailer,
            "driverCell": driverCell
        }

        request = self.post_request() \
            .set_base_url(self.endpoints['trackntrace']) \
            .set_endpoint(self._endpoint) \
            .set_timeout(10) \
            .add_header("authorization", self.jwt_access_token) \
            .add_header("customauthorization", self.custom_token) \
            .set_json(data) \
            .send()

        return request