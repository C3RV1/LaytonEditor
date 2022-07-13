from typing import Optional

from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
from formats.gds import GDSCommand
import k4pg
import pygame as pg
from formats import conf


class MultipleChoiceButton(k4pg.ButtonSprite):
    def __init__(self, is_solution, *args, **kwargs):
        super(MultipleChoiceButton, self).__init__(*args, **kwargs,
                                                   not_pressed_tag="off",
                                                   pressed_tag="on")
        self.center.update(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.is_solution: bool = is_solution

    def draw(self, cam: k4pg.Camera):
        super(MultipleChoiceButton, self).draw(cam)
        if conf.DEBUG:
            k4pg.draw.rect(cam, pg.Color(0, 255, 0), self.get_world_rect(), width=2)


class MultipleChoice(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.buttons = []
        self.pressed_btn: Optional[MultipleChoiceButton] = None

        super(MultipleChoice, self).__init__(puzzle_data)
        self.submit_btn.visible = False
        self.reset_btn.visible = False

    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x14:  # add_button
            x, y, path, is_solution, _ = cmd.params
            btn = MultipleChoiceButton(is_solution == 1, position=pg.Vector2(-256//2 + x, -192//2 + y))
            self.sprite_loader.load(f"data_lt2/ani/nazo/freebutton/{path}", btn)
            self.buttons.append(btn)

    def update_submitted(self, dt):
        for button in self.buttons:
            if button.get_pressed(self.btm_camera, dt):
                self.pressed_btn = button
                button.animate(dt)
                return True
            button.animate(dt)
        return False

    def check_solution(self):
        return self.pressed_btn.is_solution

    def draw_base(self):
        super(MultipleChoice, self).draw_base()
        for button in self.buttons:
            button.draw(self.btm_camera)
