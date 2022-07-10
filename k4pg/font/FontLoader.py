import os
import pygame as pg
import json

from .Font import PygameFont, FontMap, CharMap
from ..sprite.Text import Text


class FontLoader:
    def load(self, path: str, size: int, text: Text):
        FontLoader._load(self, path, size, text)

    def _load(self, path: str, size: int, text: Text) -> bool:
        text.font = PygameFont(pg.font.Font(pg.font.get_default_font(), size))
        return True


class FontLoaderSYS(FontLoader):
    def __init__(self, fall_back_font_sys=None):
        self.fall_back_font_sys = fall_back_font_sys

    def _load(self, path: str, size: int, text: Text) -> bool:
        if path not in pg.font.get_fonts():
            return False
        text.font = PygameFont(pg.font.SysFont(path, size))
        return True

    def load(self, path: str, size: int, text: Text):
        if FontLoaderSYS._load(self, path, size, text):
            return
        if FontLoaderSYS._load(self, self.fall_back_font_sys, size, text):
            return 
        super(FontLoaderSYS, self).load(path, size, text)


class FontLoaderOS(FontLoaderSYS):
    def __init__(self, base_path_os=None, fall_back_font_os=None, **kwargs):
        super(FontLoaderOS, self).__init__(**kwargs)
        self.base_path_os = base_path_os
        self.fall_back_font_os = fall_back_font_os

    def load(self, path: str, size: int, text: Text):
        if FontLoaderOS._load(self, path, size, text):
            return
        if self.fall_back_font_os:
            if FontLoaderOS._load(self, self.fall_back_font_os, size, text):
                return
        super(FontLoaderOS, self).load(path, size, text)

    def _load(self, path: str, size: int, text: Text):
        if self.base_path_os:
            real_path = os.path.join(self.base_path_os, path)
        else:
            real_path = path
        _, ext = os.path.splitext(real_path)
        if ext == "":
            for valid_ext in [".ttf", ".otf", ".json"]:
                if os.path.isfile(real_path + valid_ext):
                    real_path += valid_ext
                    break
            _, ext = os.path.splitext(real_path)
        if not os.path.isfile(real_path):
            return False
        path = real_path
        if ext == ".ttf" or ext == ".otf":
            pg_font = pg.font.Font(path, size)
            text.font = PygameFont(pg_font)
            return True
        elif ext == ".json":
            # font_map
            with open(real_path, "r") as font_file:
                font_data = json.loads(font_file.read())
            dir_path = os.path.dirname(real_path)
            image_path = os.path.join(dir_path, font_data["font_image"])
            if not os.path.isfile(image_path):
                return False

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
                        char["-Width"],
                        0,
                        char["-Width"]
                    )
            else:
                char_map = font_data["char_map"]

            font = FontMap(font_surf, surf_tile_width, encoding, char_map,
                           current_color, mask_color, tile_width, tile_height,
                           separator_size, character_spacing, color_commands, color_command_prefix)
            text.font = font
            return True
        return False
