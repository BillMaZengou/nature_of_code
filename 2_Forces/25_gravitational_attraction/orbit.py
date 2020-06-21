import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 600

class Mover(object):
    """docstring for Mover."""

    def __init__(self, loc, mass, vel=np.zeros(2)):
        super(Mover, self).__init__()
        self.loc = loc
        self.mass = mass
        self.vel = vel
        self.radius = self.mass * 10
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
sun = Mover(sun_pos, 5)
planets = []

for i in range(8):
    planet_pos = np.array([WIDTH/np.random.uniform(3, 10), HEIGHT/np.random.uniform(3, 10)])
    planet = Mover(planet_pos, np.random.uniform(0.5, 3), vel=np.array([np.random.uniform(0.5, 2.5),0.0]))
    planets.append(planet)

while True:
    x0, y0, x1, y1 = sun.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")

    for star in planets:
        x0, y0, x1, y1 = star.display()
        canvas.create_oval(x0, y0, x1, y1, fill="gray", outline="black")

        distance, direction = r(sun, star)

        if distance < sun.dis:
            gravity = np.zeros_like(direction)
        else:
            gravity = G * sun.mass * star.mass * direction / distance
        star.applyForce(gravity)
        star.next()

    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
