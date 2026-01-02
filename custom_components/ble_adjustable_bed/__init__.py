from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_ADDRESS,
    CONF_NAME,
    CONF_DISCONNECT_AFTER_COMMAND,
    CONF_IDLE_DISCONNECT_SECONDS,
    DEFAULT_DISCONNECT_AFTER_COMMAND,
    DEFAULT_IDLE_DISCONNECT_SECONDS,
)
from .bed_controller import BedController

PLATFORMS = ["button"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    address = entry.data.get(CONF_ADDRESS)
    name = entry.data.get(CONF_NAME, address)

    disconnect_after = entry.options.get(
        CONF_DISCONNECT_AFTER_COMMAND, DEFAULT_DISCONNECT_AFTER_COMMAND
    )
    idle_secs = entry.options.get(
        CONF_IDLE_DISCONNECT_SECONDS, DEFAULT_IDLE_DISCONNECT_SECONDS
    )

    controller = BedController(
        hass=hass,
        address=address,
        name=name,
        disconnect_after_command=disconnect_after,
        idle_disconnect_seconds=idle_secs,
    )

    hass.data[DOMAIN][entry.entry_id] = {"controller": controller}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if data:
        await data["controller"].async_disconnect()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)