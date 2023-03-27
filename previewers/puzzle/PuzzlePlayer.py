from pg_utils.rom.RomSingleton import RomSingleton
import formats.puzzle as pzd
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
import k4pg
import pygame as pg

from pg_utils.rom.rom_extract import load_smd
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer

from .PuzzleHints import PuzzleHints
from .PuzzleWinScreen import PuzzleWinScreen


class PuzzlePlayer(TwoScreenRenderer):
    MUSIC_ACTIVE = False

    def __init__(self, puzzle_data: pzd.Puzzle):
        super(PuzzlePlayer, self).__init__()
        self.show_cursor_pos = True

        self.text_pos = 0
        self.between_letters = 0.017
        self.current_between_letters = 0.0
        self.puzzle_data = puzzle_data

        self.inp = k4pg.Input()

        self.sprite_loader: k4pg.SpriteLoader = RomSingleton().get_sprite_loader()
        self.sprite_loader_os = k4pg.SpriteLoaderOS(base_path_os="data_permanent/sprites")
        self.font_loader: k4pg.FontLoader = RomSingleton().get_font_loader()

        self.top_bg = k4pg.Sprite()
        self.sprite_loader.load(f"data_lt2/bg/nazo/system/nazo_text{puzzle_data.bg_location_id}.arc", self.top_bg,
                                sprite_sheet=False)

        self.btm_bg = k4pg.Sprite()
        if not puzzle_data.bg_lang:
            self.sprite_loader.load(f"data_lt2/bg/nazo/q{puzzle_data.bg_btm_id}", self.btm_bg, False)
        else:
            self.sprite_loader.load(f"data_lt2/bg/nazo/?/q{puzzle_data.bg_btm_id}.arc", self.btm_bg, False)

        self.top_text = k4pg.Text(position=pg.Vector2(-256//2 + 8, -192 // 2 + 23),
                                  center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                                  color=pg.Color(0, 0, 0),
                                  line_spacing=2)
        self.font_loader.load("fontq", 10, self.top_text)

        self.header_top_left = []
        for i in range(4):
            header_item = k4pg.Sprite(center=pg.Vector2(k4pg.Alignment.TOP, k4pg.Alignment.LEFT))
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/nazo_text.arc", header_item, True)
            if i == 0:
                header_item.set_tag("nazo")
                header_item.position.update(-256 // 2 + 5, -192 // 2 + 4)
            else:
                i -= 1
                p_num = puzzle_data.number
                for a in range(2 - i):
                    p_num //= 10
                header_item.set_tag(str(p_num % 10))
                header_item.position.update(-256 // 2 + 23 + i * 7, -192 // 2 + 5)
            self.header_top_left.append(header_item)

        btn_off = "off"
        btn_on = "on"

        current_y = -192 // 2
        self.hints_btn = k4pg.ButtonSprite(center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.TOP),
                                           position=pg.Vector2(256 // 2, current_y), not_pressed_tag="0_off",
                                           pressed_tag="0_on")
        self.sprite_loader.load("data_lt2/ani/system/btn/?/hint.arc", self.hints_btn, True)

        current_y += self.hints_btn.get_world_rect().h
        self.quit_btn = k4pg.ButtonSprite(center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.TOP),
                                          position=pg.Vector2(256 // 2, current_y), not_pressed_tag=btn_off,
                                          pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/atode.arc", self.quit_btn, True)

        current_y += self.quit_btn.get_world_rect().h
        self.memo_btn = k4pg.ButtonSprite(center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.TOP),
                                          position=pg.Vector2(256//2, current_y), not_pressed_tag=btn_off,
                                          pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/memo.arc", self.memo_btn, True)

        current_y += self.memo_btn.get_world_rect().h
        self.reset_btn = k4pg.ButtonSprite(position=pg.Vector2(256 // 2, current_y),
                                           center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.TOP),
                                           not_pressed_tag="off", pressed_tag="on")
        self.sprite_loader.load("data_lt2/ani/system/btn/?/reset.arc", self.reset_btn, True)

        self.submit_btn = k4pg.ButtonSprite(center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.BOTTOM),
                                            position=pg.Vector2(256//2, 192//2), not_pressed_tag=btn_off,
                                            pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/hantei.arc", self.submit_btn, True)

        self.hints = PuzzleHints(self.puzzle_data, self.sprite_loader, self.font_loader)
        self.on_hints = False

        smd, swd_file, sample_bank = load_smd("data_lt2/sound/BG_035.SMD")
        self.puzzle_music = SMDLStreamPlayer(loops=True)
        self.puzzle_music.set_volume(0.5 if PuzzlePlayer.MUSIC_ACTIVE else 0)
        self.puzzle_music.create_temporal_sf2(swd_file, sample_bank)
        self.puzzle_music.load_sound(smd)
        self.puzzle_music.play()

        self.win_screen = PuzzleWinScreen(self.puzzle_data, self.sprite_loader, self.font_loader, self.hints,
                                          self.puzzle_music)
        self.on_win = False

        self.run_gds()

        self.music_toggle = k4pg.ButtonSprite(pressed_counter=0.05)
        self.music_toggle.position = pg.Vector2(-128 + 5, -96 + 5)
        self.music_toggle.scale = pg.Vector2(0.5, 0.5)
        self.music_toggle.center = pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.sprite_loader_os.load("music_active.png", self.music_toggle, sprite_sheet=True, convert_alpha=False)
        self.music_toggle.color_key = pg.Color(0, 255, 0)
        self.music_toggle.set_tag("OFF" if PuzzlePlayer.MUSIC_ACTIVE else "ON")

    def run_gds_cmd(self, cmd):
        pass

    def run_gds(self):
        for cmd in self.puzzle_data.gds.commands:
            self.run_gds_cmd(cmd)

    def update_submitted(self, dt):
        if self.submit_btn.get_pressed(self.btm_camera):
            return True
        return False

    def check_solution(self):
        return self.inp.get_key(pg.K_y)

    def unload(self):
        self.puzzle_music.stop()

    def update(self, dt: float):
        self.puzzle_music.update(dt)

        if self.on_hints:
            self.on_hints = self.hints.update(dt)
            if not self.on_hints:
                self.hints_btn.not_pressed_tag = f"{self.hints.used}_off"
                self.hints_btn.pressed_tag = f"{self.hints.used}_on"
        elif self.on_win:
            self.hints_btn.animate(dt)
            self.quit_btn.animate(dt)
            self.memo_btn.animate(dt)
            self.submit_btn.animate(dt)
            self.on_win = self.win_screen.update(dt)
        else:
            self.update_base(dt)

    def update_base(self, dt: float):
        self.hints_btn.animate(dt)
        self.quit_btn.animate(dt)
        self.memo_btn.animate(dt)
        self.submit_btn.animate(dt)
        self.reset_btn.animate(dt)

        if self.music_toggle.get_pressed(self.btm_camera):
            PuzzlePlayer.MUSIC_ACTIVE = not PuzzlePlayer.MUSIC_ACTIVE
            self.music_toggle.set_tag("OFF" if PuzzlePlayer.MUSIC_ACTIVE else "ON")
            self.puzzle_music.set_volume(0.5 if PuzzlePlayer.MUSIC_ACTIVE else 0)

        if self.text_pos < len(self.puzzle_data.text):
            self.current_between_letters += dt
            while self.current_between_letters > self.between_letters:
                self.text_pos += 1
                self.current_between_letters -= self.between_letters
            if self.inp.get_mouse_down(1):
                self.text_pos = len(self.puzzle_data.text)
            self.text_pos = min(self.text_pos, len(self.puzzle_data.text))
            self.top_text.text = self.puzzle_data.text[:self.text_pos]
            return

        if self.hints_btn.get_pressed(self.btm_camera):
            self.hints.view_hint(min(2, self.hints.used))
            self.on_hints = True
            return
        self.quit_btn.get_pressed(self.btm_camera)
        self.memo_btn.get_pressed(self.btm_camera)
        if self.reset_btn.get_pressed(self.btm_camera):
            self.restart()
            return
        if self.update_submitted(dt):
            self.win_screen.enter(self.check_solution())
            self.on_win = True
            self.puzzle_music.fade(1, False)
            return
        super(PuzzlePlayer, self).update(dt)

    def restart(self):
        pass

    def draw(self):
        self.top_bg.draw(self.top_camera)
        for header in self.header_top_left:
            header.draw(self.top_camera)
        self.top_text.draw(self.top_camera)

        if self.on_hints:
            self.hints.draw()
        elif self.on_win:
            self.draw_base()
            self.win_screen.draw()
        else:
            self.draw_base()

    def draw_base(self):
        self.btm_bg.draw(self.btm_camera)
        self.hints_btn.draw(self.btm_camera)
        self.quit_btn.draw(self.btm_camera)
        self.memo_btn.draw(self.btm_camera)
        self.submit_btn.draw(self.btm_camera)
        self.reset_btn.draw(self.btm_camera)
        self.music_toggle.draw(self.btm_camera)
        super(PuzzlePlayer, self).draw()
