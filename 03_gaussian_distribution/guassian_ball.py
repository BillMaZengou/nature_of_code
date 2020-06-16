import numpy as np
import time
from turtle import *
home()
std = 100
mean = 100
# i = 0
# iteration = 100
# while i < iteration:
dot(1, "lightblue")
while True:
    undo()
    radius = np.random.randn() * std + mean
    if radius > 0:
        dot(radius, "lightblue")
    time.sleep(0.1)
    # i += 1
done()
