import pygame as pg
from .SplineRenderer import SplineRenderer
from ..Camera import Camera
from ..input.Input import Input


class SplineEditor(SplineRenderer):
    def __init__(self, *args, **kwargs):
        super(SplineEditor, self).__init__(*args, **kwargs)
        self.inp = Input()
        self.point_i = -1
        self.editing_point = False
        self.mouse_prev = pg.Vector2(0, 0)

        # control point
        self.anchor = None
        self.c_dst = 0
        self.c_i = 0

    def update(self, cam: Camera):
        if self.inp.get_key_down(pg.K_c):
            self.spline.closed = not self.spline.closed
        if not self.editing_point:
            function = 0
            if self.inp.get_mouse_down(1):
                function = 1
            elif self.inp.get_mouse_down(3):
                function = 2
            if function != 0:
                self.point_i = -1
                mouse_pos = pg.Vector2(self.inp.get_mouse_pos())
                mouse_world = cam.from_screen(mouse_pos)
                for point_i, point in enumerate(self.spline.points):
                    if (point - mouse_world).magnitude() < 10:
                        self.point_i = point_i
                        break
                if function == 1:
                    if self.point_i == -1 and function == 1:
                        # add point
                        self.spline.add_segment(pg.Vector2(mouse_world))
                    else:
                        if self.point_i % 3 != 1:
                            # self.point_i % 3 == 2 -> self.point_i-1
                            # self.point_i % 3 == 0 -> self.point_i+1
                            if self.point_i % 3 == 2:
                                anchor_point_i = self.point_i - 1
                            else:
                                anchor_point_i = self.point_i + 1
                            self.anchor = self.spline.points[anchor_point_i % len(self.spline.points)]
                            # point_i=2, anchor=3
                            # 2 - 3 = -1
                            # corresponding = 3 - (-1) = 4
                            self.c_i = anchor_point_i + -(self.point_i - anchor_point_i)
                            self.c_i %= len(self.spline.points)
                            c = self.spline.points[self.c_i % len(self.spline.points)]
                            self.c_dst = (self.anchor - c).magnitude()
                        self.editing_point = True
                        self.mouse_prev.update(mouse_world)
                elif function == 2 and self.point_i != -1:
                    if self.point_i % 3 == 1:
                        # delete point if anchor (remove controls)
                        points = sorted([(self.point_i + i) % len(self.spline.points) for i in [-1, 0, 1]],
                                        reverse=True)
                        for point in points:
                            self.spline.points.pop(point)
                        self.editing_point = False
        else:
            if self.inp.get_mouse_up(1):
                self.editing_point = False
            mouse_pos = pg.Vector2(self.inp.get_mouse_pos())
            mouse_world = cam.from_screen(mouse_pos)
            mouse_rel = mouse_world - self.mouse_prev
            self.mouse_prev = mouse_world
            if self.point_i % 3 == 1:
                self.spline.points[(self.point_i - 1) % len(self.spline.points)] += mouse_rel
                self.spline.points[self.point_i] += mouse_rel
                self.spline.points[(self.point_i + 1) % len(self.spline.points)] += mouse_rel
            else:
                self.spline.points[self.point_i] += mouse_rel
                anchor_to_point = (self.spline.points[self.point_i] - self.anchor).normalize()
                self.spline.points[self.c_i] = anchor_to_point * -self.c_dst + self.anchor
