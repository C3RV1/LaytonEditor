from typing import Tuple

from .Alignment import Alignment
from .Camera import Camera
from .input.Input import Input
from .GameManager import GameManager
import pygame as pg


class Renderable:
    def __init__(self, *args, position: pg.Vector2 = None, use_world: bool = True, center=None, visible=True, **kwargs):
        super(Renderable, self).__init__(*args, **kwargs)
        self.position = pg.Vector2(0, 0)
        if position is not None:
            self.position.update(position.x, position.y)
        self.use_world = use_world
        self._screen_position = pg.Vector2(0, 0)
        self.center = pg.Vector2(Alignment.CENTER, Alignment.CENTER)
        if center is not None:
            self.center.update(center.x, center.y)
        self.visible = visible
        self.inp = Input()
        self.gm = GameManager()

    def _position_to_screen(self, cam: Camera):
        self._screen_position.update(self.position.x, self.position.y)
        self._screen_position = cam.to_screen(self._screen_position, use_world=self.use_world)

    def draw(self, cam: Camera):
        cam.set_surf_clip()
        self._position_to_screen(cam)

    def get_screen_rect(self, cam: Camera, do_clip=True) -> Tuple[pg.Rect, pg.Rect]:
        return pg.Rect(0, 0, 0, 0), pg.Rect(0, 0, 0, 0)

    def get_world_rect(self) -> pg.Rect:
        return pg.Rect(0, 0, 0, 0)
