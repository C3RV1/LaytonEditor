from PygameEngine.Alignment import Alignment
from PygameEngine.UI.Button import Button
from PygameEngine.UI.Text import Text
from PygameEngine.Sprite import Sprite
from PygameEngine.Animation import Animation
from PygameEngine.UI.UIManager import UIManager
from pygame_utils.rom.rom_extract import load_animation, load_bg
import formats.puzzle as pzd
from typing import TYPE_CHECKING
from pygame_utils import TwoScreenRenderer
from previewers.puzzle_preview.PuzzleHints import PuzzleHints
from utility.replace_substitutions import replace_substitutions

if TYPE_CHECKING:
    from previewers.puzzle_preview.PuzzlePlayer import PuzzlePlayer


class PuzzleMain(TwoScreenRenderer.TwoScreenRenderer):
    def __init__(self, puzzle_player):
        super(PuzzleMain, self).__init__()

        self.puzzle_player = puzzle_player  # type: PuzzlePlayer

        self.hints_btn = Button(())
        self.quit_btn = Button(())
        self.memo_btn = Button(())
        self.submit_btn = Button(())
        self.btm_bg = Sprite(())
        self.btm_bg.layer = -10
        self.text_bg = Sprite(())
        self.text_bg.layer = -10
        self.puzzle_text = Text(())

        self.puzzle_text.set_font("data_permanent/fonts/fontq.png", [7, 10], is_font_map=True)
        self.puzzle_text.color = (0, 0, 0)
        self.puzzle_text.bg_color = (0, 255, 0)
        self.puzzle_text.mask_color = (0, 255, 0)
        self.puzzle_text.draw_alignment = [Alignment.RIGHT, Alignment.BOTTOM]
        self.puzzle_text.world_rect.x = -256 // 2 + 10
        self.puzzle_text.world_rect.y = -192 // 2 + 22

        self.pz_hints = PuzzleHints(self, self.ui_manager, self.btm_group, self.top_group)

        self.puzzle_elements = []

        self.header_top_left = [Animation(()), Animation(()), Animation(()), Animation(())]
        for header in self.header_top_left:
            header.layer = 100

        self.puzzle_main_elements = [self.hints_btn, self.quit_btn, self.memo_btn, self.submit_btn]

    def load(self):
        self.btm_group.remove(self.btm_group.sprites())
        self.top_group.remove(self.btm_group.sprites())
        self.btm_group.add(self.btm_bg, self.puzzle_main_elements)
        self.hints_btn.draw_alignment = [Alignment.LEFT, Alignment.BOTTOM]
        self.hints_btn.world_rect.x = 256 // 2
        self.hints_btn.world_rect.y = -192 // 2
        self.hints_btn.pre_interact = self.hint_pre
        self.hints_btn.post_interact = self.hint_post
        self.hints_btn.time_interact_command = 0.1

        self.quit_btn.draw_alignment = [Alignment.LEFT, Alignment.BOTTOM]
        self.quit_btn.world_rect.x = 256 // 2
        self.quit_btn.pre_interact = lambda: self.btn_pre_anim(self.quit_btn)
        self.quit_btn.post_interact = self.quit_post
        self.quit_btn.time_interact_command = 0.1

        self.memo_btn.draw_alignment = [Alignment.LEFT, Alignment.BOTTOM]
        self.memo_btn.world_rect.x = 256 // 2
        self.memo_btn.pre_interact = lambda: self.btn_pre_anim(self.memo_btn)
        self.memo_btn.post_interact = self.memo_post
        self.memo_btn.time_interact_command = 0.1

        self.submit_btn.draw_alignment = [Alignment.LEFT, Alignment.TOP]
        self.submit_btn.world_rect.x = 256 // 2
        self.submit_btn.world_rect.y = 192 // 2
        self.submit_btn.pre_interact = lambda: self.btn_pre_anim(self.submit_btn)
        self.submit_btn.post_interact = lambda: self.btn_post_anim(self.submit_btn, None)
        self.submit_btn.time_interact_command = 0.1

        load_animation("data_lt2/ani/system/btn/?/hint.arc", self.hints_btn)
        self.hints_btn.set_tag(f"{self.pz_hints.hints_used}_off")
        self.hints_btn.update_transformations()

        self.quit_btn.world_rect.y = self.hints_btn.world_rect.y + self.hints_btn.world_rect.h
        load_animation("data_lt2/ani/system/btn/?/atode.arc", self.quit_btn)
        self.quit_btn.set_tag("off")

        self.memo_btn.world_rect.y = self.quit_btn.world_rect.y + self.hints_btn.world_rect.h
        load_animation("data_lt2/ani/system/btn/?/memo.arc", self.memo_btn)
        self.memo_btn.set_tag("off")

        load_animation("data_lt2/ani/system/btn/?/hantei.arc", self.submit_btn)
        self.submit_btn.set_tag("off")

        self.top_group.add([self.text_bg, self.puzzle_text])
        load_bg(self.puzzle_player.puzzle_data.btm_path, self.btm_bg)
        load_bg(f"data_lt2/bg/nazo/system/nazo_text{self.puzzle_player.puzzle_data.bg_top_id}.arc", self.text_bg)
        self.puzzle_text.text = replace_substitutions(self.puzzle_player.puzzle_data.text.decode(
            self.puzzle_player.puzzle_data.encoding), puzzle=True)

        self.load_header()

        self.pz_hints.load()

        self.ui_manager.add([self.hints_btn, self.quit_btn, self.submit_btn, self.memo_btn])

    def load_header(self):
        self.top_group.add(self.header_top_left)
        for header_top_left in self.header_top_left:
            load_animation(f"data_lt2/ani/nazo/system/?/nazo_text.arc", header_top_left)
            header_top_left.draw_alignment = [header_top_left.ALIGNMENT_RIGHT, header_top_left.ALIGNMENT_BOTTOM]

        self.header_top_left[0].set_tag("nazo")
        self.header_top_left[0].world_rect.x = -256 // 2 + 5
        self.header_top_left[0].world_rect.y = -192 // 2 + 4
        for i in range(3):
            p_num = self.puzzle_player.puzzle_data.number
            for a in range(2 - i):
                p_num //= 10
            self.header_top_left[i + 1].set_tag(str(p_num % 10))
            self.header_top_left[i + 1].world_rect.x = -256 // 2 + 23 + i * 7
            self.header_top_left[i + 1].world_rect.y = -192 // 2 + 5

    def hint_pre(self):
        self.hints_btn.set_tag(f"{self.pz_hints.hints_used}_on")

    def hint_post(self):
        self.hints_btn.set_tag(f"{self.pz_hints.hints_used}_off")
        self.open_hints()

    def open_hints(self):
        self.btm_group.remove(self.puzzle_main_elements)
        self.ui_manager.clear()
        self.pz_hints.enter_hints()

    def return_from_hints(self):
        self.btm_group.remove(self.pz_hints.hints_elements)
        self.btm_group.add(self.puzzle_main_elements)
        self.ui_manager.clear()
        self.ui_manager.add(self.puzzle_main_elements)
        load_bg(self.puzzle_player.puzzle_data.btm_path, self.btm_bg)

    def quit_post(self):
        self.quit_btn.set_tag("off")

    def memo_post(self):
        self.memo_btn.set_tag("off")

    def btn_pre_anim(self, button: Button):
        button.set_tag("on")

    def btn_post_anim(self, button: Button, follow_up):
        button.set_tag("off")
        if callable(follow_up):
            follow_up()

    def unload(self):
        self.hints_btn.unload()
        self.quit_btn.unload()
        self.memo_btn.unload()
        for puzzle_ele in self.puzzle_elements:
            puzzle_ele.unload()
        self.puzzle_elements.clear()

    def update(self):
        self.ui_manager.update()
