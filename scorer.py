class Scorer:
    def __init__(self):
        self.scores = {
            "missed": 0,
            "late": 0,
            "RTsum": 0,
            "tot": 0,
            "extraKeys": 0,
            "min": 1000,
            "max": 0
        }

    def getScore(self):
        print("+++++++++++++++++++++++++++++++++++++++++++")
        for key in self.scores.keys():
            if key == "RTsum":
                continue

            self._printScore(key, self.scores[key])
        if self.scores["RTsum"] == 0:
            meanRT = 0
        else:
            meanRT = self.scores["RTsum"]/self.scores["tot"]
        print('Mean RT: ', meanRT)  #
        print("+++++++++++++++++++++++++++++++++++++++++++")

    def _printScore(self, name, score):
        print(name, score)

    def newRT(self, reactionTime):
        self.scores["RTsum"] += reactionTime
        self.scores["tot"] += 1
        self.scores["min"] = min(self.scores["min"], reactionTime)
        self.scores["max"] = max(self.scores["max"], reactionTime)
