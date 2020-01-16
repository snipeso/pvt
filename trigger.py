import serial
import time


class Trigger:
    def __init__(self, serial_device, labels={}):
        self._port = serial.Serial(serial_device)
        self._delay = 0.01
        self._labels = labels

    def write(self, n):
        self._port.write([n])
        time.sleep(self._delay)

    def send_trigger(self, name):
        self.write(self._labels[name])

    def reset(self):
        self.write(0xFF)


# t = Trigger("/dev/ttyUSB0", {
#     "start": 0x01,
#     "end": 0x02
# })

# t.send_trigger("start")