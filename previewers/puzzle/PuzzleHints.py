import formats.puzzle as pzd
from typing import List
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
import pg_engine as pge
import pygame as pg


class PuzzleHints(TwoScreenRenderer):
    def __init__(self, puzzle_data: pzd.Puzzle, spr_loader, fnt_loader):
        super(PuzzleHints, self).__init__()

        self.puzzle_data = puzzle_data

        self.sprite_loader: pge.SpriteLoader = spr_loader
        self.font_loader: pge.FontLoader = fnt_loader

        self.used = 0
        self.selected = 0

        self.bg = pge.Sprite()

        btn_off = "off"
        btn_on = "on"

        self.back_btn = pge.Button(position=[256 // 2, -192 // 2],
                                   center=[pge.Alignment.RIGHT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                   pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/modoru_memo.arc", self.back_btn, sprite_sheet=True)

        self.unlock_btn = pge.Button(position=[-80, 40],
                                     center=[pge.Alignment.LEFT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                     pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/yes.arc", self.unlock_btn, sprite_sheet=True)

        self.no_unlock_btn = pge.Button(position=[80, 40],
                                        center=[pge.Alignment.RIGHT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                        pressed_tag=btn_on)
        self.sprite_loader.load("data_lt2/ani/system/btn/?/no.arc", self.no_unlock_btn, sprite_sheet=True)

        self.text = pge.Text(position=[-256 // 2 + 20, -192 // 2 + 42],
                             center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                             color=pg.Color(0, 0, 0))
        self.font_loader.load("fontq", 10, self.text)

        self.selected_btns: List[pge.Button] = []

        current_x = -256 // 2 + 8
        for i in range(3):
            hint_select = pge.Button(position=[current_x, -192 // 2 + 4],
                                     center=[pge.Alignment.LEFT, pge.Alignment.TOP], not_pressed_tag=btn_off,
                                     pressed_tag=btn_on)
            hint_select.visible = False
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/hint{i + 1}.arc", hint_select, sprite_sheet=True)
            current_x += hint_select.get_world_rect().w + 1
            self.selected_btns.append(hint_select)

        self.view_hint(self.progress_hints(set_hint=0))

    def progress_hints(self, set_hint=None):
        if set_hint is not None:
            self.used = set_hint
        else:
            self.used += 1
        if self.used > 0:
            hint_sprite = self.selected_btns[self.used - 1]
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/hint{self.used}.arc", hint_sprite,
                                    sprite_sheet=True)
        if self.used < 3:
            hint_sprite = self.selected_btns[self.used]
            self.sprite_loader.load(f"data_lt2/ani/nazo/system/?/hintlock{self.used + 1}.arc", hint_sprite,
                                    sprite_sheet=True)
            hint_sprite.visible = True
        return self.used

    def view_hint(self, hint_num):
        self.selected = hint_num
        if self.used > hint_num:
            self.sprite_loader.load(f"data_lt2/bg/nazo/system/?/hint_{hint_num + 1}.arc", self.bg,
                                    sprite_sheet=False)
            if hint_num == 0:
                self.text.text = self.puzzle_data.hint1
            elif hint_num == 1:
                self.text.text = self.puzzle_data.hint2
            elif hint_num == 2:
                self.text.text = self.puzzle_data.hint3
        else:
            self.sprite_loader.load(f"data_lt2/bg/nazo/system/?/jitenhint_{hint_num + 1}.arc", self.bg,
                                    sprite_sheet=False)

    def update(self, dt: float):
        if self.back_btn.pressed(self.btm_camera, dt):
            return False
        self.back_btn.animate(dt)

        for i in range(min(3, self.used + 1)):
            if self.selected_btns[i].pressed(self.btm_camera, dt):
                self.view_hint(i)
            self.selected_btns[i].animate(dt)

        if self.selected == self.used:
            if self.unlock_btn.pressed(self.btm_camera, dt):
                self.view_hint(self.progress_hints() - 1)
            self.unlock_btn.animate(dt)

            if self.no_unlock_btn.pressed(self.btm_camera, dt):
                return False
            self.no_unlock_btn.animate(dt)
        return True

    def draw(self):
        self.bg.draw(self.btm_camera)
        if self.selected == self.used:
            self.unlock_btn.draw(self.btm_camera)
            self.no_unlock_btn.draw(self.btm_camera)
        else:
            self.text.draw(self.btm_camera)
        self.back_btn.draw(self.btm_camera)
        for hint_select in self.selected_btns:
            hint_select.draw(self.btm_camera)
