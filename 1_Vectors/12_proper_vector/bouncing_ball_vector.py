import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400

class Ball(object):
    """docstring for Ball."""

    def __init__(self, radius, origin):
        super(Ball, self).__init__()
        self.radius = radius
        self.origin = origin

    def position(self):
        dis_sq = self.radius**2 / 2
        dposition = np.array([np.sqrt(dis_sq), np.sqrt(dis_sq)])
        point_1 = self.origin - dposition
        point_2 = self.origin + dposition
        return point_1, point_2

def main():
    r = np.random.randint(10, 50)
    origin = np.array([round(np.random.randint(0, WIDTH)), round(np.random.randint(0, HEIGHT))])
    ball = Ball(r, origin)
    x, y = ball.origin[0], ball.origin[1]
    point_1, point_2 = ball.position()
    vel = np.array([np.random.uniform(-4, 4), np.random.uniform(-4, 4)])

    p = Tk()
    canvas = Canvas(p, width=WIDTH, height=HEIGHT)
    p.title("Bouncing Ball")
    canvas.pack()

    ball_canvas = canvas.create_oval(point_1[0], point_1[1], point_2[0], point_2[1], fill="lightblue", outline="black")
    while True:
        if (x>WIDTH or x<0):
            vel[0] *= -1

        if (y>HEIGHT or y<0):
            vel[1] *= -1

        canvas.move(ball_canvas, vel[0], vel[1])
        p.update()
        x += vel[0]
        y += vel[1]
        time.sleep(0.01)

    canvas.mainloop()
    return

if __name__ == '__main__':
    main()
