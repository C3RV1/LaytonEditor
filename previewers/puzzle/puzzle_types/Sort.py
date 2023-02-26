from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
from formats.gds import GDSCommand
from formats import conf
import k4pg
import pygame as pg


class SortTile(k4pg.Sprite):
    def __init__(self, initial_tag, solution_tag, *args, **kwargs):
        super(SortTile, self).__init__(*args, **kwargs)
        self.center.update(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.current_tag = initial_tag
        self.solution_tag = solution_tag
        self.loop_tag = False
        self.inp = k4pg.Input()

    def update(self, cam: k4pg.Camera, dt: float):
        self.animate(dt)
        if self.inp.get_mouse_down(1):
            mouse_pos = self.inp.get_mouse_pos()
            if self.get_screen_rect(cam)[0].collidepoint(mouse_pos[0], mouse_pos[1]):
                tag_num = self.get_tag_num()
                tag_num %= self.tag_count - 1
                tag_num += 1
                self.set_tag_by_num(tag_num)
                self.current_tag = self.get_tag().name

    def load_sprite(self, *args, **kwargs):
        super(SortTile, self).load_sprite(*args, **kwargs)
        self.set_tag(self.current_tag)

    def draw(self, cam: k4pg.Camera):
        super(SortTile, self).draw(cam)
        if conf.DEBUG_PUZZLE:
            k4pg.draw.rect(cam, pg.Color(0, 255, 0), self.get_world_rect(), width=2)


class Sort(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.tiles = []
        super(Sort, self).__init__(puzzle_data)

    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x2e:
            x, y, path, initial, solution = cmd.params
            tile = SortTile(str(initial), solution, position=pg.Vector2(-256//2 + x, -192//2 + y))
            self.sprite_loader.load(f"data_lt2/ani/nazo/touch/{path}", tile, True)
            self.tiles.append(tile)

    def update_submitted(self, dt):
        for tile in self.tiles:
            tile: SortTile
            tile.update(self.btm_camera, dt)
        return super(Sort, self).update_submitted(dt)

    def draw_base(self):
        super(Sort, self).draw_base()
        for tile in self.tiles:
            tile: SortTile
            tile.draw(self.btm_camera)

    def check_solution(self):
        for tile in self.tiles:
            tile: SortTile
            if str(tile.solution_tag) != tile.current_tag:
                return False
        return True
