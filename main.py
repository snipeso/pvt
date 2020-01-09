import logging
import os
import random
import time
import sys


from screen import Screen
from psychopy import core, event
from psychopy.hardware import keyboard

from datalog import Datalog
from configuration import CONF

#########################################################################

# Initialize screen, logger and inputs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
)

# TODO: load seperate task configuration, and merge the two into the following CONF
screen = Screen(CONF)

datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["task"]["name"]), CONF=CONF)
kb = keyboard.Keyboard()
mainClock = core.MonotonicClock()  # starts clock for timestamping events
logging.info('Initialization completed')

#########################################################################

# Display overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])

# Optionally, display instructions
if CONF["instructions"]["show"]:
    screen.show_instructions()
    key = event.waitKeys()
    if key[0].name == 'q':
        sys.exit(1)

# Blank screen for initial rest
screen.show_blank()
logging.info('Starting blank period')

# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

# Start main experiment
screen.show_cue("START")
core.wait(CONF["timing"]["cue"])

sequence_number = 0
mainTimer = core.CountdownTimer(CONF["task"]["duration"])

sys.exit(4)  # TEMP

while mainTimer.getTime() > 0:

    sequence_number += 1
    logging.info('Starting iteration #%s', sequence_number)

    screen.show_fixation_box()
    datalog["sequence_number"] = sequence_number

    # Wait a random period of time
    delay = random.uniform(
        CONF["fixation"]["minDelay"], CONF["fixation"]["maxDelay"])

    datalog["delay"] = delay
    logging.info('Starting delay of %s seconds', delay)

    delayTimer = core.CountdownTimer(delay)

    # Record any extra key presses
    extraKeys = []
    while delayTimer.getTime() > 0:
        extraKey = kb.getKeys()
        if len(extraKey) > 0:
            if extraKey[0].name == 'q':  # TODO: maybe have this in just one location?
                sys.exit(2)

            # TODO: if i can get the actual keypres time, use RT here instead
            extraKeys.append(mainClock.getTime())

            # Flash the fixation box to indicate unexpected key press
            screen.flash_fixation_box(CONF["task"]["earlyColor"])
            time.sleep(CONF["fixation"]["errorFlash"])
            screen.flash_fixation_box(CONF["fixation"]["fillColor"])

        time.sleep(0.001)
    datalog["extrakeypresses"] = extraKeys

    # initialize stopwatch
    Timer = core.Clock()
    keys = []
    datalog["startTime"] = mainClock.getTime()
    kb.clock.reset()  # TODO: make this happen on first flip

    # run stopwatch
    screen.start_countdown()
    while len(keys) < 1:
        # TODO: maybe new version gets the time of the key press and not time of called function?
        keys = kb.getKeys(waitRelease=False)
        screen.show_countdown(Timer.getTime())

    # show result
    reactionTime = keys[0].rt
    screen.show_result(reactionTime)
    core.wait(CONF["fixation"]["scoreTime"])

    if keys[0].name == 'q':
        sys.exit(3)

    # save to file
    datalog["rt"] = reactionTime
    datalog["response_key"] = keys[0].name
    datalog.flush()

# Start main experiment
screen.show_cue("DONE!")
core.wait(CONF["timing"]["cue"])

# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')
# TODO: send start trigger
core.wait(CONF["timing"]["rest"])
# TODO: send end wait trigger

logging.info('Finished')
