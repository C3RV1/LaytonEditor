import pygame as pg
from ..Renderable import Renderable
from ..Camera import Camera
from .Spline import Spline


class SplineRenderer(Renderable):
    def __init__(self, spline: Spline, *args, **kwargs):
        super(SplineRenderer, self).__init__(*args, **kwargs)
        self.spline: Spline = spline

    def draw(self, cam: Camera):
        super(SplineRenderer, self).draw(cam)
        sampled_points = self.spline.sample_points()
        for sample_point in sampled_points:
            point_screen = cam.to_screen(pg.Vector2(sample_point))
            pg.draw.circle(cam.surf, pg.Color(255, 255, 255), center=point_screen, radius=1 * cam.zoom.x)
        for i, point in enumerate(self.spline.points):
            point_screen = cam.to_screen(pg.Vector2(point))
            if i % 3 == 1:
                pg.draw.circle(cam.surf, pg.Color(255, 0, 0), center=point_screen, radius=5 * cam.zoom.x)
            else:
                pg.draw.circle(cam.surf, pg.Color(0, 255, 0), center=point_screen, radius=5 * cam.zoom.x)
                if i % 3 == 2:
                    anchor_point_i = i - 1
                else:
                    anchor_point_i = i + 1
                anchor_point = self.spline.points[anchor_point_i]
                anchor_point_screen = cam.to_screen(pg.Vector2(anchor_point))
                pg.draw.line(cam.surf, pg.Color(128, 128, 128), anchor_point_screen, point_screen)
