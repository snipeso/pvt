from config.updateConfig import UpdateConfig

pvtCONF = {
    "task": {
        "name": "PVT",
        # in seconds, duration of whole experiment
        "duration": {"versionMain": 10*60, "versionDemo": 60, "versionDebug": 2*60},
        "minTime": .100,  # in miliseconds, min time to be considered a valid RT
        "maxTime": .500,  # over this, RT considered a lapse
        "warningTime": 5,  # in seconds, time before a tone plays to wake participant up
        "victoryColor": "green",
        "earlyColor": "yellow",
        "lateColor": "red",
    },
    "fixation": {
        "height": 1,
        "width": 3,
        "boxColor": "red",
        "errorFlash": 0.1,  # in seconds, how long to flash box if key pushed during delay
        "minDelay": 2,  # in seconds, minimum delay between stimuli
        "maxDelay": {"versionMain": 10, "versionDemo": 10, "versionDebug": 3},
        "scoreTime": 1  # in seconds, time to show final score
    },
    "instructions": {
        "text": "Please fixate on the red square. When it is replaced by a counter, press the shift key as fast as possible. Answers slower than .5 seconds are considered lapses.",
        "startPrompt": "Press any key to start. Press q to quit.",
        "alarm": "horn.wav",
        "questionnaireReminder": "answerQuestionnaire.wav"
    },
}

updateCofig = UpdateConfig()
updateCofig.addContent(pvtCONF)

CONF = updateCofig.getConfig()
