import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 600

class Pendulum(object):
    """docstring for Mover."""

    def __init__(self, origin, len, mass, angle=0):
        super(Pendulum, self).__init__()
        self.origin = origin
        self.len = len
        self.mass = mass
        self.angle = angle
        self.ang_vel = 0.0
        self.ang_acc = 0.0
        self.radius = self.mass * 2
        self.dis = np.sqrt(self.radius**2/2)

        self.loc = location(self.origin, self.len, self.angle)

    def next(self, g, b):
        self.ang_acc = -g * np.sin(self.angle) / self.len - b * self.ang_vel
        self.ang_vel += self.ang_acc
        self.angle += self.ang_vel
        self.loc = location(self.origin, self.len, self.angle)

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

def location(O, r, theta):
    return np.array([r*np.sin(theta), r*np.cos(theta)]) + O

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Double Pendulum")
canvas.pack()

ang_1 = np.pi/4
ang_2 = np.pi/20
g = 0.5
b = 0.001

origin = np.array([WIDTH/2, 0])
p1_pos = origin.copy() + np.array([0, HEIGHT/3])
p2_pos = p1_pos.copy() + np.array([0, HEIGHT/3])

l1 = np.linalg.norm(p1_pos-origin)
l2 = np.linalg.norm(p2_pos-p1_pos)
p1 = Pendulum(origin, l1, 10, ang_1)
p2 = Pendulum(p1_pos, l2, 10, ang_1+ang_2)

while True:
    canvas.create_line(origin[0], origin[1], p1.loc[0], p1.loc[1], fill='black')
    p1_x0, p1_y0, p1_x1, p1_y1 = p1.display()
    canvas.create_oval(p1_x0, p1_y0, p1_x1, p1_y1, fill="orange", outline="black")
    canvas.create_line(p1.loc[0], p1.loc[1], p2.loc[0], p2.loc[1], fill='black')
    p2_x0, p2_y0, p2_x1, p2_y1 = p2.display()
    canvas.create_oval(p2_x0, p2_y0, p2_x1, p2_y1, fill="orange", outline="black")
    p1.next(g, b)
    p2.next(g, b)
    p1.ang_acc = 0.0
    p2.ang_acc = 0.0
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
