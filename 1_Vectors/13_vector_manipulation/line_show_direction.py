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
        self.unit_vector = np.zeros_like(self.pos)

    def movment(self, event):
        self.pos[0] = event.x
        self.pos[1] = event.y

def magnitude(vec):
    return np.sqrt(vec[0]**2 + vec[1]**2)

def normalization(vec):
    mag = magnitude(vec)
    return vec / mag

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Lines")
canvas.pack()
origin = np.array([WIDTH/2., HEIGHT/2.])
line_pos = Motion(np.zeros(2))
root.bind('<Motion>', line_pos.movment)
while True:
    lines = line_pos.pos - origin
    unit_line = normalization(lines) * 50  # factor 50 for display
    plot_unit_line = origin + unit_line
    canvas.create_line(origin[0], origin[1], plot_unit_line[0], plot_unit_line[1])
    root.update()
    canvas.delete("all")
    time.sleep(0.01)

root.mainloop()
