import os
import logging
import json


class UpdateConfig:
    def __init__(self, CONF={}):

        # convert versions
        CONF = self._selectByVersion(CONF,  CONF["version"])


        # set the logging level
        loggingLevels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "fatal": logging.FATAL
        }

        CONF["loggingLevel"] = loggingLevels[CONF["loggingLevel"]]

        self.CONF = CONF

    def _selectByVersion(self, data, version="main"):
        "Runs through json and selects variables that has multiple options for different versions."

        if type(data) == dict:
            if "versionMain" in data:
                version = "version" + version[0].upper() + version[1:]
                if version in data:
                    return data[version]
                else:
                    return data["versionMain"]
            else:
                for key in data:
                    data[key] = self._selectByVersion(data[key], version)
        elif type(data) == list:
            for i, elem in enumerate(data):
                data[i] = self._selectByVersion(elem, version)

        return data

    def addContent(self, dictionary):
        "add new keys and values to the CONF"
        self.CONF.update(dictionary)
        self.CONF = self._selectByVersion(self.CONF,  self.CONF["version"])

    def addTriggers(self, triggers):
        "add triggers inside the already existing trigger list"
        for key in triggers.keys():
            self.CONF["trigger"]["labels"][key] = triggers[key]

    def getConfig(self):
        return self.CONF
