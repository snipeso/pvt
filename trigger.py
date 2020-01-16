import serial
import time
import logging


class Trigger:
    def __init__(self, serial_device, labels={}):
        logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s-%(levelname)s-%(message)s',
        )  # This is a log for debugging the script, and prints messages to the terminal

        self._delay = 0.01
        self._labels = labels
        
        try:
            self._port = serial.Serial(serial_device)
            
        except:
            logging.warning("NO USB THINGY FOR TRIGGERS!")

    def _write(self, n):
        self._port._write([n])
        time.sleep(self._delay)
       

    def send_trigger(self, name):
        try:
            self._write(self._labels[name])
        except:
            logging.info("pretend sent trigger %s", name)

    def reset(self):
        self._write(0xFF)


# t = Trigger("/dev/ttyUSB0", {
#     "start": 0x01,
#     "end": 0x02
# })

# t.send_trigger("start")