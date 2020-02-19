import random as rn
from dataclasses import dataclass

import pygame

SURFACE_WIDTH = 400
SURFACE_HEIGHT = 400
SURFACE_DEPTH = 400

class TheArt:
    def __init__(self):
        self.list_of_points = []
        self.list_of_lines = []

        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))

    def generate_random_point(is_3d=False):
        x = rn.randint(0, SURFACE_WIDTH)
        y = rn.randint(0, SURFACE_HEIGHT)
        z = None

        if is_3d:
            z = rn.randint(0, SURFACE_DEPTH)

        return Point(x, y, z)

    def draw_line(self, pt1, pt2):
        pygame.draw.line(self.screen, pygame.Color(255, 255, 255, 255), pt1.to_tuple(), pt2.to_tuple())

    def next_display(self):
        # TODO: Do
        pygame.display.flip()

@dataclass
class Point:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        if self.z is None:
            return (self.x, self.y)

        return (self.x, self.y, self.z)


def main():

    art = TheArt()
    continue_ = True

    while continue_:
        art.next_display()
        pygame.display.flip()