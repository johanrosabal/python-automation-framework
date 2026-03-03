import pytest

from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.loadboard.get_enum_values_enpoint import GetEnumValuesEndpoint

logger = setup_logger('TestGetEnumValues')


@loadiq_loadboard
class TestGetEnumValues(LoadIQBaseTest):

    enum_values = GetEnumValuesEndpoint.get_instance()

    @test(test_case_id="LOAD-0001", test_description="Test Get Enum Values: Equipment Code")
    def test_get_enum_values_equipment_code(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('equipment_code')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0002", test_description="Test Get Enum Values: Addon Service Type")
    def test_get_enum_values_addonservice_type(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('addonservice_type')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0003", test_description="Test Get Enum Values: Weight Uom")
    def test_get_enum_values_weight_uom(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('weight_uom')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0004", test_description="Test Get Enum Values: handling Unit Type")
    def test_get_enum_values_handling_unit_type(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('handling_unit_type')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0005", test_description="Test Get Enum Values: Packing Group Type")
    def test_get_enum_values_packing_group_type(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('packing_group_type')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0006", test_description="Test Get Enum Values: Hazmat Class Type")
    def test_get_enum_values_hazmat_class_type(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('hazmat_class_type')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0007", test_description="Test Get Enum Values: Dimension Uom")
    def test_get_enum_values_dimension_uom(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('dimension_uom')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0008", test_description="Test Get Enum Values: Document Type")
    def test_get_enum_values_document_type(self):
        # 01 Get Enum Values
        response = self.enum_values.get_response('document_type')
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)
