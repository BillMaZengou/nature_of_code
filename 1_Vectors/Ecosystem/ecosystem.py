import numpy as np
from tkinter import *
import time

# TODO: Set different rules for different species

WIDTH = 600
HEIGHT = 400
VEL_LIMIT = 1.5

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
        self.acc[0] = np.random.uniform(-0.5, 0.5)
        self.acc[1] = np.random.uniform(-0.5, 0.5)

        self.vel += self.acc
        self.loc += self.vel

        if self.vel.all() > VEL_LIMIT:
            self.vel = np.array([VEL_LIMIT, VEL_LIMIT])

    def checkEdge(self):
        if self.loc[0] > WIDTH or self.loc[0] < 0:
            self.vel[0] *= -1

        if self.loc[1] > HEIGHT or self.loc[1] < 0:
            self.vel[1] *= -1

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
root.title("Ecosystem")
canvas.pack()
movers = [Mover(30), Mover(20), Mover(10), Mover(5), Mover(5), Mover(3), Mover(3), Mover(3),]
while True:
    for i in movers:
        x0, y0, x1, y1 = i.display()
        canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")
        i.next()
        i.checkEdge()

    root.update()
    canvas.delete("all")
time.sleep(0.01)
root.mainloop()
