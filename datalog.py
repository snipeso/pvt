import datetime
import json
import collections
import os
import json
import csv

# Saves data to a file in a session specific folder


class Datalog:
    def __init__(self, OUTPUT_FOLDER, CONF):
        "Initialize Logger"

        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Determines name for output file
        OUTPUT_FILE_NAME = "{}_{}_{}_{}".format(
            CONF["participant"],
            CONF["session"],
            CONF["task"]["name"],
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
        self.path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE_NAME)

        self.CONF = CONF

        # save configuration to a file
        CONF_FILE_NAME = "{}_{}_{}_{}_configuration".format(
            CONF["participant"],
            CONF["session"],
            CONF["task"]["name"],
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))

        with open("{}.log".format(os.path.join(OUTPUT_FOLDER, CONF_FILE_NAME)), "w+") as f:
            json.dump(CONF, f)

        # initialize csv of results
        self.fieldnames = ['sequence_number', 'delay', 'startTime', 'rt', 'response_key']
        with open("{}.csv".format(self.path), mode="w",  newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()

        self.data = {}

    def __setitem__(self, key, value):
        # this magically lets you call the class directly as datalog["newfield"] = newItem
        self.data[key] = value

    def flush(self):
        # save log of everything that happened
        with open("{}.log".format(self.path), mode="a+") as f:
            json.dump(self.data, f)
            f.write("\n")
            
        #save csv of results
        with open("{}.csv".format(self.path), mode="a+",  newline='') as csv_file:
          
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames,  restval='', extrasaction='ignore')
            writer.writerow(self.data)
            self.data = {}
