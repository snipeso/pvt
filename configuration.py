import string

CONF = {
    "participant": "001",
    "session": "1",
    "instructions": {
        "show": False,
        "duration": 5,
        "text": "Please fixate on the red square. When it is replaced by a counter, press the F key as fast as possible. Answers slower than .5 seconds are considered lapses.",
        "startPrompt": "Press any key to start. Press q to quit."
    },
    "screen": {
        "size": [1000, 1000],
        "color": "#6B6B6B",
        "monitor": "testMonitor",
        "full": False,
        "units": "norm"
    },
    "timing": {
        "rest":  1,  # 60,
        "overview": 1,
        "cue": 1
    },

    "task": {
        "name": "PVT",
        "duration":  30,  # 10*60,  # in seconds
        "maxTime": 500,
        "minTime": 100,
        "victoryColor": "green",
        "earlyColor": "yellow",
        "lateColor": "red",
    },
    "fixation": {
        "height": .1,
        "width": .2,
        "fillColor": "red",
        "errorFlash": 0.1,
        "minDelay": 0.5,
        "maxDelay": 5,  # 10,
        "scoreTime": 0.5
    }
}
