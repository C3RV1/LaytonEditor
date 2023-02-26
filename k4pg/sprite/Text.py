from typing import Tuple
import pygame as pg

from ..font.Font import Font
from ..font.FontSupportive import FontSupportive
from ..sprite.Sprite import Sprite
from ..Camera import Camera
from ..Alignment import Alignment


class Text(Sprite, FontSupportive):
    def __init__(self, *args, text: str = "", color: pg.Color = pg.Color(255, 255, 255),
                 bg_color: [pg.Color, None] = None, line_spacing: int = 0,
                 align: int = Alignment.LEFT, antialiasing=True, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self._text: str = text
        self._color: pg.Color = color
        self._bg_color: [None, pg.Color] = bg_color
        self._line_spacing: int = line_spacing
        self._align: int = align
        self._antialiasing = antialiasing
        self._render_needed = True

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, v: str):
        if self._text == v:
            return
        self._text = v
        self._render_needed = True

    @property
    def color(self) -> pg.Color:
        return self._color

    @color.setter
    def color(self, v: pg.Color):
        if v == self._color:
            return
        self._color = v
        self._render_needed = True

    @property
    def bg_color(self) -> [pg.Color, None]:
        return self._bg_color

    @bg_color.setter
    def bg_color(self, v: [pg.Color, None]):
        if v == self._bg_color:
            return
        self._bg_color = v
        self._render_needed = True

    def set_font(self, f: Font):
        if self._font == f:
            return
        self._font = f
        self._render_needed = True

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, v: int):
        if v == self._line_spacing:
            return
        self._line_spacing = v
        self._render_needed = True

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, v: int):
        if v == self._align:
            return
        self._align = v
        self._render_needed = True

    @property
    def antialiasing(self):
        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, v: bool):
        if v == self._antialiasing:
            return
        self._antialiasing = v
        self._render_needed = True

    def get_world_rect(self) -> pg.Rect:
        self._render()
        return super(Text, self).get_world_rect()

    def get_screen_rect(self, *args, **kwargs) -> Tuple[pg.Rect, pg.Rect]:
        self._render()
        return super(Text, self).get_screen_rect(*args, **kwargs)

    def _render(self):
        if self._font is None:
            return 
        if not self._render_needed:
            return
        self._render_needed = False
        self.surf, self.color_key = self._font.render(self._text, self._color, self._bg_color,
                                                      line_spacing=self._line_spacing,
                                                      h_align=self._align,
                                                      antialiasing=self._antialiasing)
        
    def draw(self, cam: Camera):
        if self._font is None:
            return 
        self._render()
        super(Text, self).draw(cam)
