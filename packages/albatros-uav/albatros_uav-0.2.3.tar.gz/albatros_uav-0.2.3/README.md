# Albatros - Python libary handling mavlink commands

Provides features that allow developers to create mission management applications for an unmanned aerial vehicle communicating via MAVLink. It provides access to telemetry data and provides functions that allow you to perform actions with the connected vehicle.

---

## UAV Class

Provides commands and actions you can perform on your vehicle.

### `wait_gps_fix()`
- Description: Waits until the GPS fix is acquired by the UAV.

### `is_armed()`
- Description: Checks whether the motors of the UAV are armed.
- Returns: A boolean value indicating whether the UAV is armed.

### `wait_heartbeat()`
- Description: Waits for the heartbeat message from the UAV.
- Usage: Call this method before sending any commands to the UAV to ensure the connection is established.

### `arm()`
- Description: Arms the motors of the UAV.
- Returns: A boolean value indicating whether the UAV is successfully armed.

### `disarm()`
- Description: Disarms the motors of the UAV.

### `set_mode(mode: Union[PlaneFlightModes, CopterFlightModes])`
- Description: Sets the flight mode of the UAV.
- Arguments:
  - `mode`: The flight mode to set, which should be one of the `PlaneFlightModes` or `CopterFlightModes` enum values.

### `set_servo(instance_number: int, pwm: int)`
- Description: Sets the PWM value of a servo on the UAV.
- Arguments:
  - `instance_number`: The servo number to set.
  - `pwm`: The PWM value to set.

### `flight_to_gps_position(lat_int: int, lon_int: int, alt_m: float)`
- Description: Repositions the UAV to a specific GPS position in guided mode.
- Arguments:
  - `lat_int`: The integer latitude value of the target position.
  - `lon_int`: The integer longitude value of the target position.
  - `alt_m`: The altitude in meters of the target position.

### `send_mission_count(mission_elements_count: int)`
- Description: Sends the number of items in a mission to initiate mission upload.
- Arguments:
  - `mission_elements_count`: The number of mission items in the mission sequence.

### `send_mission_waypoint_item(seq: int, lat_int: int, lon_int: int, alt_m: float, accept_radius_m: float, hold_time_s: float = 0, pass_radius_m: float = 0, yaw_deg: Optional[float] = None)`
- Description: Sends a mission waypoint to navigate to.
- Arguments:
  - `seq`: The waypoint ID (sequence number) of the mission item.
  - `lat_int`: The integer latitude value of the waypoint.
  - `lon_int`: The integer longitude value of the waypoint.
  - `alt_m`: The altitude in meters of the waypoint.
  - `accept_radius_m`: The acceptance radius. When the UAV is within this radius of the waypoint, it is considered reached.
  - `hold_time_s` (optional): The hold time at the waypoint in seconds (ignored by fixed-wing vehicles).
  - `pass_radius_m` (optional): The pass radius. If non-zero, it specifies the radius for passing by the waypoint for trajectory control.
  - `yaw_deg` (optional): The desired yaw angle at the waypoint for rotary-wing vehicles. Set to `None` to use the current system yaw heading mode.

### `send_mission_rtl_item(seq: int)`
- Description: Sends a mission "return to launch" (RTL) item.
- Arguments:
  - `seq`: The waypoint ID (sequence number) of the mission item.

---

## Supported MAVLink telemetry messages

### MavMessage

Base class for MAVLink messages.

- `mavpackettype` (str, default: "UNKNOWN"): Type of MAVLink packet.
- `timestamp_ms` (int, default: -1): Timestamp in milliseconds.

### Heartbeat

The heartbeat message shows that a system or component is present and responding. The type and autopilot fields (along with the message component id) allow the receiving system to treat further messages from this system appropriately.

- `type` (int, default: 0): Vehicle or component type.
- `autopilot` (int, default: 0): Autopilot type/class.
- `base_mode` (int, default: 0): System mode bitmap.
- `custom_mode` (int, default: 0): Autopilot-specific flags.
- `system_status` (int, default: 0): System status flag.
- `mavlink_version` (int, default: 0): MAVLink version.

### GlobalPositionInt

The filtered global position. The position is in GPS-frame (right-handed, Z-up).

