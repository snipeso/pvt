from psychopy import visual, core, event
from psychopy.hardware import keyboard
from psychopy.visual import textbox


class Screen:
    def __init__(self, CONF):
        self.CONF = CONF
        self.window = visual.Window(
            size=CONF["screen"]["size"],
            # color=CONF["screen"]["color"],
            display_resolution=CONF["screen"]["resolution"],
            # monitor=CONF["screen"]["monitor"],
            fullscr=CONF["screen"]["full"], units="norm",
            allowGUI=False
        )

        # set up instructions and overview
        self.task = visual.TextStim(self.window,
                                    pos=[0, 0],
                                    text=CONF["task"]["name"],
                                    alignHoriz='center',
                                    alignVert='center',
                                    # anchorHoriz="center",  # TODO: get Simone's help
                                    # alignText="center",
                                    height=.3,
                                    )
        self.session = visual.TextStim(self.window,
                                       text="P" + CONF["participant"] +
                                       " Session " + CONF["session"],
                                       #    anchorHoriz="center",  # TODO: get Simone's help
                                       #    alignText="center",
                                       pos=[0, -.3],
                                       height=.1,
                                       )

        self.instructions = visual.TextStim(
            self.window, text=CONF["instructions"]["text"], height=.05)

        self.startPrompt = visual.TextStim(
            self.window, text=CONF["instructions"]["startPrompt"], height=0.05, pos=[0, -.3])

        self.cue = visual.TextStim(self.window)

        # Setup fixation box
        self.fixation_box = visual.Rect(
            self.window, height=CONF["fixation"]["height"],
            width=CONF["fixation"]["width"],
            fillColor=CONF["fixation"]["fillColor"],
            lineColor=CONF["screen"]["color"],
            units=CONF["screen"]["units"])

        # setup stopwatch
        # self.counter = visual.TextBox(self.window)
        fm = textbox.getFontManager()
        fonts = fm.getFontFamilyStyles()

        self.counter = visual.TextStim(self.window)
        # self.counter = visual.TextBox(window=self.window,
        #                               #   font_size=21,
        #                               text="hello: A B C D E F G H I J",
        #                               font_name=fonts[0][0],
        #                               border_color=[-1, -1, 1],
        #                               grid_color=[-1, 1, -1, 1],
        #                               textgrid_shape=(20, 5),
        #                               #   align_horz='left',
        #                               #   align_vert='bottom',
        #                               grid_stroke_width=1,
        #                               #   textgrid_shape=[20, 4],
        #                               font_color=[1, 1, 1],
        #                               size=(1, 1),
        #                               pos=(0.0, 0),
        #                               grid_horz_justification='center',
        #                               units='norm',
        #                               )

    def show_overview(self):
        # self.counter.draw()
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
        self.counter.setText(str(round(1000*time)))
        self.counter.draw()
        self.window.flip()

    def show_result(self, time):
        # gives different color stimulus depending on result
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
