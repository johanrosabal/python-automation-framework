import pytest
import json

from applications.api.loadiq.dtos.loadboard.save_posted_load_dto import SavePostedLoadDTO
from applications.api.loadiq.endpoints.loadboard.get_enum_values_enpoint import GetEnumValuesEndpoint
from applications.api.loadiq.endpoints.loadboard.save_posted_load_endpoint import SavePostedLoadEndpoint
from applications.api.loadiq.endpoints.loadboard.search_location_name_endpoint import SearchLocationNameEndpoint
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers
from core.utils.decorator import test
from applications.api.loadiq.common.LoadIQBaseTest import LoadIQBaseTest
from applications.api.loadiq.config.decorators import *
from applications.api.loadiq.endpoints.loadboard.generate_load_number_endpoint import GenerateLoadNumberEndpoint

logger = setup_logger('TestShipmentCreation')


@pytest.fixture(scope="class")
def shipment_creation_data():
    # path = helpers.get_file_path("shipment_creation_first_come_first_serve.json")
    # path = helpers.get_file_path("shipment_creation_pre_schedule.json")
    path = helpers.get_file_path("shipment_creation_call_for_appointment.json")
    # Extract JSON Original String
    data = JSONReader().import_json(path)
    # Convert Dynamic Field dates
    parse = helpers.parse_dynamic_dates_values(data)
    # Print JSON Data Converted
    helpers.print_json(title="Shipment Data", data=parse)
    return parse


@pytest.fixture(scope="session")
def shared_data():
    return SavePostedLoadDTO(
        load_number=None
    )


