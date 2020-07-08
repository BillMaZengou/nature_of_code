import numpy as np
from tkinter import *
import time

class Mass(object):
    def __init__(self, mass, I, loc, vel, ang, ang_vel):
        super(Mass, self).__init__()
        self.mass = mass
        self.moment_of_inertia = I
        self.loc = loc
        self.vel = vel
        self.acc = np.zeros(2)
        self.ang = ang
        self.ang_vel = ang_vel
        self.ang_acc = 0

    # Newton 2nd Law
    def applyForce(self, force):
        self.f = force.copy() / self.mass
        self.acc += self.f

    # Newton 2nd Law
    def applyTorque(self, torque):
        self.tao = torque.copy() / self.moment_of_inertia
        self.ang_acc += self.tao

    def next(self):
        self.vel += self.acc
        self.loc += self.vel
        self.acc = np.zeros(2)

        self.ang_vel += self.ang_acc
        self.ang += self.ang_vel
        self.ang_acc = 0

class Particle(Mass):
    def __init__(self, mass, I, loc, vel, ang, ang_vel):
        Mass.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.radius = self.mass * 5
        self.dis = np.sqrt(self.radius**2/2)

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
    """docstring for Mouse."""

    def __init__(self, pos):
        super(Mouse, self).__init__()
        self.pos = pos

    def position(self, event):
        self.pos[0] = event.x
        self.pos[1] = event.y

    def clear(self):
        self.pos = np.zeros_like(self.pos)

"""
Basic
"""
WIDTH = 600
HEIGHT = 600

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Spring")
mouse = Mouse(np.zeros(2))
canvas.bind("<Button-1>", mouse.position)
canvas.pack()

origin = np.array([WIDTH/2, 0])
ball_pos = origin.copy() + np.array([0, HEIGHT/2])

"""
Elasticity
"""
displacement = ball_pos-origin
rest_length = np.linalg.norm(displacement)
initial_extension = np.array([0, 500])
ball_pos += initial_extension

"""
Gravity
"""
def gravity(mass, gravitational_acc, dir=np.array([0, 1])):
    return mass*gravitational_acc * dir

"""
Wind
"""
def wind(wind_power, angle=0):
    return np.array([1., 0.])*np.cos(angle)*wind_power

"""
Drag
"""
def drag(vel, C=0.005, rho=1, A=1):
    v_mag_square = sum(vel**2)
    if np.linalg.norm(vel) < 0.000001:
        drag = np.zeros_like(vel)
    else:
        drag = -rho * A * v_mag_square * C * np.divide(vel, np.linalg.norm(vel))
    return drag

"""
Friction
"""
def friction(vel, mu=0.001):
    f = vel
    if np.linalg.norm(f) < 0.000001:
        f = np.zeros_like(vel)
    else:
        f = - mu * np.divide(f, np.linalg.norm(f))
    return f

"""
Initialisation
"""
ball = Particle(mass=5, I=0, loc=ball_pos, vel=np.zeros(2), ang=0, ang_vel=0)
spring = Spring(origin, ball_pos, rest_length, spring_constant=0.1)
F_g = gravity(ball.mass, gravitational_acc=0.9)
F_w = wind(20, 0)

while True:
    canvas.create_line(origin[0], origin[1], spring.end_pos[0], spring.end_pos[1], fill='black')
    x0, y0, x1, y1 = ball.display()
    canvas.create_oval(x0, y0, x1, y1, fill="orange", outline="black")

    F_e = spring.springForce()
    ball.applyForce(F_e)
    ball.applyForce(F_g)
    if mouse.pos[0] != 0.0:
        ball.applyForce(F_w)
    vel = ball.vel.copy()
    air_resistance = drag(vel) + friction(vel)
    if air_resistance.any() != 0.0:
        ball.applyForce(air_resistance)

    ball.next()
    mouse.clear()
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
