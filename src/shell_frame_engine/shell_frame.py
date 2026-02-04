'''
    Created on 16.01.2026

    Welcome to the shell frame engine

    The shell frame module is the core
    of the shell frame engine.
    The idea is to have frame objects
    that can be rendered in a terminal.

    Each frame can have child frames.
    Each frame has hooks that update
    the frame itself automaticly with
    custom provided functions and each
    frame can react to keyboard and
    mouseevents

    To build a shell frame application
    you only need to include the shell
    frame module, create a main_frame
    by using the Frame constructor and
    run the engine

    main_frame = Frame(10,20,0,0)
    engine = Engine()
    engine.run(main_frame)

                Author: Markus Hecker
'''

from shell_frame_engine.engine import *


'''
TODO
0. Make a calibration screen. The user must click on the button and therefore sets the absolute position of everything.
1. Make a button class that takes a callback function and executes it when pressed or after pressed inherit from frame
2. Make a drag class inheriting from frame
---

'''


class Frame:

    def __init__(self, height, width, pos_x = 0, pos_y = 0, border_style = ["╔","╗","╚","╝","║","═"]):
        self.border_style = border_style

        self.height = height
        self.width = width

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.text = ""

        self.frame = []

        self.children = []
        self.system_info = SystemInfo(0,0.0)

        for i in range(0, height):
            self.frame.append([])

        for line in self.frame:
            for i in range(0, width):
                line.append(" ")

    def add(self, frame):
        frame.parent = self
        self.children.append(frame)

    def draw_border(self):

        for line in self.frame:
            line[0] = self.border_style[4]
            line[self.width - 1] = self.border_style[4]

        for i in range(0, self.width):
            self.frame[0][i] = self.border_style[5]
            self.frame[self.height - 1][i] = self.border_style[5]

        # up left corner
        self.frame[0][0] = self.border_style[0]
        # up right corner
        self.frame[0][self.width - 1] = self.border_style[1]
        # down left corner
        self.frame[self.height - 1][0] = self.border_style[2]
        # down right corner
        self.frame[self.height - 1][self.width - 1] = self.border_style[3]

    def _render_text(self):
        text_len = len(self.text)
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i) * (self.width) + (j) < len(self.text) and text_len >= 0:
                    self.frame[i][j] = self.text[i * self.width + j]
                    text_len -= 1

    def render(self):
        self.draw_recursive()

        for line in self.frame:
            for char in line:
                print(char, end="")
            print()

    def draw(self, frame):
        for i in range(0, frame.height):
            for j in range(0, frame.width):
                if frame.pos_y + i < self.height and frame.pos_x + j < self.width:
                    self.frame[frame.pos_y + i][frame.pos_x + j] = frame.frame[i][j]

    def draw_recursive(self):
        if self.border_style:
            self.draw_border()

        self._render_text()

        for child in self.children:
            child.draw_recursive()
            for i in range(0, child.height):
                for j in range(0, child.width):
                    if child.pos_y + i < self.height and child.pos_x + j < self.width:
                        self.frame[child.pos_y + i][child.pos_x + j] = child.frame[i][j]

    def clear(self):
        #print(chr(27) + "[2J")
        print("\033c")
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.frame[i][j] = " "

    # ---- hooks ----
    def update(self, delta):
        pass

    def handle_event(self, event):
        pass

    def update_recursive(self, delta):
        self.update(delta)
        for child in self.children:
            child.update_recursive(delta)

    def handle_event_recursive(self, event):
        self.handle_event(event)
        for child in self.children:
            child.handle_event_recursive(event)


border_style = {"double":["╔","╗","╚","╝","║","═"],
                "single":["┌","┐","└","┘","│","─"]
                }