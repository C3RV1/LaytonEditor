from typing import Tuple

from pg_engine.Alignment import Alignment
from pg_engine.Camera import Camera
import pygame as pg


class Renderable:
    def __init__(self, position: list = None, use_world: bool = True, center=None):
        if position is None:
            self.position = [0, 0]
        else:
            self.position = position.copy()
        self.use_world = use_world
        self._screen_position = [0, 0]
        if center is None:
            self.center = [Alignment.CENTER, Alignment.CENTER]
        else:
            self.center = center
        self.visible = True

    def _position_to_screen(self, cam: Camera):
        self._screen_position[0] = self.position[0]
        self._screen_position[1] = self.position[1]
        if self.use_world:
            cam.to_screen(self._screen_position)

    def draw(self, cam: Camera):
        self._position_to_screen(cam)

    def get_screen_rect(self, cam: Camera) -> Tuple[pg.Rect, pg.Rect]:
        pass

    def get_world_rect(self) -> pg.Rect:
        pass

    def unload(self):
        pass
