from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List
from core.config.logger_config import setup_logger
from core.utils.helpers import *
import json


@dataclass
class FreightItems:
    freightitemid: Optional[int] = None
    is_deleted: Optional[bool] = False
    postedloadid: Optional[int] = 0
    item_number: Optional[int] = 0
    # Gross Weight
    gross_weight: Optional[str] = None
    gross_weight_in_lbs: Optional[0] = 0  # Calculated Conversion
    weight_display_value: Optional[str] = None
    gross_weight_UOM: Optional[str] = None
    handling_unit_count: Optional[str] = None
    handling_unit_type: Optional[str] = None
    handling_unit_type_display_value: Optional[str] = None
    commodity_value: Optional[str] = None

    # Dimension
    length: Optional[str] = None
    length_in_inches: Optional[str] = None  # Calculated Conversion
    width: Optional[str] = None
    width_in_inches: Optional[str] = None  # Calculated Conversion
    height: Optional[str] = None
    height_in_inches: Optional[str] = None  # Calculated Conversion

    dim_UOM: Optional[str] = None
    dim_display_value: Optional[str] = None
    is_hazmat: Optional[str] = False
    is_delete: Optional[bool] = False
    description: Optional[str] = None

    # When Hazmat is TRUE
    un_class: Optional[str] = None
    hazmat_class: Optional[str] = None
    hazmat_class_Name: Optional[str] = None
    hazmat_contact_number: Optional[str] = None
    packing_group: Optional[str] = None
    packing_group_name: Optional[str] = None
    piece_type: Optional[str] = None
    piece_count: Optional[float] = 0

    # TODO When Save Full Item, this are not trackable Fields, we need to verify this fields
    freight_class: Optional[str] = None
    gross_volume: Optional[int] = 0
    gross_volume_UOM: Optional[str] = None

    def to_dict(self):
        """Converts FreightItems to a dictionary."""
        return {to_camel_case(k, ["UOM"]): v for k, v in asdict(self).items()}


logger = setup_logger('SavePostedLoadDTO')


