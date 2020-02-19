import random as rn
import time

from dataclasses import dataclass
from enum import Enum

import pygame

class Direction(Enum):
    TOP = 0
    TOP_RIGHT = 1
    RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM = 4
    BOTTOM_LEFT = 5
    LEFT = 6
    TOP_LEFT = 7
    
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

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

@dataclass
class Figure:
    def __init__(self):
        self.list_of_lines = []

class TheArt:
    def __init__(self):
        self.surface_width = 800
        self.surface_height = 800

        self.list_of_figures = []

        self.symbol_max_width = 80
        self.symbol_max_height = 80
        self.symbol_half_w = int(self.symbol_max_width / 2)
        self.symbol_half_h = int(self.symbol_max_height / 2)
        self.lattice_size = 40

        # In ms
        self.display_delay = 100
        self.start_time = self.get_time()
        self.offset = Point(0, 0)

        pygame.init()
        self.screen = pygame.display.set_mode((self.surface_width, self.surface_height))

        self.current_iter = 0
        self.current_iter_row = 0

    def generate_random_point(self, x_beg, x_end, y_beg, y_end):
        if x_beg > x_end:
            x_beg, x_end = x_end, x_beg

        if y_beg > y_end:
            y_beg, y_end = y_end, y_beg

        x = self.round_to_value(rn.randint(x_beg, x_end), self.lattice_size)
        y = self.round_to_value(rn.randint(y_beg, y_end), self.lattice_size)

        return Point(x, y)

    def generate_second_point(self, first_point):
        # 0 = horizontal
        # 1 = vertical
        # 2 = diagonal
        orientation = rn.randint(0, 2)

        possible_direction = []

        if orientation == 0:
            if first_point.x > 0:
                possible_direction.append(Direction.LEFT)
            if first_point.x < self.symbol_half_w:
                possible_direction.append(Direction.RIGHT)

        if orientation == 1:
            if first_point.y > 0:
                possible_direction.append(Direction.TOP)
            if first_point.y < self.symbol_max_height:
                possible_direction.append(Direction.BOTTOM)

        if orientation == 2:
            if first_point.x > 0 and first_point.y > 0:
                possible_direction.append(Direction.TOP_LEFT)
            if first_point.x > 0 and first_point.y < self.symbol_max_height:
                possible_direction.append(Direction.BOTTOM_LEFT)
            if first_point.x < self.symbol_half_w and first_point.y > 0:
                possible_direction.append(Direction.TOP_RIGHT)
            if first_point.x < self.symbol_half_w and first_point.y < self.symbol_max_height:
                possible_direction.append(Direction.BOTTOM_RIGHT)

        chosen_direction = rn.choice(possible_direction)

        point = None

        # TODO: diagonal constraint
        if chosen_direction == Direction.TOP:
            point = self.generate_random_point(first_point.x, first_point.x, first_point.y - self.lattice_size, 0)
        elif chosen_direction == Direction.TOP_RIGHT:
            point = self.generate_random_point(first_point.x + self.lattice_size, self.symbol_half_w,
                                               first_point.y - self.lattice_size, 0)
        elif chosen_direction == Direction.RIGHT:
            point = self.generate_random_point(first_point.x + self.lattice_size, self.symbol_half_w,
                                               first_point.y, first_point.y)
        elif chosen_direction == Direction.BOTTOM_RIGHT:
            point = self.generate_random_point(first_point.x + self.lattice_size, self.symbol_max_height, 
                                               first_point.y + self.lattice_size, self.symbol_max_height)
        elif chosen_direction == Direction.BOTTOM:
            point = self.generate_random_point(first_point.x, first_point.x,
                                               first_point.y + self.lattice_size, self.symbol_max_height)
        elif chosen_direction == Direction.BOTTOM_LEFT:
            point = self.generate_random_point(0, first_point.x - self.lattice_size,
                                               first_point.y + self.lattice_size, self.symbol_max_height)
        elif chosen_direction == Direction.LEFT:
            point = self.generate_random_point(0, first_point.x - self.lattice_size,
                                               first_point.y, first_point.y)
        elif chosen_direction == Direction.TOP_LEFT:
            point = self.generate_random_point(0, first_point.x - self.lattice_size,
                                               first_point.y - self.lattice_size, 0)

        return point

    def draw_line(self, pt1, pt2):
        pygame.draw.line(self.screen, pygame.Color(255, 255, 255, 255), 
                         (pt1 + self.offset).to_tuple(), 
                         (pt2 + self.offset).to_tuple(), 5)

    def draw_symmetric_line(self, pt1, pt2, axis):
        if axis == 'v':
            new_pt1 = pt1
            new_pt1.x = self.symbol_max_width - new_pt1.x
            new_pt2 = pt2
            new_pt2.x = self.symbol_max_width - new_pt2.x
            pygame.draw.line(self.screen, pygame.Color(255, 255, 255, 255), 
                            (new_pt1 + self.offset).to_tuple(), 
                            (new_pt2 + self.offset).to_tuple(), 5)

    def generate_one_half(self):
        figure = Figure()
        number_of_lines = rn.randint(2, 5)
        for _ in range(number_of_lines):
            first_point = self.generate_random_point(0, self.symbol_half_w, 0, self.symbol_max_height)
            second_point = self.generate_second_point(first_point)
            figure.list_of_lines.append([first_point, second_point])

        self.list_of_figures.append(figure)

    def get_time(self):
        return int(round(time.time() * 1000))

    def round_to_value(self, value, base):
        return base * round(value / base)

    def next_symbol(self):
        self.generate_one_half()

    def generate_symbols(self, number):
        for _ in range(number):
            self.generate_one_half()

    def next_display(self):
        current_time = self.get_time()

        if current_time - self.start_time < self.display_delay:
            return
        
        self.start_time = self.get_time()

        if self.current_iter < len(self.list_of_figures):
            current_figure = self.list_of_figures[self.current_iter]
            # For debug purpose
            # pygame.draw.rect(self.screen, pygame.Color(255, 0, 0, 255), 
            #                  (self.offset.x, self.offset.y, self.symbol_max_width, self.symbol_max_height))
            
            for _, line in enumerate(current_figure.list_of_lines):
                self.draw_line(line[0], line[1])
                self.draw_symmetric_line(line[0], line[1], axis='v')

            self.current_iter += 1
            self.current_iter_row += 1

            self.offset += Point(self.symbol_max_width + 10, 0)
            
            if self.offset.x > self.surface_width:
                self.offset += Point(0, self.symbol_max_height + 10)
                self.offset.x = 0
                self.current_iter_row = 0

        pygame.display.flip()

def main():
    art = TheArt()
    art.generate_symbols(81)
    continue_ = True

    while continue_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continue_ = False

        art.next_display()

if __name__ == '__main__':
    main()