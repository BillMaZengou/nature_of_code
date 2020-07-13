import numpy as np
import tkinter as tk
import time

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
    def __init__(self, mass, I, loc, vel, ang=0, ang_vel=0):
        Mass.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.radius = self.mass * 2
        self.dis = np.sqrt(self.radius**2/2)
        self.hp = 100
        self.alive = True
        self.polygon = 0
        self.ifCollide = False
        self.collideDirection = np.zeros(2)

    def display(self):
        x0 = self.loc[0] - self.dis
        y0 = self.loc[1] - self.dis
        x1 = self.loc[0] + self.dis
        y1 = self.loc[1] + self.dis
        return x0, y0, x1, y1

    def dying(self):
        if self.hp > 0:
            self.hp -= 1
        else:
            self.alive = False

class SquareParticle(Particle):
    def __init__(self, mass, I, loc, vel, ang, ang_vel):
        Particle.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.hp = 150
        self.polygon = 1

    def display(self):
        p0 = self.loc + np.array([-self.dis, -self.dis])
        p1 = self.loc + np.array([self.dis, -self.dis])
        p2 = self.loc + np.array([self.dis, self.dis])
        p3 = self.loc + np.array([-self.dis, self.dis])
        return p0, p1, p2, p3

"""
Basic
"""
WIDTH = 1200
HEIGHT = 1200

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Draw Boxes")

mouse = Mouse(np.array([-WIDTH, HEIGHT]))
canvas.bind("<Button-1>", mouse.position)
canvas.pack()

"""
Initialisation
"""
origin = mouse.pos
particle_list = []
while True:
    # print(len(particle_list))
    particle = SquareParticle(mass=10, I=0, loc=origin, vel=np.zeros(2), ang=0, ang_vel=0)
    particle_list.append(particle)
    p0, p1, p2, p3 = particle.display()
    canvas.create_polygon(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], fill="gray", outline="gray")
    root.update()
    for i in range(len(particle_list)-1, 0, -1):
        if particle_list[i].loc[0] == particle_list[i-1].loc[0] and particle_list[i].loc[1] == particle_list[i-1].loc[1]:
            canvas.delete(particle_list[i])
            particle_list.pop(i)

time.sleep(0.01)
root.mainloop()
