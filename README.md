![BLE Adjustable Base](images/hacs.png)

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![Version](https://img.shields.io/github/v/release/daviddelahoz/BLEAdjustableBase)](https://github.com/daviddelahoz/BLEAdjustableBase/releases)
[![License](https://img.shields.io/github/license/daviddelahoz/BLEAdjustableBase)](LICENSE)
[![Maintenance](https://img.shields.io/maintenance/yes/2026.svg)](https://github.com/daviddelahoz/BLEAdjustableBase)

# BLE Adjustable Base (Mattress Firm 900) for Home Assistant

A Home Assistant custom component for integrating the **Mattress Firm 900 Adjustable Base** via **Bluetooth Low Energy (BLE)**.  
This integration enables local control and automation of bed adjustments without relying on any cloud services.

---

## Background

The official **Mattress Firm M900 iOS app** was deprecated and officially unsupported as of **December 2024**, leaving the adjustable base functional but without an actively maintained smart control solution.

Back in **2020**, while the app was still available, I manually observed and reverse engineered the Bluetooth Low Energy communication used by the M900 app. At the time, I confirmed that the same commands could be reliably replicated using a Raspberry Pi with Python and the Bleak library.

Once the commands were confirmed to work consistently outside of the mobile app, the project was eventually packaged into a Home Assistant custom component so it could be easily installed via **HACS** and used for local automation.

To improve Bluetooth reliability and range, I also deployed a Bluetooth proxy using an ESP32 powered directly from the bed’s USB port. This step is optional, but useful if your Home Assistant instance is not within reliable Bluetooth range of the bed.

This integration communicates **locally over BLE only** and does not depend on any cloud APIs.

---

## Features

- UI-based setup using Home Assistant **Config Flow** (no YAML required)
- Bluetooth discovery filtered to adjustable bases advertising names starting with **`iFlex`**
- Reliable BLE connection using `bleak-retry-connector`
- Required **initialization sequence** handled automatically on connect
- Button entities for:
  - Head Up / Down
  - Foot Up / Down
  - Lumbar Up / Down
  - Presets (Flat, Zero Gravity, Lounge, Incline, Anti-snore)
  - Massage controls
  - Under-bed light control:
    - **Light (Cycle)**
    - **Light Off (Hold 3 seconds)** to match the physical remote behavior
- Automatic disconnect support so the physical remote continues to work
- Manual **Disconnect** button
- Optional RX notification logging for debugging
- Fully local operation (no cloud, no internet dependency)
- English and Spanish UI translations

---

## Requirements

- Home Assistant with Bluetooth support  
  (Home Assistant OS or Supervised recommended)
- Mattress Firm 900 Adjustable Base (iFlex BLE models)
- Optional: ESP32 running ESPHome as a Bluetooth proxy

---

## Installation (HACS – Recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click the **three dots (⋮)** in the top-right corner
4. Select **Custom repositories**
5. Add the repository URL: https://github.com/daviddelahoz/BLEAdjustableBase
6. Select **Category: Integration**
7. Click **Add**
8. Find **BLE Adjustable Base (Mattress Firm 900)** in HACS and click **Download**
9. Restart Home Assistant
10. Go to **Settings → Devices & Services → Add Integration**
11. Search for **BLE Adjustable Bed**

---

## Bluetooth Proxy (Optional)

If your Home Assistant instance is not within reliable Bluetooth range of the bed, you can deploy a Bluetooth proxy using an ESP32.

In this setup, the ESP32 can be powered directly from the bed’s built-in USB port, providing excellent proximity and stability.

Refer to the Home Assistant Bluetooth Proxy documentation:
https://www.home-assistant.io/integrations/bluetooth/#bluetooth-proxies

---

## Notes & Limitations

- The adjustable base does **not expose real-time position or angle telemetry** over BLE.
- Commands are sent optimistically, similar to the original mobile app and physical remote.
- Only one BLE connection can be active at a time.  
If Home Assistant remains connected, the physical remote may stop responding.
- Automatic disconnect and a manual **Disconnect** button are included to avoid this issue.

---

## Disclaimer

This is an independent, community-driven project and is **not affiliated with Mattress Firm or any manufacturer**.

Use at your own risk.

---

## Contributing

Issues and pull requests are welcome.  
If you have a similar adjustable base that uses different BLE payloads, feel free to open an issue and share details.

---

📄 **También disponible en español:** [README_ES.md](README_ES.md)