import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400
VEL_LIMIT = 1.0

class Mover(object):
    """docstring for Mover."""

    def __init__(self, radius):
        super(Mover, self).__init__()
        self.radius = radius
        self.loc = np.random.random(2)
        self.vel = np.zeros(2)
        self.acc = np.zeros(2)

        self.loc[0] = self.loc[0] * WIDTH
        self.loc[1] = self.loc[1] * HEIGHT

    def next(self):
        self.vel += self.acc
        self.loc += self.vel

        if self.vel.all() > VEL_LIMIT:
            self.vel = np.array([VEL_LIMIT, VEL_LIMIT])

    def checkEdge(self):
        if self.loc[0] > WIDTH:
            self.loc[0] = 0
        elif self.loc[0] < 0:
            self.loc[0] = WIDTH

        if self.loc[1] > HEIGHT:
            self.loc[1] = 0
        elif self.loc[1] < 0:
            self.loc[1] = HEIGHT

    def display(self):
        dis_sq = self.radius**2 / 2
        dis = np.sqrt(dis_sq)
        x0 = self.loc[0] - dis
        y0 = self.loc[1] - dis
        x1 = self.loc[0] + dis
        y1 = self.loc[1] + dis
        return x0, y0, x1, y1


class Mouse(object):
    """docstring for Motion."""

    def __init__(self, pos):
        super(Mouse, self).__init__()
        self.pos = pos

    def position(self, event):
        self.pos[0] = event.x
        self.pos[1] = event.y

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Tracing Ball")
canvas.pack()
mover1 = Mover(50)
mouse = Mouse(np.zeros(2))
root.bind('<Motion>', mouse.position)

while True:
    x0, y0, x1, y1 = mover1.display()
    canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")
    mover1.acc = (mouse.pos - mover1.loc) / np.linalg.norm(mouse.pos - mover1.loc)
    mover1.acc *= 0.1
    mover1.next()
    mover1.checkEdge()

    root.update()
    canvas.delete("all")
time.sleep(0.01)
root.mainloop()
