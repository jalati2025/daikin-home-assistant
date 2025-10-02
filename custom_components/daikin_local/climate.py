"""Climate platform for Daikin Local integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    FanMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_CURRENT_HUMIDITY,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_DEVICE_NAME,
    ATTR_ERROR_STATUS,
    ATTR_FAN_DIRECTION,
    ATTR_FAN_SPEED,
    ATTR_FIRMWARE_VERSION,
    ATTR_HUMIDITY,
    ATTR_MODE,
    ATTR_POWER,
    ATTR_TEMPERATURE,
    CLIMATE_MODE_AUTO,
    CLIMATE_MODE_COOL,
    CLIMATE_MODE_DRY,
    CLIMATE_MODE_FAN_ONLY,
    CLIMATE_MODE_HEAT,
    CLIMATE_MODE_OFF,
    DAIKIN_FAN_TO_HA,
    DAIKIN_MODE_TO_HA,
    DOMAIN,
    FAN_SPEED_AUTO,
    FAN_SPEED_HIGH,
    FAN_SPEED_LOW,
    FAN_SPEED_MAX,
    FAN_SPEED_MEDIUM,
    FAN_SPEED_QUIET,
    HA_FAN_TO_DAIKIN,
    HA_MODE_TO_DAIKIN,
    MAX_TEMP,
    MIN_TEMP,
    TEMP_STEP,
)
from .daikin_client import DaikinClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Daikin Local climate based on a config entry."""
    client: DaikinClient = hass.data[DOMAIN][config_entry.entry_id]
    
    async_add_entities([DaikinClimateEntity(client, config_entry)])


class DaikinClimateEntity(ClimateEntity):
    """Representation of a Daikin climate entity."""

    _attr_hvac_modes = [
        HVACMode.OFF,
        HVACMode.AUTO,
        HVACMode.COOL,
        HVACMode.HEAT,
        HVACMode.DRY,
        HVACMode.FAN_ONLY,
    ]
    
    _attr_fan_modes = [
        FAN_SPEED_AUTO,
        FAN_SPEED_QUIET,
        FAN_SPEED_LOW,
        FAN_SPEED_MEDIUM,
        FAN_SPEED_HIGH,
        FAN_SPEED_MAX,
    ]
    
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = TEMP_STEP
    _attr_min_temp = MIN_TEMP
    _attr_max_temp = MAX_TEMP
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.TURN_OFF
        | ClimateEntityFeature.TURN_ON
    )

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the climate entity."""
        self._client = client
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_climate"
        self._attr_name = config_entry.data.get("name", "Daikin AC")
        
        # Initialize state attributes
        self._attr_current_temperature = None
        self._attr_current_humidity = None
        self._attr_target_temperature = None
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_fan_mode = FAN_SPEED_AUTO
        self._attr_fan_direction = "0"
        self._attr_power = False
        self._attr_error_status = "0"
        self._attr_device_name = None
        self._attr_firmware_version = None

    async def async_update(self) -> None:
        """Update the climate entity state."""
        try:
            # Get control info
            control_info = await self.hass.async_add_executor_job(
                self._client.get_control_info
            )
            
            # Get sensor info
            sensor_info = await self.hass.async_add_executor_job(
                self._client.get_sensor_info
            )
            
            # Get basic info (for device info)
            basic_info = await self.hass.async_add_executor_job(
                self._client.get_basic_info
            )
            
            # Update control attributes
            if "pow" in control_info:
                self._attr_power = control_info["pow"] == "1"
                self._attr_hvac_mode = (
                    HVACMode.OFF if not self._attr_power
                    else DAIKIN_MODE_TO_HA.get(int(control_info.get("mode", "1")), HVACMode.AUTO)
                )
            
            if "stemp" in control_info:
                self._attr_target_temperature = float(control_info["stemp"])
            
            if "f_rate" in control_info:
                self._attr_fan_mode = DAIKIN_FAN_TO_HA.get(control_info["f_rate"], FAN_SPEED_AUTO)
            
            if "f_dir" in control_info:
                self._attr_fan_direction = control_info["f_dir"]
            
            # Update sensor attributes
            if "htemp" in sensor_info:
                self._attr_current_temperature = float(sensor_info["htemp"])
            
            if "hhum" in sensor_info:
                self._attr_current_humidity = float(sensor_info["hhum"])
            
            # Update device info
            if "name" in basic_info:
                self._attr_device_name = basic_info["name"]
            
            if "ver" in basic_info:
                self._attr_firmware_version = basic_info["ver"]
            
            if "err" in basic_info:
                self._attr_error_status = basic_info["err"]
            
        except Exception as err:
            _LOGGER.error("Failed to update climate entity: %s", err)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        
        # Get current control info to preserve other settings
        control_info = await self.hass.async_add_executor_job(
            self._client.get_control_info
        )
        
        # Set new temperature
        success = await self.hass.async_add_executor_job(
            self._client.set_control_info,
            pow=control_info.get("pow", "1"),
            mode=control_info.get("mode", "1"),
            stemp=str(temperature),
            shum=control_info.get("shum", "0"),
            f_rate=control_info.get("f_rate", "A"),
            f_dir=control_info.get("f_dir", "0")
        )
        
        if success:
            self._attr_target_temperature = temperature
            self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.OFF:
            # Turn off - need to preserve all parameters
            control_info = await self.hass.async_add_executor_job(
                self._client.get_control_info
            )
            
            success = await self.hass.async_add_executor_job(
                self._client.set_control_info,
                pow="0",
                mode=control_info.get("mode", "0"),
                stemp=control_info.get("stemp", "22.0"),
                shum=control_info.get("shum", "0"),
                f_rate=control_info.get("f_rate", "A"),
                f_dir=control_info.get("f_dir", "0")
            )
        else:
            # Turn on with specific mode
            daikin_mode = HA_MODE_TO_DAIKIN.get(hvac_mode, "1")
            
            # Get current settings
            control_info = await self.hass.async_add_executor_job(
                self._client.get_control_info
            )
            
            success = await self.hass.async_add_executor_job(
                self._client.set_control_info,
                pow="1",
                mode=daikin_mode,
                stemp=control_info.get("stemp", "22.0"),
                shum=control_info.get("shum", "0"),
                f_rate=control_info.get("f_rate", "A"),
                f_dir=control_info.get("f_dir", "0")
            )
        
        if success:
            self._attr_hvac_mode = hvac_mode
            self._attr_power = hvac_mode != HVACMode.OFF
            self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        daikin_fan = HA_FAN_TO_DAIKIN.get(fan_mode, "A")
        
        # Get current control info
        control_info = await self.hass.async_add_executor_job(
            self._client.get_control_info
        )
        
        success = await self.hass.async_add_executor_job(
            self._client.set_control_info,
            pow=control_info.get("pow", "1"),
            mode=control_info.get("mode", "1"),
            stemp=control_info.get("stemp", "22.0"),
            shum=control_info.get("shum", "0"),
            f_rate=daikin_fan,
            f_dir=control_info.get("f_dir", "0")
        )
        
        if success:
            self._attr_fan_mode = fan_mode
            self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_POWER: self._attr_power,
            ATTR_MODE: self._attr_hvac_mode,
            ATTR_FAN_SPEED: self._attr_fan_mode,
            ATTR_FAN_DIRECTION: self._attr_fan_direction,
            ATTR_CURRENT_HUMIDITY: self._attr_current_humidity,
            ATTR_ERROR_STATUS: self._attr_error_status,
            ATTR_DEVICE_NAME: self._attr_device_name,
            ATTR_FIRMWARE_VERSION: self._attr_firmware_version,
        }
