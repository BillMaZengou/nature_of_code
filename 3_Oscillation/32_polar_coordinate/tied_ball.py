import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 600

def rotate(angle):
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

class Ball(object):
    """docstring for Mover."""

    def __init__(self, loc, mass, center, ang=0.0, ang_vel=0.0, ang_acc=0.0):
        super(Ball, self).__init__()
        self.loc = loc
        self.mass = mass
        self.center = center
        self.ang = ang
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc
        self.radius = self.mass * 3
        self.dis = np.sqrt(self.radius**2/2)
        self.rotation = np.eye(2)
        self.new_loc = self.loc.copy()

    def next(self):
        self.new_loc = self.loc.copy()
        self.ang_vel += self.ang_acc
        self.ang += self.ang_vel

        self.rotation = rotate(self.ang)
        self.new_loc = self.rotation@(self.new_loc-self.center) + self.center

    def display(self):
        x0 = self.new_loc[0] - self.dis
        y0 = self.new_loc[1] - self.dis
        x1 = self.new_loc[0] + self.dis
        y1 = self.new_loc[1] + self.dis
        return x0, y0, x1, y1

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Polar")
canvas.pack()

r = 150
ang = 0.0
ang_vel = 0.0
ang_acc = 0.001

centre = np.array([WIDTH/2, HEIGHT/2])
ball_pos = centre.copy()
ball_pos[0] += r
ball = Ball(ball_pos, 10, centre, ang, ang_vel, ang_acc)

while True:
    canvas.create_line(centre[0], centre[1], ball.new_loc[0], ball.new_loc[1], fill='black')
    x0, y0, x1, y1 = ball.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")
    ball.next()

    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