- `time_boot_ms` (int, default: 0): Timestamp (time since system boot).
- `lat` (int, default: 0): Latitude.
- `lon` (int, default: 0): Longitude.
- `alt` (int, default: 0): Altitude (MSL).
- `relative_alt` (int, default: 0): Altitude above ground.
- `vx` (int, default: 0): Ground X speed.
- `vy` (int, default: 0): Ground Y speed.
- `vz` (int, default: 0): Ground Z speed.
- `hdg` (int, default: 0): Compass heading.

### SysStatus

The general system state.

- `onboard_control_sensors_present` (int, default: 0): Bitmap showing which onboard controllers and sensors are present.
- `onboard_control_sensors_enabled` (int, default: 0): Bitmap showing which onboard controllers and sensors are enabled.
- `onboard_control_sensors_health` (int, default: 0): Bitmap showing which onboard controllers and sensors have an error.
- `load` (int, default: 0): Maximum usage in percent of the mainloop time.
- `voltage_battery` (int, default: 0): Battery voltage.
- `current_battery` (int, default: 0): Battery current.
- `battery_remaining` (int, default: 0): Battery energy remaining.
- `drop_rate_comm` (int, default: 0): Communication drop rate.

### GPSRawInt

The raw GPS position data.

- `time_usec` (int, default: 0): Timestamp.
- `fix_type` (int, default: 0): GPS fix type.
- `lat` (int, default: 0): Latitude (WGS84).
- `lon` (int, default: 0): Longitude (WGS84).
- `alt` (int, default: 0): Altitude (MSL).
- `eph` (int, default: 0): GPS HDOP horizontal dilution of position.
- `epv` (int, default: 0): GPS VDOP vertical dilution of position.
- `vel` (int, default: 0): GPS ground speed.
- `cog` (int, default: 0): GPS course over ground.
- `satellites_visible` (int, default: 0): Number of visible satellites.

### GPSStatus

The GPS status message.

- `satellite_prn` (List[int], default: None): Global satellite ID.
- `satellite_used` (List[int], default: None): 0: Satellite not used, 1: Used for localization.
- `satellite_elevation` (List[int], default: None): Elevation (0: right on top of receiver, 90: on the horizon) of satellite.
- `satellite_azimuth` (List[int], default: None): Direction of satellite, 0: 0 deg, 255: 360 deg.
- `satellite_snr` (List[int], default: None): Signal to noise ratio of satellite.

### Attitude

The attitude in the aeronautical frame (right-handed, Z-down, X-front, Y-right).

- `time_boot_ms` (int, default: 0): Timestamp (time since system boot).
- `roll` (float, default: 0.0): Roll angle (rad).
- `pitch` (float, default: 0.0): Pitch angle (rad).
- `yaw` (float, default: 0.0): Yaw angle (rad).
- `rollspeed` (float, default: 0.0): Roll angular speed (rad/s).
- `pitchspeed` (float, default: 0.0): Pitch angular speed (rad/s).
- `yawspeed` (float, default: 0.0): Yaw angular speed (rad/s).

### RcChannelsRaw

The RAW values of the RC channels sent to the MAV to override info received from the RC radio. A value of UINT16_MAX means no change to that channel. A value of 0 means control of that channel should be released back to the RC radio.

- `time_boot_ms` (int, default: 0): Timestamp (time since system boot).
- `port` (int, default: 0): System ID.
- `chan1_raw` (int, default: 0): RC channel 1 value.
- `chan2_raw` (int, default: 0): RC channel 2 value.
- `chan3_raw` (int, default: 0): RC channel 3 value.
- `chan4_raw` (int, default: 0): RC channel 4 value.
- `chan5_raw` (int, default: 0): RC channel 5 value.
- `chan6_raw` (int, default: 0): RC channel 6 value.
- `chan7_raw` (int, default: 0): RC channel 7 value.
- `chan8_raw` (int, default: 0): RC channel 8 value.
- `rssi` (int, default: 0): Receive signal strength indicator.

### BatteryStatus

Battery information.

- `current_consumed` (int, default: 0): Consumed charge.
- `energy_consumed` (int, default: 0): Consumed energy.
- `temperature` (int, default: 0): Temperature of the battery.
- `voltages` (List[int], default: None): Battery voltage of cells.
- `current_battery` (int, default: 0): Battery current.

### SystemTime

The system time.

- `time_unix_usec` (int, default: 0): Timestamp in microseconds since UNIX epoch.
- `time_boot_ms` (int, default: 0): Timestamp (time since system boot).

### ParameterValue

