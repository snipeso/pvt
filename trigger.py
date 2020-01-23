import serial
import time
import logging


class Trigger:
    def __init__(self, serial_device, shouldTrigger, labels={}):
        self.nextTriggerId = 0
        self._delay = 0.01  # TODO: could it be 0.005 ?
        self._labels = labels
        print(shouldTrigger)
        if shouldTrigger:
            self._port = serial.Serial(serial_device)

        self.shouldTrigger = shouldTrigger

    def _write(self, n):
        if self.shouldTrigger:
            self._port.write([n])
            time.sleep(self._delay)
            self._port.write([0x00])
        else:
            print("trigger: ", n)

    def send(self, name):
        trigger = self._labels[name]
        if trigger >= 128:
            raise ValueError("Manual triggers have to be < 128")
        self._write(trigger)

    def reset(self):
        self._write(0xFF)

    def sendTriggerId(self):
        currentId = self.nextTriggerId
        logging.info("triggerId: %s", currentId)
        self.nextTriggerId += 1

        triggers = id2triggers(currentId)
        for trigger in triggers:
            self._write(trigger)

        return {
            "id": currentId,
            "triggers": triggers,
            "duration": len(triggers) * self._delay
        }


BASE = 63  # this because BrainAmp uses 255 for reset; otherwise would have used 64

# What we do: the first digit of a trigger indicates if its a normal trigger(0) or if its part of an ID number (1).
# The second digit indicates if it is one of many (0) or the last number of a trigger ID sequence (1)


def id2triggers(i):
    if i < 0:
        raise ValueError("Ids can only be positive")

    triggers = []

    # split number in base 64
    n = i
    remainder = 0

    while n > 0:
        remainder = n % BASE
        n = n // BASE
        triggers.insert(0, remainder)

    if not triggers:
        triggers = [0]

    # flip leftmost bit to 1

    triggers = [t + 128 for t in triggers]

    # flip the second-to-leftmost bit of the last trigger (byte)
    triggers[-1] += 64

    return triggers


def triggers2id(triggers):

    for pos, trigger in enumerate(triggers):
        if pos == (len(triggers) - 1):
            if not trigger - 128 >= 64:
                raise ValueError("Last trigger is not a terminating trigger")
        else:
            if not trigger - 128 < 64:
                raise ValueError("Non-last trigger is a terminating trigger")

    # filter out triggers that are not part of a id-group
    triggers = filter(lambda x: x >= 128, triggers)

    # flip the leftmost bit back to 0
    triggers = [t - 128 for t in triggers]

    # flip the second-to-leftmost bit back to 0
    triggers = [t % 64 for t in triggers]

    i = 0
    for pos, n in enumerate(reversed(triggers)):
        i += n * BASE ** pos
    return i


class TriggerFinder:
    def __init__(self):
        self._current_triggers = []

    def next(self, trigger):
        self._current_triggers.append(trigger)
        try:
            i = triggers2id(self._current_triggers)
            self._current_triggers = []
            return i
        except ValueError:
            return None


def id2trigger2idTest(i):
    # print(f"i is {i}")
    triggers = id2triggers(i)
    # print(f"Triggers are: {triggers}")
    inew = triggers2id(triggers)
    # print(f"Inew is: {inew}")
    assert i == inew, "i and inew dont match!"


if __name__ == "__main__":
    test_range = [
        0,
        1,
        123,
        1000,
        33,
        43265328652386287,
    ]
    test_range += range(10000)
    [id2trigger2idTest(n) for n in test_range]


#
#
# Binary arithmetic notes

# 1000
# 11 | 001111 10 | 101000
# 001111101000
# 64 ^ 2 * x + 64 ^ 1 * y + 64 ^ 0 * 40

# 1000
# 1000 / 10 -> 100, 0
# 100 / 10 -> 10, 0
# 10 / 10 -> 1, 0
# 1 / 10 -> 0, 1

# 1000 / 64 -> 0, 15
# 40 / 64 -> 0, 40


# 11 | 111110 10 | 001000


# 123
# 10 ^ 2 * 1 + 10 ^ 1 * 2 + 10 ^ 0 * 3
# 64 ^ 2 * x + 64 ^ 1 * y + 64 ^ 0 * z

# 10001010
# 16318421
# 2426
# 8
