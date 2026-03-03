from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List
from core.config.logger_config import setup_logger
from core.utils.helpers import *
import json


@dataclass
class SearchLocationDTO:
    address_description: Optional[str] = None  # None on New Records
    location_number: Optional[str] = None  # None on New Records
    state: Optional[str] = None  # None on New Records
    postal_code: Optional[str] = None  # None on New Records
    country: Optional[str] = None  # None on New Records
    address_1: Optional[str] = None  # None on New Records
    city: Optional[str] = None  # None on New Records
    time_zone: Optional[str] = None  # None on New Records
    contact_name: Optional[str] = None  # None on New Records
    contact_phone: Optional[str] = None  # None on New Records
    contact_email: Optional[str] = None  # None on New Records
    longitude: Optional[str] = None  # None on New Records
    latitude: Optional[str] = None  # None on New Records

    def set_search_location(self, response):
        # Transform response to Dictionary
        origin_location_dict = json.loads(response.text)
        # Get First Address
        origin_location = origin_location_dict["data"][0]

        # Fill DTO Information
        self.address_description = origin_location['addressDescription']
        self.location_number = origin_location['locationNumber']
        self.state = origin_location['state']
        self.postal_code = origin_location['postalCode']
        self.country = origin_location['country']
        self.address_1 = origin_location['address1']
        self.city = origin_location['city']
        self.time_zone = origin_location['timeZone']
        self.contact_name = origin_location['contactName']
        self.contact_phone = origin_location['contactPhone']
        self.contact_email = origin_location['contactEmail']
        self.longitude = origin_location['longitude']
        self.latitude = origin_location['latitude']

        # Print Location Information on Log
        print_json(title="Search Location Origin Response", data=origin_location)

    def to_dict(self):
        """Converts SavePostedLoadDTO to a dictionary."""
        data_dict = asdict(self)
        data_dict = {to_camel_case(k): v for k, v in data_dict.items()}

        return data_dict

    def extract_fields(self, fields: List[str]) -> Dict[str, Any]:
        """
        Extracts only the specified fields and returns a dictionary.
        Handles nested DTOs properly.
        """
        full_data = self.to_dict()
        return {to_camel_case(key ): full_data[to_camel_case(key)] for key
                in fields if to_camel_case(key) in full_data}

    def to_json(self, fields: Optional[List[str]] = None) -> str:
        """
               Returns a JSON representation of the DTO.
               If `fields` is provided, only those fields are included.
               """
        data = self.extract_fields(fields) if fields else self.to_dict()
        return json.dumps(data, indent=4)

