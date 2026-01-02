from __future__ import annotations

import asyncio
from typing import Optional

from bleak import BleakClient
from bleak.exc import BleakError
from bleak_retry_connector import establish_connection

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant

from .const import COMMANDS, NUS_TX_UUID, DEVICE_NAME_UUID


class BedController:
    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        name: str,
        disconnect_after_command: bool,
        idle_disconnect_seconds: int,
    ) -> None:
        self.hass = hass
        self.address = address
        self.name = name

        self.disconnect_after_command = disconnect_after_command
        self.idle_disconnect_seconds = idle_disconnect_seconds

        self._client: Optional[BleakClient] = None
        self._lock = asyncio.Lock()
        self._initialized = False
        self._write_uuid: Optional[str] = None
        self._idle_task: Optional[asyncio.Task] = None

    async def async_disconnect(self) -> None:
        async with self._lock:
            await self._disconnect_unlocked()

    async def async_press(self, key: str) -> None:
        async with self._lock:
            await self._ensure_connected()
            await self._ensure_initialized()

            if key == "LIGHT_OFF_HOLD":
                await self._light_off_hold_3s()
            else:
                await self._write_raw(bytes.fromhex(COMMANDS[key]["value"]))

            if self.disconnect_after_command:
                await self._disconnect_unlocked()
            else:
                await self._post_command_housekeeping()

    async def _ensure_connected(self) -> None:
        if self._client and self._client.is_connected and self._write_uuid:
            return

        device = bluetooth.async_ble_device_from_address(self.hass, self.address)
        if device is None:
            device = bluetooth.BLEDevice(self.address, self.name, details=None, rssi=0)

        self._client = await establish_connection(
            BleakClient,
            device,
            self.name,
            max_attempts=3,
        )

        self._select_write_characteristic()
        self._initialized = False

    def _select_write_characteristic(self) -> None:
        if not self._client:
            raise BleakError("Client not connected")

        writable: list[str] = []
        for svc in self._client.services:
            for ch in svc.characteristics:
                props = set(getattr(ch, "properties", []) or [])
                if "write" in props or "write-without-response" in props:
                    writable.append(ch.uuid)

        if not writable:
            raise BleakError("No writable GATT characteristics found (cannot control bed).")

        if NUS_TX_UUID in writable:
            self._write_uuid = NUS_TX_UUID
            return

        filtered = [u for u in writable if u.lower() != DEVICE_NAME_UUID.lower()]
        self._write_uuid = filtered[0] if filtered else writable[0]

    async def _ensure_initialized(self) -> None:
        if self._initialized:
            return

        await self._write_raw(bytes.fromhex(COMMANDS["INIT_1"]["value"]))
        await asyncio.sleep(0.05)
        await self._write_raw(bytes.fromhex(COMMANDS["INIT_2"]["value"]))
        await asyncio.sleep(0.05)

        self._initialized = True

    async def _write_raw(self, payload: bytes) -> None:
        if not self._client or not self._client.is_connected:
            raise BleakError("Client not connected")
        if not self._write_uuid:
            raise BleakError("No selected write characteristic UUID")

        last_err: Optional[Exception] = None
        for _ in range(3):
            try:
                await self._client.write_gatt_char(self._write_uuid, payload, response=False)
                return
            except Exception as e:
                last_err = e
                await asyncio.sleep(0.1)

        self._initialized = False
        await self._disconnect_unlocked()
        raise last_err if last_err else BleakError("Write failed")

    async def _light_off_hold_3s(self) -> None:
        payload = bytes.fromhex(COMMANDS["LIGHT_OFF_HOLD"]["value"])
        loop = asyncio.get_running_loop()
        start = loop.time()

        while loop.time() - start < 3.0:
            await self._write_raw(payload)
            await asyncio.sleep(0.25)

    async def _disconnect_unlocked(self) -> None:
        if self._idle_task:
            self._idle_task.cancel()
            self._idle_task = None

        if self._client:
            try:
                await self._client.disconnect()
            except Exception:
                pass

        self._client = None
        self._initialized = False
        self._write_uuid = None

    async def _post_command_housekeeping(self) -> None:
        if self.idle_disconnect_seconds <= 0:
            return

        if self._idle_task:
            self._idle_task.cancel()

        self._idle_task = asyncio.create_task(self._idle_disconnect())

    async def _idle_disconnect(self) -> None:
        try:
            await asyncio.sleep(self.idle_disconnect_seconds)
            async with self._lock:
                await self._disconnect_unlocked()
        except asyncio.CancelledError:
            return