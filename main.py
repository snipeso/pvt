import logging
import os
import random
import time
import sys

from screen import Screen
from psychopy import core, event, sound
from psychopy.hardware import keyboard

from datalog import Datalog
from config.configPVT import CONF

#########################################################################

# Initialize screen, logger and inputs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

screen = Screen(CONF)
datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["task"]["name"]), CONF=CONF)  # This is for saving data
kb = keyboard.Keyboard()
mainClock = core.MonotonicClock()  # starts clock for timestamping events
Alarm = sound.Sound('600', secs=0.01, sampleRate=44100,
                    stereo=True)  # TODO: make it alarm-like

logging.info('Initialization completed')

#########################################################################

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
    if key[0] == 'q':
        logging.warning('Force quit after instructions')
        sys.exit(1)

# Blank screen for initial rest
screen.show_blank()
logging.info('Starting blank period')

# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

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

    extraKeys = []
    while delayTimer.getTime() > 0:

        # Record any extra key presses during wait
        extraKey = kb.getKeys()
        if extraKey:
            if extraKey[0].name == 'q':
                logging.warning('Forced quit during wait')
                sys.exit(2)

            extraKeys.append(mainClock.getTime())

            # Flash the fixation box to indicate unexpected key press
            screen.flash_fixation_box(CONF["task"]["earlyColor"])
            core.wait(CONF["fixation"]["errorFlash"])
            screen.flash_fixation_box(CONF["fixation"]["fillColor"])

        core.wait(0.0005)

    #######################
    # Stimulus presentation

    # initialize stopwatch
    Timer = core.Clock()
    keys = []
    Skipped = False

    def onFlip():  # TODO: does this go somewhere else?
        kb.clock.reset()
        datalog["startTime"] = mainClock.getTime()
        # TODO: send trigger

    # run stopwatch
    screen.window.callOnFlip(onFlip)
    screen.start_countdown()
    while not keys:
        keys = kb.getKeys(waitRelease=False)
        screen.show_counter(Timer.getTime())
        screen.window.flip()

        # end if no answer comes in time
        if Timer.getTime() > CONF["task"]["warningTime"]:
            Skipped = True
            break

    #########
    # Outcome

    if Skipped:
        # Alarm.play()
        logging.info("participant fell asleep")
        datalog["skipped"] = True

    else:
        # show result
        reactionTime = keys[0].rt
        screen.show_result(reactionTime)
        core.wait(CONF["fixation"]["scoreTime"])

        if keys[0].name == 'q':
            logging.warning('Forced quit during task')
            sys.exit(3)

        # save to memory
        datalog["rt"] = reactionTime
        datalog["response_key"] = keys[0].name

    # save data to file
    datalog["extrakeypresses"] = extraKeys
    datalog.flush()

###########
# Concluion

# End main experiment
screen.show_cue("DONE!")
core.wait(CONF["timing"]["cue"])

# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')
# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

logging.info('Finished')
