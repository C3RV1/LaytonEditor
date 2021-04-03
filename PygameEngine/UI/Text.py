from ..Sprite import Sprite
from .FontMap import FontMap
from ..Debug import Debug
import pygame as pg
import os


class Text(Sprite):
    FONTS = {}
    DEFAULT_FONTMAP = ["data_permanent/font_default.png", [7, 10], 1, 2]

    def __init__(self, groups):
        super(Text, self).__init__(groups)
        self.__font = None
        self.__current_text = None
        self.__color = pg.Color(255, 255, 255)
        self.__bg_color = pg.Color(0, 0, 0)
        self.__mask_color = pg.Color(0, 0, 0)
        self.__antialiasing = False

    def set_font(self, font_path, size, is_font_map=False, letter_spacing=1, line_spacing=1):
        if not is_font_map:
            if not isinstance(size, int):
                raise Exception("Size is not int on non font map")
            if font_path is None or not os.path.isfile(font_path):
                self.__font = pg.font.SysFont("arial", size)
                self.text = ""
                return
            font_id = f"{font_path}-{size}"
            if font_id in Text.FONTS.keys():
                self.__font = Text.FONTS[font_id]
            else:
                self.__font = pg.font.Font(font_path, size)
                Text.FONTS[font_id] = self.__font
        else:
            if FontMap.exists_font_map(font_path):
                self.__font = FontMap(font_path, size[0], size[1], letter_spacing=letter_spacing,
                                      line_spacing=line_spacing)
            elif FontMap.exists_font_map(Text.DEFAULT_FONTMAP[0]):
                Debug.log_warning(f"Font {font_path} not found, loading default font {Text.DEFAULT_FONTMAP[0]}", self)
                self.__font = FontMap(Text.DEFAULT_FONTMAP[0], Text.DEFAULT_FONTMAP[1][0], Text.DEFAULT_FONTMAP[1][1],
                                      letter_spacing=Text.DEFAULT_FONTMAP[2], line_spacing=Text.DEFAULT_FONTMAP[3])
            else:
                Debug.log_warning(f"FontMap {font_path} not found, loading system default", self)
                self.__font = pg.font.Font(None, 16)
        self.text = ""

    def __render_text(self):
        if self.__font is None:
            return
        self.set_color_key(self.__mask_color)
        if isinstance(self.__font, pg.font.Font):
            self.__font: pg.font.Font
            self.original_image = self.__font.render(self.__current_text, self.__antialiasing, self.__color,
                                                     self.__bg_color)
        elif isinstance(self.__font, FontMap):
            self.__font: FontMap
            self.original_image = self.__font.render(self.__current_text, color=self.__color, bg_color=self.__bg_color)

    def update_transformations(self):
        if not self.should_transform:
            return
        self.__render_text()
        super().update_transformations()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if self.__color == value:
            return
        self.__color = value
        self.render_again()

    @property
    def antialiasing(self):
        return self.__antialiasing

    @antialiasing.setter
    def antialiasing(self, value):
        if self.__antialiasing == value:
            return
        self.__antialiasing = value
        self.render_again()

    @property
    def bg_color(self):
        return self.__bg_color

    @bg_color.setter
    def bg_color(self, value):
        if self.__bg_color == value:
            return
        self.__bg_color = value
        self.render_again()

    @property
    def mask_color(self):
        return self.__mask_color

    @mask_color.setter
    def mask_color(self, value):
        if self.__mask_color == value:
            return
        self.__mask_color = value
        self.render_again()

    @property
    def text(self):
        return self.__current_text

    @text.setter
    def text(self, value):
        if self.__current_text == value:
            return
        self.__current_text = value
        self.render_again()
