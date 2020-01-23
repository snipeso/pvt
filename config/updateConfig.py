import os
import logging
import git
import json


class UpdateConfig:
    def __init__(self):

        # start configuration
        CONF = {}

        # find configuration
        CONFIG_SESSION_PATHS = [
            '../configSession.json',
            '~/configSession.json',
            './config/configSession.json',
            './config/configSession_template.json']

        for path in CONFIG_SESSION_PATHS:
            # stop searching once CONF found
            if CONF:
                break

            path = os.path.expanduser(path)
            if not os.path.isfile(path):
                continue

            # load CONF when found
            with open(path, 'r+') as f:
                CONF = json.load(f)

                # log
                logging.info("Taking json config from: %s", path)
                CONF['confJsonPath'] = path

        # convert versions
        CONF = self._selectByVersion(CONF,  CONF["version"])

        # save the git version of the experiment
        repo = git.Repo(search_parent_directories=True)
        CONF["gitHash"] = repo.head.object.hexsha

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
