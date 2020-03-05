import random as rn

from math import asin, sqrt, pi
import turtle

import numpy as np

import pygame
from pygame.locals import QUIT

from tools import Point

DISPLAY_SIZE_X = 800
DISPLAY_SIZE_Y = 600

def distance(p1, p2):
    return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def f(val, lst):
    lst.append(val)
    if val <= 1:
        return
    elif val % 2 == 0:
        return f(val / 2, lst)
    else:
        return f(val + 1, lst)

def compute_syracuse(val):
    tests = []
    for i in range(val):
        number = rn.randint(50000, 200000000000)
        # print(f'Computing for {number}')
        test = []
        f(number, test)
        test.reverse()
        tests.append(np.asarray(test))

    return tests

def rescale(data):
    biggest_y = max([max(x) for x in data])
    return [DISPLAY_SIZE_Y * curve / biggest_y for curve in data]

def get_rotation_angle(A, B):
    C = Point(B.x, A.y)
    return asin(distance(B, C) / distance(A, B)) * 180 / pi

def display_once(data):

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


def turtle_art(data):
    scaled_data = rescale(data)
    biggest_x = max([len(x) for x in data])
    x_scale = DISPLAY_SIZE_X / biggest_x

    playground = turtle.Screen()
    turtly = turtle.Turtle(visible=False)

    playground.screensize(DISPLAY_SIZE_X, DISPLAY_SIZE_Y)
    turtly.speed('fastest')

    origin = Point(-DISPLAY_SIZE_X / 2, -DISPLAY_SIZE_Y / 2)

    pt = origin
    length_pt = Point(0, 0)

    for curve_number, curve in enumerate(scaled_data):
        print(f'Drawing curve n°{curve_number}/{len(scaled_data)}', end='\r')
        length_multiplier = 1

        turtle.tracer(0, 0)
        turtly.penup()
        turtly.setpos(origin.x, origin.y)
        turtly.pendown()
        pt = origin

        for i, y in enumerate(curve):
            last_pt = pt
            last_length_pt = length_pt
            pt = Point(i * x_scale + origin.x, data[curve_number][i] + origin.y)
            length_pt = Point(i * x_scale + origin.x, y + origin.y)

            length = distance(length_pt, last_length_pt) * length_multiplier

            rotation_angle = get_rotation_angle(last_pt, pt)

            if int(data[curve_number][i]) % 2 == 0:
                rotation_angle *= 1
                turtly.left(rotation_angle)
                turtly.forward(length)
                turtly.right(rotation_angle)
            else:
                rotation_angle *= 2
                turtly.right(rotation_angle)
                turtly.forward(length)
                turtly.left(rotation_angle)

            length_multiplier *= 0.999999


        turtle.update()

    print('')
    print('Done !')
    playground.exitonclick()


if __name__ == '__main__':
    data = compute_syracuse(500)
    turtle_art(data)