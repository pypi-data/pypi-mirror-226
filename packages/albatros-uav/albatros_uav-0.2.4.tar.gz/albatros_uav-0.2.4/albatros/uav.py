import logging
from time import sleep, time
from typing import Union

from pymavlink.dialects.v20.ardupilotmega import (
    MAV_CMD_COMPONENT_ARM_DISARM,
    MAV_CMD_DO_REPOSITION,
    MAV_CMD_DO_SET_MODE,
    MAV_CMD_DO_SET_SERVO,
    MAV_CMD_NAV_RETURN_TO_LAUNCH,
    MAV_CMD_NAV_TAKEOFF,
    MAV_CMD_NAV_WAYPOINT,
    MAV_MODE_FLAG_SAFETY_ARMED,
    MAVLink,
)

from .commands import (
    get_command_int_message,
    get_command_long_message,
    get_mission_count_message,
    get_mission_item_int,
)
from .enums import CopterFlightModes, PlaneFlightModes
from .message_models import MissionACK
from .telemetry import ConnectionType, Telemetry

logger = logging.getLogger(__name__)


class UAV:
    def __init__(
        self,
        vehicle_system_id: int = 1,
        vehicle_component_id: int = 1,
        my_sys_id: int = 1,
        my_cmp_id: int = 191,
        connection_type: ConnectionType = ConnectionType.DIRECT,
        device: str = "udpin:0.0.0.0:14550",
        baud_rate: int = 115200,
        host: str = "localhost",
    ) -> None:
        self.target_system = vehicle_system_id
        self.target_component = vehicle_component_id
        self.mav = MAVLink(0, my_sys_id, my_cmp_id)
        self.telem = Telemetry(connection_type, device, baud_rate, host)

        # mission state
        self.__mission_count = -1
        self.__item_seq = 0

    def wait_gps_fix(self) -> None:
        while (
            self.telem.data.gps_raw_int.fix_type < 3
            or self.telem.data.gps_raw_int.lat == 0
        ):
            sleep(0.1)

    def is_armed(self) -> bool:
        armed_flag = self.telem.data.heartbeat.base_mode & MAV_MODE_FLAG_SAFETY_ARMED
        return bool(armed_flag)

    def wait_heartbeat(self) -> None:
        while time() * 1000 - self.telem.data.heartbeat.timestamp_ms > 100:
            sleep(0.1)
        sleep(0.1)

    def arm(self) -> bool:
        """
        Arms motors.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_COMPONENT_ARM_DISARM,
            param1=1,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("Arm command sent.")
        self.wait_heartbeat()
        logger.info("heartbeat received")

        return self.is_armed()

    def disarm(self) -> None:
        """
        Disarms motors.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_COMPONENT_ARM_DISARM,
            param1=0,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("Disarm command sent.")

    def set_mode(self, mode: Union[PlaneFlightModes, CopterFlightModes]) -> None:
        """
        Set system mode.

        Args:
        - mode: ardupilot flight mode you want to set.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_DO_SET_MODE,
            param1=1,
            param2=mode.value,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("Set mode command sent")

    def set_servo(self, instance_number: int, pwm: int) -> None:
        """
        Set a servo to a desired PWM value.

        Args:
        - instance_number: servo number.
        - pwm: PWM to set.
        """
        msg = get_command_long_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_DO_SET_SERVO,
            param1=instance_number,
            param2=pwm,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("Set servo command sent.")

    def flight_to_gps_position(self, lat_int: int, lon_int: int, alt_m: float) -> None:
        """
        Works only in Guided mode. Reposition the vehicle to a specific WGS84 global position.
        """
        msg = get_command_int_message(
            target_system=self.target_system,
            target_component=self.target_component,
            command=MAV_CMD_DO_REPOSITION,
            x=lat_int,
            y=lon_int,
            z=alt_m,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("Flight to point command sent.")

    def wait_mission_request_int(self) -> int:
        clock_start = time()
        while True:
            time_dif = time() * 1000 - self.telem.data.mission_request_int.timestamp_ms
            if time_dif < 100:
                self.telem.data.mission_request_int.timestamp_ms = 0
                return self.telem.data.mission_request_int.seq
            sleep(0.1)
            if time() - clock_start > 0.250:
                raise TimeoutError

    def get_mission_ack(self) -> MissionACK:
        clock_start = time()
        while True:
            time_dif = time() * 1000 - self.telem.data.mission_ack.timestamp_ms
            if time_dif < 100:
                self.telem.data.mission_ack.timestamp_ms = 0
                return self.telem.data.mission_ack
            sleep(0.1)
            if time() - clock_start > 0.250:
                raise TimeoutError

        return self.telem.data.mission_ack

    def send_mission_count(self, mission_elements_count: int) -> None:
        """
        Send the number of items in a mission. This is used to initiate mission upload.

        Args:
        - mission_elements_count (int): Number of mission items in the sequence.
        """
        msg = get_mission_count_message(
            target_system=self.target_system,
            target_component=self.target_component,
            count=mission_elements_count,
        )

        self.__mission_count = mission_elements_count
        self.telem.send(msg.pack(self.mav))
        logger.info("mission_count message sent.")

    def send_mission_takeoff_item(
        self,
        pitch: float,
        altitude: float,
        yaw: float = 0,
    ) -> None:
        seq = self.wait_mission_request_int()

        msg = get_mission_item_int(
            target_system=self.target_system,
            target_component=self.target_component,
            seq=seq,
            command=MAV_CMD_NAV_TAKEOFF,
            param1=pitch,
            param4=yaw,
            z=altitude,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("mission_rtl message sent.")

    def send_mission_waypoint_item(
        self,
        lat_int: int,
        lon_int: int,
        alt_m: float,
        accept_radius_m: float,
        hold_time_s: float = 0,
        pass_radius_m: float = 0,
        yaw_deg: float = 0,
    ) -> None:
        """
        Sends a mission waypoint to navigate to.

        Args:
        - seq (int): Waypoint ID (sequence number). Starts at zero. Increases monotonically for each mission item.
        - lat (int): Latitude of the waypoint.
        - lon (int): Longitude of the waypoint.
        - alt_m (float): Altitude of the waypoint in meters.
        - accept_radius_m (float): Acceptance radius. If the sphere with this radius is hit, the waypoint counts as reached.
        - hold_time_s (float, optional): Hold time at the waypoint in seconds. Ignored by fixed-wing vehicles. Defaults to 0.
        - pass_radius_m (float, optional): Pass radius. If > 0, it specifies the radius to pass by the waypoint.
            Allows trajectory control. Positive value for clockwise orbit, negative value for counterclockwise orbit. Defaults to 0.
        - yaw_deg (float, optional): Desired yaw angle at the waypoint for rotary-wing vehicles.
            Set to NaN to use the current system yaw heading mode. Defaults to None.

        Returns: None
        """
        seq = self.wait_mission_request_int()

        msg = get_mission_item_int(
            target_system=self.target_system,
            target_component=self.target_component,
            seq=seq,
            command=MAV_CMD_NAV_WAYPOINT,
            param1=hold_time_s,
            param2=accept_radius_m,
            param3=pass_radius_m,
            param4=yaw_deg,
            x=lat_int,
            y=lon_int,
            z=alt_m,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("mission_waypoint message sent.")

    def send_mission_rtl_item(
        self,
    ) -> None:
        """
        Sends a mission return to launch location.

        Args:
        - seq (int): Waypoint ID (sequence number). Starts at zero. Increases monotonically for each mission item.

        Returns: None
        """
        seq = self.wait_mission_request_int()

        msg = get_mission_item_int(
            target_system=self.target_system,
            target_component=self.target_component,
            seq=seq,
            command=MAV_CMD_NAV_RETURN_TO_LAUNCH,
        )

        self.telem.send(msg.pack(self.mav))
        logger.info("mission_rtl message sent.")
