from psychopy import visual, core, event
from psychopy.hardware import keyboard


class Screen:
    def __init__(self, CONF):
        self.CONF = CONF
        self.window = visual.Window(
            size=CONF["screen"]["size"],
            color=CONF["screen"]["color"],
            monitor=CONF["screen"]["monitor"],
            fullscr=CONF["screen"]["full"], units="norm")

        # Setup fixation box
        self.fixation_box = visual.Rect(
            self.window, height=CONF["fixation"]["height"],
            width=CONF["fixation"]["width"],
            fillColor=CONF["fixation"]["fillColor"],
            lineColor=CONF["screen"]["color"],
            units=CONF["screen"]["units"])

        # Setup word and tasks
        self.cue = visual.TextStim(self.window)
        self.task_before = visual.TextStim(self.window,
                                           text="before",
                                           pos=[-.3, 0],
                                           height=.3)

        self.task_after = visual.TextStim(self.window,
                                          text="after",
                                          pos=[.3, 0],
                                          height=.2)

        # setup overview info
        self.task = visual.TextStim(self.window,
                                    text=CONF["task"]["name"],
                                    # alignHoriz="center",
                                    # anchorHoriz="center",  # TODO: get Simone's help
                                    # alignText="center",
                                    height=.3,
                                    )
        self.session = visual.TextStim(self.window,
                                       text="P" + CONF["participant"] +
                                       " Session " + CONF["session"],
                                       # anchorHoriz="center", TODO: get Simone's help
                                       # alignText="center",
                                       pos=[0, -.3],
                                       height=.1,
                                       )
        # self.counter = visual.TextBox(self.window,
        #                               font_size=2, font_color="red",
        #                               size=(.5, .5),
        #                               pos=(0.0, .5),
        #                               units="norm") TODO: get Simone to help
        self.counter = visual.TextStim(self.window)
        self.kb = keyboard.Keyboard()
        self.instructions = visual.TextStim(
            self.window, text=CONF["instructions"]["text"], height=.05)

        self.startPrompt = visual.TextStim(
            self.window, text=CONF["instructions"]["startPrompt"], height=0.05, pos=[0, -.3])

    def show_overview(self):
        self.task.draw()
        self.session.draw()
        self.window.flip()

    def show_instructions(self):
        self.instructions.draw()
        self.startPrompt.draw()
        self.window.flip()

    def show_blank(self):
        self.window.flip()

    def show_cue(self, word):
        self.cue.setText(word)
        self.cue.draw()
        self.window.flip()

    def show_fixation_box(self):
        self.fixation_box.draw()
        self.window.flip()

    def flash_fixation_box(self, color):
        self.fixation_box.fillColor = color
        self.fixation_box.draw()
        self.window.flip()

    def start_countdown(self):
        self.counter.color = "white"
        self.counter.setText("0")
        self.counter.draw()
        self.window.flip()  # TODO: Here, run script for trigger and saving start time

    def show_countdown(self, time):
        # mainClock.getTime()
        self.counter.setText(str(round(1000*time)))
        self.counter.draw()
        self.window.flip()

    def show_result(self, time):
        # presses[0].rt
        speed = round(1000*time)
        self.counter.setText(str(speed))
        if speed < self.CONF["task"]["minTime"]:
            self.counter.color = self.CONF["task"]["earlyColor"]
        elif speed < self.CONF["task"]["maxTime"]:
            self.counter.color = self.CONF["task"]["victoryColor"]
        else:
            self.counter.color = self.CONF["task"]["lateColor"]
        self.counter.draw()
        self.window.flip()

    def stopwatch(self):
        # keys = kb.getKeys()  # , waitDuration=True

        # if button is pressed, show white
        presses = []  # TODO: make it clear cache?
        while len(presses) < 1:
            presses = self.kb.getKeys(waitRelease=True)
            # 1

        # 2

        core.wait(2)
