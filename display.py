import cairo
import numpy as np
import cv2

from syracuse import SyracuseArt

CANVAS_WIDTH, CANVAS_HEIGHT = 1200, 600
BACKGROUND_COLOR = (0, 0, 0)

class CairoCanvas:
    def __init__(self, w, h, colour):
        """
            Create canvas.
        """
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        self.ctx = cairo.Context(self.surface)
        self.ctx.scale(w, h)
        self.background(colour)
        self.display_offset = 0.05

    def background(self, colour):
        """
            Create canvas background.
        """
        pat = cairo.SolidPattern(*colour)
        self.ctx.rectangle(0, 0, 1, 1)
        self.ctx.set_source(pat)
        self.ctx.fill()

    def draw_straight_line(self, origin, dest, linewidth=0.01, colour=(1, 1, 1), reverse_y=True):
        self.ctx.set_line_width(linewidth)
        self.ctx.set_source_rgb(1, 0, 0)

        if reverse_y:
            self.ctx.move_to(origin.x, 1 - origin.y)
            self.ctx.line_to(dest.x, 1 - dest.y)
        else:
            self.ctx.move_to(origin.x, origin.y)
            self.ctx.line_to(dest.x, dest.y)

        self.ctx.stroke()

    def draw_all_lines(self, curve):
        for i, pt in enumerate(curve):
            if i < len(curve) - 1:
                self.draw_straight_line(pt, curve[i + 1], linewidth=0.002)

    def draw_all_curves(self, data):
        for curve in data:
            self.draw_all_lines(curve)

    def display(self):
        buf = self.surface.get_data()
        array = np.ndarray(shape=(CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.uint8, buffer=buf)
        cv2.imshow("Array", array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, name='art'):
        self.surface.write_to_png(f"{name}.png")

if __name__ == '__main__':
    s_art = SyracuseArt()
    s_art.compute_syracuse(100, randmin=2, randmax=200)

    canvas = CairoCanvas(CANVAS_WIDTH, CANVAS_HEIGHT, BACKGROUND_COLOR)

    s_art.rescale(0, 1, canvas.display_offset, 1 - canvas.display_offset)

    canvas.draw_all_curves(s_art.return_data_as_points(rescaled=True))
    canvas.display()
