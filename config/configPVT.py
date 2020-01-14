from config.configSession import CONF

CONF.update({
    "task": {
        "name": "PVT",
        "duration": 10*60,  # in seconds, duration of whole experiment
        "minTime": 100,  # in miliseconds, min time to be considered a valid RT
        "maxTime": 500,  # over this, RT considered a lapse
        "warningTime": 5,  # in seconds, time before a tone plays to wake participant up
        "victoryColor": "green",
        "earlyColor": "yellow",
        "lateColor": "red",
    },
    "fixation": {
        "height": .1,
        "width": .2,
        "fillColor": "red",
        "errorFlash": 0.1,  # in seconds, how long to flash box if key pushed during delay
        "minDelay": 1,  # in seconds, minimum delay between stimuli
        "maxDelay": 3,  # maximum delay between stimuli
        "scoreTime": 0.5  # in seconds, time to show final score
    },
    "instructions": {
        "text": "Please fixate on the red square. When it is replaced by a counter, press the F key as fast as possible. Answers slower than .5 seconds are considered lapses.",
        "startPrompt": "Press any key to start. Press q to quit."
    },
})
