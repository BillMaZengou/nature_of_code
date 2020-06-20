import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400

class Mover(object):
    """docstring for Mover."""

    def __init__(self, radius):
        super(Mover, self).__init__()
        self.radius = radius
        self.loc = np.array([WIDTH/2, HEIGHT/2])
        self.vel = np.zeros(2)
        self.acc = np.zeros(2)

        self.dis = np.sqrt(self.radius**2 / 2)

    # Newton 2nd Law
    def addForce(self, force):
        self.acc += force

    def next(self):
        self.vel += self.acc
        self.loc += self.vel
        self.acc = np.zeros(2)

    def checkEdge(self):
        if (self.loc[0]+self.dis) > WIDTH or (self.loc[0]-self.dis) < 0:
            self.vel[0] = -self.vel[0]

        if (self.loc[1]+self.dis) > HEIGHT or (self.loc[1]-self.dis) < 0:
            self.vel[1] = -self.vel[1]

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

class Mouse(object):
    """docstring for Motion."""

    def __init__(self, pos):
        super(Mouse, self).__init__()
        self.pos = pos

    def position(self, event):
        self.pos[0] = event.x
        self.pos[1] = event.y

    def clear(self):
        self.pos = np.zeros_like(self.pos)

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Force")
mouse = Mouse(np.zeros(2))
canvas.bind("<Button-1>", mouse.position)
canvas.pack()
mover1 = Mover(20)
gravity = np.array([0, 0.3])
wind = np.array([1, 0])

while True:
    x0, y0, x1, y1 = mover1.display()
    canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")

    mover1.addForce(gravity)
    if mouse.pos[0] != 0:
        mover1.addForce(wind)
    mover1.next()
    mover1.checkEdge()
    mouse.clear()

    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
