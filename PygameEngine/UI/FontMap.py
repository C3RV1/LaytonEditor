import pygame as pg
import json
import os


class FontMap:
    FONT_CACHE = {}

    def __init__(self, name, tile_width, tile_height, letter_spacing=1):
        self.name = name
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.letter_spacing = letter_spacing
        if name not in FontMap.FONT_CACHE:
            self.font_surface = pg.image.load(name + ".png").convert_alpha()
            self.font_surface.set_colorkey(pg.Color(255, 255, 255))
            with open(name + ".json", "rb") as font_data_file:
                font_data = json.loads(font_data_file.read().decode("utf-8"))

            self.char_dict = {}
            self.create_char_dict(font_data)

            FontMap.FONT_CACHE[name] = {
                "font_surface": self.font_surface,
                "char_dict": self.char_dict
            }
        else:
            self.font_surface = FontMap.FONT_CACHE[name]["font_surface"]
            self.char_dict = FontMap.FONT_CACHE[name]["char_dict"]

    def create_char_dict(self, font_data):
        for char_code in font_data["CharMap"]["CharInfo"]:
            char_id = int(char_code["-Code"], 16)
            if char_id in self.char_dict.keys():
                continue
            self.char_dict[char_id] = {
                "index": int(char_code["-Index"]),
                "width": int(char_code["-Width"])
            }

    def get_str_size(self, text):
        width = 0
        for letter in text:
            if letter not in self.char_dict:
                continue
            width += self.char_dict[letter]["width"] + self.letter_spacing
        return width, self.tile_height

    def render(self, text, bg_color=pg.Color(255, 255, 255)):
        text_encoded = list(text.encode("cp1252"))
        return_surface = pg.Surface(self.get_str_size(text_encoded))
        return_surface.fill(bg_color)
        current_x = 0
        for letter in text_encoded:
            if letter not in self.char_dict.keys():
                print(f"Letter in position {text_encoded.index(letter)} not found. Text: {text}")
                continue
            index_x = self.char_dict[letter]["index"] % 16
            index_y = self.char_dict[letter]["index"] // 16
            return_surface.blit(self.font_surface, [current_x, 0], area=pg.Rect(2 + index_x * (self.tile_width + 2),
                                                                                2 + index_y * (self.tile_height + 2),
                                                                                self.tile_width,
                                                                                self.tile_height))
            current_x += self.char_dict[letter]["width"] + self.letter_spacing
        return return_surface

    @staticmethod
    def exists_font_map(path):
        if not os.path.isfile(path + ".png") or not os.path.isfile(path + ".json"):
            return False
        return True
