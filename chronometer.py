import time


class Chronometer:
    def __init__(self, name, treshold):
        self.name = name
        self.old = 0
        self.countNOK = 0
        self.countTOT = 0
        self.treshold = treshold

    def lap(self):
        now = time.time()
        diff = now-self.old
        self.countTOT += 1
        if diff > self.treshold and self.countTOT:
            self.countNOK += 1
            freq = self.countNOK / self.countTOT
            print(f'{self.name} took {diff}s. It happened with a frequency of {freq}')
        self.old = now

    # chrono1 = Chronometer("keyboardresponse", 0.001)
    # chrono1.lap()
