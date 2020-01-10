from config.configSession import CONF

CONF.update({
    "task": {
        "name": "PVT",
        "duration": 10*60,  # in seconds
        "minTime": 100,  # in miliseconds
        "maxTime": 500,
        "warningTime": 5,  # in seconds
        "victoryColor": "green",
        "earlyColor": "yellow",
        "lateColor": "red",
    },
    "fixation": {
        "height": .1,
        "width": .2,
        "fillColor": "red",
        "errorFlash": 0.1,
        "minDelay": 2,
        "maxDelay": 10,  # 10,
        "scoreTime": 0.5
    },
    "instructions": {
        "duration": 5,
        "text": "Please fixate on the red square. When it is replaced by a counter, press the F key as fast as possible. Answers slower than .5 seconds are considered lapses.",
        "startPrompt": "Press any key to start. Press q to quit."
    },
})
