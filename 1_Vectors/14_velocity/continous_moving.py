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
        self.loc = np.random.random(2)
        self.vel = np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2)])

        self.loc[0] = self.loc[0] * WIDTH
        self.loc[1] = self.loc[1] * HEIGHT

    def next(self):
        self.loc += self.vel

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

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Lines")
canvas.pack()
mover1 = Mover(10)
mover2 = Mover(30)
while True:
    x0, y0, x1, y1 = mover1.display()
    canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")
    mover1.next()
    mover1.checkEdge()

    x0, y0, x1, y1 = mover2.display()
    canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")
    mover2.next()
    mover2.checkEdge()

    root.update()
    canvas.delete("all")
time.sleep(0.01)
root.mainloop()
