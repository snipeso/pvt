CONF = {
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
    "loggingLevel": {
        "versionMain": "warning",
        "versionDemo": "info",
        "versionDebug": "info"
    },
    "showInstructions": {
        "versionMain": True,
        "versionDemo": True,
        "versionDebug": False
    },
    "sendTriggers": {
        "versionMain": True,
        "versionDemo": False,
        "versionDebug": False
    },
    "recordEyetracking": {
        "versionMain": True,
        "versionDemo": False,
        "versionDebug": False
    },
    "savePupillometry": {
        "versionMain": True,
        "versionDemo": False,
        "versionDebug": False
    },
    "includeRest": True,
    "screen": {
        "resolution": { "versionMain": [3840, 2160], "versionDebug": [1000, 1000] },
        "size": { "versionMain": [34.4, 19.3], "versionDebug": [10, 10] },
        "units": "cm",
        "full": { "versionMain": True, "versionDemo": True, "versionDebug": False }
    },
    "timing": {
        "overview": 1,
        "cue": 1,
        "rest": { "versionMain": 60, "versionDemo": 1, "versionDebug": 1 }
    },
    "instructionSizes": {
        "taskHeight": 0.5,
        "taskPos": [0, 0],
        "sessionHeight": 0.5,
        "sessionPos": [0, -3],
        "instructionsHeight": 0.5,
        "startPromptHeight": 0.5
    },
    "trigger": {
        "serial_device": "/dev/usb/lp0",
        "labels": {
        "Start": 1,
        "End": 2,
        "Stim": 3,
        "Response": 4,
        "BadResponse": 5,
        "StartBlank": 6,
        "EndBlank": 7,
        "ALARM": 8,
        "Quit": 9
        }
    },
    "pupillometry": {
        "ip": "192.168.0.11",
        "port": 50020
    }
}