import numpy as np

from math import sqrt

from tools import Point

class Art:
    def __init__(self):
        self.all_curves = []
        self.rescaled_curves = []

        self.x_interval = -1
        self.x_scale = []
        self.rescaled_x_scale = []

        self.max_x = -1

    def distance(self, p1, p2):
        return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def rescale(self, min_x, max_x, min_y, max_y):
        max_x_in_values = max([len(x) for x in self.all_curves])
        min_y_in_values = min([min(x) for x in self.all_curves])
        max_y_in_values = max([max(x) for x in self.all_curves])

        for curve in self.all_curves:
            curve = np.asarray(curve)
            self.rescaled_curves.append(np.interp(curve, (min_y_in_values, max_y_in_values), (min_y, max_y)))

        self.x_interval = 1 / max_x_in_values
        self.x_scale = [x for x in range(max_x_in_values)]
        self.rescaled_x_scale = [self.x_interval * i for i in range(max_x_in_values)]

    def return_data_as_points(self, rescaled=False):
        list_of_points = []

        data_to_use = self.all_curves
        x_scale_to_use = self.x_scale

        if rescaled:
            data_to_use = self.rescaled_curves
            x_scale_to_use = self.rescaled_x_scale

        for curve in data_to_use:
            curve_as_points = []
            for i, pt in enumerate(curve):
                curve_as_points.append(Point(x_scale_to_use[i], pt))
            list_of_points.append(curve_as_points)

        return list_of_points
