from psychopy import visual, core, event


class Screen:
    def __init__(self, CONF):
        self.CONF = CONF
        self.window = visual.Window(
            size=CONF["screen"]["size"],
            color=CONF["screen"]["color"],
            monitor=CONF["screen"]["monitor"],
            fullscr=CONF["screen"]["full"], units="norm")

        # Setup fixation cross
        self.fixation_cross = visual.TextStim(self.window, text="+")

        # Setup word and tasks
        self.word = visual.TextStim(self.window)
        self.task_before = visual.TextStim(self.window,
                                           text="before",
                                           pos=[-.3, 0],
                                           height=.3)

        self.task_after = visual.TextStim(self.window,
                                          text="after",
                                          pos=[.3, 0],
                                          height=.2)

    def show_fixation_cross(self):
        self.fixation_cross.draw()
        self.window.flip()

    def show_planning(self, word):
        self.task_before.color = "red"
        self.task_before.draw()
        self.task_after.color = "blue"
        self.task_after.draw()
        self.word.setText(word.upper())
        self.word.draw()
        self.window.flip()

    def show_thinking(self):
        self.task_before.color = "green"
        self.task_before.draw()
        self.task_after.color = "brown"
        self.task_after.draw()
        self.word.draw()
        self.window.flip()

    def show_victory(self, word):
        self.word.setText(word.upper())
        self.word.draw()
        self.window.flip()
