import random as rn

import matplotlib
import matplotlib.pyplot as plt

import pygame
from pygame.locals import QUIT

def f(val, lst):
    lst.append(val)
    if val <= 1:
        return
    elif val % 2 == 0:
        return f(val / 2, lst)
    else:
        return f(val + 1, lst)

def compute_syracuse(val, max_iter):
    tests = []
    for i in range(2000):
        number = rn.randint(1, 2000000)
        print(f'Computing for {number}')
        test = []
        f(number, test)
        tests.append(test)
    plot_art(tests)

def display_once(data):
    biggest_x = max([len(x) for x in data])
    biggest_y = max([max(x) for x in data])

    for curve in data:
        pass


def plot_art(data):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    continue_display = True

    display_once(data)

    while continue_display:
        for event in pygame.event.get():
            if event.type == QUIT:
                continue_display = False

        pygame.display.flip()
        

if __name__ == '__main__':
    compute_syracuse(8, 1)
    plot_art