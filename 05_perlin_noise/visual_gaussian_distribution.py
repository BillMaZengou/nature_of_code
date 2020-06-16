import numpy as np
from turtle import *
home()
std = 100
initial_colour = (0.98, 0.98, 0.98)
number_occur = []

while True:
    h = np.random.randn()
    h *= std
    if h not in number_occur:
        color_factor = number_occur - np.ones_like(number_occur) * h
        color_factor = [abs(x) <= 10 for x in color_factor]
        color_factor = sum(color_factor)
        number_occur.append(h)
    else:
        color_factor = 20

    penup()
    goto(h, 0)
    pendown()
    if color_factor <= 0:
        colour = initial_colour
    else:
        colour_list = np.divide(initial_colour, color_factor)
        colour = (colour_list.item(0), colour_list.item(1), colour_list.item(2))
    dot(20, colour)
done()
