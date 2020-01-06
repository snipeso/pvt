import datetime
import json
import collections
import os
import json


class Datalog:
    def __init__(self, OUTPUT_FOLDER, CONF):
        "Initialize Logger"

        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Determines name for output fole
        OUTPUT_FILE_NAME = "{}_{}".format(
            CONF["participant"],
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
        self.path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE_NAME)

        # TODO: auto create output folder

        self.CONF = CONF

        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def flush(self):
        with open("{}.log".format(self.path), "a+") as f:
            json.dump(self.data, f)
            f.write("\n")
            self.data = {}
