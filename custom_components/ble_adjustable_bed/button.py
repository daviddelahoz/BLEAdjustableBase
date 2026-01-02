from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, COMMANDS, BUTTON_COMMAND_KEYS, ICONS


async def async_setup_entry(hass, entry, async_add_entities):
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]

    entities = [BedButton(entry, controller, key) for key in BUTTON_COMMAND_KEYS]
    entities.append(DisconnectButton(entry, controller))
    async_add_entities(entities)


class BedButton(ButtonEntity):
    def __init__(self, entry, controller, key):
        self._controller = controller
        self._key = key
        self._attr_name = COMMANDS[key]["name"]
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_icon = ICONS.get(key, "mdi:bed")

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._controller.address)},
            name=self._controller.name,
            manufacturer="Mattress Firm",
            model="900 Adjustable Base",
        )

    async def async_press(self):
        await self._controller.async_press(self._key)


class DisconnectButton(ButtonEntity):
    def __init__(self, entry, controller):
        self._controller = controller
        self._attr_name = "Disconnect (enable remote)"
        self._attr_unique_id = f"{entry.entry_id}_disconnect"
        self._attr_icon = ICONS.get("DISCONNECT", "mdi:bluetooth-off")

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._controller.address)},
            name=self._controller.name,
            manufacturer="Mattress Firm",
            model="900 Adjustable Base",
        )

    async def async_press(self):
        await self._controller.async_disconnect()