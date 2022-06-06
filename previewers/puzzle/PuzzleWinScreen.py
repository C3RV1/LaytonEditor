from pg_utils.TwoScreenRenderer import TwoScreenRenderer
from pg_utils.ScreenFader import ScreenFader
import formats.puzzle as pzd
import pg_engine as pge


class PuzzleWinScreen(TwoScreenRenderer):
    def __init__(self, puzzle_data: pzd.Puzzle, spr_loader, fnt_loader):
        super(PuzzleWinScreen, self).__init__()

        self.puzzle_data = puzzle_data

        self.sprite_loader: pge.SpriteLoader = spr_loader
        self.font_loader: pge.FontLoader = fnt_loader

        self.fader = ScreenFader()
        self.fader.load_fader()

        self.is_correct = False
        self.stage = 0

        self.bg_id = 0
        self.bg_timer = 0
        self.bg_anim_time = 4 / 60
        self.bg_hold_time = 36 / 60
        self.bg_clear_time = 10 / 60
        self.clearing = False
        self.bg = pge.Sprite()

    def enter(self, correct):
        self.fader.fade_out(False)
        self.stage = 0
        self.is_correct = correct

    def update(self, dt: float):
        if self.stage == 0:
            self.fader.update(dt)
            if not self.fader.fading:
                self.stage += 1
                self.bg_id = 1
                self.load_bg()
                self.bg_timer = self.bg_anim_time
                self.clearing = False
            else:
                return True
        if self.stage == 1:
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
                self.stage += 1
            return True
        return False

    def progress_bg(self):
        self.bg_id += 1
        self.load_bg()
        self.bg_timer = self.bg_anim_time
        if self.bg_id in [3, 6, 9, 13]:
            self.bg_timer = self.bg_hold_time

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
        if self.stage == 0:
            self.fader.draw(self.btm_camera)
            self.fader.draw(self.top_camera)
        elif self.stage == 1:
            self.clear()
            self.bg.draw(self.btm_camera)
