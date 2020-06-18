import numpy as np
from tkinter import *
import time

WIDTH = 600
HEIGHT = 400

class Ball(object):
    """docstring for Ball."""

    def __init__(self, radius, x0, y0):
        super(Ball, self).__init__()
        self.radius = radius
        self.x0 = x0
        self.y0 = y0

    def position(self):
        dis_sq = self.radius**2 / 2
        dis = np.sqrt(dis_sq)
        x1 = self.x0 - dis
        y1 = self.y0 - dis
        x2 = self.x0 + dis
        y2 = self.y0 + dis
        return x1, y1, x2, y2

def main():
    r = np.random.randint(10, 50)
    ball = Ball(r, round(np.random.randint(0, WIDTH)), round(np.random.randint(0, HEIGHT)))
    x, y = ball.x0, ball.y0
    x1, y1, x2, y2 = ball.position()
    v_x = np.random.uniform(-4, 4)
    v_y = np.random.uniform(-4, 4)

    p = Tk()
    canvas = Canvas(p, width=WIDTH, height=HEIGHT)
    p.title("Bouncing Ball")
    canvas.pack()

    ball_canvas = canvas.create_oval(x1, y1, x2, y2, fill="lightblue", outline="black")
    while True:
        if (x>WIDTH or x<0):
            v_x *= -1

        if (y>HEIGHT or y<0):
            v_y *= -1

        canvas.move(ball_canvas, v_x, v_y)
        p.update()
        x += v_x
        y += v_y
        time.sleep(0.01)

    canvas.mainloop()
    return

if __name__ == '__main__':
    main()
