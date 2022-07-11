from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
import k4pg
import pygame as pg


class NullPuzzle(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        super(NullPuzzle, self).__init__(puzzle_data)
        self.submit_btn.visible = False

        self.no_btn = k4pg.ButtonSprite(center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.BOTTOM),
                                        position=pg.Vector2(256//2, 192//2), pressed_tag="on", not_pressed_tag="off")
        self.sprite_loader.load("data_lt2/ani/system/btn/?/no.arc", self.no_btn)

        self.yes_btn = k4pg.ButtonSprite(center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.BOTTOM),
                                         position=pg.Vector2(256//2, 192//2 - self.no_btn.get_world_rect().h),
                                         pressed_tag="on", not_pressed_tag="off")
        self.sprite_loader.load("data_lt2/ani/system/btn/?/yes.arc", self.yes_btn)

        self.is_correct = False

    def update_submitted(self, dt):
        if self.no_btn.get_pressed(self.btm_camera, dt):
            self.is_correct = False
            return True
        elif self.yes_btn.get_pressed(self.btm_camera, dt):
            self.is_correct = True
            return True
        self.no_btn.animate(dt)
        self.yes_btn.animate(dt)
        return False

    def check_solution(self):
        return self.is_correct

    def draw_base(self):
        super(NullPuzzle, self).draw_base()
        self.no_btn.draw(self.btm_camera)
        self.yes_btn.draw(self.btm_camera)
