import numpy as np
from opensimplex import OpenSimplex
from PIL import Image

from tools import Point

class SimplexArt:
    def __init__(self, w, h, s):
        self.simplex = OpenSimplex()
        self.w = w
        self.h = h
        self.s = s

    def noise(self, x, y):
        return self.simplex.noise2d(x / self.s, y / self.s)

    def generate_2d_noise(self, min_range, max_range):
        print('Generating map...')
        noise_map = np.ndarray((self.w, self.h))

        for y in range(0, self.h):
            for x in range(0, self.w):
                value = self.simplex.noise2d(x / self.s, y / self.s)
                value = np.interp(value, (-1, 1), (min_range, max_range))
                noise_map[x, y] = value

        return noise_map

    def generate_wrong_warping(self, amplitude=10):
        original_map = self.generate_2d_noise(0, 255)
        x_displacement = self.generate_2d_noise(-1, 1)
        y_displacement = self.generate_2d_noise(-1, 1)

        new_map = original_map.copy()

        for x in range(self.w):
            for y in range(self.h):
                new_x = x - (x_displacement[x, y] * amplitude)
                new_y = y - (y_displacement[x, y] * amplitude)

                # Wrapping around the edges
                new_x = new_x % self.w
                new_y = new_y % self.h

                new_map[x, y] = original_map[int(new_x), int(new_y)]

        self.display(new_map)

    def display(self, img):
        img = Image.fromarray(img.astype('uint8').T, 'L')
        img.show()

if __name__ == '__main__':
    simplex_art = SimplexArt(1024, 512, 24)
    simplex_art.generate_wrong_warping(5)

