import numpy as np
from tkinter import *
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

class WindSummon(object):
    """docstring for Key."""

    def __init__(self):
        super(WindSummon, self).__init__()
        self.ifWind = False

    def summon(self, event):
        if event.keycode == 119:
            self.ifWind = True

    def hault(self):
        self.ifWind = False

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

"""
0: circle
1: square
2: triangle
3: trapezium
4: star
"""
class Particle(Mass):
    def __init__(self, mass, I, loc, vel, ang=0, ang_vel=0):
        Mass.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.radius = self.mass * 2
        self.dis = np.sqrt(self.radius**2/2)
        self.hp = 100
        self.alive = True
        self.polygon = 0

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

        p0 = rotation(self.ang)@(p0-self.loc) + self.loc
        p1 = rotation(self.ang)@(p1-self.loc) + self.loc
        p2 = rotation(self.ang)@(p2-self.loc) + self.loc
        p3 = rotation(self.ang)@(p3-self.loc) + self.loc
        return p0, p1, p2, p3

class TriangleParticle(Particle):
    def __init__(self, mass, I, loc, vel, ang, ang_vel):
        Particle.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.hp = 80
        self.polygon = 2

    def display(self):
        p0 = self.loc + np.array([0, self.dis])
        p1 = self.loc + np.array([-self.dis * np.sqrt(3)/2, -self.dis/2])
        p2 = self.loc + np.array([self.dis * np.sqrt(3)/2, -self.dis/2])

        p0 = rotation(self.ang)@(p0-self.loc) + self.loc
        p1 = rotation(self.ang)@(p1-self.loc) + self.loc
        p2 = rotation(self.ang)@(p2-self.loc) + self.loc
        return p0, p1, p2

class TrapeziumParticle(Particle):
    def __init__(self, mass, I, loc, vel, ang, ang_vel):
        Particle.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.polygon = 3

    def display(self):
        p0 = self.loc + np.array([-self.dis*4/3, -self.dis])
        p1 = self.loc + np.array([self.dis*4/3, -self.dis])
        p2 = self.loc + np.array([self.dis*2/3, self.dis])
        p3 = self.loc + np.array([-self.dis*2/3, self.dis])

        p0 = rotation(self.ang)@(p0-self.loc) + self.loc
        p1 = rotation(self.ang)@(p1-self.loc) + self.loc
        p2 = rotation(self.ang)@(p2-self.loc) + self.loc
        p3 = rotation(self.ang)@(p3-self.loc) + self.loc
        return p0, p1, p2, p3

class StarParticle(Particle):
    def __init__(self, mass, I, loc, vel, ang, ang_vel):
        Particle.__init__(self, mass, I, loc, vel, ang, ang_vel)
        self.hp = 200
        self.polygon = 4

    def display(self):
        p0 = self.loc + np.array([0, self.dis*4/3])
        p1 = self.loc + np.array([0, self.dis*2/3])
        p1 = rotation(36)@(p1-self.loc) + self.loc
        points = [p0, p1]
        for i in range(2, 10):
            i = rotation(72)@(points[i-2]-self.loc) + self.loc
            points.append(i)

        for point in points:
            point = rotation(self.ang)@(point-self.loc) + self.loc
        return points

class ParticleSystem(object):
    """docstring for ParticleSystem."""

    def __init__(self, origin):
        super(ParticleSystem, self).__init__()
        self.origin = origin
        self.items = []
        self.thrusts = []

    def addUniForce(self, force):
        for item in self.items:
            item.applyForce(force)

    def run(self, canvas):
        loc = self.origin+np.random.random(2)*10
        angle = -90 + np.random.randn()*50
        thrust_mag = np.random.randint(0, 50)
        r = np.random.uniform(0, 1)
        if r < 0.2:
            particle = SquareParticle(mass=10, I=0, loc=loc, vel=np.zeros(2), ang=0, ang_vel=np.random.uniform(-5, 5))
        elif r < 0.4:
            particle = TriangleParticle(mass=10, I=0, loc=loc, vel=np.zeros(2), ang=0, ang_vel=np.random.uniform(-5, 5))
        elif r < 0.6:
            particle = TrapeziumParticle(mass=10, I=0, loc=loc, vel=np.zeros(2), ang=0, ang_vel=np.random.uniform(-5, 5))
        elif r < 0.7:
            particle = StarParticle(mass=10, I=0, loc=loc, vel=np.zeros(2), ang=0, ang_vel=0)
        else:
            particle = Particle(mass=10, I=0, loc=loc, vel=np.zeros(2), ang=0, ang_vel=0)
        F_thrust = thrust(thrust_mag, angle=angle)
        self.items.append(particle)
        self.thrusts.append(F_thrust)

        # Currently, mass is the same. If not, F_g cannot be uniform
        F_g = gravity(self.items[0].mass, gravitational_acc=0.2)
        self.addUniForce(F_g)

        for i in range(len(self.items)-1, -1, -1):
            item = self.items[i]
            if item.alive == True:
                color = '#' + hex(250-item.hp)[-2:] * 3
                if item.polygon == 0:
                    x0, y0, x1, y1 = item.display()
                    canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)
                elif item.polygon == 1 or item.polygon == 3:
                    p0, p1, p2, p3 = item.display()
                    canvas.create_polygon(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], fill=color, outline=color)
                elif item.polygon == 2:
                    p0, p1, p2 = item.display()
                    canvas.create_polygon(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], fill=color, outline=color)
                else:
                    p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 = item.display()
                    canvas.create_polygon(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1],
                                        p3[0], p3[1], p4[0], p4[1], p5[0], p5[1],
                                        p6[0], p6[1], p7[0], p7[1], p8[0], p8[1], p9[0], p9[1], fill=color, outline=color)
                item.applyForce(self.thrusts[i])
                self.thrusts[i] = np.zeros_like(F_thrust)

                vel = item.vel.copy()
                air_resistance = drag(vel) + friction(vel)
                if air_resistance.any() != 0.0:
                    item.applyForce(air_resistance)

                item.next()
                item.dying()
            else:
                self.items.pop(i)
                self.thrusts.pop(i)


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
WIDTH = 1200
HEIGHT = 1200

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
root.title("Pop")
wind_blow = WindSummon()

xLabel = Label(root, text="Press W for wind")
xLabel.focus_set()
xLabel.pack()
xLabel.bind("<Key>", wind_blow.summon)

mouse = Mouse(np.array([-WIDTH, HEIGHT]))
canvas.bind("<Button-1>", mouse.position)
canvas.pack()

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
origin = mouse.pos
particles = ParticleSystem(origin)
wind = thrust(10)

while True:
    particles.run(canvas)
    if wind_blow.ifWind == True:
        particles.addUniForce(wind)
        wind_blow.hault()
    root.update()
    canvas.delete("all")

time.sleep(0.01)
root.mainloop()
