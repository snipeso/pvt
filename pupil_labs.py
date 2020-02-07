import zmq
import msgpack
import logging
import msgpack as serializer
from time import sleep, time


class PupilCore:
    def __init__(self, ip='127.0.0.1', port=50020, shouldRecord=False, shouldSave=False):
        self._ip = ip
        self._port = port
        self._subscribers = {}
        self.shouldRecord = shouldRecord
        self.shouldSave = shouldSave

        if shouldRecord:
            logging.info("Trying to connect to pupil labs...")
            self._ctx = zmq.Context()
            self._remote = zmq.Socket(self._ctx, zmq.REQ)
            self._remote.connect("tcp://{}:{}".format(self._ip, self._port))

            self._remote.send_string("PUB_PORT")
            pub_port = self._remote.recv_string()
            self._pub_socket = zmq.Socket(self._ctx, zmq.PUB)
            self._pub_socket.connect("tcp://{}:{}".format(self._ip, pub_port))

            # Setup zmq context and remote helper

            # In order for the annotations to be correlated correctly with the rest of
            # the data it is required to change Pupil Capture's time base to this scripts
            # clock. We only set the time base once. Consider using Pupil Time Sync for
            # a more precise and long term time synchronization
            self._time_fn = time  # Use the appropriate time function here

            # Set Pupil Capture's time base to this scripts time. (Should be done before
            # starting the recording)
            self._remote.send_string("T {}".format(self._time_fn()))
            self._remote.recv_string()

            sleep(1.)
        else:
            logging.warning("Not connecting to pupil labs")

    def start_recording(self, filepath):
        if self.shouldRecord:
            self._notify({
                "subject": "start_plugin",
                "name": "Annotation_Capture",
                "args": {}}
            )
            self._remote.send_string("R {}".format(filepath))
            self._remote.recv_string()
        else:
            logging.info("Start recording pupillometry (pretend)")

    def stop_recording(self):
        if self.shouldRecord:  # TODO: in a moment of calm, see if this is necessary
            self._remote.send_string("r")
            self._remote.recv_string()
        else:
            logging.info("Stop recording pupillometry (pretend)")

    def subscribe(self, topic):
        if self.shouldRecord:
            if topic in self._subscribers:
                return self._subscribers[topic]

            sub = self._ctx.socket(zmq.SUB)
            self._remote.send_string('SUB_PORT')
            port = self._remote.recv_string()

            sub.connect('tcp://{}:{}'.format(self._ip, port))
            sub.subscribe(topic)
            self._subscribers[topic] = sub

            return sub
        else:
            return "no sub"

    def _notify(self, notification):
        """LOW LEVEL, Sends ``notification`` to Pupil Remote"""
        topic = "notify." + notification["subject"]
        payload = serializer.dumps(notification, use_bin_type=True)
        self._remote.send_string(topic, flags=zmq.SNDMORE)
        self._remote.send(payload)
        return self._remote.recv_string()

    def send_message(self, msg):
        if self.shouldRecord:
            payload = serializer.dumps(msg, use_bin_type=True)
            self._pub_socket.send_string(msg["topic"], flags=zmq.SNDMORE)
            self._pub_socket.send(payload)

    def send_trigger(self, label, data={}):
        # Send a trigger with the current time

        if self.shouldRecord:
            msg = {
                "topic": "annotation",
                "label": label,
                "timestamp": self._time_fn(),
                "duration": 0,  # TODO: see if it makes sense to make this duration of stim
            }
            msg.update(data)
            self.send_message(msg)
        else:
            print(label, data)

    def getPupildiameter(self):
        if self.shouldRecord and self.shouldSave:
            topic = 'pupil.0'
            sub = self.subscribe(topic)

            topic, payload = sub.recv_multipart()
            message = msgpack.loads(payload)
            # read-out the diameter according to 3D pupil model.
            diam = message[b'diameter_3d']
        else:
            diam = 0

        return diam

# if __name__ == '__main__':
#     pupil = PupilCore(ip='192.168.0.17')
#     pupil.send_trigger('123', {'myfancykey': 99})
