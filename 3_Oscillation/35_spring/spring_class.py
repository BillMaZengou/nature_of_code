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

class Spring(object):
    """docstring for Spring."""

    def __init__(self, origin, end_pos, rest_length, spring_constant):
        super(Spring, self).__init__()
        self.origin = origin
        self.end_pos = end_pos
        self.rest_length = rest_length
        self.spring_constant = spring_constant

    def springForce(self):
        self.displacement = self.end_pos - self.origin
        self.current_len = np.linalg.norm(self.displacement)
        self.force_dir = self.displacement / self.current_len
        self.extension = self.current_len - self.rest_length
        return -self.spring_constant*self.extension * self.force_dir

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
root.title("Spring")
mouse = Mouse(np.zeros(2))
canvas.bind("<Button-1>", mouse.position)
canvas.pack()

"""
Basic
"""
origin = np.array([WIDTH/2, 0])
ball_pos = origin.copy() + np.array([0, HEIGHT/2])

"""
Elasticity
"""
k = 0.1
displacement = ball_pos-origin
rest_length = np.linalg.norm(displacement)
# initial_extension = np.array([0, 10])
# ball_pos += initial_extension

"""
Initialisation
"""
ball = Ball(ball_pos, 5)
spring = Spring(origin, ball_pos, rest_length, k)

"""
Gravity
"""
g = 0.9
def gravity(mass, gravitational_acc, dir=np.array([0, 1])):
    return mass*gravitational_acc * dir

F_g = gravity(ball.mass, g)

"""
Wind
"""
wind = np.array([1., 0])*20

"""
Drag
"""
C = 0.5 * 0.03
def drag(vel, C, rho=1, A=1):
    v_mag_square = sum(vel**2)
    if np.linalg.norm(vel) < 0.000001:
        drag = np.zeros_like(vel)
    else:
        drag = -rho * A * v_mag_square * C * np.divide(vel, np.linalg.norm(vel))
    return drag

"""
Friction
"""
mu = 0.001
def friction(vel, mu):
    f = vel
    if np.linalg.norm(f) < 0.000001:
        f = np.zeros_like(vel)
    else:
        f = - mu * np.divide(f, np.linalg.norm(f))
    return f

while True:
    canvas.create_line(origin[0], origin[1], ball.loc[0], ball.loc[1], fill='black')
    x0, y0, x1, y1 = ball.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")

    spring_force = spring.springForce()
    ball.applyForce(spring_force)
    ball.applyForce(F_g)
    if mouse.pos[0] != 0:
        ball.applyForce(wind)
    vel = ball.vel.copy()
    air_resistance = drag(vel, C) + friction(vel, mu)
    if air_resistance.any() != 0.0:
        ball.applyForce(air_resistance)

    ball.next()
    mouse.clear()
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
