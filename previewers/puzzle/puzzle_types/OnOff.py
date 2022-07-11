from formats.gds import GDSCommand
from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
import k4pg
import pygame as pg
from formats import conf


class OnOffToggle(k4pg.Sprite):
    def __init__(self, is_solution, *args, **kwargs):
        super(OnOffToggle, self).__init__(*args, **kwargs)
        self.solution_set = is_solution
        self.center.update(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.not_pressed_tag = "off"
        self.pressed_tag = "on"
        self.visible = False
        self.inp = k4pg.Input()

    def load_sprite(self, *args, **kwargs):
        super(OnOffToggle, self).load_sprite(*args, **kwargs)
        self.set_tag("gfx")

    def update(self, cam: k4pg.Camera):
        if self.inp.get_mouse_down(1):
            mouse_pos = self.inp.get_mouse_pos()
            if self.get_screen_rect(cam)[0].collidepoint(mouse_pos[0], mouse_pos[1]):
                self.visible = not self.visible

    def draw(self, cam: k4pg.Camera):
        super(OnOffToggle, self).draw(cam)
        if conf.DEBUG:
            k4pg.draw.rect(cam, pg.Color(0, 255, 0), self.get_world_rect(), width=2)


class OnOff(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.options = []
        super(OnOff, self).__init__(puzzle_data)
        
    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x14:
            x, y, path, solution_set, _ = cmd.params
            option = OnOffToggle(solution_set == 1, position=pg.Vector2(-256//2 + x, -192//2 + y))
            self.sprite_loader.load(f"data_lt2/ani/nazo/onoff/{path}", option)
            self.options.append(option)

    def check_solution(self):
        for option in self.options:
            option: OnOffToggle
            if option.visible != option.solution_set:
                return False
        return True

    def update_submitted(self, dt):
        for option in self.options:
            option: OnOffToggle
            option.update(self.btm_camera)
        return super(OnOff, self).update_submitted(dt)

    def draw_base(self):
        super(OnOff, self).draw_base()
        for option in self.options:
            option: OnOffToggle
            option.draw(self.btm_camera)
