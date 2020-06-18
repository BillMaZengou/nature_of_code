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
            self.x += np.random.uniform(-1, 1) * 100
            self.y += np.random.uniform(-1, 1) * 100
        else:
            self.x += np.random.uniform(-1, 1) * 5
            self.y += np.random.uniform(-1, 1) * 5


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
