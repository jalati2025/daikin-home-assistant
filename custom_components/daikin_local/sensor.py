"""Sensor platform for Daikin Local integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .daikin_client import DaikinClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Daikin Local sensors based on a config entry."""
    client: DaikinClient = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = [
        DaikinTemperatureSensor(client, config_entry),
        DaikinHumiditySensor(client, config_entry),
        DaikinErrorStatusSensor(client, config_entry),
        DaikinFirmwareVersionSensor(client, config_entry),
    ]
    
    async_add_entities(entities)


class DaikinBaseSensor(SensorEntity):
    """Base class for Daikin sensors."""

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry, sensor_type: str) -> None:
        """Initialize the sensor."""
        self._client = client
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} {sensor_type.replace('_', ' ').title()}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": config_entry.data.get("name", "Daikin AC"),
            "manufacturer": "Daikin",
        }
        self._attr_should_poll = True


class DaikinTemperatureSensor(DaikinBaseSensor):
    """Representation of a Daikin temperature sensor."""

    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the temperature sensor."""
        super().__init__(client, config_entry, "temperature")
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} Temperature"

    async def async_update(self) -> None:
        """Update the sensor state."""
        try:
            sensor_info = await self.hass.async_add_executor_job(
                self._client.get_sensor_info
            )
            
            if "htemp" in sensor_info:
                self._attr_native_value = float(sensor_info["htemp"])
            else:
                self._attr_native_value = None
                
        except Exception as err:
            _LOGGER.error("Failed to update temperature sensor: %s", err)
            self._attr_native_value = None


class DaikinHumiditySensor(DaikinBaseSensor):
    """Representation of a Daikin humidity sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the humidity sensor."""
        super().__init__(client, config_entry, "humidity")
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} Humidity"

    async def async_update(self) -> None:
        """Update the sensor state."""
        try:
            sensor_info = await self.hass.async_add_executor_job(
                self._client.get_sensor_info
            )
            
            if "hhum" in sensor_info:
                self._attr_native_value = float(sensor_info["hhum"])
            else:
                self._attr_native_value = None
                
        except Exception as err:
            _LOGGER.error("Failed to update humidity sensor: %s", err)
            self._attr_native_value = None


class DaikinErrorStatusSensor(DaikinBaseSensor):
    """Representation of a Daikin error status sensor."""

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the error status sensor."""
        super().__init__(client, config_entry, "error_status")
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} Error Status"

    async def async_update(self) -> None:
        """Update the sensor state."""
        try:
            basic_info = await self.hass.async_add_executor_job(
                self._client.get_basic_info
            )
            
            if "err" in basic_info:
                error_code = basic_info["err"]
                if error_code == "0":
                    self._attr_native_value = "No Error"
                else:
                    self._attr_native_value = f"Error Code: {error_code}"
            else:
                self._attr_native_value = "Unknown"
                
        except Exception as err:
            _LOGGER.error("Failed to update error status sensor: %s", err)
            self._attr_native_value = "Connection Error"


class DaikinFirmwareVersionSensor(DaikinBaseSensor):
    """Representation of a Daikin firmware version sensor."""

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the firmware version sensor."""
        super().__init__(client, config_entry, "firmware_version")
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} Firmware Version"

    async def async_update(self) -> None:
        """Update the sensor state."""
        try:
            basic_info = await self.hass.async_add_executor_job(
                self._client.get_basic_info
            )
            
            if "ver" in basic_info:
                self._attr_native_value = basic_info["ver"]
            else:
                self._attr_native_value = "Unknown"
                
        except Exception as err:
            _LOGGER.error("Failed to update firmware version sensor: %s", err)
            self._attr_native_value = "Unknown"
