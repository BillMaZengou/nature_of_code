import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 600

class Ball(object):
    """docstring for Mover."""

    def __init__(self, loc, mass, vel=np.zeros(2)):
        super(Ball, self).__init__()
        self.loc = loc
        self.mass = mass
        self.vel = vel
        self.radius = self.mass * 5
        self.acc = np.zeros(2)
        self.dis = np.sqrt(self.radius**2/2)


    # Newton 2nd Law
    def applyForce(self, force):
        self.f = force.copy() / self.mass
        self.acc += self.f

    def next(self):
        self.vel += self.acc
        self.loc += self.vel
        self.acc = np.zeros(2)

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

class Box(object):
    """docstring for Mover."""

    def __init__(self, loc, mass, vel=np.zeros(2), ang=0, ang_vel=0):
        super(Box, self).__init__()
        self.loc = loc
        self.mass = mass
        self.vel = vel
        self.ang = ang
        self.ang_vel = ang_vel

        self.dis = self.mass * 5
        self.acc = np.zeros(2)
        self.ang_acc = 0.0001
        self.rotation = np.eye(2)

    # Newton 2nd Law
    def applyForce(self, force):
        self.f = force.copy() / self.mass
        self.acc += self.f

    def next(self):
        self.vel += self.acc
        self.loc += self.vel
        self.acc = np.zeros(2)

        self.ang_vel += self.ang_acc
        self.ang += self.ang_vel
        # self.aug_acc = 0
        self.rotation = np.array([[np.cos(self.ang), -np.sin(self.ang)], [np.sin(self.ang), np.cos(self.ang)]])

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] - self.dis
        y1 = self.loc[1] + self.dis
        x2 = self.loc[0] + self.dis
        y2 = self.loc[1] + self.dis
        x3 = self.loc[0] + self.dis
        y3 = self.loc[1] - self.dis

        p0 = np.array([x0, y0])
        p1 = np.array([x1, y1])
        p2 = np.array([x2, y2])
        p3 = np.array([x3, y3])

        p0 = self.rotation@(p0-self.loc) + self.loc
        p1 = self.rotation@(p1-self.loc) + self.loc
        p2 = self.rotation@(p2-self.loc) + self.loc
        p3 = self.rotation@(p3-self.loc) + self.loc

        return p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]

def r(M, m):
    M_pos = M.loc.copy()
    m_pos = m.loc.copy()
    r_vec = M_pos - m_pos
    r_mag = np.sqrt(r_vec[0]**2 + r_vec[1]**2)
    r_unit = r_vec / r_mag
    return r_mag, r_unit

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Force")
canvas.pack()

G = 0.5
sun_pos = np.array([WIDTH/2, HEIGHT/2])
sun = Ball(sun_pos, 10)
planets = []

for i in range(8):
    planet_pos = np.array([WIDTH/np.random.uniform(3, 10), HEIGHT/np.random.uniform(3, 10)])
    planet = Box(planet_pos, np.random.uniform(0.5, 3), vel=np.array([np.random.uniform(0.5, 2.5),0.0]))
    planets.append(planet)

while True:
    x0, y0, x1, y1 = sun.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")

    for star in planets:
        x0, y0, x1, y1, x2, y2, x3, y3 = star.display()
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill="gray", outline="black")

        distance, direction = r(sun, star)

        if distance < sun.dis/5.:
            gravity = np.zeros_like(direction)
        else:
            gravity = G * sun.mass * star.mass * direction / distance
        star.applyForce(gravity)
        star.next()

    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
