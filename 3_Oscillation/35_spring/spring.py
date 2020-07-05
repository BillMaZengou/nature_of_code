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

def location(O, r, theta):
    return np.array([r*np.sin(theta), r*np.cos(theta)]) + O

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Spring")
canvas.pack()

g = 0.5
b = 0.001
k = 0.1

origin = np.array([WIDTH/2, 0])
ball_pos = origin.copy() + np.array([0, HEIGHT/2])
displacement = ball_pos-origin
rest_length = np.linalg.norm(displacement)
dir = displacement/rest_length
initial_extension = np.array([0, 10])
ball_pos += initial_extension
ball = Ball(ball_pos, 5)

while True:
    canvas.create_line(origin[0], origin[1], ball.loc[0], ball.loc[1], fill='black')
    x0, y0, x1, y1 = ball.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")
    current_len = np.linalg.norm(ball_pos-origin)
    extension = current_len - rest_length
    spring_force = (-k*extension) * dir
    ball.applyForce(spring_force)
    ball.next()
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