@loadiq_loadboard
class TestShipmentCreation(LoadIQBaseTest):

    generate_load_number = GenerateLoadNumberEndpoint.get_instance()
    search_location_name = SearchLocationNameEndpoint.get_instance()
    save_posted_load = SavePostedLoadEndpoint.get_instance()
    enum_values = GetEnumValuesEndpoint.get_instance()

    '''
    Precondition: Generate a Load Number
    '''
    @test(test_case_id="LOAD-0001", test_description="Test Shipment Creation | Precondition: Generate Load Number")
    def test_create_shipment_generate_load_number(self, shared_data):
        # 01 Get Load Number
        response = self.generate_load_number.get_response()
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_generate_load_number, status_code=200, response=response)
        # 03. Extract The Load Number ID From the Request after pass the success Request with the Customer Portal Account
        dict_response = json.loads(response.text)
        shared_data.load_number = dict_response["data"]

    '''
    Precondition: Gets Origin Search Location from JSON step_1.origin_location.name
    '''
    @test(test_case_id="LOAD-0002", test_description="Test Shipment Creation | Precondition: Get Search Location Origin")
    def test_search_location_name_origin(self, shared_data, shipment_creation_data):
        origin_name = shipment_creation_data['tests']['step_1']['origin_location']['name']
        # 01 Gets Location Data
        origin_response = self.search_location_name.get_response_location(location_name=origin_name)
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_search_location_name_origin, status_code=200, response=origin_response)
        # 03. Extract The Load Number ID From the Request after pass the success Request with the Customer Portal Account
        dict_response = json.loads(origin_response.text)
        # 04. Gets First Location Found on List
        location = dict_response["data"][0]
        helpers.print_json(title="Search Location Origin Response, First Element on List", data=location)
        # 05. Fill Search Information

        shared_data.origin_address_description = location['addressDescription']
        shared_data.origin_number = location['locationNumber']
        shared_data.origin_state = location['state']
        shared_data.origin_postal_code = location['postalCode']
        shared_data.origin_country = location['country']
        shared_data.origin_address_1 = location['address1']
        shared_data.origin_city = location['city']
        shared_data.origin_time_zone = location['timeZone']
        shared_data.origin_contact_name = location['contactName']
        shared_data.origin_contact_phone = location['contactPhone']
        shared_data.origin_contact_email = location['contactEmail']
        shared_data.origin_longitude = location['longitude']
        shared_data.origin_latitude = location['latitude']

    @test(test_case_id="LOAD-0003", test_description="Test Shipment Creation | Step 1: Origin Information")
    def test_create_shipment_step_1_origin_information(self, shared_data, shipment_creation_data):
        logger.info(f"Load Number > Step 1:{shared_data.load_number}")

        # Parse Json Data to Body Request
        payload = shared_data.payload_origin_json(shipment_creation_data)

        # Send Post Request
        response = self.save_posted_load.get_response(payload=payload)

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_step_1_origin_information, status_code=200, response=response)

        # Load Response Data to shared data: Include Date Conversions
        shared_data.get_origin_response(response)
        helpers.print_json(title="Origin Response", data=shared_data.to_json())

        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\request_{shared_data.load_number}_step_1.json"
        )

        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\response_{shared_data.load_number}_step_1.json"
        )

    '''
    Precondition: Gets Origin Search Location from JSON step_2.destination_location.name
    '''
    @test(test_case_id="LOAD-0004", test_description="Test Shipment Creation | Precondition: Get Search Location Destination")
    def test_search_location_name_destination(self, shared_data, shipment_creation_data):
        dest_name = shipment_creation_data['tests']['step_2']['destination_location']['name']
        # 01 Gets Location Data
        dest_response = self.search_location_name.get_response_location(location_name=dest_name)
        # 02. Validate Standard Response
        self.add_report(test_data=self.test_search_location_name_destination, status_code=200, response=dest_response)
        # 03. Extract The Load Number ID From the Request after pass the success Request with the Customer Portal Account
        dict_response = json.loads(dest_response.text)
        # 04. Gets First Location Found on List
        location = dict_response["data"][0]
        helpers.print_json(title="Search Location Origin Response, First Element on List", data=location)
        # 05. Fill Search Information

        shared_data.dest_address_description = location['addressDescription']
        shared_data.dest_number = location['locationNumber']
        shared_data.dest_state = location['state']
        shared_data.dest_postal_code = location['postalCode']
        shared_data.dest_country = location['country']
        shared_data.dest_address_1 = location['address1']
        shared_data.dest_city = location['city']
        shared_data.dest_time_zone = location['timeZone']
        shared_data.dest_contact_name = location['contactName']
        shared_data.dest_contact_phone = location['contactPhone']
        shared_data.dest_contact_email = location['contactEmail']
        shared_data.dest_longitude = location['longitude']
        shared_data.dest_latitude = location['latitude']

    @test(test_case_id="LOAD-0005", test_description="Test Shipment Creation | Step 2: Destination Information")
    def test_create_shipment_step_2_destination_information(self, shared_data, shipment_creation_data):

        # Parse Json Data to Body Request
        payload = shared_data.payload_destination_json(shipment_creation_data)

        # Send Post Request
        response = self.save_posted_load.get_response(payload=payload)

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_step_2_destination_information, status_code=200, response=response)

        # Load Response Data to shared data: Include Date Conversions
        shared_data.get_destination_response(response)
        helpers.print_json(title="Destination Response", data=shared_data.to_json())

        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\request_{shared_data.load_number}_step_2.json"
        )

        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\response_{shared_data.load_number}_step_2.json"
        )

    '''
    Precondition: Gets Equipment Information use step_3.shipment_details.equipment_name from JSON
    '''

    @test(test_case_id="LOAD-0006", test_description="Test Shipment Creation | Precondition: Get Enum Values: Equipment Code")
    def test_get_enum_values_equipment_code(self, shared_data, shipment_creation_data):
        # Search Equipment
        equipment_name = shipment_creation_data['tests']['step_3']['shipment_details']['equipment_name']

        # 01 Get Enum Values
        response = self.enum_values.get_response('equipment_code')

        # Filter Equipment by Name
        shared_data.get_equipment_response(response, equipment_name)

        # 02. Validate Standard Response
        self.add_report(test_data=self.test_get_enum_values_equipment_code, status_code=200, response=response)

    @test(test_case_id="LOAD-0007", test_description="Test Shipment Creation | Step 3: Shipment Details")
    def test_create_shipment_step_3_shipment_details(self, shared_data, shipment_creation_data):

        # Parse Json Data to Body Request
        payload = shared_data.payload_shipment_details(shipment_creation_data)

        # Send Post Request
        response = self.save_posted_load.get_response(payload=payload)

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_step_2_destination_information, status_code=200, response=response)

        # Load Response Data to shared data: Include Date Conversions
        shared_data.get_shipment_details_response(response)
        helpers.print_json(title="Shipment Details Response", data=shared_data.to_json())

        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\request_{shared_data.load_number}_step_3.json"
        )

        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\response_{shared_data.load_number}_step_3.json"
        )

    @test(test_case_id="LOAD-0009", test_description="Test Shipment Creation | Step 4: Freight Items")
    def test_create_shipment_step_4_freight_items(self, shared_data, shipment_creation_data):
        # Parse Json Data to Body Request
        payload = shared_data.payload_freight_items(shipment_creation_data)

        # Send Post Request
        response = self.save_posted_load.get_response(payload=payload)

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_step_4_freight_items, status_code=200, response=response)

        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\request_{shared_data.load_number}_step_4.json"
        )

        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\response_{shared_data.load_number}_step_4.json"
        )

    @test(test_case_id="LOAD-0010", test_description="Test Shipment Creation | Step 5: Bid Parameters")
    def test_create_shipment_step_5_bid_parameters(self, shared_data, shipment_creation_data):
        payload = shared_data.payload_bid_parameters(shipment_creation_data)

        # Send Post Request
        response = self.save_posted_load.get_response(payload=payload)

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_step_5_bid_parameters, status_code=200, response=response)

        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\request_{shared_data.load_number}_step_5.json"
        )

        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\response_{shared_data.load_number}_step_5.json"
        )

