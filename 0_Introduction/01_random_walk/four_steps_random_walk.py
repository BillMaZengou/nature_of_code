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
        state = np.random.randint(0, 4)
        if state == 0:
            self.x += 5
        elif state == 1:
            self.x -= 5
        elif  state == 2:
            self.y += 5
        else:
            self.y -= 5

def setup():
    w = Walker(round(np.random.random(), ndigits=2), round(np.random.random(), ndigits=2))
    return w

def main():
    home()
    # width, height = screensize()
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
