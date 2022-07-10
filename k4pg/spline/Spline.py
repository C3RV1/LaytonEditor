import pygame as pg
from typing import List


SPLINE_STEPS = 100


def lerp(a: pg.Vector2, b: pg.Vector2, t: float):
    return a + (b-a)*t


def quadratic_beizer(a: pg.Vector2, b: pg.Vector2, c: pg.Vector2, t: float):
    p0 = lerp(a, b, t)
    p1 = lerp(b, c, t)
    return lerp(p0, p1, t)


def cubic_beizer(a: pg.Vector2, b: pg.Vector2, c: pg.Vector2, d: pg.Vector2, t: float):
    p0 = quadratic_beizer(a, b, c, t)
    p1 = quadratic_beizer(b, c, d, t)
    return lerp(p0, p1, t)


class Spline:
    def __init__(self, points: List[pg.Vector2], closed=False):
        # control, anchor, control, control, anchor, control, control, anchor, control
        # 0,      1,       2,       3,      4,       5,      6,       7,       8
        # if point_i % 3 == 1: anchor else: control
        # line segment i = points[(i * 3), (i * 3) + 1, (i * 3) + 2, (i * 3) + 3]
        # line segment_count = len(points) / 3
        self.points: List[pg.Vector2] = points
        self.closed = closed

    @property
    def segment_count(self):
        if self.closed:
            return len(self.points) // 3
        else:
            return (len(self.points) // 3) - 1

    def get_segment_points(self, segment_i):
        points = []
        for i in range(0, 4):
            points.append(self.points[(segment_i*3 + 1 + i) % len(self.points)])
        return points

    def sample_points(self):
        sampled_points = []
        for line_segment_i in range(self.segment_count):
            a1, c1, c2, a2 = self.get_segment_points(line_segment_i)
            for i in range(SPLINE_STEPS):
                point = cubic_beizer(a1, c1, c2, a2, i / SPLINE_STEPS)
                sampled_points.append(point)
        return sampled_points

    def get_anchors(self):
        return self.points[1::3]

    def add_segment(self, a):
        # if we have less than 2 anchor points we cannot set the controls automatically
        if len(self.points) // 3 < 1:
            c1 = a + pg.Vector2(0, 50)
            c2 = a - pg.Vector2(0, 50)
        else:
            prev_anchor = self.points[-2]
            # next_anchor = self.points[1]
            # direction = (prev_anchor - a).normalize() - (next_anchor - a).normalize()
            direction = (prev_anchor - a).normalize()
            magnitude = (prev_anchor - a).magnitude() / 4
            direction.normalize_ip()
            c1 = a + direction * magnitude
            c2 = a + direction * -magnitude
        self.points.append(c1)
        self.points.append(a)
        self.points.append(c2)
