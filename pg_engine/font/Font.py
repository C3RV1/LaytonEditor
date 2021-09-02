from dataclasses import dataclass
from typing import Tuple, Any, Dict

import pygame as pg
from ..Alignment import Alignment


class Font:

    def render(self, text: str, color: pg.Color, bg_color: pg.Color, line_spacing=0,
               h_align: int = Alignment.LEFT) -> Tuple[pg.Surface, Any]:
        lines = text.split("\n")
        alpha = bg_color is None
        if alpha:
            bg_color = pg.Color(255-color.r, 255-color.g, 255-color.b)
        self._set_color(color)
        self._set_bg_color(bg_color)
        widths, heights = list(), list()
        for line in lines:
            w, h = self._get_line_size(line)
            widths.append(w)
            heights.append(h)
        surf_w = max(widths)
        surf_h = sum(heights) + line_spacing * (len(heights) - 1)
        surf = pg.Surface((surf_w, surf_h))
        surf.fill(bg_color)
        current_y = 0
        for i, line in enumerate(lines):
            w, h = widths[i], heights[i]
            line_surf_pos = (int(surf_w * h_align - w * h_align), current_y)
            self._render_line(surf, line_surf_pos, line)
            current_y += h + line_spacing
        if alpha:
            return surf, bg_color
        return surf, None

    def _set_color(self, color: pg.Color):
        pass

    def _set_bg_color(self, bg_color: pg.Color):
        pass

    def _get_line_size(self, line: str) -> tuple:
        pass

    def _render_line(self, surf: pg.Surface, pos: Tuple[int, int], text: str):
        pass


class PygameFont(Font):
    def __init__(self, pygame_font: pg.font.Font):
        self._pg_font: pg.font.Font = pygame_font
        self._color = pg.Color(255, 255, 255)
        self._bg_color = pg.Color(0, 0, 0)

    def _set_color(self, color: pg.Color):
        self._color = color

    def _set_bg_color(self, bg_color: pg.Color):
        self._bg_color = bg_color

    def _get_line_size(self, line: str) -> tuple:
        return self._pg_font.size(line)

    def _render_line(self, surf: pg.Surface, pos: Tuple[int, int], text: str):
        surf.blit(self._pg_font.render(text, False, self._color, self._bg_color), pos)


@dataclass
class CharMap:
    index: int
    width: int
    left_spacing: int
    total_width: int


class FontMap(Font):
    MASKING_COLOR = pg.Color(0, 240, 0)

    def __init__(self, font_surface: pg.Surface, font_surface_tile_width: int, encoding: str,
                 char_map: Dict[int, CharMap], current_color: pg.Color, mask_color: pg.Color, tile_width: int, tile_height: int,
                 separator_size: int, character_spacing: int,
                 color_commands: Dict[str, pg.Color], color_command_prefix="#"):
        self._font_surface = font_surface
        self._font_surface_tile_width = font_surface_tile_width
        self._tile_width = tile_width
        self._tile_height = tile_height
        self._separator_size = separator_size
        self._char_spacing = character_spacing
        self._char_map = char_map
        self._color = current_color
        self._color_commands = {}
        self._encoding = encoding
        for command, command_color in color_commands.items():
            command = self._encode_char(command)
            self._color_commands[command] = command_color
        self._color_command_prefix = self._encode_char(color_command_prefix)
        pg.transform.threshold(self._font_surface, self._font_surface, mask_color, set_color=self.MASKING_COLOR,
                               inverse_set=True)
        self._font_surface.set_colorkey(self.MASKING_COLOR)

    def _encode_char(self, char: str):
        return int.from_bytes(char.encode(self._encoding), "big")

    def _get_line_size(self, line: str) -> tuple:
        w, h = 0, self._tile_height
        i = 0
        chars_rendered = 0
        while i < len(line):
            char = self._encode_char(line[i])
            i += 1
            if char == self._color_command_prefix:
                i += 1
                continue

            if char not in self._char_map:
                continue

            c_map = self._char_map[char]
            w += c_map.total_width + self._char_spacing
            chars_rendered += 1
        return w, h

    def _set_color(self, color: pg.Color):
        if color == self._color:
            return
        if color == self.MASKING_COLOR:
            color.g -= 1
        pg.transform.threshold(self._font_surface, self._font_surface, self._color, set_color=color, inverse_set=True)
        self._color = color

    def _render_line(self, surf: pg.Surface, pos: Tuple[int, int], text: str):
        pos = list(pos)
        i = 0
        chars_rendered = 0
        while i < len(text):
            char = self._encode_char(text[i])
            i += 1

            if char == self._color_command_prefix:
                if i == len(text):
                    continue
                color_command = self._encode_char(text[i])
                i += 1
                color = self._color_commands.get(color_command, None)
                if color:
                    self._set_color(color)
                continue

            if char not in self._char_map:
                continue

            char_map = self._char_map[char]

            if self._font_surface_tile_width is not None:
                tile_x = char_map.index % self._font_surface_tile_width
                tile_y = char_map.index // self._font_surface_tile_width
            else:
                tile_x = char_map.index
                tile_y = 0

            source = pg.Rect(tile_x * (self._tile_width + self._separator_size) + self._separator_size,
                             tile_y * (self._tile_height + self._separator_size) + self._separator_size,
                             char_map.width,
                             self._tile_height)
            surf.blit(self._font_surface, [pos[0] + char_map.left_spacing, pos[1]], area=source)

            pos[0] += char_map.total_width + self._char_spacing

            chars_rendered += 1
