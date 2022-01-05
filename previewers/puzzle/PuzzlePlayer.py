from typing import List

from pg_utils.rom.RomSingleton import RomSingleton
import formats.puzzle as pzd
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
import pg_engine as pge
import pygame as pg

from pg_utils.rom.rom_extract import load_smd
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer


class PuzzlePlayer(TwoScreenRenderer):
    def __init__(self, puzzle_data: pzd.Puzzle):
        super(PuzzlePlayer, self).__init__()

        self.hints_used = 0
        self.selected_hint = 0
        self.text_pos = 0
        self.between_letters = 0.017
        self.current_between_letters = 0.0
        self.on_hints = False
        self.puzzle_data = puzzle_data

        self.inp = pge.Input()

        self.sprite_loader: pge.SpriteLoader = RomSingleton().get_sprite_loader()
        self.font_loader: pge.FontLoader = RomSingleton().get_font_loader()

        self.top_bg = pge.Sprite()
        self.sprite_loader.load(f"data_lt2/bg/nazo/system/nazo_text{puzzle_data.bg_top_id}.arc", self.top_bg,
                                sprite_sheet=False)

        self.btm_bg = pge.Sprite()
        if not puzzle_data.bg_lang:
            self.sprite_loader.load(f"data_lt2/bg/nazo/q{puzzle_data.internal_id}.arc", self.btm_bg, sprite_sheet=False)
        else:
            self.sprite_loader.load(f"data_lt2/bg/nazo/?/q{puzzle_data.internal_id}.arc", self.btm_bg,
                                    sprite_sheet=False)

        self.top_text = pge.Text(position=[-256//2 + 8, -192 // 2 + 23],
                                 center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                                 color=pg.Color(0, 0, 0),
                                 line_spacing=2)
        self.font_loader.load("fontq", 10, self.top_text)

        self.header_top_left = []
        for i in range(4):
            header_item = pge.Sprite(center=[pge.Alignment.TOP, pge.Alignment.LEFT])
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/nazo_text.arc", header_item, sprite_sheet=True)
            if i == 0:
                header_item.set_tag("nazo")
                header_item.position = [-256 // 2 + 5, -192 // 2 + 4]
            else:
                i -= 1
                p_num = puzzle_data.number
                for a in range(2 - i):
                    p_num //= 10
                header_item.set_tag(str(p_num % 10))
                header_item.position = [-256 // 2 + 23 + i * 7, -192 // 2 + 5]
            self.header_top_left.append(header_item)

        self.hint_bg = pge.Sprite()

        btn_off = "off"
        btn_on = "on"

        current_y = -192 // 2
        self.hints_btn = pge.Button(center=[pge.Alignment.RIGHT, pge.Alignment.TOP],
                                    position=[256 // 2, current_y], not_pressed_tag="0_off",
                                    pressed_tag="0_on")
        self.sprite_loader.load("data_lt2/ani/system/btn/?/hint.arc", self.hints_btn, sprite_sheet=True)

        current_y += self.hints_btn.get_world_rect().h
        self.quit_btn = pge.Button(center=[pge.Alignment.RIGHT, pge.Alignment.TOP],
                                   position=[256 // 2, current_y], not_pressed_tag=btn_off,
                                   pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/atode.arc", self.quit_btn, sprite_sheet=True)

        current_y += self.quit_btn.get_world_rect().h
        self.memo_btn = pge.Button(center=[pge.Alignment.RIGHT, pge.Alignment.TOP],
                                   position=[256//2, current_y], not_pressed_tag=btn_off,
                                   pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/memo.arc", self.memo_btn, sprite_sheet=True)

        self.submit_btn = pge.Button(center=[pge.Alignment.RIGHT, pge.Alignment.BOTTOM],
                                     position=[256//2, 192//2], not_pressed_tag=btn_off,
                                     pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/hantei.arc", self.submit_btn, sprite_sheet=True)

        self.hint_back = pge.Button(position=[256 // 2, -192 // 2],
                                    center=[pge.Alignment.RIGHT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                    pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/modoru_memo.arc", self.hint_back, sprite_sheet=True)

        self.hint_unlock = pge.Button(position=[-80, 40],
                                      center=[pge.Alignment.LEFT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                      pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/yes.arc", self.hint_unlock, sprite_sheet=True)

        self.hint_no_unlock = pge.Button(position=[80, 40],
                                         center=[pge.Alignment.RIGHT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                         pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/no.arc", self.hint_no_unlock, sprite_sheet=True)

        self.hint_text = pge.Text(position=[-256 // 2 + 20, -192 // 2 + 42],
                                  center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                                  color=pg.Color(0, 0, 0))
        self.font_loader.load("fontq", 10, self.hint_text)

        self.hint_selected: List[pge.Button] = []

        current_x = -256 // 2 + 8
        for i in range(3):
            hint_select = pge.Button(position=[current_x, -192 // 2 + 4],
                                     center=[pge.Alignment.LEFT, pge.Alignment.TOP], not_pressed_tag="OFF",
                                     pressed_tag="ON")
            hint_select.visible = False
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/hint{i + 1}.arc", hint_select, sprite_sheet=True)
            current_x += hint_select.get_world_rect().w + 1
            self.hint_selected.append(hint_select)

        self.view_hint(self.progress_hints(set_hint=0))

        smd, presets = load_smd("data_lt2/sound/BG_035.SMD")
        self.puzzle_bg_music = SMDLStreamPlayer()
        self.puzzle_bg_music.set_volume(0.5)
        self.puzzle_bg_music.set_preset_dict(presets)
        self.puzzle_bg_music.start_sound(smd, loops=True)

    def unload(self):
        self.puzzle_bg_music.stop()

    def progress_hints(self, set_hint=None):
        if set_hint is not None:
            self.hints_used = set_hint
        else:
            self.hints_used += 1
        self.hints_btn.not_pressed_tag = f"{self.hints_used}_off"
        self.hints_btn.pressed_tag = f"{self.hints_used}_on"
        if self.hints_used > 0:
            hint_sprite = self.hint_selected[self.hints_used - 1]
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/hint{self.hints_used}.arc", hint_sprite,
                                    sprite_sheet=True)
        if self.hints_used < 3:
            hint_sprite = self.hint_selected[self.hints_used]
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/hintlock{self.hints_used + 1}.arc", hint_sprite,
                                    sprite_sheet=True)
            hint_sprite.visible = True
        return self.hints_used

    def view_hint(self, hint_num):
        self.selected_hint = hint_num
        if self.hints_used > hint_num:
            self.sprite_loader.load(f"data_lt2/bg/nazo/system/?/hint_{hint_num + 1}.arc", self.hint_bg,
                                    sprite_sheet=False)
            if hint_num == 0:
                self.hint_text.text = self.puzzle_data.hint1
            elif hint_num == 1:
                self.hint_text.text = self.puzzle_data.hint2
            elif hint_num == 2:
                self.hint_text.text = self.puzzle_data.hint3
        else:
            self.sprite_loader.load(f"data_lt2/bg/nazo/system/?/jitenhint_{hint_num + 1}.arc", self.hint_bg,
                                    sprite_sheet=False)

    def update(self, dt: float):
        self.puzzle_bg_music.update_(dt)
        if self.text_pos < len(self.puzzle_data.text):
            self.current_between_letters += dt
            while self.current_between_letters > self.between_letters:
                self.text_pos += 1
                self.current_between_letters -= self.between_letters
            if self.inp.get_mouse_down(1):
                self.text_pos = len(self.puzzle_data.text)
            self.text_pos = min(self.text_pos, len(self.puzzle_data.text))
            self.top_text.text = self.puzzle_data.text[:self.text_pos]

        if not self.on_hints:
            self.update_base(dt)
        else:
            self.update_hints(dt)

    def update_base(self, dt: float):
        if self.hints_btn.pressed(self.btm_camera, dt):
            self.view_hint(min(2, self.hints_used))
            self.on_hints = True
            return
        self.quit_btn.pressed(self.btm_camera, dt)
        self.memo_btn.pressed(self.btm_camera, dt)
        self.submit_btn.pressed(self.btm_camera, dt)

        self.hints_btn.animate(dt)
        self.quit_btn.animate(dt)
        self.memo_btn.animate(dt)
        self.submit_btn.animate(dt)

    def update_hints(self, dt: float):
        if self.hint_back.pressed(self.btm_camera, dt):
            self.on_hints = False
            return
        self.hint_back.animate(dt)

        for i in range(min(3, self.hints_used + 1)):
            if self.hint_selected[i].pressed(self.btm_camera, dt):
                self.view_hint(i)
            self.hint_selected[i].animate(dt)

        if self.selected_hint == self.hints_used:
            if self.hint_unlock.pressed(self.btm_camera, dt):
                self.view_hint(self.progress_hints() - 1)
            self.hint_unlock.animate(dt)

            if self.hint_no_unlock.pressed(self.btm_camera, dt):
                self.on_hints = False
                return
            self.hint_no_unlock.animate(dt)

    def draw(self):
        self.top_bg.draw(self.top_camera)
        for header in self.header_top_left:
            header.draw(self.top_camera)
        self.top_text.draw(self.top_camera)

        if not self.on_hints:
            self.draw_base()
        else:
            self.draw_hints()

    def draw_base(self):
        self.btm_bg.draw(self.btm_camera)
        self.hints_btn.draw(self.btm_camera)
        self.quit_btn.draw(self.btm_camera)
        self.memo_btn.draw(self.btm_camera)
        self.submit_btn.draw(self.btm_camera)

    def draw_hints(self):
        self.hint_bg.draw(self.btm_camera)
        if self.selected_hint == self.hints_used:
            self.hint_unlock.draw(self.btm_camera)
            self.hint_no_unlock.draw(self.btm_camera)
        else:
            self.hint_text.draw(self.btm_camera)
        self.hint_back.draw(self.btm_camera)
        for hint_select in self.hint_selected:
            hint_select.draw(self.btm_camera)
