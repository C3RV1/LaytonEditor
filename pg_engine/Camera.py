import pygame as pg

from pg_engine import Alignment


class Camera:
    def __init__(self, surf: pg.Surface, world_position=None, alignment=None, viewport: [pg.Rect, list, tuple] = None,
                 zoom=None):
        if world_position is None:
            world_position = [0, 0]
        if alignment is None:
            alignment = [Alignment.CENTER, Alignment.CENTER]
        if zoom is None:
            zoom = [1, 1]
        self.world_position = world_position.copy()
        self.alignment = alignment
        if viewport is not None:
            self.viewport = viewport
            if not isinstance(self.viewport, pg.Rect):
                self.viewport = pg.Rect(self.viewport)
        else:
            self.viewport = pg.Rect(0, 0, surf.get_width(), surf.get_height())
        self.zoom = zoom
        self.surf = surf

    def to_screen(self, point: list):
        point[0] *= self.zoom[0]
        point[1] *= self.zoom[1]
        point[0] += self.viewport[0] + self.viewport[2] * self.alignment[0] - self.world_position[0]
        point[1] += self.viewport[1] + self.viewport[3] * self.alignment[1] - self.world_position[1]

    def from_screen(self, point: list):
        point[0] -= self.viewport[0] + self.viewport[2] * self.alignment[0] - self.world_position[0]
        point[1] -= self.viewport[1] + self.viewport[3] * self.alignment[1] - self.world_position[1]
        point[0] /= self.zoom[0]
        point[1] /= self.zoom[1]
