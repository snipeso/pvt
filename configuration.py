import string

CONF = {
    "participant": "001",
    "session": "1",
    "keys": {
        "before": ["1", "left", "minus"],
        "after": ["2", "right", "plus"],
        "start": "5",
    },
    "screen": {
        "size": [1000, 1000],
        "color": "#6B6B6B",
        "monitor": "testMonitor",
        "full": False,
        "units": "norm"
    },
    "timing": {
        "rest":  2,  # 60,
        "overview": 2,
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
        "lineColor": "red",
        "minDelay": 0.5,
        "maxDelay": 5,  # 10,

    }
}