@dataclass
class SavePostedLoadDTO:
    postedloadid: Optional[str] = None  # None on New Records
    edition: Optional[int] = None  # None on New Records
    load_number: Optional[str] = None  # None on New Records
    tendered_to_carrier_number: Optional[str] = None  # ??? What is this field

    date_created: Optional[str] = None  # Since Step 2
    date_modified: Optional[str] = None  # Since Step 2
    created_by: Optional[str] = None  # Since Step 2
    customer_number: Optional[str] = None  # Since Step 2

    isdeleted: Optional[bool] = False  # None on New Records
    is_draft: Optional[bool] = True  # None on New Records
    is_expedited: Optional[bool] = False  # None on New Records  ????

    load_board_status: Optional[str] = None  # None on New Records
    load_board_status_type: Optional[str] = None  # None on New Records
    load_board_API_status: Optional[str] = None  # None on New Records

    draft_page: Optional[str] = None  # "destination" on New Records ??
    next_tab: Optional[str] = None  # Step 1 empty ""

    # TOTALS
    target_rate: Optional[int] = 0  # None on New Records
    distance: Optional[str] = None  # TODO Need to Know how it gets this value ???
    distance_UOM: Optional[str] = None  # None on New Records

    # ------------------------------------------ ORIGIN ----------------------------------------------------------------
    origin_number: Optional[str] = None  # None on New Records
    # Origin Location From JSON
    origin_name: Optional[str] = None  # Step 1: JSON origin_location.name
    origin_address_description: Optional[str] = None  # Step 1: JSON origin_location.address_description
    origin_city: Optional[str] = None  # Step 1: JSON origin_location.location
    origin_address_1: Optional[str] = None  # Step 1: JSON origin_location.address_line_1
    origin_address_2: Optional[str] = None  # Step 1: JSON origin_location.address_line_1

    # Origin Location: Data Capture From Endpoint 'SearchLocationEndpoint' or JSON
    origin_state: Optional[str] = None  # Step 1: JSON origin_location.state
    origin_postal_code: Optional[str] = None  # Step 1: JSON origin_location.postal_code
    origin_country: Optional[str] = None  # Step 1: JSON origin_location.country

    # Contact Name: Data Capture From Endpoint 'SearchLocationEndpoint'
    origin_contact_name: Optional[str] = None  # Step 1: data.contactName From 'SearchLocationEndpoint'
    origin_contact_email: Optional[str] = None  # Step 1: data.contactEmail From 'SearchLocationEndpoint'
    origin_contact_phone: Optional[str] = None  # Step 1: data.contactPhone From 'SearchLocationEndpoint'
    origin_longitude: Optional[float] = None  # Step 1: data.longitude From 'SearchLocationEndpoint'
    origin_latitude: Optional[float] = None  # Step 1: data.latitude From 'SearchLocationEndpoint'
    origin_time_zone: Optional[str] = None  # Step 1: data.timeZone From 'SearchLocationEndpoint' ***

    # Delivery Appointment From JSON
    origin_appointment_required: Optional[bool] = False  # TODO Ask for this field
    origin_datetime_option: Optional[str] = None  # Step 1: JSON origin_pickup.pick_up_type
    # Date Conversions
    origin_global_arrival_datetime: Optional[str] = None  # None on New Records
    origin_local_arrival_datetime: Optional[str] = None  # TODO Date Convertion on New Records
    origin_global_departure_datetime: Optional[str] = None  # None on New Records
    origin_local_departure_datetime: Optional[str] = None  # TODO Date Convertion on New Records
    origin_UTC_Arrival_Datetime: Optional[str] = None  # TODO Date Convertion on New Records
    origin_UTC_Departure_Datetime: Optional[str] = None  # TODO Date Convertion on New Records
    origin_open_time: Optional[str] = None  # Step 1: JSON origin_pickup.Hours+Minutes+Indicator
    origin_close_time: Optional[str] = None  # Step 1: JSON origin_pickup.Hours+Minutes+Indicator
    pickup_local_datetime: Optional[str] = None

    # Point of Contact From JSON
    origin_use_current_contact: Optional[str] = None  # Step 1: Boolean
    origin_appointment_contact_name: Optional[str] = None  # Step 1: JSON point_of_contact.name
    origin_appointment_contact_phone: Optional[str] = None  # Step 1: JSON point_of_contact.phone
    origin_appointment_contact_email: Optional[str] = None  # Step 1: JSON point_of_contact.email

    # ------------------------------------------ DESTINATION -----------------------------------------------------------
    dest_number: Optional[str] = None  # None on New Records
    # Origin Location From JSON
    dest_name: Optional[str] = None  # Step 1: JSON destination_location.name
    dest_city: Optional[str] = None  # Step 1: JSON destination_location.location
    dest_address_description: Optional[str] = None  # Step 1: JSON destination_location.address_description
    dest_address_1: Optional[str] = None  # Step 1: JSON destination_location.address_line_1
    dest_address_2: Optional[str] = None  # Step 1: JSON destination_location.address_line_1

    # Origin Location: Data Capture From Endpoint 'SearchLocationEndpoint'
    dest_state: Optional[str] = None  # Step 1: data.state From 'SearchLocationEndpoint'
    dest_postal_code: Optional[str] = None  # Step 1: data.postalCode From 'SearchLocationEndpoint'
    dest_country: Optional[str] = None  # Step 1: data.country From 'SearchLocationEndpoint'

    # Contact Name: Data Capture From Endpoint 'SearchLocationEndpoint'
    dest_contact_name: Optional[str] = None  # Step 1: data.contactName From 'SearchLocationEndpoint'
    dest_contact_email: Optional[str] = None  # Step 1: data.contactEmail From 'SearchLocationEndpoint'
    dest_contact_phone: Optional[str] = None  # Step 1: data.contactPhone From 'SearchLocationEndpoint'
    dest_longitude: Optional[float] = None  # Step 1: data.longitude From 'SearchLocationEndpoint'
    dest_latitude: Optional[float] = None  # Step 1: data.latitude From 'SearchLocationEndpoint'
    dest_time_zone: Optional[str] = None  # Step 1: data.timeZone From 'SearchLocationEndpoint' ***

    # Delivery Appointment From JSON
    dest_appointment_required: Optional[bool] = False  # Since Step 3
    dest_datetime_option: Optional[str] = None  # Step 1: JSON origin_pickup.pick_up_type
    # Date Conversions
    dest_global_arrival_datetime: Optional[str] = None  # None on New Records
    dest_local_arrival_datetime: Optional[str] = None  # TODO Date Convertion on New Records
    dest_global_departure_datetime: Optional[str] = None  # None on New Records
    dest_local_departure_datetime: Optional[str] = None  # TODO Date Convertion on New Records
    dest_UTC_Arrival_Datetime: Optional[str] = None  # TODO Date Convertion on New Records
    dest_UTC_Departure_Datetime: Optional[str] = None  # TODO Date Convertion on New Records
    #
    dest_open_time: Optional[str] = None  # Step 1: JSON destination_pickup.Hours+Minutes+Indicator
    dest_close_time: Optional[str] = None  # Step 1: JSON destination_pickup.Hours+Minutes+Indicator
    delivery_Local_datetime: Optional[str] = None

    # Point of Contact From JSON
    dest_use_current_contact: Optional[str] = None  # Step 1: Boolean
    dest_appointment_contact_name: Optional[str] = None  # Step 1: JSON point_of_contact.name
    dest_appointment_contact_phone: Optional[str] = None  # Step 1: JSON point_of_contact.phone
    dest_appointment_contact_email: Optional[str] = None  # Step 1: JSON point_of_contact.email

    # ------------------------------------------ SHIPMENT DETAILS ------------------------------------------------------
    transport_mode: Optional[str] = None  # Since Step 3
    equipment_code: Optional[str] = None  # Since Step 3
    equipment_Name: Optional[str] = None  # None on New Records
    add_on_service: Optional[str] = None  # None on New Records
    add_on_services: List[str] = field(default_factory=list)  # None on New Records []
    po_number: Optional[str] = None  # Since Step 3
    bol_number: Optional[str] = None  # Since Step 3
    pickup_number: Optional[str] = None  # Since Step 3
    comment: Optional[str] = None  # Since Step 3
    min_temperature: Optional[str] = None  # Since Step 3
    max_temperature: Optional[str] = None  # Since Step 3

    # ------------------------------------------ FREIGHT ITEMS ---------------------------------------------------------
    is_hazmat: Optional[str] = False  # Since Step 2
    load_value: Optional[float] = None  # Since Step 2
    weight: Optional[float] = None  # None on New Records
    weight_in_libs: Optional[float] = None  # None on New Records
    weight_UOM: Optional[str] = None  # None on New Records
    volume: Optional[float] = None  # None on New Records
    volume_UOM: Optional[str] = None  # None on New Records
    volume_in_cuft: Optional[float] = None  # None on New Records

    piece_count: Optional[int] = 0
    piece_type: Optional[str] = None

    freight_item: Optional[str] = None  # None on New Records
    freight_items: List[FreightItems] = field(default_factory=list)  # None on New Records []

    # ------------------------------------------ BID PARAMETERS --------------------------------------------------------
    book_now_price: Optional[str] = 0  # 0 on New Records
    expiration_datetime: Optional[str] = None  # None on New Records
    posted_load_bid: List[str] = field(default_factory=list)  # None on New Records []

    def to_dict(self):
        """Converts SavePostedLoadDTO to a dictionary."""
        data_dict = asdict(self)
        data_dict = {to_camel_case(k, ["API", "UTC", "UOM"]): v for k, v in data_dict.items()}

        if self.freight_items:
            data_dict["freightItems"] = [
                {to_camel_case(k, ["API", "UTC", "UOM"]): v for k, v in item.to_dict().items()}
                for item in self.freight_items
            ]

        return data_dict

    def extract_fields(self, fields: List[str]) -> Dict[str, Any]:
        """
        Extracts only the specified fields and returns a dictionary.
        Handles nested DTOs properly.
        """
        full_data = self.to_dict()
        return {to_camel_case(key, ["API", "UTC", "UOM"]): full_data[to_camel_case(key, ["API", "UTC", "UOM"])] for key
                in fields if to_camel_case(key, ["API", "UTC", "UOM"]) in full_data}

    def to_json(self, fields: Optional[List[str]] = None) -> str:
        """
               Returns a JSON representation of the DTO.
               If `fields` is provided, only those fields are included.
               """
        data = self.extract_fields(fields) if fields else self.to_dict()
        return json.dumps(data, indent=4)

    def payload_origin_json(self, shipment_creation_data):

        step_1 = shipment_creation_data['tests']['step_1']
        # Origin Location
        if step_1.get('origin_location', {}).get('name') is not None:
            self.origin_name = step_1['origin_location']['name']

        if step_1.get('origin_location', {}).get('address_description') is not None:
            self.origin_address_description = step_1['origin_location']['address_description']

        if step_1.get('origin_location', {}).get('state') is not None:
            self.origin_state = step_1['origin_location']['state']

        if step_1.get('origin_location', {}).get('postal_code') is not None:
            self.origin_postal_code = step_1['origin_location']['postal_code']

        if step_1.get('origin_location', {}).get('country') is not None:
            self.origin_country = step_1['origin_location']['country']

        if step_1.get('origin_location', {}).get('address_line_1') is not None:
            self.origin_address_1 = step_1['origin_location']['address_line_1']

        if step_1.get('origin_location', {}).get('address_line_2') is not None:
            self.origin_address_2 = step_1['origin_location']['address_line_2']

        if step_1.get('origin_location', {}).get('city') is not None:
            self.origin_city = step_1['origin_location']['city']

        if step_1.get('origin_location', {}).get('time_zone') is not None:
            self.origin_time_zone = step_1['origin_location']['time_zone']

        if step_1.get('origin_location', {}).get('longitude') is not None:
            self.origin_longitude = float(step_1['origin_location']['longitude'])

        if step_1.get('origin_location', {}).get('latitude') is not None:
            self.origin_latitude = float(step_1['origin_location']['latitude'])

        # Contact Name Fill Information if Is not Null on the JSON Payload
        if step_1.get('origin_contact', {}).get('name') is not None:
            self.origin_contact_name = step_1['origin_contact']['name']
        if step_1.get('origin_contact', {}).get('phone') is not None:
            self.origin_contact_phone = format_phone_number(step_1['origin_contact']['phone'])
        if step_1.get('origin_contact', {}).get('email') is not None:
            self.origin_contact_email = step_1['origin_contact']['email']

        # Appointment
        self.origin_datetime_option = step_1['origin_appointment']['datetime_option']
        self.origin_appointment_required = bool(step_1['origin_appointment']['appointment_required'])

        if self.origin_datetime_option == "first_come_first_serve":
            # OPEN DATES CALCULATION
            open_hours = step_1['origin_appointment']['open_hours']
            open_minutes = step_1['origin_appointment']['open_minutes']
            open_indicator = step_1['origin_appointment']['open_indicator']

            open_date = step_1['origin_appointment']['from_day']
            open_time = f"{open_hours}:{open_minutes} {open_indicator}"
            open_time_24 = convert_to_24_hour(open_time)
            pickup_from_day = convert_date_format_to_iso8601(date_str=open_date, time_str=open_time)
            # Date Local Time Conversion to ISO 8601
            self.origin_local_arrival_datetime = pickup_from_day
            self.origin_open_time = f"{open_time_24}"

            # CLOSE DATE CALCULATION
            close_hours = step_1['origin_appointment']['close_hours']
            close_minutes = step_1['origin_appointment']['close_minutes']
            close_indicator = step_1['origin_appointment']['close_indicator']

            close_date = step_1['origin_appointment']['to_day']
            close_time = f"{close_hours}:{close_minutes} {close_indicator}"
            close_time_24 = convert_to_24_hour(close_time)
            pickup_to_day = convert_date_format_to_iso8601(date_str=close_date, time_str=close_time)
            # Date Local Time Conversion to ISO 8601
            self.origin_local_departure_datetime = pickup_to_day
            self.origin_close_time = f"{close_time_24}"

        if self.origin_datetime_option == "pre_scheduled":
            # OPEN DATES CALCULATION
            hours = step_1['origin_appointment']['hours']
            minutes = step_1['origin_appointment']['minutes']
            indicator = step_1['origin_appointment']['indicator']

            date_ = step_1['origin_appointment']['to_day']
            time_ = f"{hours}:{minutes} {indicator}"
            pickup_to_day = convert_date_format_to_iso8601(date_str=date_, time_str=time_)
            # Date Local Time Conversion to ISO 8601
            self.origin_local_arrival_datetime = pickup_to_day
            self.origin_local_departure_datetime = pickup_to_day
            # These Fields Should be Null on Pre-Schedule
            self.origin_open_time = None
            self.origin_close_time = None

        if self.origin_datetime_option == "call_for_appointment":
            self.origin_use_current_contact = None

        # Point of Contact
        if step_1.get('point_of_contact', {}).get('use_current_contact') is not False:
            self.origin_use_current_contact = step_1['point_of_contact']['use_current_contact']

        if step_1.get('point_of_contact', {}).get('name') is not None:
            self.origin_appointment_contact_name = step_1['point_of_contact']['name']

        if step_1.get('point_of_contact', {}).get('email') is not None:
            self.origin_appointment_contact_email = step_1['point_of_contact']['email']

        if step_1.get('point_of_contact', {}).get('phone') is not None:
            self.origin_appointment_contact_phone = format_phone_number(step_1['point_of_contact']['phone'])

        self.draft_page = "destination"
        self.next_tab = ""

        json_data = self.to_json(fields=[
            "postedloadid", "edition", "date_created", "date_modified", "isdeleted", "load_number", "po_number",
            "bol_number", "comment", "is_draft", "draft_page", "customer_number", "load_board_API_status",
            "transport_mode", "is_expedited", "equipment_code", "equipment_name", "weight", "weight_UOM",
            "volume", "volume_UOM", "distance", "distance_UOM", "book_now_price", "expiration_datetime", "created_by",
            "freightItem", "add_on_service", "origin_global_arrival_datetime", "origin_local_arrival_datetime",
            "origin_global_departure_datetime", "origin_local_departure_datetime", "origin_state", "origin_postal_code",
            "origin_country", "origin_number", "origin_name", "origin_address_1", "origin_address_2", "origin_city",
            "origin_contact_name", "origin_contact_email", "origin_contact_phone", "origin_longitude",
            "origin_latitude",
            "origin_appointment_contact_phone", "originAppointmentContactName", "origin_appointment_contact_email",
            "dest_longitude", "dest_latitude", "dest_global_arrival_datetime", "dest_local_arrival_datetime",
            "dest_global_departure_datetime", "dest_local_departure_datetime", "dest_state", "dest_postal_code",
            "dest_country", "dest_number", "dest_name", "dest_address1", "dest_address2", "dest_city",
            "dest_contact_name", "dest_contact_email", "dest_contact_phone", "dest_datetime_option", "dest_open_time",
            "dest_close_time", "dest_appointment_contact_phone", "dest_appointment_contact_name",
            "dest_appointment_contact_email", "dest_appointment_required", "next_tab", "freight_items",
            "add_on_services", "posted_load_bid", "target_rate", "load_board_status", "load_board_status_type",
            "origin_address_description", "dest_address_description", "min_temperature", "max_temperature",
            "pickup_number", "origin_datetime_option", "origin_open_time", "origin_close_time",
        ])

        return json_data

    def payload_destination_json(self, shipment_creation_data):
        self.edition = 1
        step_2 = shipment_creation_data['tests']['step_2']
        # Destination Location
        if step_2.get('destination_location', {}).get('name') is not None:
            self.dest_name = step_2['destination_location']['name']

        if step_2.get('destination_location', {}).get('address_description') is not None:
            self.dest_address_description = step_2['destination_location']['address_description']

        if step_2.get('destination_location', {}).get('state') is not None:
            self.dest_state = step_2['destination_location']['state']

        if step_2.get('destination_location', {}).get('postal_code') is not None:
            self.dest_postal_code = step_2['destination_location']['postal_code']

        if step_2.get('destination_location', {}).get('country') is not None:
            self.dest_country = step_2['destination_location']['country']

        if step_2.get('destination_location', {}).get('address_line_1') is not None:
            self.dest_address_1 = step_2['destination_location']['address_line_1']

        if step_2.get('destination_location', {}).get('address_line_2') is not None:
            self.dest_address_2 = step_2['destination_location']['address_line_2']

        if step_2.get('destination_location', {}).get('city') is not None:
            self.dest_city = step_2['destination_location']['city']

        if step_2.get('destination_location', {}).get('time_zone') is not None:
            self.dest_time_zone = step_2['destination_location']['time_zone']

        if step_2.get('destination_location', {}).get('longitude') is not None:
            self.dest_longitude = float(step_2['destination_location']['longitude'])

        if step_2.get('destination_location', {}).get('latitude') is not None:
            self.dest_latitude = float(step_2['destination_location']['latitude'])

        # Contact Name Fill Information if Is not Null on the JSON Payload
        if step_2.get('destination_contact', {}).get('name') is not None:
            self.dest_contact_name = step_2['destination_contact']['name']

        if step_2.get('destination_contact', {}).get('phone') is not None:
            self.dest_contact_phone = format_phone_number(step_2['destination_contact']['phone'])

        if step_2.get('destination_contact', {}).get('email') is not None:
            self.dest_contact_email = step_2['destination_contact']['email']

        # Appointment
        self.dest_datetime_option = step_2['destination_appointment']['datetime_option']
        self.dest_appointment_required = bool(step_2['destination_appointment']['appointment_required'])

        if self.dest_datetime_option == "first_come_first_serve":
            # OPEN DATES CALCULATION
            open_hours = step_2['destination_appointment']['open_hours']
            open_minutes = step_2['destination_appointment']['open_minutes']
            open_indicator = step_2['destination_appointment']['open_indicator']

            open_date = step_2['destination_appointment']['from_day']
            open_time = f"{open_hours}:{open_minutes} {open_indicator}"
            open_time_24 = convert_to_24_hour(open_time)
            pickup_from_day = convert_date_format_to_iso8601(date_str=open_date, time_str=open_time)
            # Date Local Time Conversion to ISO 8601
            self.dest_local_arrival_datetime = pickup_from_day
            self.dest_open_time = f"{open_time_24}"

            # CLOSE DATE CALCULATION
            close_hours = step_2['destination_appointment']['close_hours']
            close_minutes = step_2['destination_appointment']['close_minutes']
            close_indicator = step_2['destination_appointment']['close_indicator']

            close_date = step_2['destination_appointment']['to_day']
            close_time = f"{close_hours}:{close_minutes} {close_indicator}"
            close_time_24 = convert_to_24_hour(close_time)
            pickup_to_day = convert_date_format_to_iso8601(date_str=close_date, time_str=close_time)
            # Date Local Time Conversion to ISO 8601
            self.dest_local_departure_datetime = pickup_to_day
            self.dest_close_time = f"{close_time_24}"

        if self.dest_datetime_option == "pre_scheduled":
            # OPEN DATES CALCULATION
            hours = step_2['destination_appointment']['hours']
            minutes = step_2['destination_appointment']['minutes']
            indicator = step_2['destination_appointment']['indicator']

            date_ = step_2['destination_appointment']['to_day']
            time_ = f"{hours}:{minutes} {indicator}"
            pickup_to_day = convert_date_format_to_iso8601(date_str=date_, time_str=time_)
            # Date Local Time Conversion to ISO 8601
            self.dest_local_arrival_datetime = pickup_to_day
            self.dest_local_departure_datetime = pickup_to_day
            # These Fields Should be Null on Pre-Schedule
            self.dest_open_time = None
            self.dest_close_time = None

        if self.dest_datetime_option == "call_for_appointment":
            self.dest_use_current_contact = None

        # Point of Contact
        if step_2.get('point_of_contact', {}).get('use_current_contact') is not False:
            self.origin_use_current_contact = step_2['point_of_contact']['use_current_contact']

        if step_2.get('point_of_contact', {}).get('name') is not None:
            self.origin_appointment_contact_name = step_2['point_of_contact']['name']

        if step_2.get('point_of_contact', {}).get('email') is not None:
            self.origin_appointment_contact_email = step_2['point_of_contact']['email']

        if step_2.get('point_of_contact', {}).get('phone') is not None:
            self.origin_appointment_contact_phone = format_phone_number(step_2['point_of_contact']['phone'])

        self.draft_page = "details"
        self.next_tab = "destination"
        self.customer_number = "landtrans"
        self.load_board_status = "Posted"
        self.load_board_status_type = "posted"
        self.is_expedited = False

        json_data = self.to_json(fields=[
            "postedloadid", "edition", "date_created", "date_modified", "isdeleted", "load_number",
            "is_draft", "draft_page", "customer_number", "tendered_to_carrier_number", "load_board_status",
            "load_board_status_type",
            "is_expedited", "is_hazmat", "book_now_price", "target_Rate", "created_by", "pickup_local_datetime",

            "origin_UTC_arrival_datetime", "origin_local_arrival_datetime", "origin_UTC_departure_datetime",
            "origin_local_departure_datetime",
            "origin_datetime_option", "origin_open_time", "origin_close_time", "origin_state", "origin_postal_code",
            "origin_country", "origin_number",
            "origin_name", "origin_address1", "origin_city", "origin_time_zone", "origin_address_description",
            "origin_longitude", "origin_latitude",
            "origin_contact_name", "origin_contact_email", "origin_contact_phone", "origin_appointment_required",

            "dest_address_description", "dest_appointment_required", "next_tab", "dest_local_arrival_datetime",
            "dest_local_departure_datetime", "expiration_datetime", "",
            "dest_state", "dest_postal_code", "dest_country", "dest_number", "dest_name", "dest_address2",
            "dest_address1", "dest_latitude", "dest_longitude", "dest_city",
            "dest_contact_name", "dest_contact_email", "dest_contact_phone", "dest_datetime_option", "dest_open_time",
            "dest_close_time",
            "dest_appointment_contact_name", "dest_appointment_contact_email", "dest_Appointment_contact_phone"
        ])

        return json_data

    def payload_shipment_details(self, shipment_creation_data):
        self.edition = 2
        self.next_tab = "destination"
        self.draft_page = "commodity"

        step_3 = shipment_creation_data['tests']['step_3']

        self.transport_mode = step_3['shipment_details']['transport_mode']
        self.equipment_Name = step_3['shipment_details']['equipment_name']
        # self.equipment_code = step_3['shipment_details']['equipment_code']
        self.pickup_number = step_3['shipment_details']['pick_up_number']
        self.po_number = step_3['shipment_details']['po_number']
        self.bol_number = step_3['shipment_details']['bill_of_landing_number']
        self.comment = step_3['shipment_details']['shipment_instructions']

        json_data = self.to_json(fields=[
            "postedloadid", "edition", "date_created", "date_modified", "isdeleted", "load_number",
            "is_draft", "draft_page", "customer_number", "tendered_to_carrier_number", "load_board_status",
            "load_board_status_type",
            "transport_mode", "is_expedited", "equipment_code", "distance", "is_hazmat", "book_now_price",
            "target_Rate", "created_by", "pickup_local_datetime",

            "origin_UTC_arrival_datetime", "origin_local_arrival_datetime", "origin_UTC_departure_datetime",
            "origin_local_departure_datetime",
            "origin_datetime_option", "origin_open_time", "origin_close_time", "origin_state", "origin_postal_code",
            "origin_country", "origin_number",
            "origin_name", "origin_address1", "origin_city", "origin_time_zone", "origin_address_description",
            "origin_longitude", "origin_latitude",
            "origin_contact_name", "origin_contact_email", "origin_contact_phone", "origin_appointment_required",

            "delivery_local_datetime", "dest_UTC_arrival_datetime", "dest_local_arrival_datetime",
            "dest_UTC_departure_datetime", "dest_local_departure_datetime",
            "dest_datetime_option", "dest_open_time", "dest_close_time", "dest_state", "dest_postal_code",
            "dest_country", "dest_time_zone", "dest_number",
            "dest_name", "dest_address1", "dest_city", "dest_address_description", "dest_longitude", "dest_latitude",
            "dest_contact_name", "dest_contact_email", "dest_contact_phone", "destAppointmentRequired",

            "next_tab", "po_number", "bol_number", "equipment_code", "transport_mode", "comment", "pickup_number",
            "max_temperature", "min_temperature"
        ])

        return json_data

    def payload_freight_items(self, shipment_creation_data):
        self.edition = 3
        self.next_tab = "freightitem"
        self.draft_page = "additional"

        step_4 = shipment_creation_data['tests']['step_4']

        freight_lines = step_4['freight_line']

        freight_new_list = []

        self.load_value = 0  # Sum All Items
        self.weight = 0  # Sum All Items
        self.weight_in_libs = 0  # Sum All Items
        self.weight_UOM = "0"  # Sum All Items

        self.volume = 0  # Sum All Items
        self.volume_in_cuft = 0  # Sum All Items

        for freight_item in freight_lines:
            self.load_value = self.load_value + float(freight_item['item']['commodity_value'])
            self.weight = self.weight + float(freight_item['item']['gross_weight'])
            self.weight_in_libs = self.weight
            self.weight_UOM = freight_item['item']['gross_weight_UOM']
            self.volume = 0
            self.volume_in_cuft = 0

            # Item ----------------------------------------------------------------------------------
            freight_new_list.append(
                FreightItems(
                    commodity_value=freight_item['item']['commodity_value'],
                    gross_weight=freight_item['item']['gross_weight'],
                    gross_weight_in_lbs=freight_item['item']['gross_weight'],
                    gross_weight_UOM=freight_item['item']['gross_weight_UOM'],
                    weight_display_value=freight_item['item']['weight_display_value'],
                    handling_unit_count=freight_item['item']['handling_unit_count'],
                    handling_unit_type=freight_item['item']['handling_unit_type'],
                    handling_unit_type_display_value=freight_item['item']['handling_unit_display_value'],
                    is_deleted=freight_item['item']['is_delete'],
                    height=freight_item['dimension']['height'],
                    height_in_inches=freight_item['dimension']['height'],
                    length=freight_item['dimension']['length'],
                    length_in_inches=freight_item['dimension']['length'],
                    width=freight_item['dimension']['width'],
                    width_in_inches=freight_item['dimension']['width'],
                    dim_UOM=freight_item['dimension']['dim_UOM'],
                    dim_display_value=freight_item['dimension']['dim_display_value'],
                    description=freight_item['dimension']['description']
                )
            )

        # Fill Items List
        self.freight_items = freight_new_list

        json_data = self.to_json(
            fields=[
                "postedloadid", "edition", "date_created", "date_modified", "isdeleted", "load_number",

                "po_number", "bol_number", "pickup_number", "comment", "load_value", "is_draft", "draft_page",
                "customer_number", "tendered_to_carrier_number", "load_board_status",
                "load_board_status_type",
                "transport_mode", "is_expedited", "equipment_code", "equipmentName", "distance", "is_hazmat",
                "book_now_price",
                "weight", "weight_in_libs", "weight_UOM", "volume", "volume_in_cuft",
                "distance", "is_hazmat", "book_now_price", "target_Rate", "created_by",

                "pickup_local_datetime",
                "origin_UTC_arrival_datetime", "origin_local_arrival_datetime", "origin_UTC_departure_datetime",
                "origin_local_departure_datetime",
                "origin_datetime_option",
                "origin_open_time", "origin_close_time", "origin_state", "origin_postal_code",

                "origin_country", "origin_number", "origin_name", "origin_address1", "origin_address2",
                "origin_city", "origin_time_zone", "origin_address_description",
                "origin_longitude", "origin_latitude",
                "origin_contact_name", "origin_contact_email", "origin_contact_phone", "origin_appointment_required",

                "delivery_local_datetime",
                "dest_UTC_arrival_datetime", "dest_local_arrival_datetime",
                "dest_UTC_departure_datetime", "dest_local_departure_datetime",
                "dest_datetime_option",
                "dest_open_time", "dest_close_time", "dest_state", "dest_postal_code",
                "dest_country", "dest_time_zone", "dest_number",
                "dest_name", "dest_address1", "dest_address2",
                "dest_city", "dest_address_description",
                "dest_longitude", "dest_latitude",
                "dest_contact_name", "dest_contact_email", "dest_contact_phone", "destAppointmentRequired",
                "next_tab",
                "freight_items",
            ]
        )
        return json_data

    def payload_bid_parameters(self, shipment_creation_data):
        self.edition = 4
        self.next_tab = "freightitem"
        self.draft_page = "additional"
        self.is_draft = False

        step_5 = shipment_creation_data['tests']['step_5']

        self.book_now_price = step_5['bid_parameters']['book_it_now_rate']

        # OPEN DATES CALCULATION
        hours = step_5['bid_parameters']['hours']
        minutes = step_5['bid_parameters']['minutes']
        indicator = step_5['bid_parameters']['indicator']

        date = step_5['bid_parameters']['bid_expiration_date']
        time_ = f"{hours}:{minutes} {indicator}"
        expiration_date = f"{date} {time_}"

        self.expiration_datetime = convert_to_utc(expiration_date, "Central Standard Time")

        json_data = self.to_json(
            fields=[
                "postedloadid", "edition", "date_created", "date_modified", "isdeleted", "load_number",

                "po_number", "bol_number", "pickup_number", "comment", "load_value", "is_draft", "draft_page",
                "customer_number", "tendered_to_carrier_number", "load_board_status",
                "load_board_status_type",
                "transport_mode", "is_expedited", "equipment_code", "equipmentName",
                "weight", "weight_in_libs", "weight_UOM", "volume", "volume_in_cuft", "distance", "is_hazmat", "book_now_price",
                "distance", "is_hazmat", "book_now_price", "target_Rate", "", "created_by",

                "pickup_local_datetime",
                "origin_UTC_arrival_datetime", "origin_local_arrival_datetime", "origin_UTC_departure_datetime",
                "origin_local_departure_datetime",
                "origin_datetime_option",
                "origin_open_time", "origin_close_time", "origin_state", "origin_postal_code",

                "origin_country", "origin_number", "origin_name", "origin_address1", "origin_address2",
                "origin_city", "origin_time_zone", "origin_address_description",
                "origin_longitude", "origin_latitude",
                "origin_contact_name", "origin_contact_email", "origin_contact_phone", "origin_appointment_required",

                "delivery_local_datetime",
                "dest_UTC_arrival_datetime", "dest_local_arrival_datetime",
                "dest_UTC_departure_datetime", "dest_local_departure_datetime",
                "dest_datetime_option",
                "dest_open_time", "dest_close_time", "dest_state", "dest_postal_code",
                "dest_country", "dest_time_zone", "dest_number",
                "dest_name", "dest_address1", "dest_address2",
                "dest_city", "dest_address_description",
                "dest_longitude", "dest_latitude",
                "dest_contact_name", "dest_contact_email", "dest_contact_phone", "destAppointmentRequired",
                "next_tab",
                "freight_items",
                "expiration_datetime"
            ]
        )
        return json_data

    def get_equipment_response(self, response, search_value):
        data = json.loads(response.text)['data']

        # Filter value
        filtered_items = [item for item in data if item["displayValue"] == search_value]
        self.equipment_code = filtered_items[0]['code']
        self.equipment_Name = filtered_items[0]['displayValue']

    def get_origin_response(self, response):
        data = json.loads(response.text)['data']

        self.postedloadid = data['postedloadid']
        self.edition = data['edition']
        self.date_created = data['dateCreated']
        self.date_modified = data['dateModified']
        self.isdeleted = data['isdeleted']
        self.load_number = data['loadNumber']

        self.is_draft = data['isDraft']
        self.customer_number = data['customerNumber']
        self.tendered_to_carrier_number = data['tenderedToCarrierNumber']
        self.load_board_status = data['loadBoardStatus']
        self.load_board_status_type = data['loadBoardStatusType']
        self.is_expedited = data['isExpedited']
        self.is_hazmat = data['isHazmat']
        self.book_now_price = data['bookNowPrice']
        self.target_rate = data['targetRate']
        self.created_by = data['createdBy']

        if data.get('pickupLocalDatetime') is not None:
            self.pickup_local_datetime = data['pickupLocalDatetime']

        if data.get('originLocalArrivalDatetime') is not None:
            self.origin_local_arrival_datetime = data['originLocalArrivalDatetime']

        if data.get('originLocalDepartureDatetime') is not None:
            self.origin_local_departure_datetime = data['originLocalDepartureDatetime']

        self.origin_datetime_option = data['originDatetimeOption']

        if data.get('originOpenTime') is not None:
            self.origin_open_time = data['originOpenTime']

        if data.get('originCloseTime') is not None:
            self.origin_close_time = data['originCloseTime']

        self.origin_appointment_required = data['originAppointmentRequired']
        self.dest_address_description = data['destAddressDescription']
        self.dest_appointment_required = data['destAppointmentRequired']

    def get_destination_response(self, response):
        data = json.loads(response.text)['data']

        if data.get('originUTCArrivalDatetime') is not None:
            self.origin_UTC_Arrival_Datetime = data['originUTCArrivalDatetime']

        if data.get('originUTCArrivalDatetime') is not None:
            self.origin_UTC_Departure_Datetime = data['originUTCDepartureDatetime']

        self.created_by = data['createdBy']

        if data.get('deliveryLocalDatetime') is not None:
            self.delivery_Local_datetime = data['deliveryLocalDatetime']

        if data.get('destUTCArrivalDatetime') is not None:
            self.dest_UTC_Arrival_Datetime = data['destUTCArrivalDatetime']

        if data.get('destLocalArrivalDatetime') is not None:
            self.dest_local_arrival_datetime = data['destLocalArrivalDatetime']

        if data.get('destUTCDepartureDatetime') is not None:
            self.dest_UTC_Departure_Datetime = data['destUTCDepartureDatetime']

        if data.get('destLocalDepartureDatetime') is not None:
            self.dest_local_departure_datetime = data['destLocalDepartureDatetime']

        self.dest_datetime_option = data['destDatetimeOption']

        if data.get('destOpenTime') is not None:
            self.dest_open_time = data['destOpenTime']

        if data.get('destCloseTime') is not None:
            self.dest_close_time = data['destCloseTime']

        self.dest_address_description = data['destAddressDescription']
        self.dest_appointment_required = data['destAppointmentRequired']

    def get_shipment_details_response(self, response):
        data = json.loads(response.text)['data']

        self.postedloadid = data['postedloadid']
        self.edition = data['edition']
        self.date_created = data['dateCreated']
        self.date_modified = data['dateModified']
        self.isdeleted = data['isdeleted']
        self.load_number = data['loadNumber']
        self.po_number = data['poNumber']
        self.bol_number = data['bolNumber']
        self.pickup_number = data['pickupNumber']
        self.comment = data['comment']
        self.is_draft = data['isDraft']
        self.draft_page = data['draftPage']
        self.customer_number = data['customerNumber']
        self.tendered_to_carrier_number = data['tenderedToCarrierNumber']
        self.load_board_status = data['loadBoardStatus']
        self.load_board_status_type = data['loadBoardStatusType']
        self.transport_mode = data['transportMode']
        self.is_expedited = data['isExpedited']
        self.equipment_code = data['equipmentCode']
        self.equipment_Name = data['equipmentName']
        self.is_hazmat = data['isHazmat']
        self.book_now_price = data['bookNowPrice']
        self.target_rate = data['targetRate']
        self.created_by = data['createdBy']

        if data.get('originUTCArrivalDatetime') is not None:
            self.origin_UTC_Arrival_Datetime = data['originUTCArrivalDatetime']

        if data.get('originLocalArrivalDatetime') is not None:
            self.origin_local_arrival_datetime = data['originLocalArrivalDatetime']

        if data.get('originUTCDepartureDatetime') is not None:
            self.origin_UTC_Departure_Datetime = data['originUTCDepartureDatetime']

        if data.get('originLocalDepartureDatetime') is not None:
            self.origin_local_departure_datetime = data['originLocalDepartureDatetime']

        self.origin_datetime_option = data['originDatetimeOption']

        if data.get('originOpenTime') is not None:
            self.origin_open_time = data['originOpenTime']
        if data.get('originCloseTime') is not None:
            self.origin_close_time = data['originCloseTime']

        self.origin_state = data['originState']
        self.origin_postal_code = data['originPostalCode']
        self.origin_country = data['originCountry']
        self.origin_number = data['originNumber']
        self.origin_name = data['originName']
        self.origin_address_1 = data['originAddress1']
        self.origin_address_2 = data['originAddress2']
        self.origin_city = data['originCity']
        self.origin_time_zone = data['originTimeZone']
        self.origin_address_description = data['originAddressDescription']
        self.origin_longitude = data['originLongitude']
        self.origin_latitude = data['originLatitude']
        self.origin_contact_name = data['originContactName']
        self.origin_contact_email = data['originContactEmail']
        self.origin_contact_phone = data['originContactPhone']
        self.origin_appointment_required = data['originAppointmentRequired']
        self.dest_appointment_required = data['destAppointmentRequired']

    def get_freight_items_response(self, response):
        data = json.loads(response.text)['data']

        self.postedloadid = data['postedloadid']
        self.edition = data['edition']
        self.load_number = data['loadNumber']
        self.tendered_to_carrier_number = data['tenderedToCarrierNumber']

        self.date_created = data['dateCreated']
        self.date_modified = data['dateModified']
        self.created_by = data['createdBy']

        self.customer_number = data['customerNumber']
        self.isdeleted = data['isdeleted']
        self.is_draft = data['isDraft']
        self.is_expedited = data['isExpedited']
        self.load_board_status = data['loadBoardStatus']
        self.load_board_status_type = data['loadBoardStatusType']
        self.draft_page = data['draftPage']

        self.target_rate = data['targetRate']
        self.distance = data['distance']




