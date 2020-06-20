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

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Lines")
canvas.pack()
mover1 = Mover(20)
force = np.array([0.2, 0.3])
while True:
    x0, y0, x1, y1 = mover1.display()
    canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")

    mover1.addForce(force)
    mover1.next()
    mover1.checkEdge()

    root.update()
    canvas.delete("all")
time.sleep(0.01)
root.mainloop()
