import numpy as np
import time
from turtle import *
home()
std = 100
mean = 100
dot(1, "lightblue")

while True:
    undo()
    radius = np.random.randn() * std + mean
    if radius > 0:
        dot(radius, "lightblue")
    time.sleep(0.1)
done()
