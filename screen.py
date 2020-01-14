from psychopy import visual, core, event, monitors
from psychopy.hardware import keyboard
from psychopy.visual import textbox


class Screen:
    def __init__(self, CONF):
        self.CONF = CONF

        # fetch the most recent calib for this monitor
        mon = monitors.Monitor('tesfgft')
        mon.setWidth(CONF["screen"]["size"][0])
        mon.setSizePix(CONF["screen"]["resolution"])

        self.window = visual.Window(
            size=CONF["screen"]["resolution"],
            # display_resolution=CONF["screen"]["resolution"],
            monitor=mon,
            fullscr=CONF["screen"]["full"],
            # units="cm",
            allowGUI=True
        )

        # set up instructions and overview
        self.task = visual.TextStim(self.window,
                                    pos=[0.7, 0.1],
                                    text=CONF["task"]["name"],
                                    alignHoriz='center',
                                    alignVert='center',
                                    height=.3,
                                    # pos=(0, 0),  # TEMP
                                    units="norm"
                                    )
        self.session = visual.TextStim(self.window,
                                       text="P" + CONF["participant"] +
                                       " Session " + CONF["session"],
                                       pos=[.7, -.2],  # TEMP
                                       height=.1,
                                       alignHoriz='center',
                                       alignVert='center',
                                       units="norm"
                                       )

        self.instructions = visual.TextStim(
            self.window, text=CONF["instructions"]["text"], height=.05, pos=[0.5, 0.1])

        self.startPrompt = visual.TextStim(
            self.window, text=CONF["instructions"]["startPrompt"], height=0.05, pos=[0.5, -0.2])

        self.cue = visual.TextStim(self.window, pos=[0.87, 0])

        # Setup fixation box
        self.fixation_box = visual.Rect(
            self.window, height=CONF["fixation"]["height"],
            width=CONF["fixation"]["width"],
            fillColor=CONF["fixation"]["boxColor"],
            lineColor=CONF["fixation"]["boxColor"],
            units=CONF["screen"]["units"])

        # setup stopwatch
        fm = textbox.getFontManager()
        fonts = fm.getFontFamilyStyles()

        # self.counter = visual.TextStim(self.window)
        self.counter = visual.TextBox(window=self.window,
                                      # border_color=[-1, -1, 1],
                                      ## grid_color=[-1, -1, 1],
                                      ## textgrid_shape=(10, 1),
                                      # grid_stroke_width=1,
                                      # textgrid_shape=[20, 4],
                                      font_color=[1, 1, 1],
                                      size=(1, 1),
                                      font_size=41,
                                      pos=(0.05, 0),
                                      grid_horz_justification='center',
                                      grid_vert_justification='center',
                                      # units='norm',
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
        self.window.flip()

    def show_counter(self, time, colored=False):
        speed = round(1000*time)
        text = "{}   ".format(speed)  # hack to show the relevant digits
        self.counter.setText(text)

        speed = speed/1000
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
