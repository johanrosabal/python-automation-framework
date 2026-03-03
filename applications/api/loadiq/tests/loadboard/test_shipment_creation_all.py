import pytest
import json

from applications.api.loadiq.dtos.loadboard.save_posted_load_dto import SavePostedLoadDTO
from applications.api.loadiq.dtos.loadboard.search_location_dto import SearchLocationDTO
from applications.api.loadiq.endpoints.loadboard.get_enum_values_enpoint import GetEnumValuesEndpoint
from applications.api.loadiq.endpoints.loadboard.save_posted_load_endpoint import SavePostedLoadEndpoint
from applications.api.loadiq.endpoints.loadboard.search_location_name_endpoint import SearchLocationNameEndpoint
from applications.api.loadiq.endpoints.location.get_driving_distance_endpoint import GetDrivingDistanceEndpoint
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
def first_serve_first_come_data():
    path = helpers.get_file_path("shipment_creation_first_come_first_serve.json")
    # Extract JSON Original String
    data = JSONReader().import_json(path)
    # Convert Dynamic Field dates
    parse = helpers.parse_dynamic_dates_values(data)
    # Print JSON Data Converted
    helpers.print_json(title="Shipment Data: First Serve, First Come", data=parse)
    return parse


@pytest.fixture(scope="class")
def pre_schedule_data():
    path = helpers.get_file_path("shipment_creation_pre_schedule.json")
    # Extract JSON Original String
    data = JSONReader().import_json(path)
    # Convert Dynamic Field dates
    parse = helpers.parse_dynamic_dates_values(data)
    # Print JSON Data Converted
    helpers.print_json(title="Shipment Data: Pre-Schedule", data=parse)
    return parse


@pytest.fixture(scope="class")
def call_for_appointment_data():
    path = helpers.get_file_path("shipment_creation_call_for_appointment.json")
    # Extract JSON Original String
    data = JSONReader().import_json(path)
    # Convert Dynamic Field dates
    parse = helpers.parse_dynamic_dates_values(data)
    # Print JSON Data Converted
    helpers.print_json(title="Shipment Data: Call for Appointment", data=parse)
    return parse


@pytest.fixture(scope="session")
def first_serve_dto():
    return SavePostedLoadDTO(
        load_number=None
    )


@pytest.fixture(scope="session")
def pre_schedule_dto():
    return SavePostedLoadDTO(
        load_number=None
    )


@pytest.fixture(scope="session")
def call_for_appointment_dto():
    return SavePostedLoadDTO(
        load_number=None
    )


