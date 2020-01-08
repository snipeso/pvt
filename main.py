import json
import logging
import os
import random
import time
from psychopy import core
from screen import Screen
import inputs
from datalog import Datalog
from configuration import CONF
from psychopy.hardware import keyboard


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
)

# Initialize screen, logger and inputs

# TODO: load seperate task configuration, and merge the two into the following CONF
screen = Screen(CONF)
datalog = Datalog(OUTPUT_FOLDER='output', CONF=CONF)
inputs = inputs.Input(CONF)
logging.info('Initialization completed')

# Overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])

# instructions
if CONF["instructions"]["show"]:
    screen.show_instructions()
    core.wait(CONF["instructions"]["duration"])

# Blank screen
screen.show_blank()
# starts clock for timestamping events
kb = keyboard.Keyboard()
mainClock = core.MonotonicClock()
logging.info('Starting experiment clock')

# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

screen.show_cue("START")
core.wait(CONF["timing"]["cue"])

# Main experiment loop
sequence_number = 0
mainTimer = core.CountdownTimer(CONF["task"]["duration"])

while mainTimer.getTime() > 0:
    # while True:
    # Planning phase
    sequence_number += 1
    logging.info('Starting iteration #%s', sequence_number)

    # logger.data['sequence'] = sequence_number
    # logger.data['time_start_planning'] = clock.getTime()
    screen.show_fixation_box()
    datalog["sequence_number"] = sequence_number

    direction = inputs.get_keys()
    datalog["response_key"] = 3

    # logger.append_data()

    # actual experiment:

    # wait a random period of time

    delay = random.uniform(
        CONF["fixation"]["minDelay"], CONF["fixation"]["maxDelay"])
    datalog["delay"] = delay
    logging.info('Starting delay of %s seconds', delay)

    delayTimer = core.CountdownTimer(delay)
    extraKeys = []
    while delayTimer.getTime() > 0:
        # save extra key presses
        extraKey = kb.getKeys()
        if len(extraKey) > 0:
            # TODO: if i can get the actual keypres time, use RT here instead
            extraKeys.append(mainClock.getTime())
            screen.flash_fixation_box(CONF["task"]["earlyColor"])
            time.sleep(0.1)
            screen.flash_fixation_box(CONF["fixation"]["fillColor"])

        time.sleep(0.001)
    datalog["extrakeypresses"] = extraKeys

    # run counter
    Timer = core.Clock()
    keys = []
    datalog["startTime"] = mainClock.getTime()  # maybe remove?
    kb.clock.reset()  # TODO: make this happen on first flip
    screen.start_countdown()
    while len(keys) < 1:
        # TODO: maybe new version gets the time of the key press and not time of called function?
        keys = kb.getKeys()
        screen.show_countdown(Timer.getTime())
    reactionTime = keys[0].rt
    screen.show_result(reactionTime)
    datalog["rt"] = reactionTime
    core.wait(CONF["fixation"]["scoreTime"])

    datalog.flush()


# Presents simple fixation until the end
logging.info('Showing fixation cross')
screen.show_fixation_box()

logging.info('Quitting')
