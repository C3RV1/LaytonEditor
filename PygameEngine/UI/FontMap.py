import pygame as pg
import json
import os


class FontMap:
    FONT_CACHE = {}

    def __init__(self, name, tile_width, tile_height, letter_spacing=1, line_spacing=1, encoding="cp1252"):
        self.name = name
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.letter_spacing = letter_spacing
        self.encoding = encoding
        self.color = pg.Color(0, 0, 0)
        self.line_spacing = line_spacing
        if "?" in self.name:
            self.encoding = self.name.split("?")[1]
            self.name = self.name.split("?")[0]

        if self.name not in FontMap.FONT_CACHE or True:
            self.font_surface = pg.image.load(self.name).convert_alpha()
            pg.transform.threshold(self.font_surface, self.font_surface, pg.Color(255, 255, 255),
                                   set_color=pg.Color(0, 240, 0), inverse_set=True)
            self.font_surface.set_colorkey(pg.Color(0, 240, 0))
            with open(self.name + ".json", "rb") as font_data_file:
                font_data = json.loads(font_data_file.read().decode("utf-8"))

            self.char_dict = {}
            self.create_char_dict(font_data)

            FontMap.FONT_CACHE[self.name] = {
                "font_surface": self.font_surface,
                "char_dict": self.char_dict
            }
        else:
            self.font_surface = FontMap.FONT_CACHE[self.name]["font_surface"]
            self.char_dict = FontMap.FONT_CACHE[self.name]["char_dict"]

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
        width = [0]
        height = self.tile_height
        for letter in text:
            if letter == "\n".encode(self.encoding)[0]:
                height += self.tile_height + self.line_spacing
                width.append(0)
                continue
            if letter not in self.char_dict:
                continue
            width[-1] += self.char_dict[letter]["width"] + self.letter_spacing
        return max(width), height

    def render(self, text, color=pg.Color(255, 255, 255), bg_color=pg.Color(0, 0, 0)):
        text_encoded = list(text.encode(self.encoding))
        return_surface = pg.Surface(self.get_str_size(text_encoded))
        if not isinstance(color, pg.Color):
            color = pg.Color(color)
        return_surface.fill(bg_color)
        current_x = 0
        current_y = 0

        self.set_color(color)

        while len(text_encoded) > 0:
            letter = text_encoded[0]
            text_encoded = text_encoded[1:]
            if letter == "#".encode(self.encoding)[0]:
                if len(text_encoded) > 0:
                    if text_encoded[0] == "r".encode(self.encoding)[0]:
                        self.set_color(pg.Color(240, 0, 0))
                    if text_encoded[0] == "x".encode(self.encoding)[0]:
                        self.set_color(pg.Color(0, 0, 0))
                    text_encoded = text_encoded[1:]
                continue
            if letter == "\n".encode(self.encoding)[0]:
                current_y += self.tile_height + self.line_spacing
                current_x = 0
                continue
            if letter not in self.char_dict.keys():
                print(f"Letter {letter} not found. Text: {text}")
                continue
            index_x = self.char_dict[letter]["index"] % 16
            index_y = self.char_dict[letter]["index"] // 16
            return_surface.blit(self.font_surface, [current_x, current_y],
                                area=pg.Rect(2 + index_x * (self.tile_width + 2),
                                             2 + index_y * (self.tile_height + 2),
                                             self.tile_width,
                                             self.tile_height))
            current_x += self.char_dict[letter]["width"] + self.letter_spacing
        return return_surface

    def set_color(self, value):
        if self.color == value:
            return
        if value == pg.Color(0, 240, 0):
            value = pg.Color(0, 241, 0)
        pg.transform.threshold(self.font_surface, self.font_surface, self.color, set_color=value, inverse_set=True)
        self.color = value

    @staticmethod
    def exists_font_map(path):
        if "?" in path:
            path = path.split("?")[0]
        if not os.path.isfile(path) or not os.path.isfile(path + ".json"):
            return False
        return True
