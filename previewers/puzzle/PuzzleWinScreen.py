from pg_utils.TwoScreenRenderer import TwoScreenRenderer
from pg_utils.ScreenFader import ScreenFader
import formats.puzzle as pzd
import pg_engine as pge
import pygame as pg


class PuzzleWinScreen(TwoScreenRenderer):
    # Progressive state machine
    STATE_FADE_OUT = 0
    STATE_JUDGE_CHAR = 1
    STATE_MOVE_UP = 2
    STATE_PICARATS = 3
    STATE_FADE_OUT2 = 4
    STATE_TEXT = 5
    STATE_FADE_OUT3 = 6
    STATE_FAIL_BTN = 7
    STATE_RETURN = 7

    def __init__(self, puzzle_data: pzd.Puzzle, spr_loader, fnt_loader):
        super(PuzzleWinScreen, self).__init__()

        self.puzzle_data = puzzle_data
        self.inp = pge.Input()

        self.sprite_loader: pge.SpriteLoader = spr_loader
        self.font_loader: pge.FontLoader = fnt_loader

        self.fader = ScreenFader()
        self.fader.fade_time = .2
        self.fader.load_fader()

        self.is_correct = False
        self.stage = self.STATE_FADE_OUT

        self.bg_id = 0
        self.bg_timer = 0
        self.bg_anim_time = 4 / 60
        self.bg_hold_time = 36 / 60
        self.bg_clear_time = 10 / 60
        self.clearing = False
        self.bg = pge.Sprite()
        self.bg2 = pge.Sprite()

        self.picarats_bg = pge.Sprite()
        self.sprite_loader.load("data_lt2/bg/nazo/system/?/picarat_get.arc", self.picarats_bg, sprite_sheet=False)

        self.btm_text = pge.Text(position=[-256//2 + 8, -192 // 2 + 15],
                                 center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                                 color=pg.Color(0, 0, 0),
                                 line_spacing=2)
        self.text = ""
        self.text_pos = 0
        self.between_letters = 0.017
        self.current_between_letters = 0.0
        self.font_loader.load("fontq", 10, self.btm_text)

        self.bg_move_up_time = 0.4
        self.fade_in = False

        self.retry_btn = pge.Button()
        self.hints_btn = pge.Button()
        self.quit_btn = pge.Button()

    def enter(self, correct):
        self.enter_state(self.STATE_FADE_OUT)
        self.is_correct = correct
        if self.is_correct:
            self.btm_text.position[1] = -192 // 2 + 23
        else:
            self.btm_text.position[1] = -192 // 2 + 15

    def enter_state(self, state):
        self.stage = state
        if self.stage == self.STATE_FADE_OUT:
            self.fader.fade_out(False)
        elif self.stage == self.STATE_JUDGE_CHAR:
            self.bg_id = 1
            self.load_bg()
            self.bg_timer = self.bg_anim_time
            self.clearing = False
        elif self.stage == self.STATE_MOVE_UP:
            self.bg.position[1] = 192
            self.bg_timer = self.bg_move_up_time
            self.fader.fade_in(None)
        elif self.stage == self.STATE_PICARATS:
            self.fader.fade_in(None)
        elif self.stage == self.STATE_FADE_OUT2:
            self.fader.fade_out(None)
        elif self.stage == self.STATE_TEXT:
            self.fader.fade_in(None)
            self.current_between_letters = 0
            self.text_pos = 0
            if self.is_correct:
                self.text = self.puzzle_data.correct_answer
            else:
                self.text = self.puzzle_data.incorrect_answer

            if self.is_correct:
                filename = f"nazo_seikai{self.puzzle_data.bg_location_id}.arc"
                if self.puzzle_data.ans_bg_lang:
                    ans_bg_path = "data_lt2/bg/nazo/?/"
                else:
                    ans_bg_path = "data_lt2/bg/nazo/"
                ans_filename = f"q{self.puzzle_data.internal_id}a.arc"
                self.sprite_loader.load(ans_bg_path + ans_filename, self.bg, sprite_sheet=False)
            else:
                filename = f"nazo_fail{self.puzzle_data.bg_location_id}.arc"
            self.sprite_loader.load(f"data_lt2/bg/nazo/system/{filename}", self.bg2, sprite_sheet=False)
        elif self.stage == self.STATE_FADE_OUT3:
            self.fader.fade_out(False)
        elif self.stage == self.STATE_FAIL_BTN:
            self.sprite_loader.load(f"data_lt2/bg/nazo/system/jiten_seikai.arc", self.bg2, sprite_sheet=False)
            self.fader.fade_in(False)

    def update(self, dt: float):
        if self.stage == self.STATE_FADE_OUT:
            self.fader.update(dt)
            if not self.fader.fading:
                self.enter_state(self.STATE_JUDGE_CHAR)
        if self.stage == self.STATE_JUDGE_CHAR:
            self.bg_timer -= dt
            if not self.clearing:
                if self.bg_timer <= 0:
                    if self.bg_id in [3, 6, 9, 13]:
                        self.clearing = True
                        self.bg_timer = self.bg_clear_time
                    else:
                        self.progress_bg()
            else:
                self.bg.alpha = (self.bg_timer/self.bg_clear_time) * 255
                if self.bg_timer <= 0:
                    self.clearing = False
                    self.bg.alpha = 255
                    self.progress_bg()
            if self.bg_id == 14:
                self.enter_state(self.STATE_MOVE_UP)
        if self.stage == self.STATE_MOVE_UP:
            self.fader.update(dt)
            if not self.fader.fading:
                self.bg_timer -= dt
                self.bg.position[1] = 192 * (self.bg_timer / self.bg_move_up_time)
                if self.bg_timer <= 0:
                    self.bg.position[1] = 0
                    self.enter_state(self.STATE_PICARATS)
        if self.stage == self.STATE_PICARATS:
            self.fader.update(dt)
            if self.inp.get_mouse_down(1):
                if not self.fader.fading:
                    self.enter_state(self.STATE_FADE_OUT2)
        if self.stage == self.STATE_FADE_OUT2:
            self.fader.update(dt)
            if not self.fader.fading:
                self.enter_state(self.STATE_TEXT)
        if self.stage == self.STATE_TEXT:
            self.fader.update(dt)
            if not self.fader.fading:
                self.current_between_letters += dt
                while self.current_between_letters > self.between_letters:
                    self.text_pos += 1
                    self.current_between_letters -= self.between_letters
                self.text_pos = min(self.text_pos, len(self.text))
                if self.inp.get_mouse_down(1):
                    if self.text_pos == len(self.text):
                        if self.is_correct:
                            self.enter_state(self.STATE_RETURN)
                        else:
                            self.enter_state(self.STATE_FADE_OUT3)
                    else:
                        self.text_pos = len(self.text)
                self.btm_text.text = self.text[:self.text_pos]
        if self.stage == self.STATE_FADE_OUT3:
            self.fader.update(dt)
            if not self.fader.fading:
                self.enter_state(self.STATE_FAIL_BTN)
        if self.stage == self.STATE_RETURN:
            return False
        return True

    def progress_bg(self):
        self.bg_id += 1
        self.load_bg()
        self.bg_timer = self.bg_anim_time
        if self.bg_id in [3, 6, 9, 13]:
            self.bg_timer = self.bg_hold_time
            if self.bg_id == 13:
                self.bg_timer *= 2

    def load_bg(self):
        bid = self.bg_id
        if self.bg_id < 14:
            bg_path = f"data_lt2/bg/nazo/hantei/"
        else:
            bg_path = f"data_lt2/bg/nazo/hantei/?/"
        if not self.is_correct and bid >= 7:
            bid += 100
        bg_name = f"judge_{'r' if self.puzzle_data.judge_char == 0 else 'l'}{bid}_bg.arc"
        self.sprite_loader.load(bg_path + bg_name, self.bg, sprite_sheet=False)

    def draw(self):
        if self.stage == self.STATE_FADE_OUT:
            self.fader.draw(self.btm_camera)
            self.fader.draw(self.top_camera)
        elif self.stage == self.STATE_JUDGE_CHAR:
            self.clear()
            self.bg.draw(self.btm_camera)
        elif self.stage == self.STATE_MOVE_UP:
            self.clear()
            self.bg.draw(self.top_camera)
            self.bg.position[1] -= 192
            self.bg.draw(self.btm_camera)
            self.bg.position[1] += 192
            self.fader.draw(self.btm_camera)
        elif self.stage == self.STATE_PICARATS:
            self.bg.draw(self.top_camera)
            self.picarats_bg.draw(self.btm_camera)
            self.fader.draw(self.btm_camera)
        elif self.stage == self.STATE_FADE_OUT2:
            self.bg.draw(self.top_camera)
            self.picarats_bg.draw(self.btm_camera)
            self.fader.draw(self.btm_camera)
            if self.is_correct:
                self.fader.draw(self.top_camera)
        elif self.stage == self.STATE_TEXT:
            self.bg.draw(self.top_camera)
            self.bg2.draw(self.btm_camera)
            self.btm_text.draw(self.btm_camera)
            self.fader.draw(self.btm_camera)
            if self.is_correct:
                self.fader.draw(self.top_camera)
        elif self.stage == self.STATE_FADE_OUT3:
            self.bg.draw(self.top_camera)
            self.bg2.draw(self.btm_camera)
            self.btm_text.draw(self.btm_camera)
            self.fader.draw(self.btm_camera)
        elif self.stage == self.STATE_FAIL_BTN:
            self.bg.draw(self.top_camera)
            self.bg2.draw(self.btm_camera)
            self.fader.draw(self.btm_camera)
