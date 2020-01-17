import serial
import time
import logging


class Trigger:
    def __init__(self, serial_device, shouldTrigger, labels={}):

        self._delay = 0.01
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
        # TODO: if name not in list, throw error
        self._write(self._labels[name])

    def reset(self):
        self._write(0xFF)
