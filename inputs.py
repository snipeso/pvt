import sys
import time
from psychopy import event
from psychopy.hardware import keyboard


class Input:
    def __init__(self, CONF):
        self.CONF = CONF
        self.kb = keyboard.Keyboard()
        self.mouse = event.Mouse()

    def get_keys(self):
        return self.kb.getKeys()

    # def wait_for_input(self):
    #     direction = None
    #     trigger_count = 0

    #     while not direction or trigger_count < self.CONF["trigger_timing"]["resting"]:
    #         # Checks keyboard input
    #         for thisKey in event.getKeys():
    #             if thisKey in self.CONF["keys"]["before"]:
    #                 direction = "before"
    #             elif thisKey in self.CONF["keys"]["after"]:
    #                 direction = "after"
    #             elif thisKey == "escape":
    #                 sys.exit(1)
    #             elif thisKey == "5":
    #                 trigger_count += 1

    #         # If no keyboard input, checks network input
    #         if not direction:
    #             prediction = self._get_classifier_input(block=False)
    #             if prediction:
    #                 prediction = float(prediction)
    #                 if abs(prediction) <= self.CONF['classifier']['acceptance_treshold']:
    #                     return 'prediction_below_treshold'
    #                 return 'before' if prediction < 0 else 'after'

    #         # waits 1/100 of a sec and checks again
    #         time.sleep(0.01)
    #     return direction
