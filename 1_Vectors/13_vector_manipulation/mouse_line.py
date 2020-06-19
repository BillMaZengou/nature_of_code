import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400

class Motion(object):
    """docstring for Motion."""

    def __init__(self, pos):
        super(Motion, self).__init__()
        self.pos = pos

    def movment(self, event):
        self.pos[0] = event.x
        self.pos[1] = event.y


root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Lines")
canvas.pack()
origin = np.array([WIDTH/2., HEIGHT/2.])
line_pos = Motion(np.zeros(2))
root.bind('<Motion>', line_pos.movment)
while True:
    canvas.create_line(origin[0], origin[1], line_pos.pos[0], line_pos.pos[1])
    root.update()
    canvas.delete("all")
    time.sleep(0.01)

root.mainloop()
