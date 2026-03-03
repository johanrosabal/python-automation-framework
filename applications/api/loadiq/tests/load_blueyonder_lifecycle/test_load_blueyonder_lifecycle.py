import allure
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.web.loadiq.common.BlueYonderUploadLoad import SubmitLoadEndpoint


logger = setup_logger('SearchAnnouncementsTest')

@loadiq_user_management
class TestLoadBlueYonderLifeCycle(LoadIQBaseTest):

    submit_load_endpoint = SubmitLoadEndpoint.get_instance()

    @allure.title('Verify search a load in My Offers')
    @allure.description(
        'Verifies that the Complete Delivery button is only visible when all delivery milestones have been input, and that the status transitions correctly from Delivered to Completed.')
    @allure.tag("LOADIQ")
    @allure.link("https://crowley.atlassian.net/browse/CT-xxxx", name="Jira")
    @allure.testcase("CT-xxxx")
    @allure.feature("Status Update")
    @test(test_case_id="CT-xxxx", test_description="Verify that the Expedite field is displayed in My Offers list view",
          feature="MyOffersDetails", skip=False)
    def test_search_offers_with_a_valid_loadNumber(self, load_iq_login_carrier_portal, load_iq_upload_blueyonder_load, record_property):
        project_root = Path(__file__).parent.parent.parent.parent.parent
        xml_path = project_root / "applications/web/loadiq/data/carrier_portal/my_loads/blueyoder_loads/single/load_tender_accepted/LoadTenderAccepted_10000048625.xml"
        # 1. Create the load via API
        result = self.submit_load_endpoint.process_load_from_file_upload(xml_path)
        response_dict = json.loads(result.text)
        load_number = response_dict['data']['loadNumber']
        assert result.status_code == 200