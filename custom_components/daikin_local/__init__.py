"""Daikin Local Integration for Home Assistant."""
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .daikin_client import DaikinClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Daikin Local from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Create the Daikin client
    client = DaikinClient(
        ip_address=entry.data["ip_address"],
        uuid=entry.data["uuid"],
        key=entry.data["key"]
    )
    
    # Test the connection
    try:
        await hass.async_add_executor_job(client.test_connection)
        _LOGGER.info("Successfully connected to Daikin unit at %s", entry.data["ip_address"])
    except Exception as err:
        _LOGGER.error("Failed to connect to Daikin unit: %s", err)
        return False
    
    # Store the client in hass data
    hass.data[DOMAIN][entry.entry_id] = client
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
