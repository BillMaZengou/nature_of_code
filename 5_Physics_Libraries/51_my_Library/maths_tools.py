import numpy as np

"""
Geometry
"""
def rotation(angle):
    radian = angle*np.pi/180
    return np.array([[np.cos(radian), -np.sin(radian)],
                    [np.sin(radian), np.cos(radian)]])