This interface represents a parameter value.

- `param_id` (str, default: ""): Onboard parameter id.
- `param_value` (float, default: 0.0): Onboard parameter value.
- `param_type` (int, default: 0): Onboard parameter type.
- `param_count` (int, default: 0): Total number of onboard parameters.
- `param_index` (int, default: 0): Index of this onboard parameter.

### CommandLong

Send a command with up to seven parameters to the MAV. 

- `target_system` (int, default: 0): System which should execute the command.
- `target_component` (int, default: 0): Component which should execute the command.
- `command` (int, default: 0): Command ID.
- `confirmation` (int, default: 0): 0: First transmission of this command. 1-255: Confirmation transmissions (e.g., for retries).
- `param1` (float, default: 0.0): Parameter 1.
- `param2` (float, default: 0.0): Parameter 2.
- `param3` (float, default: 0.0): Parameter 3.
- `param4` (float, default: 0.0): Parameter 4.
- `param5` (float, default: 0.0): Parameter 5.
- `param6` (float, default: 0.0): Parameter 6.
- `param7` (float, default: 0.0): Parameter 7.

---

## Examples

### Creating connection
```python
from albatros.uav import UAV
from albatros.telemetry import ConnectionType

# SITL connection is default
vehicle = UAV() 

# Direct connection to the flight controller
vehicle = UAV(device="/dev/tty/USB0/", baud_rate=57600)

# Connecting via RabbitMQ
vehicle = UAV(host="localhost", connection_type=ConnectionType.RABBITMQ)

# You can also specify the ID of the vehicle you want to connect to and the ID of your system
# read more about MAVLink Routing in ArduPilot: https://ardupilot.org/dev/docs/mavlink-routing-in-ardupilot.html
vehicle = UAV(vehicle_system_id=1, vehicle_component_id=1, my_sys_id=1, my_cmp_id=191)

```

### Arming vehicle (in SITL simulation)

Simply arm and disarm vehicle

Flow:
- arm vehicle
- wait for the vehicle to be armed
- disarm vehicle

```bash
$ python -m examples.arming_vehicle
```

```python
from albatros.uav import UAV

vehicle = UAV()

while not vehicle.arm():
    print("waiting ARM")

vehicle.disarm()
```

### Takeoff (Plane)

Flow:
- arm plane
- wait for the vehicle to be armed
- set mode TAKEOFF
- print plane altitude

```bash
$ python -m examples.takeoff
```

```python
from time import sleep

from albatros.enums import PlaneFlightModes
from albatros.uav import UAV

plane = UAV()

while not plane.arm():
    print("waiting ARM")

plane.set_mode(PlaneFlightModes.TAKEOFF)

while True:
    print(f"Altitude: {plane.telem.data.global_position_int.relative_alt / 1000.0} m")
    sleep(1)

```

### Fly to point (Plane)

Example of flying plane to the designated point in GUIDED mode.

Flow:
- wait GPS fix
- arm plane
- wait for the plane to be armed
- set mode TAKEOFF
- wait until the aircraft reaches 30 m AGL
- set mode GUIDED
- specify the point to which the plane will fly
- print distance to point

```bash
$ python -m examples.takeoff
```

```python
from time import sleep

from albatros.enums import PlaneFlightModes
from albatros.nav.position import PositionGPS, distance_between_points
from albatros.uav import UAV

plane = UAV()

plane.wait_gps_fix()

while not plane.arm():
    print("waiting ARM")


plane.set_mode(PlaneFlightModes.TAKEOFF)

while plane.telem.data.global_position_int.relative_alt < 30_000:
    print(f"Altitude: {plane.telem.data.global_position_int.relative_alt / 1000.0} m")
    sleep(1)


# because mavlink sends coordinates in scaled form as integers
# we use function which scales WGS84 coordinates by 7 decimal places (degE7)
target = PositionGPS()
target.scale_global_position(lat=-35.35674492, lon=149.16324842, alt=50)

plane.set_mode(PlaneFlightModes.GUIDED)
plane.flight_to_gps_position(target.lat, target.lon, target.alt)

while True:
    current_position = PositionGPS(
        lat=plane.telem.data.global_position_int.lat,
        lon=plane.telem.data.global_position_int.lon,
        alt=50,
    )

    dist = distance_between_points(current_position, target)

    print(f"Distance to target: {dist} m")
    sleep(1)
```