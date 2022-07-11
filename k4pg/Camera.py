from typing import Union, List, Tuple

import pygame as pg

from k4pg import Alignment


class Camera:
    def __init__(self, surf: pg.Surface, world_position: pg.Vector2 = None, alignment: pg.Vector2 = None,
                 viewport: [pg.Rect, list, tuple] = None, zoom: pg.Vector2 = None):
        self.world_position = pg.Vector2(0, 0)
        if world_position is not None:
            self.world_position.update(world_position.x, world_position.y)

        self.alignment = pg.Vector2(Alignment.CENTER, Alignment.CENTER)
        if alignment is not None:
            self.alignment.update(alignment.x, alignment.y)

        self.zoom = pg.Vector2(1, 1)
        if zoom is not None:
            self.zoom.update(zoom.x, zoom.y)

        if viewport is not None:
            self.viewport = viewport
            if not isinstance(self.viewport, pg.Rect):
                self.viewport = pg.Rect(self.viewport)
        else:
            self.viewport = pg.Rect(0, 0, surf.get_width(), surf.get_height())
        self.surf = surf

    def to_screen(self, point: Union[pg.Vector2, List, Tuple], use_world=True) -> pg.Vector2:
        point = pg.Vector2(point)
        if use_world:
            point -= self.world_position
        point *= self.zoom.elementwise()
        point += pg.Vector2(self.viewport[0], self.viewport[1])
        point += pg.Vector2(self.viewport[2], self.viewport[3]) * self.alignment.elementwise()
        return point

    def from_screen(self, point: Union[pg.Vector2, List, Tuple], use_world=True) -> pg.Vector2:
        point = pg.Vector2(point)
        point -= pg.Vector2(self.viewport[2], self.viewport[3]) * self.alignment.elementwise()
        point -= pg.Vector2(self.viewport[0], self.viewport[1])
        point /= self.zoom.elementwise()
        if use_world:
            point += self.world_position
        return point

    def clip_rect(self, r):
        clip = [0, 0, 0, 0]
        for i in [0, 1]:
            if r[i] < self.viewport[i]:
                clip[i] = self.viewport[i] - r[i]
                r[i] = self.viewport[i]
                r[i + 2] -= clip[i]
            if r[i] + r[i + 2] > self.viewport[i] + self.viewport[i + 2]:
                r[i + 2] -= (r[i] + r[i + 2]) - (self.viewport[i] + self.viewport[i + 2])
        clip[2:4] = r[2:4]
        return clip

    def set_surf_clip(self):
        if self.surf.get_clip() != self.viewport:
            self.surf.set_clip(self.viewport)

    def clear(self, color: pg.Color):
        self.set_surf_clip()
        self.surf.fill(color, self.viewport)
