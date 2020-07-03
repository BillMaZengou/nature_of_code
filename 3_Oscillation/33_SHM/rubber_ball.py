import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 600

class Ball(object):
    """docstring for Mover."""

    def __init__(self, loc, mass, amplitude=0, period=0, vel=np.zeros(2)):
        super(Ball, self).__init__()
        self.loc = loc
        self.mass = mass
        self.amplitude = amplitude
        self.period = period
        self.vel = vel
        self.radius = self.mass * 2
        self.acc = np.zeros(2)
        self.dis = np.sqrt(self.radius**2/2)
        self.displacement = 0
        self.frequency = 1 / self.period

    # Newton 2nd Law
    def applyForce(self, force):
        self.f = force.copy() / self.mass
        self.acc += self.f

    def next(self):
        self.vel += self.acc
        self.loc += self.vel

        self.displacement = self.amplitude * np.sin(time.time()*self.frequency*np.pi)
        print(self.displacement)
        self.loc[1] += self.displacement
        self.acc = np.zeros(2)

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("SHM")
canvas.pack()

amplitude = 5
period = 0.5
centre = np.array([WIDTH/2, HEIGHT/2])
ball_pos = centre.copy() + np.array([0, 10])
ball = Ball(ball_pos, 10, amplitude, period)

while True:
    canvas.create_line(centre[0], centre[1], ball.loc[0], ball.loc[1], fill='black')
    x0, y0, x1, y1 = ball.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")
    ball.next()
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
