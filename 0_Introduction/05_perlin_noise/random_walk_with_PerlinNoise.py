import numpy as np
from turtle import *

class Walker(object):
    """docstring for Walker."""

    def __init__(self, x, y, tx, ty):
        super(Walker, self).__init__()
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty

    def display(self):
        undo()
        goto(self.x, self.y)
        dot(5, "red")

    def walk(self):
        self.x = noise(self.tx) * np.random.uniform(-50, 50)
        self.y = noise(self.ty) * np.random.uniform(-50, 50)
        self.tx += 0.1
        self.ty += 0.1

def setup():
    w = Walker(round(np.random.random(), ndigits=2), round(np.random.random(), ndigits=2), 0, 100)
    return w

"""
Perlin Noise
"""
def cos_interpolation(a, b, mu):
    mu = 1-np.cos(mu*np.pi/2)
    return a*(1-mu) + b*mu

def random_noise(t0, tE, t_interval, amp):
    random_list_size = (tE - t0)//t_interval
    random_list = [np.random.rand()*amp for i in range(random_list_size)]
    return random_list

def perlin_noise():
    t0 = 0
    amp = 100
    t_interval = 10
    tE = 100
    noise_list_len = 300

    first_list = random_noise(t0, tE, t_interval, amp)
    second_list = random_noise(t0, tE, t_interval//2, amp//2)
    third_list = random_noise(t0, tE, t_interval//10, amp//10)

    extend_first = np.zeros(noise_list_len)
    extend_second = np.zeros(noise_list_len)
    extend_third = np.zeros(noise_list_len)

    num_of_inter1 = noise_list_len // len(first_list)
    num_of_inter2 = noise_list_len // len(second_list)
    num_of_inter3 = noise_list_len // len(third_list)

    for i in range(noise_list_len):
        if i % num_of_inter1 == 0:
            idx = i//num_of_inter1
            extend_first[i] = first_list[idx]
        else:
            step = (i%num_of_inter1) / num_of_inter1
            if idx == len(first_list)-1:
                extend_first[i] = cos_interpolation(first_list[idx], first_list[0], step)
            else:
                extend_first[i] = cos_interpolation(first_list[idx], first_list[idx+1], step)

    for i in range(noise_list_len):
        if i % num_of_inter2 == 0:
            idx = i//num_of_inter2
            extend_second[i] = second_list[idx]
        else:
            step = (i%num_of_inter2) / num_of_inter2
            if idx == len(second_list)-1:
                extend_second[i] = cos_interpolation(second_list[idx], second_list[0], step)
            else:
                extend_second[i] = cos_interpolation(second_list[idx], second_list[idx+1], step)

    for i in range(noise_list_len):
        if i % num_of_inter3 == 0:
            idx = i//num_of_inter3
            extend_third[i] = third_list[idx]
        else:
            step = (i%num_of_inter3) / num_of_inter3
            if idx == len(third_list)-1:
                extend_third[i] = cos_interpolation(third_list[idx], third_list[0], step)
            else:
                extend_third[i] = cos_interpolation(third_list[idx], third_list[idx+1], step)

    perlin_noise_list = np.add(extend_first, extend_second)
    perlin_noise_list = np.add(perlin_noise_list, extend_third)

    return perlin_noise_list

def noise(time):
    choice = perlin_noise()
    choice_max = max(choice)
    if time >= 0 and time <= 10000:
        p = choice[int(time//100)]/choice_max
    else:
        print("Time should be less than 10000")
    return p

def main():
    home()
    walker = setup()

    penup()
    goto(walker.x, walker.y)
    pendown()
    dot(5, "red")
    while True:
        walker.walk()
        walker.display()
    done()

if __name__ == '__main__':
    main()
