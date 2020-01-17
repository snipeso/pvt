CONF = {
    "participant": "01",
    "session": "1",
    "showInstructions": True,
    "sendTriggers": False,
    "loggingLevel": logging.WARNING,
    "screen": {
        "full": True,
        "color": "#6B6B6B",
        "monitor": 'Extreme',  # "testMonitor",
        # screen size when not fullscreen
        "debugResolution":  [1000, 1000],  # [384, 216],
        "debugSize": [10, 10],
        "units": "norm",
        "resolution": [3840, 2160],
        # Obtain from xrandr in command window
        "size": [34.4, 19.3]
    },
    "timing": {
        "rest":  1,  # 60,
        "overview": 1,
        "cue": 1
    },
    "trigger": {
        "serial_device": "COM3", #this is computer and OS and port and random specific. see readme on how to get
        "labels": {
            "Start": 0x01,
            "End": 0x02,
            "Stim": 0x03,
            "Response": 0x04,
            "BadResponse": 0x05,
            "StartBlank": 0x06,
            "EndBlank": 0x07,
            "ALARM": 0x08,
            "Quit": 0x09
        }
    }
}
