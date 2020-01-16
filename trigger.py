import serial
import time
import logging


class Trigger:
    def __init__(self, serial_device, labels={}):
        logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s-%(levelname)s-%(message)s',
        )  # This is a log for debugging the script, and prints messages to the terminal

        self._delay = 0.03
        self._labels = labels

        self._port = serial.Serial(serial_device)
        # try:
            
        # except:
        #     logging.warning("NO USB THINGY FOR TRIGGERS!")

    def _write(self, n):
        self._port.write([n])
        time.sleep(self._delay)
        self._port.write([0x00])
       

    def send(self, name):
        #TODO: if name not in list, throw error
            self._write(self._labels[name])
        # try:
        # except:
        #     logging.info("pretend sent trigger %s", name)
        #     raise KeyError

    def reset(self):
        self._write(0xFF)


# t = Trigger("/dev/ttyUSB0", {
#     "start": 0x01,
#     "end": 0x02
# })

# t.send("start")
