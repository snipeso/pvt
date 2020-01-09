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
            allowGUI=True
        )

        # set up instructions and overview
        self.task = visual.TextStim(self.window,
                                    # pos=[0, 0],
                                    text=CONF["task"]["name"],
                                    alignHoriz='center',
                                    alignVert='center',
                                    height=.3,
                                    pos=(0, 0),  # TEMP
                                    units="norm"
                                    )
        self.session = visual.TextStim(self.window,
                                       text="P" + CONF["participant"] +
                                       " Session " + CONF["session"],
                                       pos=[.75, -.3],  # TEMP
                                       height=.1,
                                       alignHoriz='center',
                                       alignVert='center',
                                       units="norm"
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

        # self.counter = visual.TextStim(self.window)
        self.counter = visual.TextBox(window=self.window,
                                      #   font_size=21,
                                      #   font_name=fonts[0][0],
                                      # border_color=[-1, -1, 1],
                                      grid_color=[-1, -1, 1],
                                      textgrid_shape=(10, 1),
                                      #   #   align_horz='left',
                                      #   #   align_vert='bottom',
                                      #   grid_stroke_width=1,
                                      #textgrid_shape=[20, 4],
                                      font_color=[1, 1, 1],
                                      size=(1, 1),
                                      #   pos=(0.0, 0),
                                      #   grid_horz_justification='center',
                                      #   units='norm',
                                      font_size=41,
                                      pos=(0, 0.25),
                                      grid_horz_justification='center',
                                      grid_vert_justification='center',
                                      #   units='norm',
                                      )

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
        self.show_counter(0)
        self.set_counter_color("white")
        self.window.flip()  # TODO: Here, run script for trigger and saving start time

    def show_counter(self, time, colored=False):
        speed = round(1000*time)
        text = "{}   ".format(speed)  # hack to show the relevant digits
        self.counter.setText(text)
        if colored:
            if speed < self.CONF["task"]["minTime"]:
                self.set_counter_color(self.CONF["task"]["earlyColor"])
            elif speed < self.CONF["task"]["maxTime"]:
                self.set_counter_color(self.CONF["task"]["victoryColor"])
            else:
                self.set_counter_color(self.CONF["task"]["lateColor"])

        self.counter.draw()
        return speed

    def set_counter_color(self, color):
        self.counter.setFontColor(color)

    def show_result(self, time):
        # gives different color stimulus depending on result
        speed = self.show_counter(time, colored=True)
        # self.counter.setText(str(speed))

        self.counter.draw()
        self.window.flip()
