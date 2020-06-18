import numpy as np
from turtle import *
import time

home()

number_occur = []
width = screensize()[0]
dot(1, "black")
while True:
    undo()
    h = np.random.uniform(-width/2, width/2)
    penup()
    goto(h, 0)
    pendown()
    dot(20, "black")
    time.sleep(0.15)
done()
