DOMAIN = "ble_adjustable_bed"

CONF_ADDRESS = "address"
CONF_NAME = "name"

CONF_DISCONNECT_AFTER_COMMAND = "disconnect_after_command"
CONF_IDLE_DISCONNECT_SECONDS = "idle_disconnect_seconds"
CONF_ENABLE_RX_NOTIFICATIONS = "enable_rx_notifications"

DEFAULT_DISCONNECT_AFTER_COMMAND = False
DEFAULT_IDLE_DISCONNECT_SECONDS = 8
DEFAULT_ENABLE_RX_NOTIFICATIONS = True

NUS_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
NUS_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
DEVICE_NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"

COMMANDS = {
    "HEAD_UP": {"name": "Head Up", "value": "5A0103103000A5", "handle": 14},
    "HEAD_DOWN": {"name": "Head Down", "value": "5A0103103001A5", "handle": 14},
    "FOOT_UP": {"name": "Foot Up", "value": "5A0103103002A5", "handle": 14},
    "FOOT_DOWN": {"name": "Foot Down", "value": "5A0103103003A5", "handle": 14},
    "ANTI_SNORE": {"name": "Anti-snore", "value": "5A0103103016A5", "handle": 14},
    "LOUNGE": {"name": "Lounge", "value": "5A0103103017A5", "handle": 14},
    "ZERO_GRAVITY": {"name": "Zero Gravity", "value": "5A0103103013A5", "handle": 14},
    "INCLINE": {"name": "Incline", "value": "5A0103103018A5", "handle": 14},
    "FLAT": {"name": "Flat", "value": "5A0103103010A5", "handle": 14},
    "LUMBAR_UP": {"name": "Lumbar Up", "value": "5A0103103006A5", "handle": 14},
    "LUMBAR_DOWN": {"name": "Lumbar Down", "value": "5A0103103007A5", "handle": 14},
    "MASSAGE_1": {"name": "Massage 1", "value": "5A0103103052A5", "handle": 14},
    "MASSAGE_2": {"name": "Massage 2", "value": "5A0103103053A5", "handle": 14},
    "MASSAGE_3": {"name": "Massage 3", "value": "5A0103103054A5", "handle": 14},
    "MASSAGE_STOP": {"name": "Massage Stop", "value": "5A010310306FA5", "handle": 14},
    "MASSAGE_UP": {"name": "Massage Up", "value": "5A0103104060A5", "handle": 14},
    "MASSAGE_DOWN": {"name": "Massage Down", "value": "5A0103104063A5", "handle": 14},

    "LIGHT_CYCLE": {"name": "Light (Cycle)", "value": "5A0103103070A5", "handle": 14},
    "LIGHT_OFF_HOLD": {"name": "Light Off (Hold 3s)", "value": "5A0103103074A5", "handle": 14},

    "INIT_1": {"name": "Init 1", "value": "09050A23050000", "handle": 58},
    "INIT_2": {"name": "Init 2", "value": "5A0B00A5", "handle": 14},
}

BUTTON_COMMAND_KEYS = [
    k for k in COMMANDS
    if k not in ("INIT_1", "INIT_2")
]