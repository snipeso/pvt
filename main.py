import json
import logging
import os
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
screen = Screen(CONF)
datalog = Datalog(OUTPUT_FOLDER='output', CONF=CONF)
inputs = inputs.Input(CONF)
logging.info('Initialization completed')


# Presents simple fixation
screen.show_fixation_cross()
# starts clock for timestamping events
clock = core.Clock()
logging.info('Starting experiment clock')

# Main experiment loop
sequence_number = 0
for _ in range(10):
    # while True:
    # Planning phase
    sequence_number += 1
    logging.info('Starting iteration #%s', sequence_number)

    logging.info('Starting planning phase')
    # logger.data['sequence'] = sequence_number
    # logger.data['time_start_planning'] = clock.getTime()
    screen.show_planning("tricheco")

    datalog["sequence_number"] = sequence_number

    direction = inputs.get_keys()
    datalog["response_key"] = 3

    datalog.flush()
    # logger.append_data()


# Presents simple fixation until the end
logging.info('Showing fixation cross')
screen.show_fixation_cross()

logging.info('Quitting')
