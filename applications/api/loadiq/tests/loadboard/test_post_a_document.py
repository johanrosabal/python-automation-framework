import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.loadboard.save_load_document_endpoint import SaveLoadDocumentEndpoint

logger = setup_logger('TestPostADocument')


@loadiq_loadboard
class TestPostADocument(LoadIQBaseTest):

    upload_document = SaveLoadDocumentEndpoint.get_instance()

    @test(test_case_id="LOAD-0001", test_description="Test Post a document")
    def test_post_a_document(self):

        # Getting Endpoint Response
        response = self.upload_document.post_document(
            is_deleted=False,
            load_document_id=None,
            document_type="bol",
            document_format="jpg",
            content="iVBORw0KGgoAAAANSUhEUgAAAbkAAAEFCAIAAADxPg5xAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAVSSURBVHhe7d3bceJKFEDRiYuAiIdoSIZgPOBhLg/L3oLhQpdY648qc1r62SXUIP/6AKBoJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWcmm3227W69Vq9evM/uV6vdlud8c/grejlc+1XR/r8w/W2+Owg+36ImqzXAw42e1n9bDVenNRzIefEQxJK59qt7m9bF+d0nLfvNVl7T7d1Nyztj36jGBQWvlUg7by1mvDswFayZvQyqcaspW3f4rWSt6PVj7Xg+/u3VeqyzJNHdJqvTnfxzns92zOPqSfD3C/kveglYP4mpypu4rXJlp5a3cmWvf9iMMe+X7FWWvcd0YwKK0cxKta+YDafkMrWRStHMSrWvn/FU0rWRStHMQ4rXxU0rSSRdHKQbyqlRMTHhQ1rWRRtHIQr2rl1IXlwdVO+B20kkXRykG8rJXfxfLTvxRTK1kUrRzEw1r5s6mS9pC7kqmVLIpWDuJJrfxm6E/Xlv+5sZhayaJo5SBe28r9pJkPz1it5/ZSK1kUrRzEq1t5MLeX83KplSyKVg7iSa3snZ/jzxh/NufYtJJF0cpBPKyVN++DT6sH//bRaSWLopWDGK2Vf/xwkZmHp5UsilYOYsxWftpfYh5nX6jj00oWRSsHMXAr96bui2olb0UrBzF2K6cW0kreilYOQithaFo5iBe18rDsnK+Xfz28XEgrWRStHMRrWnl6/4/BnChlr6OVLIpWDuJhrZzhlLnr93/+5Ht3WvfwT8mmvzTUSdZKFkUrB/HMVp5Cd+f7Z128aiWLopWDeE0rJ5adYU4ptZKF0cpBvKiVN09YzQvlnlayKFo5iN3VfcHVzLDMfDTQhevc1W+/j258fuW9ZwRD0kr+2m03+7xdVXP/ev254XP8I3hTWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBGhaCdC0EqBpJUDTSoCmlQBNKwGaVgI0rQRoWgnQtBKgaSVA00qAppUATSsBmlYCNK0EaFoJ0LQSoGklQNNKgKaVAE0rAZpWAjStBCgfH78BanKdHItkUPoAAAAASUVORK5CYII=",
            document_name="TEST",
            date_created="2025-02-07T20:41:55.586Z",
            posted_load_id=958
        )

        # Validate Standard Response
        self.add_report(test_data=self.test_post_a_document, status_code=200, response=response)
