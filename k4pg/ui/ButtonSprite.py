from ..sprite.Sprite import Sprite
from ..ui.Button import Button
import pygame as pg
from ..sprite.SpriteLoader import SpriteLoader


class ButtonSprite(Button, Sprite):
    def __init__(self, *args, pressed_tag=None, hover_tag=None, not_pressed_tag=None, **kwargs):
        self._pressed_tag = pressed_tag
        self._hover_tag = hover_tag
        self._not_pressed_tag = not_pressed_tag
        super(ButtonSprite, self).__init__(*args, **kwargs)

    def load_sprite(self, loader: 'SpriteLoader', surface: pg.Surface, frame_info, tag_info, vars_=None):
        super(ButtonSprite, self).load_sprite(loader, surface, frame_info, tag_info, vars_=vars_)
        self.set_tag(self.not_pressed_tag)

    def get_hover(self, cam):
        mouse_pos = self.inp.get_mouse_pos()
        if self.get_screen_rect(cam)[0].collidepoint(mouse_pos[0], mouse_pos[1]) and self.visible:
            return True
        return False

    def get_press(self):
        if self.inp.get_mouse_down(1) and self.visible:
            return True
        return False

    def on_not_pressed(self):
        if self._not_pressed_tag:
            self.set_tag(self._not_pressed_tag)

    def on_pressed(self):
        if self._pressed_tag:
            self.set_tag(self._pressed_tag)

    def on_hover(self):
        if self._hover_tag:
            self.set_tag(self._hover_tag)

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

    @property
    def hover_tag(self):
        return self._hover_tag

    @hover_tag.setter
    def hover_tag(self, v: str):
        self._hover_tag = v
        if self._hovering:
            self.set_tag(v)
