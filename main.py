import logging
import os
import random
import time
import sys

from screen import Screen
from psychopy import core, event
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
logging.info('Initialization completed')

#########################################################################

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

# Start main experiment
screen.show_cue("START")
core.wait(CONF["timing"]["cue"])


sequence_number = 0
mainTimer = core.CountdownTimer(CONF["task"]["duration"])


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

    # Record any extra key presses during wait
    extraKeys = []
    while delayTimer.getTime() > 0:
        extraKey = kb.getKeys()
        if extraKey:
            if extraKey[0].name == 'q':
                logging.warning('Forced quit during wait')
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
    # kb.clock.reset()  # TODO: make this happen on first flip

    def onFlip():
        kb.clock.reset()
        # TODO: send trigger

    # run stopwatch
    screen.window.callOnFlip(onFlip)
    screen.start_countdown()
    while not keys:
        # TODO: maybe new version gets the time of the key press and not time of called function?
        keys = kb.getKeys(waitRelease=False)
        screen.show_counter(Timer.getTime())
        screen.window.flip()

    # show result
    reactionTime = keys[0].rt
    screen.show_result(reactionTime)
    core.wait(CONF["fixation"]["scoreTime"])

    if keys[0].name == 'q':
        logging.warning('Forced quit during task')
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
