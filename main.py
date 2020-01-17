import logging
import os
import random
import time
import sys

from screen import Screen
from scorer import Scorer
from trigger import Trigger
from psychopy import core, event, sound
from psychopy.hardware import keyboard

from datalog import Datalog
from config.configPVT import CONF

#########################################################################

# Initialize screen, logger and inputs
logging.basicConfig(
    level=CONF["loggingLevel"],
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

screen = Screen(CONF)
datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["task"]["name"]), CONF=CONF)  # This is for saving data
kb = keyboard.Keyboard()
mainClock = core.MonotonicClock()  # starts clock for timestamping events
Alarm = sound.Sound(os.path.join('sounds', CONF["instructions"]["alarm"]), secs=0.01, sampleRate=44100,
                    stereo=True)  # TODO: make it alarm-like
scorer = Scorer()
trigger = Trigger(CONF["trigger"]["serial_device"], CONF["sendTriggers"], CONF["trigger"]["labels"])

logging.info('Initialization completed')

#########################################################################


def quitExperimentIf(toQuit):
    "Quit experiment if condition is met"

    if toQuit:

        scorer.getScore()
        logging.info('quit experiment')
        trigger.send("Quit")
        trigger.reset()
        sys.exit(2)

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

# Blank screen for initial rest
screen.show_blank()
logging.info('Starting blank period')

trigger.send("StartBlank")
core.wait(CONF["timing"]["rest"])
trigger.send("EndBlank")

# import sys
# sys.exit(1)

# Cue start of the experiment
screen.show_cue("START")
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
    trigger.send("Start")

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

    #########
    # Outcome

    if missed:   

        # play alarm to wake participant up
        alarmTime = mainClock.getTime()
        trigger.send("ALARM")
        Alarm.play()


        # log
        logging.info("participant fell asleep")
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