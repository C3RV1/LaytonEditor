import os
import pygame as pg

from .Font import PygameFont
from ..sprite.Text import Text


class FontLoader:
    def load(self, path: str, size: int, text: Text):
        text.font = PygameFont(pg.font.Font(pg.font.get_default_font(), size))


class FontLoaderSYS(FontLoader):
    def load(self, path: str, size: int, text: Text):
        if path not in pg.font.get_fonts():
            super(FontLoaderSYS, self).load(path, size, text)
            return
        text.font = PygameFont(pg.font.SysFont(path, size))


class FontLoaderOS(FontLoaderSYS):
    def __init__(self, base_path=None):
        self.base_path = base_path

    def load(self, path: str, size: int, text: Text):
        if self.base_path:
            path = os.path.join(self.base_path, path)
        if not os.path.isfile(path):
            super(FontLoaderOS, self).load(path, size, text)
            return
        _, ext = os.path.splitext(path)
        if ext == ".ttf" or ext == ".otf":
            pg_font = pg.font.Font(path, size)
            text.font = PygameFont(pg_font)
