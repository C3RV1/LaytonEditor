import os
import pygame as pg
import json

from .Font import PygameFont, FontMap, CharMap
from ..sprite.Text import Text


class FontLoader:
    def load(self, path: str, size: int, text: Text):
        text.font = PygameFont(pg.font.Font(pg.font.get_default_font(), size))


class FontLoaderSYS(FontLoader):
    def __init__(self, fall_back_font=None):
        self.fall_back_font = fall_back_font

    def load(self, path: str, size: int, text: Text):
        if path not in pg.font.get_fonts() and self.fall_back_font:
            path = self.fall_back_font
        if path not in pg.font.get_fonts():
            super(FontLoaderSYS, self).load(path, size, text)
            return
        text.font = PygameFont(pg.font.SysFont(path, size))


class FontLoaderOS(FontLoaderSYS):
    def __init__(self, base_path=None, **kwargs):
        super(FontLoaderOS, self).__init__(**kwargs)
        self.base_path = base_path

    def load(self, path: str, size: int, text: Text):
        if self.base_path:
            real_path = os.path.join(self.base_path, path)
        else:
            real_path = path
        _, ext = os.path.splitext(real_path)
        if ext == "":
            for valid_ext in [".ttf", ".otf", ".json"]:
                if os.path.exists(real_path + valid_ext):
                    real_path += valid_ext
                    break
            _, ext = os.path.splitext(real_path)
        if not os.path.isfile(real_path):
            super(FontLoaderOS, self).load(path, size, text)
            return
        path = real_path
        if ext == ".ttf" or ext == ".otf":
            pg_font = pg.font.Font(path, size)
            text.font = PygameFont(pg_font)
        elif ext == ".json":
            # font_map
            with open(real_path, "r") as font_file:
                font_data = json.loads(font_file.read())
            dir_path = os.path.dirname(real_path)
            image_path = os.path.join(dir_path, font_data["font_image"])
            if not os.path.isfile(image_path):
                super(FontLoaderOS, self).load(path, size, text)
                return

            font_surf = pg.image.load(image_path).convert()
            surf_tile_width = font_data["image_tile_width"]
            encoding = font_data["encoding"]
            current_color = pg.Color(font_data["text_color"])
            tile_width = font_data["tile_width"]
            tile_height = font_data["tile_height"]
            mask_color = pg.Color(font_data["mask_color"])
            separator_size = font_data["separator_size"]
            character_spacing = font_data["character_spacing"]
            color_commands = {}
            for command, command_color in font_data["color_commands"].items():
                color_commands[command] = pg.Color(command_color)
            color_command_prefix = font_data["color_command_prefix"]

            if isinstance(font_data["char_map"], list):
                char_map = {}
                for char in font_data["char_map"]:
                    code = char["-Code"]
                    if isinstance(code, str):
                        code = int(code, 16)
                    char_map[code] = CharMap(
                        char["-Index"],
                        char["-Width"]
                    )
            else:
                char_map = font_data["char_map"]


            font = FontMap(font_surf, surf_tile_width, encoding, char_map,
                           current_color, tile_width, tile_height, mask_color,
                           separator_size, character_spacing, color_commands, color_command_prefix)
            text.font = font
