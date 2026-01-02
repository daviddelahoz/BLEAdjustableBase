from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.core import callback

from .const import DOMAIN, CONF_ADDRESS, CONF_NAME


class BleAdjustableBedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        devices = bluetooth.async_discovered_service_info(self.hass)
        options = _build_device_options(devices) or {}

        if user_input is not None:
            address = user_input.get(CONF_ADDRESS)
            if not address or address not in options:
                errors["base"] = "no_iflex_found"
            else:
                name = options[address].split(" (", 1)[0]
                await self.async_set_unique_id(address)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_ADDRESS: address,
                        CONF_NAME: name,
                    },
                )

        if options:
            schema = vol.Schema(
                {vol.Required(CONF_ADDRESS): vol.In(options)}
            )
        else:
            schema = vol.Schema(
                {vol.Required(CONF_ADDRESS, default=""): str}
            )
            errors["base"] = "no_iflex_found"

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )


@callback
def _build_device_options(devices) -> dict[str, str]:
    out: dict[str, str] = {}

    for info in devices:
        name = getattr(info, "name", None)
        address = getattr(info, "address", None)

        if not name or not address:
            continue

        if not name.lower().startswith("iflex"):
            continue

        out[address] = f"{name} ({address})"

    return dict(sorted(out.items(), key=lambda kv: kv[1].lower()))