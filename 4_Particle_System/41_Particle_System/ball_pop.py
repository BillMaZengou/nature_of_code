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
        self.hp = 200
        self.alive = True

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

    def dying(self):
        if self.hp > 0:
            self.hp -= 2
        else:
            self.alive = False

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
Geometry
"""
def rotation(angle):
    radian = angle*np.pi/180
    return np.array([[np.cos(radian), -np.sin(radian)],
                    [np.sin(radian), np.cos(radian)]])

"""
Basic
"""
WIDTH = 600
HEIGHT = 600

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Pop")
mouse = Mouse(np.zeros(2))
canvas.bind("<Button-1>", mouse.position)
canvas.pack()

origin = np.array([WIDTH/2, HEIGHT/3])

"""
Gravity
"""
def gravity(mass, gravitational_acc, dir=np.array([0, 1])):
    return mass*gravitational_acc * dir

"""
Thrust
"""
def thrust(magnitude, angle=0):
    return rotation(angle)@np.array([1., 0.])*magnitude

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
ball = Particle(mass=5, I=0, loc=origin, vel=np.zeros(2), ang=0, ang_vel=0)
Id = id(ball)
F_g = gravity(ball.mass, gravitational_acc=0.1)
F_w = thrust(20, angle=0)
F_thrust = thrust(10, angle=-90+np.random.uniform(-100, 100))

ball.applyForce(F_thrust)
while True:
    if Id != 0:
        if ball.alive == True:
            x0, y0, x1, y1 = ball.display()
            color = '#' + hex(255-ball.hp)[-2:] * 3
            canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)
            ball.applyForce(F_g)

            if mouse.pos[0] != 0.0:
                ball.applyForce(F_w)
            vel = ball.vel.copy()
            air_resistance = drag(vel) + friction(vel)
            if air_resistance.any() != 0.0:
                ball.applyForce(air_resistance)
            ball.next()
            ball.dying()
        else:
            Id = 0
            del ball
    else:
        continue

    mouse.clear()
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
