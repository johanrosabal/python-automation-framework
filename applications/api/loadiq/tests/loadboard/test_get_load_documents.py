import pytest

from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.loadboard.get_load_documents_endpoint import GetLoadDocuments

logger = setup_logger('TestGetEnumValues')


@loadiq_loadboard
class TestGetLoadDocuments(LoadIQBaseTest):

    get_load_documents = GetLoadDocuments.get_instance()

    @test(test_case_id="LOAD-0001", test_description="Test Get Enum Values: Equipment Code")
    def test_get_enum_values_equipment_code(self):
        # 01 Get Enum Values
        response = self.get_load_documents.get_response('958')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)