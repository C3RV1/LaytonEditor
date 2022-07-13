from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
from formats.gds import GDSCommand
import k4pg
import pygame as pg
import string


class Write(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.write_bg = k4pg.Sprite()
        self.writing_answer = False
        self.answer = ""
        self.current_ans = ""
        self.input_len = 1
        self.allowed_chars = string.ascii_lowercase if puzzle_data.type == Puzzle.WRITE_CHARS else string.digits

        super(Write, self).__init__(puzzle_data)
        self.reset_btn.visible = False

        self.sprite_loader.load("data_lt2/ani/nazo/drawinput/?/di_hantei.arc", self.submit_btn)
        self.submit_btn.position.update(0, 192//2)
        self.submit_btn.center.update(k4pg.Alignment.CENTER, k4pg.Alignment.BOTTOM)
        self.submit_btn.visible = False

        self.write_ans_btn = k4pg.ButtonSprite(position=pg.Vector2(256//2, 192//2),
                                               center=pg.Vector2(k4pg.Alignment.RIGHT,
                                                                 k4pg.Alignment.BOTTOM),
                                               not_pressed_tag="off",
                                               pressed_tag="on")
        self.sprite_loader.load("data_lt2/ani/nazo/drawinput/?/di_kaito.arc", self.write_ans_btn)

        pos = pg.Vector2(self.hints_btn.get_world_rect().bottomright)
        self.clear_btn = k4pg.ButtonSprite(position=pos, center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.TOP),
                                           not_pressed_tag="off", pressed_tag="on")
        self.sprite_loader.load("data_lt2/ani/nazo/drawinput/?/di_allreset.arc", self.clear_btn)
        self.clear_btn.visible = False

        self.back_btn = k4pg.ButtonSprite(position=pg.Vector2(256//2, 192//2),
                                          center=pg.Vector2(k4pg.Alignment.RIGHT,
                                                            k4pg.Alignment.BOTTOM),
                                          not_pressed_tag="off", pressed_tag="on")
        self.sprite_loader.load("data_lt2/ani/nazo/drawinput/?/di_modoru.arc", self.back_btn)
        self.back_btn.visible = False

        input_text_positions = {
            1: pg.Vector2(0, -75),
            2: pg.Vector2(0, -75),
            3: pg.Vector2(0, -70),
            4: pg.Vector2(0, -70)
        }
        self.input_text = k4pg.Text(position=input_text_positions[self.input_len],
                                    center=pg.Vector2(k4pg.Alignment.CENTER, k4pg.Alignment.TOP),
                                    color=pg.Color(0, 0, 0))
        if self.puzzle_data.type == Puzzle.WRITE_ALT:
            self.input_text.position.update(0, -70)
        self.font_loader.load("font18", 12, self.input_text)
        self.input_text.visible = False

    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x43:
            self.sprite_loader.load(f"data_lt2/bg/nazo/drawinput/{cmd.params[0]}", self.write_bg)
        elif cmd.command == 0x42:
            self.answer = cmd.params[1]
        elif cmd.command == 0x41:
            unk1, unk2, unk3, self.input_len = cmd.params

    def enter_writing(self):
        self.writing_answer = True
        self.write_ans_btn.visible = False
        self.btm_bg.visible = False
        self.write_bg.visible = True
        self.submit_btn.visible = True
        self.clear_btn.visible = True
        self.back_btn.visible = True
        self.input_text.visible = True

        self.quit_btn.visible = False
        self.memo_btn.visible = False

    def exit_writing(self):
        self.writing_answer = False
        self.write_ans_btn.visible = True
        self.btm_bg.visible = True
        self.write_bg.visible = False
        self.submit_btn.visible = False
        self.clear_btn.visible = False
        self.back_btn.visible = False
        self.input_text.visible = False

        self.quit_btn.visible = True
        self.memo_btn.visible = True

    def check_solution(self):
        return self.answer == self.current_ans

    def update_base(self, dt: float):
        self.write_ans_btn.animate(dt)
        self.clear_btn.animate(dt)
        self.back_btn.animate(dt)
        super(Write, self).update_base(dt)
        if self.write_ans_btn.get_pressed(self.btm_camera, dt):
            self.enter_writing()
        if self.clear_btn.get_pressed(self.btm_camera, dt):
            self.current_ans = ""
        if self.back_btn.get_pressed(self.btm_camera, dt):
            self.exit_writing()
        if self.writing_answer:
            for char in self.allowed_chars:
                if self.inp.get_key_down(ord(char)):
                    self.current_ans += char
                    self.current_ans = self.current_ans[:self.input_len]
            if self.inp.get_key_down(pg.K_BACKSPACE):
                self.current_ans = self.current_ans[:-1]
            self.update_visual_text()

    def update_visual_text(self):
        ans = []
        for i in range(self.input_len):
            if i < len(self.current_ans):
                ans.append(self.current_ans[i])
            else:
                ans.append(" ")
        if self.puzzle_data.type == Puzzle.WRITE_DATE:
            self.input_text.text = f"{ans[0]} {ans[1]}   {ans[2]} {ans[3]}"
            return
        join_chars = "  " if self.input_len < 4 else " "
        if self.puzzle_data.type == Puzzle.WRITE_ALT:
            join_chars = "    "
        self.input_text.text = join_chars.join(ans).upper()

    def draw_base(self):
        self.write_bg.draw(self.btm_camera)
        super(Write, self).draw_base()
        self.write_ans_btn.draw(self.btm_camera)
        self.clear_btn.draw(self.btm_camera)
        self.back_btn.draw(self.btm_camera)
        self.input_text.draw(self.btm_camera)
