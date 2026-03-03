from core.utils.random_utils import generate_random_code
from core.config.logger_config import setup_logger
import random
from tabulate import tabulate
logger = setup_logger('CustomerAppliersAddressDto')


class CustomerAppliersAddressDto:
    mapping = {
        "address_code": "address_code",
        "address_line_1": "address_line_1",
        "address_line_2": "address_line_2",
        "address_line_3": "address_line_3",
        "address_line_4": "address_line_4",
        "address_line_5": "address_line_5",
        "address_line_6": "address_line_6",
        "address_line_7": "address_line_7",
        "secondary_language_line_1": "secondary_language_line_1",
        "secondary_language_line_2": "secondary_language_line_2",
        "secondary_language_line_3": "secondary_language_line_3",
        "secondary_language_line_4": "secondary_language_line_4",
        "secondary_language_line_5": "secondary_language_line_5",
        "secondary_language_line_6": "secondary_language_line_6",
        "secondary_language_line_7": "secondary_language_line_7",
        "contact_1": "contact_1",
        "contact_2": "contact_2",
        "contact_type": "contact_type",
        "street_line_1": "street_line_1",
        "street_line_2": "street_line_2",
        "street_line_3": "street_line_3",
        "location": "location",
        "postal_code": "postal_code",
        "city_name": "city_name",
        "country": "country",
        "province": "province",
        "ban": "ban",
        "coordinates_edit": "coordinates_edit",
        "coordinates_latitude": "coordinates_latitude",
        "coordinates_longitude": "coordinates_longitude",
        "is_hide": "is_hide",
        "is_web_booking": "is_web_booking"
    }

    def __init__(self,
                 address_code,
                 address_line_1,
                 address_line_2,
                 address_line_3,
                 address_line_4,
                 address_line_5,
                 address_line_6,
                 address_line_7,
                 secondary_language_line_1,
                 secondary_language_line_2,
                 secondary_language_line_3,
                 secondary_language_line_4,
                 secondary_language_line_5,
                 secondary_language_line_6,
                 secondary_language_line_7,
                 contact_1,
                 contact_2,
                 contact_type,
                 street_line_1,
                 street_line_2,
                 street_line_3,
                 postal_code,
                 location,
                 city_name,
                 country,
                 province,
                 ban,
                 coordinates_edit,
                 coordinates_latitude,
                 coordinates_longitude,
                 is_hide,
                 is_web_booking
                 ):
        self.address_code = generate_random_code(address_code)  # Attach random number to code
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.address_line_4 = address_line_4
        self.address_line_5 = address_line_5
        self.address_line_6 = address_line_6
        self.address_line_7 = address_line_7
        self.secondary_language_line_1 = secondary_language_line_1
        self.secondary_language_line_2 = secondary_language_line_2
        self.secondary_language_line_3 = secondary_language_line_3
        self.secondary_language_line_4 = secondary_language_line_4
        self.secondary_language_line_5 = secondary_language_line_5
        self.secondary_language_line_6 = secondary_language_line_6
        self.secondary_language_line_7 = secondary_language_line_7
        self.contact_1 = contact_1
        self.contact_2 = contact_2
        self.contact_type = contact_type
        self.street_line_1 = street_line_1
        self.street_line_2 = street_line_2
        self.street_line_3 = street_line_3
        self.location = location
        self.postal_code = postal_code
        self.city_name = city_name
        self.country = country
        self.province = province
        self.ban = ban
        self.coordinates_edit = coordinates_edit
        self.coordinates_latitude = coordinates_latitude
        self.coordinates_longitude = coordinates_longitude
        self.is_hide = is_hide
        self.is_web_booking = is_web_booking

    @staticmethod
    def get_list_address():
        addresses = [
            CustomerAppliersAddressDto("9999",
                                       "123 Main St", "123 Calle Principal","Address Line 3", "Address Line 4", "Address Line 5", "Address Line 6", "Address Line 7",
                                       "Sec Lan 1", "Sec Lan 2", "Sec Lan 3", "Sec Lan 4", "Sec Lan 5", "Sec Lan 6", "Sec Lan 7",
                                       "Contact Test 1", "Contact Test 2", "EM",
                                       "555-1231", "Main Street", "Apt 1", "27006",
                                       "$0D5Z", "Jacksonville, NC", "United States","North Carolina",
                                       "BAN0000", False, 34.753956, -77.428955,
                                       False, False),
            CustomerAppliersAddressDto("9999",
                                       "123 Main St", "123 Calle Principal", "Address Line 3", "Address Line 4",
                                       "Address Line 5", "Address Line 6", "Address Line 7",
                                       "Sec Lan 1", "Sec Lan 2", "Sec Lan 3", "Sec Lan 4", "Sec Lan 5", "Sec Lan 6",
                                       "Sec Lan 7",
                                       "Contact Test 1", "Contact Test 2", "EM",
                                       "555-1231", "Main Street", "Apt 1", "60001",
                                       "$04OU", "Springfield, IL", "United States", "Illinois",
                                       "BAN0000", False, 39.799999, -89.650002,
                                       False, False)
          ]

        return addresses

    @staticmethod
    def get_random_address():
        addresses = CustomerAppliersAddressDto.get_list_address()
        index = random.randint(0, len(addresses) - 1)

        # Create Here Tabulate Info
        address = addresses[index]

        # Get headers dynamically from 'mapping' keys
        headers = list(CustomerAppliersAddressDto.mapping.keys())

        # Get address values dynamically from object attributes
        values = [getattr(address, key) for key in headers]

        # Print tabulated info
        logger.info("\n"+tabulate([values], headers=headers, tablefmt="pretty"))

        return address

    def __repr__(self):
        return (f"CustomerAppliersAddressDto("
                f"address_code={self.address_code},"
                f"address_line_1={self.address_line_1},"
                f"address_line_2={self.address_line_2},"
                f"address_line_3={self.address_line_3},"
                f"address_line_4={self.address_line_4},"
                f"address_line_5={self.address_line_5},"
                f"address_line_6={self.address_line_6},"
                f"address_line_7={self.address_line_7},"
                f"secondary_language_line_1={self.secondary_language_line_1},"
                f"secondary_language_line_2={self.secondary_language_line_2},"
                f"secondary_language_line_3={self.secondary_language_line_3},"
                f"secondary_language_line_4={self.secondary_language_line_4},"
                f"secondary_language_line_5={self.secondary_language_line_5},"
                f"secondary_language_line_6={self.secondary_language_line_6},"
                f"secondary_language_line_7={self.secondary_language_line_7},"
                f"contact_1={self.contact_1},"
                f"contact_2={self.contact_2},"
                f"contact_type={self.contact_type},"
                f"street_line_1={self.street_line_1},"
                f"street_line_2={self.street_line_2},"
                f"street_line_3={self.street_line_3},"
                f"location={self.location},"
                f"postal_code={self.postal_code},"
                f"city_name={self.city_name},"
                f"country={self.country},"
                f"province={self.province},"
                f"ban={self.ban},"
                f"coordinates_edit={self.coordinates_edit},"
                f"coordinates_latitude={self.coordinates_latitude},"
                f"coordinates_longitude={self.coordinates_longitude},"
                f"is_hide={self.is_hide},"
                f"is_web_booking={self.is_web_booking},"
                f")")
