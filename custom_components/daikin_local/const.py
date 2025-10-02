"""Constants for the Daikin Local integration."""

DOMAIN = "daikin_local"

# Configuration keys
CONF_IP_ADDRESS = "ip_address"
CONF_UUID = "uuid"
CONF_KEY = "key"

# Default values
DEFAULT_PORT = 443
DEFAULT_TIMEOUT = 10

# API endpoints
ENDPOINT_BASIC_INFO = "/common/basic_info"
ENDPOINT_CONTROL_INFO = "/aircon/get_control_info"
ENDPOINT_SENSOR_INFO = "/aircon/get_sensor_info"
ENDPOINT_SET_CONTROL = "/aircon/set_control_info"
ENDPOINT_REGISTER_TERMINAL = "/common/register_terminal"

# Climate modes
CLIMATE_MODE_OFF = "off"
CLIMATE_MODE_AUTO = "auto"
CLIMATE_MODE_COOL = "cool"
CLIMATE_MODE_HEAT = "heat"
CLIMATE_MODE_DRY = "dry"
CLIMATE_MODE_FAN_ONLY = "fan_only"

# Daikin mode mapping
DAIKIN_MODE_TO_HA = {
    0: CLIMATE_MODE_FAN_ONLY,
    1: CLIMATE_MODE_AUTO,
    2: CLIMATE_MODE_DRY,
    3: CLIMATE_MODE_COOL,
    4: CLIMATE_MODE_HEAT,
}

HA_MODE_TO_DAIKIN = {v: k for k, v in DAIKIN_MODE_TO_HA.items()}

# Fan speeds
FAN_SPEED_AUTO = "auto"
FAN_SPEED_QUIET = "quiet"
FAN_SPEED_LOW = "low"
FAN_SPEED_MEDIUM = "medium"
FAN_SPEED_HIGH = "high"
FAN_SPEED_MAX = "max"

# Daikin fan speed mapping
DAIKIN_FAN_TO_HA = {
    "A": FAN_SPEED_AUTO,
    "B": FAN_SPEED_QUIET,
    "3": FAN_SPEED_LOW,
    "4": FAN_SPEED_MEDIUM,
    "5": FAN_SPEED_HIGH,
    "6": FAN_SPEED_MAX,
}

HA_FAN_TO_DAIKIN = {v: k for k, v in DAIKIN_FAN_TO_HA.items()}

# Temperature limits
MIN_TEMP = 16.0
MAX_TEMP = 32.0
TEMP_STEP = 0.5

# Device attributes
ATTR_POWER = "power"
ATTR_MODE = "mode"
ATTR_TEMPERATURE = "temperature"
ATTR_HUMIDITY = "humidity"
ATTR_FAN_SPEED = "fan_speed"
ATTR_FAN_DIRECTION = "fan_direction"
ATTR_CURRENT_TEMPERATURE = "current_temperature"
ATTR_CURRENT_HUMIDITY = "current_humidity"
ATTR_ERROR_STATUS = "error_status"
ATTR_DEVICE_NAME = "device_name"
ATTR_FIRMWARE_VERSION = "firmware_version"
