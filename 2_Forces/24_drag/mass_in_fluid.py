import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400

class Mover(object):
    """docstring for Mover."""

    def __init__(self):
        super(Mover, self).__init__()
        self.mass = np.random.randint(1, 4)
        self.radius = self.mass * 10
        self.loc = np.array([np.random.uniform(10, WIDTH-10), 10])
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

    def checkEdge(self, gravity):
        if (self.loc[1]+self.dis) > HEIGHT:
            self.vel[1] = 0
            self.applyForce(-gravity)

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

class Liquid(object):
    """docstring for Liquid."""

    def __init__(self, p1, p2, coeff):
        super(Liquid, self).__init__()
        self.p1 = p1
        self.p2 = p2
        self.coeff = coeff

def if_inside(x1_lowest, x2_highest):
    if x1_lowest > x2_highest:
        return True

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Force")
canvas.pack()

gravitational_acc = np.array([0, 0.4])
rho = 1
A = 1

num_of_movers = 8
movers = []
for i in range(num_of_movers):
    movers.append(Mover())

liquid = Liquid(np.array([0, HEIGHT/2]), np.array([WIDTH, HEIGHT]), 0.3)
while True:
    canvas.create_rectangle(liquid.p1[0], liquid.p1[1], liquid.p2[0], liquid.p2[1], fill="lightblue", outline="white")
    for mover in movers:
        x0, y0, x1, y1 = mover.display()
        canvas.create_oval(x0, y0, x1, y1, fill="gray", outline="black")

        mover.applyForce(gravitational_acc * mover.mass)

        condition = if_inside(mover.loc[1]+mover.dis, liquid.p1[1])
        if condition:
            vel = mover.vel.copy()
            v_mag_square = mover.vel[0]**2 + mover.vel[1]**2
            C = 0.5 * liquid.coeff
            if np.linalg.norm(vel) < 0.000001:
                drag = np.zeros_like(mover.vel)
            else:
                drag = - rho * A * v_mag_square * C * np.divide(vel, np.linalg.norm(vel))
            mover.applyForce(drag)

        mover.next()
        mover.checkEdge(gravitational_acc * mover.mass)

    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