@loadiq_loadboard
class TestShipmentCreation(LoadIQBaseTest):

    generate_load_number = GenerateLoadNumberEndpoint.get_instance()
    search_location_name = SearchLocationNameEndpoint.get_instance()
    save_posted_load = SavePostedLoadEndpoint.get_instance()
    enum_values = GetEnumValuesEndpoint.get_instance()
    get_driving_distance = GetDrivingDistanceEndpoint.get_instance()

    @test(test_case_id="CT-2546", test_description="Test Shipment Creation | Fist Come, First Serve", skip=False)
    def test_create_shipment_first_serve_first_come(self, first_serve_dto, first_serve_first_come_data):

        # Precondition
        # 01 Get Load Number
        load_number_response = self.generate_load_number.get_response()
        load_number_dict = json.loads(load_number_response.text)
        first_serve_dto.load_number = load_number_dict["data"]
        helpers.print_json(title="Load Number Response", data=load_number_dict)
        # Save Response Text File
        helpers.save_text_to_file(
            text=load_number_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{first_serve_dto.load_number}_response_load_number.json"
        )

        # Precondition
        # Search Location Origin
        # Read Json Origin Location
        origin_name = first_serve_first_come_data['tests']['step_1']['origin_location']['name']
        # Get Response
        origin_response = self.search_location_name.get_response_location(location_name=origin_name)
        # Transform response to Dictionary
        origin_location_dict = json.loads(origin_response.text)
        # Get First Address
        origin_location = origin_location_dict["data"][0]

        # Fill DTO Information
        first_serve_dto.origin_address_description = origin_location['addressDescription']
        first_serve_dto.origin_number = origin_location['locationNumber']
        first_serve_dto.origin_state = origin_location['state']
        first_serve_dto.origin_postal_code = origin_location['postalCode']
        first_serve_dto.origin_country = origin_location['country']
        first_serve_dto.origin_address_1 = origin_location['address1']
        first_serve_dto.origin_city = origin_location['city']
        first_serve_dto.origin_time_zone = origin_location['timeZone']
        first_serve_dto.origin_contact_name = origin_location['contactName']
        first_serve_dto.origin_contact_phone = origin_location['contactPhone']
        first_serve_dto.origin_contact_email = origin_location['contactEmail']
        first_serve_dto.origin_longitude = origin_location['longitude']
        first_serve_dto.origin_latitude = origin_location['latitude']

        # Print Location Information on Log
        helpers.print_json(title="Search Location Origin Response", data=origin_location)
        # Save Response Text File
        helpers.save_text_to_file(
            text=origin_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{first_serve_dto.load_number}_response_location_origin.json"
        )

        # Precondition
        # Search Location Destination
        # Read Json Destination Location
        dest_name = first_serve_first_come_data['tests']['step_2']['destination_location']['name']
        # Get Response
        dest_response = self.search_location_name.get_response_location(location_name=dest_name)
        # Transform response to Dictionary
        destination_location_dict = json.loads(dest_response.text)
        # Get First Address
        destination_location = destination_location_dict["data"][0]

        # Fill DTO Information
        first_serve_dto.dest_address_description = destination_location['addressDescription']
        first_serve_dto.dest_number = destination_location['locationNumber']
        first_serve_dto.dest_state = destination_location['state']
        first_serve_dto.dest_postal_code = destination_location['postalCode']
        first_serve_dto.dest_country = destination_location['country']
        first_serve_dto.dest_address_1 = destination_location['address1']
        first_serve_dto.dest_city = destination_location['city']
        first_serve_dto.dest_time_zone = destination_location['timeZone']
        first_serve_dto.dest_contact_name = destination_location['contactName']
        first_serve_dto.dest_contact_phone = destination_location['contactPhone']
        first_serve_dto.dest_contact_email = destination_location['contactEmail']
        first_serve_dto.dest_longitude = destination_location['longitude']
        first_serve_dto.dest_latitude = destination_location['latitude']
        # Print Response
        helpers.print_json(title="Search Location Destination Response, First Element on List", data=destination_location)
        # Save Response Text File
        helpers.save_text_to_file(
            text=dest_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{first_serve_dto.load_number}_response_location_destination.json"
        )

        # Precondition
        # Get Distance Between Points
        distance_response = self.get_driving_distance.get_response(
            from_longitude=first_serve_dto.origin_longitude,
            from_latitude=first_serve_dto.origin_latitude,
            to_longitude=first_serve_dto.dest_longitude,
            to_latitude=first_serve_dto.dest_latitude
        )
        # Print Response
        helpers.print_json(title="Get Driving Distance", data=distance_response.text)
        # Save Response Text File
        helpers.save_text_to_file(
            text=distance_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{first_serve_dto.load_number}_response_distance.json"
        )

        # Transform response to Dictionary
        distance_response_dict = json.loads(distance_response.text)
        first_serve_dto.distance = distance_response_dict['data']

        # Precondition
        # Equipment Code
        equipment_name = first_serve_first_come_data['tests']['step_3']['shipment_details']['equipment_name']
        equipment_response = self.enum_values.get_response('equipment_code')
        first_serve_dto.get_equipment_response(equipment_response, equipment_name)

        # Set Origin Information on DTO
        first_serve_dto.payload_origin_json(first_serve_first_come_data)
        # Set Destination Information on DTO
        first_serve_dto.payload_destination_json(first_serve_first_come_data)
        # Set Shipment Details
        first_serve_dto.payload_shipment_details(first_serve_first_come_data)
        # Set Freight Items
        first_serve_dto.payload_freight_items(first_serve_first_come_data)
        # Set Bid Parameters
        first_serve_dto.payload_bid_parameters(first_serve_first_come_data)
        # Edition Number for Load
        first_serve_dto.edition = 1

        # Send POST REQUEST
        response = self.save_posted_load.get_response(payload=first_serve_dto.to_json())

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_first_serve_first_come, status_code=200, response=response)
        # Save Response Text File
        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\{first_serve_dto.load_number}_request.json"
        )
        # Save Response Text File
        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{first_serve_dto.load_number}_response.json"
        )

    @test(test_case_id="CT-2553", test_description="Test Shipment Creation | Pre-Schedule", skip=False)
    def test_create_shipment_pre_schedule(self, pre_schedule_dto, pre_schedule_data):

        # Precondition
        # 01 Get Load Number
        load_number_response = self.generate_load_number.get_response()
        load_number_dict = json.loads(load_number_response.text)
        pre_schedule_dto.load_number = load_number_dict["data"]
        helpers.print_json(title="Load Number Response", data=load_number_dict)
        # Save Response Text File
        helpers.save_text_to_file(
            text=load_number_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{pre_schedule_dto.load_number}_response_load_number.json"
        )

        # Precondition
        # Search Location Origin
        # Read Json Origin Location
        origin_name = pre_schedule_data['tests']['step_1']['origin_location']['name']
        # Get Response
        origin_response = self.search_location_name.get_response_location(location_name=origin_name)
        # Transform response to Dictionary
        origin_location_dict = json.loads(origin_response.text)
        # Get First Address
        origin_location = origin_location_dict["data"][0]

        # Fill DTO Information
        pre_schedule_dto.origin_address_description = origin_location['addressDescription']
        pre_schedule_dto.origin_number = origin_location['locationNumber']
        pre_schedule_dto.origin_state = origin_location['state']
        pre_schedule_dto.origin_postal_code = origin_location['postalCode']
        pre_schedule_dto.origin_country = origin_location['country']
        pre_schedule_dto.origin_address_1 = origin_location['address1']
        pre_schedule_dto.origin_city = origin_location['city']
        pre_schedule_dto.origin_time_zone = origin_location['timeZone']
        pre_schedule_dto.origin_contact_name = origin_location['contactName']
        pre_schedule_dto.origin_contact_phone = origin_location['contactPhone']
        pre_schedule_dto.origin_contact_email = origin_location['contactEmail']
        pre_schedule_dto.origin_longitude = origin_location['longitude']
        pre_schedule_dto.origin_latitude = origin_location['latitude']

        # Print Location Information on Log
        helpers.print_json(title="Search Location Origin Response", data=origin_location)
        # Save Response Text File
        helpers.save_text_to_file(
            text=origin_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{pre_schedule_dto.load_number}_response_location_origin.json"
        )

        # Precondition
        # Search Location Destination
        # Read Json Destination Location
        dest_name = pre_schedule_data['tests']['step_2']['destination_location']['name']
        # Get Response
        dest_response = self.search_location_name.get_response_location(location_name=dest_name)
        # Transform response to Dictionary
        destination_location_dict = json.loads(dest_response.text)
        # Get First Address
        destination_location = destination_location_dict["data"][0]

        # Fill DTO Information
        pre_schedule_dto.dest_address_description = destination_location['addressDescription']
        pre_schedule_dto.dest_number = destination_location['locationNumber']
        pre_schedule_dto.dest_state = destination_location['state']
        pre_schedule_dto.dest_postal_code = destination_location['postalCode']
        pre_schedule_dto.dest_country = destination_location['country']
        pre_schedule_dto.dest_address_1 = destination_location['address1']
        pre_schedule_dto.dest_city = destination_location['city']
        pre_schedule_dto.dest_time_zone = destination_location['timeZone']
        pre_schedule_dto.dest_contact_name = destination_location['contactName']
        pre_schedule_dto.dest_contact_phone = destination_location['contactPhone']
        pre_schedule_dto.dest_contact_email = destination_location['contactEmail']
        pre_schedule_dto.dest_longitude = destination_location['longitude']
        pre_schedule_dto.dest_latitude = destination_location['latitude']
        # Print Response
        helpers.print_json(title="Search Location Origin Response, First Element on List", data=destination_location)
        # Save Response Text File
        helpers.save_text_to_file(
            text=dest_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{pre_schedule_dto.load_number}_response_location_destination.json"
        )

        # Precondition
        # Get Distance Between Points
        distance_response = self.get_driving_distance.get_response(
            from_longitude=pre_schedule_dto.origin_longitude,
            from_latitude=pre_schedule_dto.origin_latitude,
            to_longitude=pre_schedule_dto.dest_longitude,
            to_latitude=pre_schedule_dto.dest_latitude
        )
        # Print Response
        helpers.print_json(title="Get Driving Distance", data=distance_response.text)
        # Save Response Text File
        helpers.save_text_to_file(
            text=distance_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{pre_schedule_dto.load_number}_response_distance.json"
        )

        # Transform response to Dictionary
        distance_response_dict = json.loads(distance_response.text)
        pre_schedule_dto.distance = distance_response_dict['data']

        # Precondition
        # Equipment Code
        equipment_name = pre_schedule_data['tests']['step_3']['shipment_details']['equipment_name']
        equipment_response = self.enum_values.get_response('equipment_code')
        pre_schedule_dto.get_equipment_response(equipment_response, equipment_name)

        # Set Origin Information on DTO
        pre_schedule_dto.payload_origin_json(pre_schedule_data)
        # Set Destination Information on DTO
        pre_schedule_dto.payload_destination_json(pre_schedule_data)
        # Set Shipment Details
        pre_schedule_dto.payload_shipment_details(pre_schedule_data)
        # Set Freight Items
        pre_schedule_dto.payload_freight_items(pre_schedule_data)
        # Set Bid Parameters
        pre_schedule_dto.payload_bid_parameters(pre_schedule_data)

        # Send POST REQUEST
        response = self.save_posted_load.get_response(payload=pre_schedule_dto.to_json())

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_pre_schedule, status_code=200, response=response)
        # Save Response Text File
        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\{pre_schedule_dto.load_number}_request.json"
        )
        # Save Response Text File
        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{pre_schedule_dto.load_number}_response.json"
        )

    @test(test_case_id="CT-2554", test_description="Test Shipment Creation | Call for Appointment", skip=False)
    def test_create_shipment_call_for_appointment(self,  call_for_appointment_dto, call_for_appointment_data):

        # Precondition
        # 01 Get Load Number
        load_number_response = self.generate_load_number.get_response()
        load_number_dict = json.loads(load_number_response.text)
        call_for_appointment_dto.load_number = load_number_dict["data"]
        helpers.print_json(title="Load Number Response", data=load_number_dict)
        # Save Response Text File
        helpers.save_text_to_file(
            text=load_number_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{call_for_appointment_dto.load_number}_response_load_number.json"
        )

        # Precondition
        # Search Location Origin
        # Read Json Origin Location
        origin_name = call_for_appointment_data['tests']['step_1']['origin_location']['name']
        # Get Response
        origin_response = self.search_location_name.get_response_location(location_name=origin_name)
        # Transform response to Dictionary
        origin_location_dict = json.loads(origin_response.text)
        # Get First Address
        origin_location = origin_location_dict["data"][0]

        # Fill DTO Information
        call_for_appointment_dto.origin_address_description = origin_location['addressDescription']
        call_for_appointment_dto.origin_number = origin_location['locationNumber']
        call_for_appointment_dto.origin_state = origin_location['state']
        call_for_appointment_dto.origin_postal_code = origin_location['postalCode']
        call_for_appointment_dto.origin_country = origin_location['country']
        call_for_appointment_dto.origin_address_1 = origin_location['address1']
        call_for_appointment_dto.origin_city = origin_location['city']
        call_for_appointment_dto.origin_time_zone = origin_location['timeZone']
        call_for_appointment_dto.origin_contact_name = origin_location['contactName']
        call_for_appointment_dto.origin_contact_phone = origin_location['contactPhone']
        call_for_appointment_dto.origin_contact_email = origin_location['contactEmail']
        call_for_appointment_dto.origin_longitude = origin_location['longitude']
        call_for_appointment_dto.origin_latitude = origin_location['latitude']

        # Print Location Information on Log
        helpers.print_json(title="Search Location Origin Response", data=origin_location)
        # Save Response Text File
        helpers.save_text_to_file(
            text=origin_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{call_for_appointment_dto.load_number}_response_location_origin.json"
        )

        # Precondition
        # Search Location Destination
        # Read Json Destination Location
        dest_name = call_for_appointment_data['tests']['step_2']['destination_location']['name']
        # Get Response
        dest_response = self.search_location_name.get_response_location(location_name=dest_name)
        # Transform response to Dictionary
        destination_location_dict = json.loads(dest_response.text)
        # Get First Address
        destination_location = destination_location_dict["data"][0]

        # Fill DTO Information
        call_for_appointment_dto.dest_address_description = destination_location['addressDescription']
        call_for_appointment_dto.dest_number = destination_location['locationNumber']
        call_for_appointment_dto.dest_state = destination_location['state']
        call_for_appointment_dto.dest_postal_code = destination_location['postalCode']
        call_for_appointment_dto.dest_country = destination_location['country']
        call_for_appointment_dto.dest_address_1 = destination_location['address1']
        call_for_appointment_dto.dest_city = destination_location['city']
        call_for_appointment_dto.dest_time_zone = destination_location['timeZone']
        call_for_appointment_dto.dest_contact_name = destination_location['contactName']
        call_for_appointment_dto.dest_contact_phone = destination_location['contactPhone']
        call_for_appointment_dto.dest_contact_email = destination_location['contactEmail']
        call_for_appointment_dto.dest_longitude = destination_location['longitude']
        call_for_appointment_dto.dest_latitude = destination_location['latitude']
        # Print Response
        helpers.print_json(title="Search Location Origin Response, First Element on List", data=destination_location)
        # Save Response Text File
        helpers.save_text_to_file(
            text=dest_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{call_for_appointment_dto.load_number}_response_location_destination.json"
        )

        # Precondition
        # Get Distance Between Points
        distance_response = self.get_driving_distance.get_response(
            from_longitude=call_for_appointment_dto.origin_longitude,
            from_latitude=call_for_appointment_dto.origin_latitude,
            to_longitude=call_for_appointment_dto.dest_longitude,
            to_latitude=call_for_appointment_dto.dest_latitude
        )
        # Print Response
        helpers.print_json(title="Get Driving Distance", data=distance_response.text)
        # Save Response Text File
        helpers.save_text_to_file(
            text=distance_response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{call_for_appointment_dto.load_number}_response_distance.json"
        )

        # Transform response to Dictionary
        distance_response_dict = json.loads(distance_response.text)
        call_for_appointment_dto.distance = distance_response_dict['data']

        # Equipment Code
        equipment_name = call_for_appointment_data['tests']['step_3']['shipment_details']['equipment_name']
        equipment_response = self.enum_values.get_response('equipment_code')
        call_for_appointment_dto.get_equipment_response(equipment_response, equipment_name)

        # Set Origin Information on DTO
        call_for_appointment_dto.payload_origin_json(call_for_appointment_data)
        # Set Destination Information on DTO
        call_for_appointment_dto.payload_destination_json(call_for_appointment_data)
        # Set Shipment Details
        call_for_appointment_dto.payload_shipment_details(call_for_appointment_data)
        # Set Freight Items
        call_for_appointment_dto.payload_freight_items(call_for_appointment_data)
        # Set Bid Parameters
        call_for_appointment_dto.payload_bid_parameters(call_for_appointment_data)

        # Send POST REQUEST
        response = self.save_posted_load.get_response(payload=call_for_appointment_dto.to_json())

        # Validate Standard Response
        self.add_report(test_data=self.test_create_shipment_call_for_appointment, status_code=200, response=response)

        # Save Response Text File
        helpers.save_text_to_file(
            text=response.request.body,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\requests\\{call_for_appointment_dto.load_number}_request.json"
        )
        # Save Response Text File
        helpers.save_text_to_file(
            text=response.text,
            filename=f"applications\\api\\loadiq\\tests\\loadboard\\responses\\{call_for_appointment_dto.load_number}_response.json"
        )


