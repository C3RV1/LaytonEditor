from typing import Tuple, Any

import pygame as pg
from ..Alignment import Alignment


class Font:

    def render(self, text: str, color: pg.Color, bg_color: pg.Color, line_spacing=0,
               h_align: int = Alignment.LEFT) -> Tuple[pg.Surface, Any]:
        lines = text.split("\n")
        alpha = bg_color is None
        if alpha:
            bg_color = pg.Color(255-color.r, 255-color.g, 255-color.b)
        if len(lines) == 1:
            surf = self._render_line(None, (0, 0), text, color, bg_color)
        else:
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
                self._render_line(surf, line_surf_pos, line, color, bg_color)
                current_y += h + line_spacing
        if alpha:
            return surf, bg_color
        return surf, None

    def _get_line_size(self, line: str) -> tuple:
        pass

    def _render_line(self, surf: [pg.Surface], pos: Tuple[int, int], text: str, color: pg.Color, bg_color: pg.Color):
        pass


class PygameFont(Font):
    def __init__(self, pygame_font: pg.font.Font):
        self._pg_font: pg.font.Font = pygame_font

    def _get_line_size(self, line: str) -> tuple:
        return self._pg_font.size(line)

    def _render_line(self, surf: [pg.Surface], pos: Tuple[int, int], text: str, color: pg.Color, bg_color: pg.Color):
        if surf is not None:
            surf.blit(self._pg_font.render(text, False, color, bg_color), pos)
        else:
            return self._pg_font.render(text, False, color, bg_color)


# TODO: Font Map
