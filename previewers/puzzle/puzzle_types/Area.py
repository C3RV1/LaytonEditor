from typing import List, Union

from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
from formats.gds import GDSCommand
from formats import conf
import k4pg
import pygame as pg


class AreaTile(k4pg.Sprite):
    def __init__(self, *args, **kwargs):
        super(AreaTile, self).__init__(*args, **kwargs)
        self.solution_set = False
        self.visible = False
        self.center.update(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.inp = k4pg.Input()

    def update(self, cam: k4pg.Camera):
        if self.inp.get_mouse_down(1):
            mouse_pos = pg.Vector2(self.inp.get_mouse_pos())
            mouse_pos = cam.from_screen(mouse_pos)
            if self.get_world_rect().collidepoint(mouse_pos.x, mouse_pos.y):
                self.visible = not self.visible

    def draw(self, cam: k4pg.Camera):
        super(AreaTile, self).draw(cam)
        if conf.DEBUG:
            k4pg.draw.rect(cam, pg.Color(0, 255, 0), self.get_world_rect(),
                           width=2)


class Area(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.tiles: List[List[Union[AreaTile, None]]] = []
        super(Area, self).__init__(puzzle_data)

    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x4a:
            x, y, tiles_w, tiles_h, tile_size_w, tile_size_h, r, g, b, a = cmd.params
            board_pos = pg.Vector2(x, y) - pg.Vector2(256 // 2, 192 // 2)
            tile_size = pg.Vector2(tile_size_w, tile_size_h)

            tile_color = pg.Color(r << 3, g << 3, b << 3)
            tile_surf = pg.Surface(tile_size)
            tile_surf.fill(tile_color)

            for tile_x in range(tiles_w):
                tile_column = []
                for tile_y in range(tiles_h):
                    pos = pg.Vector2(tile_x, tile_y)
                    pos *= tile_size.elementwise()
                    pos += board_pos
                    tile = AreaTile(position=pos)
                    tile.surf = tile_surf
                    tile.alpha = a << 3
                    tile_column.append(tile)
                self.tiles.append(tile_column)
        elif cmd.command == 0x6e:
            x, y, w, h = cmd.params
            for x_ in range(x, x + w):
                for y_ in range(y, y + h):
                    self.tiles[x_][y_] = None
        elif cmd.command == 0x4b:
            x, y, w, h = cmd.params
            for x_ in range(x, x + w):
                for y_ in range(y, y + h):
                    self.tiles[x_][y_].solution_set = True

    def update_submitted(self, dt):
        for tile_col in self.tiles:
            for tile in tile_col:
                if tile:
                    tile.update(self.btm_camera)
        return super(Area, self).update_submitted(dt)

    def check_solution(self):
        for x, tile_col in enumerate(self.tiles):
            for y, tile in enumerate(tile_col):
                if tile:
                    if tile.visible != tile.solution_set:
                        return False
        return True

    def draw_base(self):
        super(Area, self).draw_base()
        for tile_col in self.tiles:
            for tile in tile_col:
                if tile:
                    tile.draw(self.btm_camera)
