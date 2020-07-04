import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 600

class Ball(object):
    """docstring for Mover."""

    def __init__(self, origin, len, mass, angle=0, vel=np.zeros(2)):
        super(Ball, self).__init__()
        self.origin = origin
        self.len = len
        self.mass = mass
        self.vel = vel
        self.angle = angle
        self.ang_vel = 0.0
        self.ang_acc = 0.0
        self.radius = self.mass * 2
        self.acc = np.zeros(2)
        self.dis = np.sqrt(self.radius**2/2)

        self.loc = location(self.origin, self.len, self.angle)

    # Newton 2nd Law
    def applyForce(self, force):
        self.f = force.copy() / self.mass
        self.acc += self.f

    def next(self, g, b):
        self.vel += self.acc
        self.loc += self.vel

        self.ang_acc = -g * np.sin(self.angle) / self.len - b * self.ang_vel
        self.ang_vel += self.ang_acc
        self.angle += self.ang_vel
        self.loc = location(self.origin, self.len, self.angle)
        self.acc = np.zeros(2)

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
root.title("Pendulum")
canvas.pack()

angle = np.pi/4
g = 0.5
b = 0.001

origin = np.array([WIDTH/2, 0])
ball_pos = origin.copy() + np.array([0, HEIGHT/2])

length = np.linalg.norm(ball_pos-origin)
ball = Ball(origin, length, 10, angle)

while True:
    canvas.create_line(origin[0], origin[1], ball.loc[0], ball.loc[1], fill='black')
    x0, y0, x1, y1 = ball.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")
    ball.next(g, b)
    ball.ang_acc = 0.0
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
