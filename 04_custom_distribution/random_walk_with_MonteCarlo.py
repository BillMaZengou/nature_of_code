import numpy as np
from turtle import *

class Walker(object):
    """docstring for Walker."""

    def __init__(self, x, y):
        super(Walker, self).__init__()
        self.x = x
        self.y = y

    def display(self):
        undo()
        goto(self.x, self.y)
        dot(5, "red")

    def walk(self):
        r = np.random.randint(0, 100)
        if r < 1:
            self.x += np.random.uniform(-1, 1) * 200
            self.y += np.random.uniform(-1, 1) * 200
        else:
            stepsize = monteCarlo() * 8
            self.x += np.random.uniform(-1, 1) * stepsize
            self.y += np.random.uniform(-1, 1) * stepsize

def monteCarlo():
    selection = True
    while selection:
        r1 = np.random.rand()
        r2 = np.random.rand()

        probability = r1 * r1  # Custom function (only polynominal, for logrithmic r1 and r2 need modification)

        if r2 < probability:
            selection = False
    return r1

def setup():
    w = Walker(round(np.random.random(), ndigits=2), round(np.random.random(), ndigits=2))
    return w

def main():
    home()
    walker = setup()

    penup()
    goto(walker.x, walker.y)
    pendown()
    dot(5, "red")
    i = 0
    while True:
        walker.walk()
        walker.display()
    done()

if __name__ == '__main__':
    main()
