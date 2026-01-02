# BLE Adjustable Base (Mattress Firm 900) for Home Assistant

A Home Assistant custom component for integrating the **Mattress Firm 900 Adjustable Base** via **Bluetooth Low Energy (BLE)**.  
This integration enables local control and automation of bed adjustments without relying on any cloud services.

---

## Background

The original iPhone app for this adjustable base was deprecated around 2020, leaving the hardware functional but without official smart control.

At the time, I manually observed the Bluetooth Low Energy communication used by the mobile app and later confirmed that the same commands could be reliably replicated using a Raspberry Pi with Python and the Bleak library.

Once I confirmed the commands worked reliably from a Raspberry Pi using Python/Bleak, I turned the project into a Home Assistant integration so anyone can install it via HACS and automate it locally.

To improve Bluetooth reliability and range, I also deployed a Bluetooth proxy using an ESP32 powered directly from the bed’s USB port. This step is optional, but useful if your Home Assistant instance is not within Bluetooth range of the bed.

This project communicates **locally over BLE only** and does not depend on any cloud APIs.

---

## Features

- **UI-based Config Flow** (no YAML required)
- Bluetooth discovery filtered to beds advertising names starting with **`iFlex`**
- Reliable BLE connection using `bleak-retry-connector`
- Required **initialization sequence** handled automatically on connect
- Button entities for:
  - Head Up / Down
  - Foot Up / Down
  - Lumbar Up / Down
  - Presets (Flat, Zero Gravity, Lounge, Incline, Anti-snore)
  - Massage levels and controls
  - Light control:
    - **Light (Cycle)**
    - **Light Off (Hold 3s)** — simulates the long-press behavior of the physical remote
- **Automatic disconnect support** to ensure the physical remote continues working
- Optional RX notification logging for debugging and experimentation
- Fully local operation (no internet required)

---

## Requirements

- Home Assistant with Bluetooth support  
  - Home Assistant OS or Supervised is recommended
- Mattress Firm 900 Adjustable Base (iFlex BLE models)
- Optional: ESP32 running ESPHome as a Bluetooth Proxy

---

## Installation (HACS)

1. Open **HACS**
2. Add this repository as a **Custom Repository**
   - Category: **Integration**
3. Install **BLE Adjustable Base**
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration**
6. Search for **BLE Adjustable Bed**

---

## Bluetooth Proxy (Optional)

If your Home Assistant instance is not within reliable Bluetooth range of the bed, you can deploy a Bluetooth proxy using an ESP32.

In my setup, the ESP32 is powered directly from the bed’s built-in USB port, providing excellent proximity and stability.

Refer to the Home Assistant Bluetooth Proxy documentation for ESPHome configuration:
https://www.home-assistant.io/integrations/bluetooth/#bluetooth-proxies

---

## Notes & Limitations

- This adjustable base does **not expose real-time position or angle telemetry** over BLE.
- Commands are sent optimistically (fire-and-forget), similar to the original remote and mobile app.
- Only one BLE connection may be active at a time.  
  If Home Assistant remains connected, the physical remote may stop responding.
  - Auto-disconnect and a manual **Disconnect** button are provided to avoid this issue.

---

## Disclaimer

This project is an independent, community-driven integration and is **not affiliated with Mattress Firm or any manufacturer**.

Use at your own risk.

---

## Contributing

Issues, logs, and pull requests are welcome.  
If you have a similar adjustable base that uses different BLE payloads, feel free to open an issue and share details.

📄 También disponible en español: [README_ES.md](README_ES.md)