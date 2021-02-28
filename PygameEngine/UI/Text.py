import PygameEngine.Sprite
import PygameEngine.UI.FontMap
import pygame as pg
import os

import PygameEngine.Screen


class Text(PygameEngine.Sprite.Sprite):
    FONTS = {}

    def __init__(self, groups):
        super(Text, self).__init__(groups)
        self.font = None
        self.current_text = None

    def set_font(self, font_path, size, is_font_map=False, letter_spacing=1):
        if not is_font_map:
            if not isinstance(size, int):
                raise Exception("Size is not int on non font map")
            if font_path is None or not os.path.isfile(font_path):
                self.font = pg.font.SysFont("arial", size)
                self.set_text("")
                return
            font_id = f"{font_path}-{size}"
            if font_id in Text.FONTS.keys():
                self.font = Text.FONTS[font_id]
            else:
                self.font = pg.font.Font(font_path, size)
                Text.FONTS[font_id] = self.font
        else:
            if PygameEngine.UI.FontMap.FontMap.exists_font_map(font_path):
                self.font = PygameEngine.UI.FontMap.FontMap(font_path, size[0], size[1], letter_spacing=letter_spacing)
            else:
                self.font = pg.font.Font(None, 16)
        self.set_text("")

    def set_text(self, text, color=(255, 255, 255), antialias=False, bg_color=(0, 0, 0), mask_color=(0, 0, 0)):
        if self.font is None:
            return
        if self.current_text == text:
            return
        self.current_text = text
        if isinstance(self.font, pg.font.Font):
            self.font: pg.font.Font
            self.image = self.font.render(text, antialias, color, bg_color)
        elif isinstance(self.font, PygameEngine.UI.FontMap.FontMap):
            self.font: PygameEngine.UI.FontMap.FontMap
            self.image = self.font.render(text, bg_color=bg_color)
        rect_wh = self.image.get_rect()
        self.world_rect.w = rect_wh.w
        self.world_rect.h = rect_wh.h
        self.reset_world_rect()
        self.set_color_key(mask_color)
        self.dirty = 1

