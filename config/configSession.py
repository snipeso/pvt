CONF = {
    "participant": "01",
    "session": "1",
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
    "showInstructions": True,
    "trigger": {
        "serial_device": "/dev/ttyUSB0", #this is computer and OS and port and random specific. see readme on how to get
        "labels": {
            "" #TODO
        }
    }
}
