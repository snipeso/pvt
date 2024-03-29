import logging
import os
import random
import time
import sys
import datetime

from screen import Screen
from scorer import Scorer
from trigger import Trigger
from psychopy import core, event, sound, gui
from psychopy.hardware import keyboard
from pupil_labs import PupilCore
from datalog import Datalog
from config.updateConfig import UpdateConfig
from config.configPVT import CONF

#########################################################################

######################################
# Initialize screen, logger and inputs

# get user inputs
sessionInfoDlg = gui.Dlg(title="Session Info")
sessionInfoDlg.addField("Participant ID: ")
sessionInfoDlg.addField('Session: ')
sessionInfoDlg.addField('Version: ', choices=["main", "demo", "debug"])

sessionInfo = sessionInfoDlg.show()

if not sessionInfoDlg.OK:
     sys.exit(2)

# Append output to CONF
CONF["participant"] = sessionInfo[0]
CONF["session"] = sessionInfo[1]
CONF["version"] = sessionInfo[2]

CONF = UpdateConfig(CONF).getConfig()

logging.basicConfig(
    level=CONF["loggingLevel"],
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

# initiate contact with eyetracker, if used
eyetracker = PupilCore(ip=CONF["pupillometry"]
                       ["ip"], port=CONF["pupillometry"]["port"], shouldRecord=CONF["recordEyetracking"])

# initiate contact with EEG system
trigger = Trigger(CONF["trigger"]["serial_device"],
                  CONF["sendTriggers"], CONF["trigger"]["labels"])

# Start showing experiment screen
screen = Screen(CONF)

# initiate system for saving data
datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["participant"] + "_" + CONF["session"]), CONF=CONF)  # This is for saving data TODO: apply everywhere


# initiate psychopy stuff
kb = keyboard.Keyboard()

mainClock = core.MonotonicClock()  # starts clock for timestamping events

alarm = sound.Sound(os.path.join('sounds', CONF["instructions"]["alarm"]),
                    stereo=True)

questionnaireReminder = sound.Sound(os.path.join(
    'sounds', CONF["instructions"]["questionnaireReminder"]), stereo=True)

scorer = Scorer()

logging.info('Initialization completed')


#########################################################################

# function for quitting
def quitExperimentIf(shouldQuit):
    "Quit experiment if condition is met"

    if shouldQuit:
        scorer.getScore()
        logging.warning('quit experiment')
        trigger.send("Quit")
        eyetracker.stop_recording()
        trigger.reset()
        sys.exit(2)

# function for showing screen stuff
def onFlip():
    "Send and restart clocks as soon as screen changes"
    trigger.send("Stim")
    kb.clock.reset()
    datalog["startTime"] = mainClock.getTime()


##############
# Introduction
##############

# Display overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])

# Optionally, display instructions
if CONF["showInstructions"]:
    screen.show_instructions()
    key = event.waitKeys()
    quitExperimentIf(key[0] == 'q')

eyetracker.start_recording(os.path.join(
    CONF["participant"], CONF["task"]["name"], CONF["session"]))

# Blank screen for initial rest
screen.show_blank()
logging.info('Starting blank period')

trigger.send("StartBlank")
core.wait(CONF["timing"]["rest"])
trigger.send("EndBlank")


# Cue start of the experiment
screen.show_cue("START")
trigger.send("Start")
core.wait(CONF["timing"]["cue"])

##########################################################################

#################
# Main experiment
#################

sequence_number = 0
mainTimer = core.CountdownTimer(CONF["task"]["duration"])

while mainTimer.getTime() > 0:
    # log
    sequence_number += 1
    datalog["trialID"] = trigger.sendTriggerId()
    logging.info('Starting iteration #%s', sequence_number)

    ###############################
    # Wait a random period of time

    delay = random.uniform(
        CONF["fixation"]["minDelay"], CONF["fixation"]["maxDelay"])

    # log
    datalog["sequence_number"] = sequence_number
    datalog["delay"] = delay
    logging.info('Starting delay of %s seconds', delay)

    # start
    delayTimer = core.CountdownTimer(delay)
    screen.show_fixation_box()

    extraKeys = []
    while delayTimer.getTime() > 0:

        # Record any extra key presses during wait
        extraKey = kb.getKeys()
        if extraKey:
            quitExperimentIf(extraKey[0].name == 'q')
            trigger.send("BadResponse")
            extraKeys.append(mainClock.getTime())

            # Flash the fixation box to indicate unexpected key press
            screen.flash_fixation_box(CONF["task"]["earlyColor"])
            core.wait(CONF["fixation"]["errorFlash"])
            screen.flash_fixation_box(CONF["fixation"]["boxColor"])

        core.wait(0.0005)

    datalog["extrakeypresses"] = extraKeys
    scorer.scores["extraKeys"] += len(extraKeys)


    #######################
    # Stimulus presentation

    eyetracker.send_trigger("Stim", {"ISI": delay, "ID": sequence_number})
    
    # initialize stopwatch
    Timer = core.Clock()
    keys = []
    missed = False

    # run stopwatch
    screen.window.callOnFlip(onFlip)
    screen.start_countdown()
    while not keys:
        keys = kb.getKeys(waitRelease=False)
        screen.draw_counter(Timer.getTime())
        screen.window.flip()

        # end if no answer comes in time
        if Timer.getTime() > CONF["task"]["warningTime"]:
            missed = True
            break
        elif keys:
            trigger.send("Response")
            eyetracker.send_trigger("Response", {"ID": sequence_number})

    #########
    # Outcome

    if missed:

        # play alarm to wake participant up
        alarmTime = mainClock.getTime()
        trigger.send("ALARM")
        eyetracker.send_trigger("Alarm")
        alarm.play()
        core.wait(2)

        # log
        logging.warning("participant fell asleep")
        datalog["missed"] = True
        datalog["alarmTime"] = alarmTime
        scorer.scores["missed"] += 1

    else:
        # show result
        reactionTime = keys[0].rt
        screen.show_result(reactionTime)
        core.wait(CONF["fixation"]["scoreTime"])

        # exit if asked
        quitExperimentIf(keys[0].name == 'q')

        # save to memory
        datalog["rt"] = reactionTime
        datalog["response_key"] = keys[0].name
        if reactionTime > CONF["task"]["maxTime"]:
            datalog["late"] = True
            scorer.scores["late"] += 1
        elif reactionTime > CONF["task"]["minTime"]:
            scorer.newRT(reactionTime)

    # save data to file
    datalog.flush()

###########
# Concluion

# End main experiment
screen.show_cue("DONE!")
trigger.send("End")
core.wait(CONF["timing"]["cue"])

# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')

trigger.send("StartBlank")
core.wait(CONF["timing"]["rest"])
trigger.send("EndBlank")


logging.info('Finished')
scorer.getScore()
trigger.reset()
eyetracker.stop_recording()

if CONF["playReminder"]:
    questionnaireReminder.play()
    core.wait(2)
