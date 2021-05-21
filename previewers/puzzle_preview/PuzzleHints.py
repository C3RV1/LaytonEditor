from PygameEngine.Alignment import Alignment
from PygameEngine.UI.Button import Button
from PygameEngine.UI.UIManager import UIManager
from PygameEngine.UI.Text import Text
from pygame_utils.rom.rom_extract import load_animation, load_bg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from previewers.puzzle_preview.PuzzleMain import PuzzleMain


class PuzzleHints:
    def __init__(self, puzzle_player, ui_manager, btm_group, top_group):
        self.pz_main = puzzle_player  # type: PuzzleMain
        self.ui_manager = ui_manager  # type: UIManager
        self.btm_group = btm_group
        self.top_group = top_group

        self.hint_back = Button(())
        self.hint_unlock = Button(())
        self.hint_no_unlock = Button(())
        self.hint_text = Text(())
        self.hint_select_btn = []

        self.hint_back.draw_alignment = [Alignment.LEFT, Alignment.BOTTOM]
        self.hint_back.world_rect.x = 256 // 2
        self.hint_back.world_rect.y = -192 // 2
        self.hint_back.pre_interact = lambda: self.btn_pre_anim(self.hint_back)
        self.hint_back.post_interact = self.hint_back_post
        self.hint_back.time_interact_command = 0.1

        self.hint_unlock.draw_alignment = [Alignment.RIGHT, Alignment.BOTTOM]
        self.hint_unlock.world_rect.x = -80
        self.hint_unlock.world_rect.y = 40
        self.hint_unlock.pre_interact = lambda: self.btn_pre_anim(self.hint_unlock)
        self.hint_unlock.post_interact = self.hint_unlock_post

        self.hint_no_unlock.draw_alignment = [Alignment.LEFT, Alignment.BOTTOM]
        self.hint_no_unlock.world_rect.x = -self.hint_unlock.world_rect.x
        self.hint_no_unlock.world_rect.y = self.hint_unlock.world_rect.y
        self.hint_no_unlock.pre_interact = lambda: self.btn_pre_anim(self.hint_no_unlock)
        self.hint_no_unlock.post_interact = self.hint_no_unlock_post

        self.hint_text.draw_alignment = [Alignment.RIGHT, Alignment.BOTTOM]
        self.hint_text.world_rect.x = -256 // 2 + 20
        self.hint_text.world_rect.y = -192 // 2 + 42
        self.hint_text.set_font("data_permanent/fonts/fontq.png", [7, 10], is_font_map=True)
        self.hint_text.color = (0, 0, 0)
        self.hint_text.bg_color = (0, 255, 0)
        self.hint_text.mask_color = (0, 255, 0)

        for i in range(3):
            new_hint = Button(())
            new_hint.draw_alignment = [Alignment.RIGHT, Alignment.BOTTOM]
            new_hint.world_rect.x = -256 // 2 + 8
            new_hint.world_rect.y = -192 // 2 + 4
            new_hint.pre_interact = lambda index=i: self.btn_pre_anim(self.hint_select_btn[index])
            new_hint.post_interact = lambda index=i: self.view_hint(index)
            new_hint.time_interact_command = 0.1
            self.hint_select_btn.append(new_hint)

        self.hints_used = 0

        self.hints_elements = [self.hint_text, self.hint_back, self.hint_no_unlock, self.hint_unlock,
                               self.hint_select_btn]

    def load(self):
        self.hints_used = 0
        self.update_hint_select(sprites=True)
        for i in range(3):
            if i != 0:
                prev = self.hint_select_btn[i - 1]
                self.hint_select_btn[i].world_rect.x = prev.world_rect.x + prev.world_rect.w + 1

        load_animation("data_lt2/ani/system/btn/?/modoru_memo.arc", self.hint_back)
        load_animation("data_lt2/ani/system/btn/?/yes.arc", self.hint_unlock)
        load_animation("data_lt2/ani/system/btn/?/no.arc", self.hint_no_unlock)

    def unload(self):
        self.hint_back.unload()
        self.hint_unlock.unload()
        self.hint_no_unlock.unload()
        self.hint_text.unload()
        for i in range(3):
            self.hint_select_btn[i].unload()

    def update_hint_select(self, sprites=False):
        self.ui_manager.add(self.hint_select_btn)
        for i in range(3):
            path = f"data_lt2/ani/nazo/system/?/hint{i + 1}.arc"
            if self.hints_used < i:
                self.hint_select_btn[i].kill()
                self.ui_manager.remove(self.hint_select_btn[i])
            elif self.hints_used == i:
                path = f"data_lt2/ani/nazo/system/?/hintlock{i + 1}.arc"
            if sprites:
                load_animation(path, self.hint_select_btn[i])
            self.hint_select_btn[i].set_tag("off")

    def enter_hints(self):
        self.btm_group.add([self.hint_back, self.hint_select_btn])
        self.ui_manager.add([self.hint_back])
        self.view_hint(0)

    def view_hint(self, hint_num):
        self.update_hint_select()
        if self.hints_used > hint_num:
            load_bg(f"data_lt2/bg/nazo/system/?/hint_{hint_num + 1}.arc", self.pz_main.btm_bg)
            self.btm_group.remove([self.hint_unlock, self.hint_no_unlock])
            self.btm_group.add([self.hint_text])
            self.pz_main.ui_manager.remove([self.hint_unlock, self.hint_no_unlock])
            if hint_num == 0:
                self.hint_text.text = self.pz_main.puzzle_player.puzzle_data.hint1.decode("ascii")
            elif hint_num == 1:
                self.hint_text.text = self.pz_main.puzzle_player.puzzle_data.hint2.decode("ascii")
            elif hint_num == 2:
                self.hint_text.text = self.pz_main.puzzle_player.puzzle_data.hint3.decode("ascii")
        else:
            load_bg(f"data_lt2/bg/nazo/system/?/jitenhint_{hint_num + 1}.arc", self.pz_main.btm_bg)
            self.pz_main.ui_manager.add([self.hint_unlock, self.hint_no_unlock])
            self.btm_group.add([self.hint_unlock, self.hint_no_unlock])
            self.btm_group.remove([self.hint_text])

    def btn_pre_anim(self, button: Button):
        button.set_tag("on")

    def hint_unlock_post(self):
        self.hint_unlock.set_tag("off")
        self.hints_used += 1
        self.update_hint_select(sprites=True)
        if self.hints_used < 3:
            self.pz_main.btm_group.add(self.hint_select_btn[self.hints_used])
        self.view_hint(self.hints_used - 1)
        self.pz_main.hints_btn.set_tag(f"{self.hints_used}_off")

    def hint_back_post(self):
        self.hint_back.set_tag("off")
        self.return_puzzle()

    def hint_no_unlock_post(self):
        self.hint_no_unlock.set_tag("off")
        self.return_puzzle()

    def return_puzzle(self):
        self.pz_main.return_from_hints()
