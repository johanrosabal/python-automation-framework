
from applications.web.csight.fixtures.bookings import *
from applications.web.csight.fixtures.fixtures import *

from applications.web.csight.config.decorators import csight
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from core.utils.helpers import extract_test_id

logger = setup_logger('TestBookingWithFixtures')


BOOKING_CONTAINERS = [
    "../../../data/bookings/CT-2209_create_booking_container_single_reefer.json",                                                                   # Container
    "../../../data/bookings/CT-4137_create_booking_container_multiple_reefer.json",                                                                 # Container
    "../../../data/bookings/CT-2210_create_booking_container_single_dry.json",                                                                      # Container
    "../../../data/bookings/CT-4182_create_booking_container_multiple_dry.json",                                                                    # Container
    "../../../data/bookings/CT-2211_create_booking_container_single_reefer_hazmat.json",                                                            # Container
    "../../../data/bookings/CT-4184_create_booking_container_multiple_reefer_hazmat.json",                                                          # Container
    "../../../data/bookings/CT-4188_create_booking_container_multiple_dry_hazmat.json",                                                             # Container
    "../../../data/bookings/CT-2212_create_booking_container_single_dry_hazmat.json",                                                               # Container
    "../../../data/bookings/CT-2213_create_booking_container_door_to_door.json",                                                                    # Container
    "../../../data/bookings/CT-2214_create_booking_container_door_to_port.json",                                                                    # Container
    "../../../data/bookings/CT-4190_create_booking_container_multiple_stops.json",                                                                  # Container
    "../../../data/bookings/CT-4195_create_booking_container_port_to_port.json",                                                                    # Container
    "../../../data/bookings/CT-4196_create_booking_container_motor_rail.json",                                                                      # Container
    "../../../data/bookings/CT-4197_create_booking_container_motor_rail_combo.json",                                                                # Container
    "../../../data/bookings/CT-4199_create_booking_container_all_motor_with_x_dock.json",                                                           # Container
    "../../../data/bookings/CT-4202_create_booking_container_all_motor.json",                                                                       # Container
    "../../../data/bookings/CT-4206_create_booking_container_drop_pull.json",                                                                       # Container
    "../../../data/bookings/CT-4208_create_booking_container_special_equipment_created.json",                                                       # Container

    "../../../data/bookings/CT-2479_create_booking_vehicle_single_new_creation_NCC.json",                                                           # Vehicle | NCC
    "../../../data/bookings/CT-2485_create_booking_vehicle_multiple_new_creation_NCC.json",                                                         # Vehicle | NCC
    "../../../data/bookings/CT-4217_create_booking_vehicle_with_different_commodity_NCC.json",                                                      # Vehicle | NCC
    "../../../data/bookings/CT-2668_create_booking_vehicle_single_used_creation_NCC.json",                                                          # Vehicle | NCC
    "../../../data/bookings/CT-2670_create_booking_vehicle_multiple_used_creation_NCC.json",                                                        # Vehicle | NCC
    "../../../data/bookings/CT-2682_create_booking_vehicle_single_vintage_new_creation_NCC.json",                                                   # Vehicle | NCC
    "../../../data/bookings/CT-2683_create_booking_vehicle_multiple_vintage_new_creation_NCC.json",                                                 # Vehicle | NCC
    "../../../data/bookings/CT-2790_create_booking_vehicle_vintage_with_different_commodity_different_propulsion_creation_NCC.json",                # Vehicle | NCC
    "../../../data/bookings/CT-4216_create_booking_vehicle_single_used_creation_with_different_commodity_different_propulsion_creation_NCC.json",   # Vehicle | NCC
    "../../../data/bookings/CT-4213_create_booking_vehicle_single_new_creation_with_different_commodity_different_propulsion_creation_NCC.json",    # Vehicle | NCC
    "../../../data/bookings/CT-4218_create_booking_vehicle_with_nested_units_NCC.json",                                                             # Vehicle | NCC

    "../../../data/bookings/CT-2561_create_booking_breakbulk_single_hazardous_wheel_cargo_towable_creation_NCC.json",                               # Breakbulk | NCC
    "../../../data/bookings/CT-4219_create_booking_breakbulk_multiple_hazardous_wheel_cargo_towable_creation_NCC.json",                             # Breakbulk | NCC
    "../../../data/bookings/CT-2560_create_booking_breakbulk_multiple_wheel_cargo_towable_creation_NCC.json",                                       # Breakbulk | NCC
    "../../../data/bookings/CT-3490_create_booking_breakbulk_single_hazardous_wheel_cargo_drivable_creation_NCC.json",                              # Breakbulk | NCC
    "../../../data/bookings/CT-3652_create_booking_breakbulk_multiple_hazardous_wheel_cargo_drivable_creation_NCC.json",                            # Breakbulk | NCC
    "../../../data/bookings/CT-4220_create_booking_breakbulk_single_wheel_cargo_drivable_creation_NCC.json",                                        # Breakbulk | NCC
    "../../../data/bookings/CT-4221_create_booking_breakbulk_multiple_wheel_cargo_drivable_creation_NCC.json",                                      # Breakbulk | NCC
    "../../../data/bookings/CT-4258_create_booking_breakbulk_single_wheel_cargo_towable_creation_NCC.json",                                         # Breakbulk | NCC
    "../../../data/bookings/CT-4272_create_booking_breakbulk_single_hazardous_non_wheel_cargo_creation_NCC.json",                                   # Breakbulk | NCC
    "../../../data/bookings/CT-4273_create_booking_breakbulk_multiple_hazardous_non_wheel_cargo_creation_NCC.json",                                 # Breakbulk | NCC
    "../../../data/bookings/CT-3663_create_booking_breakbulk_single_non_wheel_cargo_drivable_creation_NCC.json",                                    # Breakbulk | NCC
    "../../../data/bookings/CT-4259_create_booking_breakbulk_multiple_non_wheel_cargo_drivable_creation_NCC.json",                                  # Breakbulk | NCC
    "../../../data/bookings/CT-4260_create_booking_breakbulk_single_wheel_cargo_drivable_with_nested_units_creation_NCC.json",                      # Breakbulk | NCC
    "../../../data/bookings/CT-4396_create_booking_breakbulk_single_non_wheel_cargo_drivable_with_nested_units_creation_NCC.json",                  # Breakbulk | NCC
    "../../../data/bookings/CT-4261_create_booking_breakbulk_single_wheel_cargo_towable_with_nested_units_creation_NCC.json",                       # Breakbulk | NCC
    "../../../data/bookings/CT-4262_create_booking_breakbulk_single_transfers_hazardous_non_wheel_cargo_creation_NCC.json",                         # Breakbulk | NCC

    "../../../data/bookings/CT-4263_create_booking_container_multiple_transfers_hazardous_creation_NCC.json",                                       # Container | NCC
    "../../../data/bookings/CT-4264_create_booking_container_single_transfer_NCC.json",                                                             # Container | NCC
    "../../../data/bookings/CT-4265_create_booking_container_multiple_transfer_NCC.json",                                                           # Container | NCC
    "../../../data/bookings/CT-2529_create_booking_vehicle_single_transfers_new_creation_NCC.json",                                                 # Vehicle | NCC
    "../../../data/bookings/CT-4266_create_booking_vehicle_multiple_transfers_new_creation_NCC.json",                                               # Vehicle | NCC
]


@pytest.mark.web
@csight
class TestBookingWithFixtures(BaseTest):
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    @pytest.mark.parametrize("booking_creation", BOOKING_CONTAINERS, indirect=True, ids=[extract_test_id(path) for path in BOOKING_CONTAINERS])
    @test(test_case_id="", test_description="Create a booking creation", feature="Booking Container", skip=False)
    def test_create_booking(self, csight_login, booking_creation, record_property):
        # Process File
        assert isinstance(booking_creation, dict)
        test_id = booking_creation["test_case_id"]
        record_property("test_key", test_id)
