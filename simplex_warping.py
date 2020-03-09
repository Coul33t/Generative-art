import numpy as np
from opensimplex import OpenSimplex
from PIL import Image

class SimplexArt:
    def __init__(self, w, h, s, c1=None, c2=None):
        self.simplex = OpenSimplex()
        self.w = w
        self.h = h
        self.s = s

        self.c1 = c1
        self.c2 = c2

        self.final_map = None

    def noise(self, x, y):
        return self.simplex.noise2d(x / self.s, y / self.s)

    def generate_2d_noise(self, min_range, max_range, noise_type='simplex'):
        print('Generating map...')
        noise_map = np.ndarray((self.w, self.h))

        if noise_type == 'simplex':
            for y in range(0, self.h):
                for x in range(0, self.w):
                    value = self.simplex.noise2d(x / self.s, y / self.s)
                    value = np.interp(value, (-1, 1), (min_range, max_range))
                    noise_map[x, y] = value

        return noise_map


    def generate_warping(self, amplitude=10):
        original_map = self.generate_2d_noise(0, 255)
        x_displacement = self.generate_2d_noise(-1, 1)
        y_displacement = self.generate_2d_noise(-1, 1)

        self.final_map = original_map.copy()

        for x in range(self.w):
            for y in range(self.h):
                new_x = x - (x_displacement[x, y] * amplitude)
                new_y = y - (y_displacement[x, y] * amplitude)

                # Wrapping around the edges
                new_x = new_x % self.w
                new_y = new_y % self.h

                self.final_map[x, y] = original_map[int(new_x), int(new_y)]


        if self.c1 and self.c2:
            self.final_map = self.colour_map(self.final_map)

    def colour_lerping(self, c1, c2, factor, mode='RGB'):
        if factor > 1:
            print('COLOUR LERPING ERROR: factor must be in the range [0;1] (returning black).')
            return (0, 0, 0)
        if mode == 'RGB':
            return (c1[0] + (c2[0] - c1[0]) * factor,
                    c1[1] + (c2[1] - c1[1]) * factor,
                    c1[2] + (c2[2] - c1[2]) * factor)

    def colour_map(self, grayscale_to_colour):
        new_map = np.ndarray((self.w, self.h, 3))
        max_val = np.amax(grayscale_to_colour)

        for x in range(self.w):
            for y in range(self.h):
                new_map[x, y] = self.colour_lerping(self.c1, self.c2, grayscale_to_colour[x, y] / max_val, mode='RGB')

        return new_map

    def display(self, img=None, mode='RGB'):
        if not img:
            img = self.final_map

        if mode == 'L':
            img = Image.fromarray(img.astype('uint8').T, 'L')
        elif mode == 'RGB':
            # Transpose column and rows, not colours
            img = Image.fromarray(img.astype('uint8').transpose(1, 0, 2), 'RGB')

        img.show()


if __name__ == '__main__':
    c1 = [0, 0, 0]
    c2 = [150, 150, 255]
    simplex_art = SimplexArt(1024, 512, 24, c1, c2)
    simplex_art.generate_warping(100)
    simplex_art.display(mode='RGB')
