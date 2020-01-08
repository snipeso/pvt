import json
import logging
import os
import random
from psychopy import core
from screen import Screen
import inputs
from datalog import Datalog
from configuration import CONF

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

screen.stopwatch()

# Overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])
# Blank screen
screen.show_blank()
# starts clock for timestamping events
mainClock = core.MonotonicClock()
logging.info('Starting experiment clock')

# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

screen.show_cue("START")
core.wait(CONF["timing"]["cue"])

# Main experiment loop
sequence_number = 0
timer = core.CountdownTimer(CONF["task"]["duration"])

while timer.getTime() > 0:
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
    datalog["startDelay"] = mainClock.getTime()
    delay = random.uniform(
        CONF["fixation"]["minDelay"], CONF["fixation"]["maxDelay"])
    datalog["delay"] = delay
    logging.info('Starting delay of %s seconds', delay)

    core.wait(delay)

    # run counter
    # stopwatch(CONF)
    screen.counter()

    datalog.flush()


# Presents simple fixation until the end
logging.info('Showing fixation cross')
screen.show_fixation_box()

logging.info('Quitting')
