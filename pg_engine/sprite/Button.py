from .Sprite import Sprite
from ..Input import Input
from ..Camera import Camera
import pygame as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .SpriteLoader import SpriteLoader


class Button(Sprite):
    def __init__(self, *args, pressed_tag=None, not_pressed_tag=None, pressed_counter=0.1, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self._pressed_tag = pressed_tag
        self._not_pressed_tag = not_pressed_tag
        self._pressed = False
        self.pressed_counter = pressed_counter
        self._current_pressed_counter = 0
        self.input_manager = Input()
        if self._not_pressed_tag:
            self.set_tag(self._not_pressed_tag)

    def load_sprite(self, loader: 'SpriteLoader', surface: pg.Surface, frame_info, tag_info, vars_=None):
        super(Button, self).load_sprite(loader, surface, frame_info, tag_info, vars_=vars_)
        self.set_tag(self._not_pressed_tag)

    def pressed(self, cam: Camera, dt: float):
        if not self._pressed:
            if self.input_manager.get_mouse_down(1):
                mouse_pos = self.input_manager.get_mouse_pos()
                if self.get_screen_rect(cam)[0].collidepoint(mouse_pos[0], mouse_pos[1]):
                    self._pressed = True
                    if self._pressed_tag:
                        self.set_tag(self._pressed_tag)
                    self._current_pressed_counter = self.pressed_counter
                    return False
        else:
            if self._current_pressed_counter is None:
                self._pressed = False
                return True
            if self._current_pressed_counter <= 0:
                self.set_tag(self._not_pressed_tag)
                self._current_pressed_counter = None
                return False
            self._current_pressed_counter -= dt
        return False

    @property
    def not_pressed_tag(self):
        return self._not_pressed_tag

    @not_pressed_tag.setter
    def not_pressed_tag(self, v: str):
        self._not_pressed_tag = v
        if not self._pressed:
            self.set_tag(v)

    @property
    def pressed_tag(self):
        return self._pressed_tag

    @pressed_tag.setter
    def pressed_tag(self, v: str):
        self._pressed_tag = v
        if self._pressed:
            self.set_tag(v)
