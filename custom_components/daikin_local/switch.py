"""Switch platform for Daikin Local integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up Daikin Local switches based on a config entry."""
    client: DaikinClient = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = [
        DaikinPowerSwitch(client, config_entry),
        DaikinFanDirectionSwitch(client, config_entry),
    ]
    
    async_add_entities(entities)


class DaikinBaseSwitch(SwitchEntity):
    """Base class for Daikin switches."""

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry, switch_type: str) -> None:
        """Initialize the switch."""
        self._client = client
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_{switch_type}"
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} {switch_type.replace('_', ' ').title()}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": config_entry.data.get("name", "Daikin AC"),
            "manufacturer": "Daikin",
        }
        self._attr_should_poll = True


class DaikinPowerSwitch(DaikinBaseSwitch):
    """Representation of a Daikin power switch."""

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the power switch."""
        super().__init__(client, config_entry, "power")
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} Power"
        self._attr_icon = "mdi:power"

    async def async_update(self) -> None:
        """Update the switch state."""
        try:
            control_info = await self.hass.async_add_executor_job(
                self._client.get_control_info
            )
            
            if "pow" in control_info:
                self._attr_is_on = control_info["pow"] == "1"
            else:
                self._attr_is_on = False
                
        except Exception as err:
            _LOGGER.error("Failed to update power switch: %s", err)
            self._attr_is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        # Get current control info to preserve settings
        control_info = await self.hass.async_add_executor_job(
            self._client.get_control_info
        )
        
        success = await self.hass.async_add_executor_job(
            self._client.set_control_info,
            pow="1",
            mode=control_info.get("mode", "1"),
            stemp=control_info.get("stemp", "22.0"),
            shum=control_info.get("shum", "0"),
            f_rate=control_info.get("f_rate", "A"),
            f_dir=control_info.get("f_dir", "0")
        )
        
        if success:
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        # Get current control info to preserve settings
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
        
        if success:
            self._attr_is_on = False
            self.async_write_ha_state()


class DaikinFanDirectionSwitch(DaikinBaseSwitch):
    """Representation of a Daikin fan direction switch."""

    def __init__(self, client: DaikinClient, config_entry: ConfigEntry) -> None:
        """Initialize the fan direction switch."""
        super().__init__(client, config_entry, "fan_direction")
        self._attr_name = f"{config_entry.data.get('name', 'Daikin AC')} Fan Direction"
        self._attr_icon = "mdi:fan"

    async def async_update(self) -> None:
        """Update the switch state."""
        try:
            control_info = await self.hass.async_add_executor_job(
                self._client.get_control_info
            )
            
            if "f_dir" in control_info:
                self._attr_is_on = control_info["f_dir"] == "1"
            else:
                self._attr_is_on = False
                
        except Exception as err:
            _LOGGER.error("Failed to update fan direction switch: %s", err)
            self._attr_is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn fan direction swing on."""
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
            f_rate=control_info.get("f_rate", "A"),
            f_dir="1"
        )
        
        if success:
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn fan direction swing off."""
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
            f_rate=control_info.get("f_rate", "A"),
            f_dir="0"
        )
        
        if success:
            self._attr_is_on = False
            self.async_write_ha_state()
