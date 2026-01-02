from __future__ import annotations

import asyncio
from typing import Optional

from bleak import BleakClient
from bleak_retry_connector import establish_connection
from bleak.exc import BleakError

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant

from .const import COMMANDS, NUS_TX_UUID, NUS_RX_UUID, DEVICE_NAME_UUID


class BedController:
    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        name: str,
        disconnect_after_command: bool,
        idle_disconnect_seconds: int,
        enable_rx_notifications: bool,
    ) -> None:
        self.hass = hass
        self.address = address
        self.name = name

        self.disconnect_after_command = disconnect_after_command
        self.idle_disconnect_seconds = idle_disconnect_seconds
        self.enable_rx_notifications = enable_rx_notifications

        self._client: Optional[BleakClient] = None
        self._lock = asyncio.Lock()
        self._initialized = False
        self._write_uuid: Optional[str] = None
        self._idle_task: Optional[asyncio.Task] = None

    async def async_disconnect(self) -> None:
        async with self._lock:
            await self._disconnect()

    async def async_press(self, key: str) -> None:
        async with self._lock:
            await self._connect()
            await self._initialize()

            if key == "LIGHT_OFF_HOLD":
                await self._light_off_hold()
            else:
                await self._write(bytes.fromhex(COMMANDS[key]["value"]))

            if self.disconnect_after_command:
                await self._disconnect()
            else:
                self._schedule_idle_disconnect()

    async def _connect(self) -> None:
        if self._client and self._client.is_connected and self._write_uuid:
            return

        device = bluetooth.async_ble_device_from_address(self.hass, self.address)
        self._client = await establish_connection(BleakClient, device, self.name)

        self._select_write_char()

        if self.enable_rx_notifications:
            try:
                await self._client.start_notify(NUS_RX_UUID, lambda *_: None)
            except Exception:
                pass

        self._initialized = False

    def _select_write_char(self) -> None:
        chars = []
        for svc in self._client.services:
            for ch in svc.characteristics:
                if "write" in ch.properties or "write-without-response" in ch.properties:
                    chars.append(ch.uuid)

        if NUS_TX_UUID in chars:
            self._write_uuid = NUS_TX_UUID
        else:
            self._write_uuid = next(
                u for u in chars if u.lower() != DEVICE_NAME_UUID.lower()
            )

    async def _initialize(self) -> None:
        if self._initialized:
            return

        await self._write(bytes.fromhex(COMMANDS["INIT_1"]["value"]))
        await asyncio.sleep(0.05)
        await self._write(bytes.fromhex(COMMANDS["INIT_2"]["value"]))
        self._initialized = True

    async def _write(self, payload: bytes) -> None:
        if not self._client or not self._write_uuid:
            raise BleakError("Not connected")

        await self._client.write_gatt_char(self._write_uuid, payload, response=False)

    async def _light_off_hold(self) -> None:
        payload = bytes.fromhex(COMMANDS["LIGHT_OFF_HOLD"]["value"])
        start = asyncio.get_running_loop().time()

        while asyncio.get_running_loop().time() - start < 3.0:
            await self._write(payload)
            await asyncio.sleep(0.25)

    async def _disconnect(self) -> None:
        if self._idle_task:
            self._idle_task.cancel()
            self._idle_task = None

        if self._client:
            try:
                await self._client.disconnect()
            except Exception:
                pass

        self._client = None
        self._write_uuid = None
        self._initialized = False

    def _schedule_idle_disconnect(self) -> None:
        if self.idle_disconnect_seconds <= 0:
            return

        if self._idle_task:
            self._idle_task.cancel()

        self._idle_task = asyncio.create_task(self._idle_timer())

    async def _idle_timer(self) -> None:
        await asyncio.sleep(self.idle_disconnect_seconds)
        async with self._lock:
            await self._disconnect()