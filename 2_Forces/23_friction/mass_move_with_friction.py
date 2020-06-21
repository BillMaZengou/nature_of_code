import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400

class Mover(object):
    """docstring for Mover."""

    def __init__(self):
        super(Mover, self).__init__()
        self.mass = np.random.randint(1, 3)
        self.radius = self.mass * 10
        self.loc = np.array([np.random.uniform(10, WIDTH-10), np.random.uniform(10, HEIGHT-50)])
        self.vel = np.zeros(2)
        self.acc = np.zeros(2)

        self.dis = np.sqrt(self.radius**2 / 2)

    # Newton 2nd Law
    def applyForce(self, force):
        self.f = force.copy() / self.mass
        self.acc += self.f

    def next(self):
        self.vel += self.acc
        self.loc += self.vel
        self.acc = np.zeros(2)

    def checkEdge(self):
        if (self.loc[0]+0.5*self.dis) > WIDTH:
            self.loc[0] = self.loc[0] - self.dis
            self.vel[0] = -self.vel[0]
        elif (self.loc[0]-0.5*self.dis) < 0:
            self.loc[0] = self.loc[0] + self.dis
            self.vel[0] = -self.vel[0]

        if (self.loc[1]+0.5*self.dis) > HEIGHT:
            self.loc[1] = self.loc[1] - self.dis
            self.vel[1] = -self.vel[1]
        elif(self.loc[1]-0.5*self.dis) < 0:
            self.loc[1] = self.loc[1] + self.dis
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

gravity = np.array([0, 0.4])
wind = np.array([1., 0])

num_of_movers = 1
movers = []
for i in range(num_of_movers):
    movers.append(Mover())

while True:
    for mover in movers:
        x0, y0, x1, y1 = mover.display()
        canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")

        mover.applyForce(gravity * mover.mass)
        if mouse.pos[0] != 0:
            mover.applyForce(wind)

        mu = 0.01
        friction = mover.vel.copy()
        if np.linalg.norm(friction) < 0.000001:
            friction = np.zeros_like(mover.vel)
        else:
            friction = - mu * np.divide(friction, np.linalg.norm(friction))
        mover.applyForce(friction)

        mover.next()
        mover.checkEdge()
    mouse.clear()

    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
