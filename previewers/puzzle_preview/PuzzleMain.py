from PygameEngine.Alignment import Alignment
from PygameEngine.UI.Button import Button
from PygameEngine.UI.Text import Text
from PygameEngine.Sprite import Sprite
from PygameEngine.UI.UIManager import UIManager
from pygame_utils.rom.rom_extract import load_animation, load_bg
from formats.puzzles.puzzle_data import PuzzleData as pzd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from previewers.puzzle_preview.PuzzlePlayer import PuzzlePlayer


class PuzzleMain:
    def __init__(self, puzzle_player, ui_manager, btm_group, top_group):
        self.pz_player = puzzle_player  # type: PuzzlePlayer
        self.ui_manager = ui_manager  # type: UIManager
        self.btm_group = btm_group
        self.top_group = top_group

        self.hints_btn = Button(())
        self.quit_btn = Button(())
        self.memo_btn = Button(())

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

        self.submit_btn = Button(())
        self.submit_btn.draw_alignment = [Alignment.LEFT, Alignment.TOP]
        self.submit_btn.world_rect.x = 256 // 2
        self.submit_btn.world_rect.y = 192 // 2
        self.submit_btn.pre_interact = lambda: self.btn_pre_anim(self.submit_btn)
        self.submit_btn.post_interact = lambda: self.btn_post_anim(self.submit_btn, self.show_end_dialogue)

        self.prize_window = Sprite(())
        self.prize_window.layer = 10
        self.prize_window_text = Text(())
        self.prize_window_text.layer = 12
        self.prize_window_text.draw_alignment = [Alignment.CENTER, Alignment.BOTTOM]
        self.prize_window_text.world_rect.y = -20
        self.prize_window_text.set_font("data_permanent/fonts/fontq.png", [7, 10], is_font_map=True)
        self.prize_window_text.color = (0, 0, 0)
        self.prize_window_text.bg_color = (0, 255, 0)
        self.prize_window_text.mask_color = (0, 255, 0)
        self.prize_window_text.text = "1st for correct, 2nd for incorrect"

        self.correct_ok = Button(())
        self.correct_ok.world_rect.x = -60
        self.correct_ok.world_rect.y = 15
        self.correct_ok.layer = 11
        self.correct_ok.pre_interact = lambda: self.btn_pre_anim(self.correct_ok)
        self.correct_ok.post_interact = lambda: self.btn_post_anim(self.correct_ok, self.correct_answer)
        self.correct_ok.time_interact_command = 0.1

        self.incorrect_ok = Button(())
        self.incorrect_ok.world_rect.x = -self.correct_ok.world_rect.x
        self.incorrect_ok.world_rect.y = self.correct_ok.world_rect.y
        self.incorrect_ok.layer = 11
        self.incorrect_ok.pre_interact = lambda: self.btn_pre_anim(self.incorrect_ok)
        self.incorrect_ok.post_interact = lambda: self.btn_post_anim(self.incorrect_ok, self.incorrect_answer)
        self.incorrect_ok.time_interact_command = 0.1

        self.back_prize = Button(())
        self.back_prize.world_rect.x = 0
        self.back_prize.world_rect.y = self.correct_ok.world_rect.y + 10
        self.back_prize.layer = 11
        self.back_prize.pre_interact = lambda: self.btn_pre_anim(self.back_prize)
        self.back_prize.post_interact = lambda: self.btn_post_anim(self.back_prize, self.hide_end_dialogue)
        self.back_prize.time_interact_command = 0.1

        self.puzzle_elements = []

    def enter_puzzle(self):
        load_bg(self.pz_player.puzzle_data.bg_path, self.pz_player.btm_bg)
        self.pz_player.remove_all_btm()
        self.btm_group.add([self.memo_btn, self.quit_btn, self.hints_btn, self.submit_btn, self.puzzle_elements])
        self.ui_manager.add([self.hints_btn, self.quit_btn, self.memo_btn, self.submit_btn, self.puzzle_elements])

    def hint_pre(self):
        self.hints_btn.set_tag(f"{self.pz_player.pz_hints.hints_used}_on")

    def hint_post(self):
        self.hints_btn.set_tag(f"{self.pz_player.pz_hints.hints_used}_off")
        self.pz_player.open_hints()

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

    def load(self):
        self.btm_group.add([self.hints_btn, self.quit_btn, self.memo_btn])
        self.ui_manager.add([self.hints_btn, self.quit_btn, self.memo_btn])

        load_animation("data_lt2/ani/system/btn/?/hint.arc", self.hints_btn)
        self.hints_btn.set_tag(f"{self.pz_player.pz_hints.hints_used}_off")
        self.hints_btn.update_transformations()

        self.quit_btn.world_rect.y = self.hints_btn.world_rect.y + self.hints_btn.world_rect.h
        load_animation("data_lt2/ani/system/btn/?/atode.arc", self.quit_btn)
        self.quit_btn.set_tag("off")

        self.memo_btn.world_rect.y = self.quit_btn.world_rect.y + self.hints_btn.world_rect.h
        load_animation("data_lt2/ani/system/btn/?/memo.arc", self.memo_btn)
        self.memo_btn.set_tag("off")

        load_animation("data_lt2/ani/system/btn/?/hantei.arc", self.submit_btn)
        self.submit_btn.set_tag("off")

        load_animation("data_lt2/ani/system/prize_window.arc", self.prize_window)
        load_animation("data_lt2/ani/system/btn/?/yes.arc", self.correct_ok)
        load_animation("data_lt2/ani/system/btn/?/yes.arc", self.incorrect_ok)
        load_animation("data_lt2/ani/system/btn/?/cancel.arc", self.back_prize)

        self.load_gds()

    def load_gds(self):
        for command in self.pz_player.puzzle_data.gds.commands:
            if self.pz_player.puzzle_data.type == pzd.MULTIPLE_CHOICE:
                if command.command == 0x14:
                    new_btn = Button(())
                    new_btn.draw_alignment = [Alignment.RIGHT, Alignment.BOTTOM]
                    new_btn.world_rect.x = command.params[0] - 256 // 2
                    new_btn.world_rect.y = command.params[1] - 192 // 2
                    load_animation("data_lt2/ani/nazo/freebutton/" + command.params[2], new_btn)
                    new_btn.set_tag("off")
                    new_btn.pre_interact = lambda btn=new_btn: self.btn_pre_anim(btn)
                    new_btn.time_interact_command = 0.1
                    if command.params[3]:
                        new_btn.post_interact = lambda btn=new_btn: self.btn_post_anim(btn, self.correct_answer)
                    else:
                        new_btn.post_interact = lambda btn=new_btn: self.btn_post_anim(btn, self.incorrect_answer)
                    self.puzzle_elements.append(new_btn)
        self.btm_group.add(self.puzzle_elements)
        self.ui_manager.add(self.puzzle_elements)

    def show_end_dialogue(self):
        self.btm_group.add([self.prize_window, self.correct_ok, self.incorrect_ok, self.back_prize,
                            self.prize_window_text])
        self.ui_manager.clear()
        self.ui_manager.add([self.correct_ok, self.incorrect_ok, self.back_prize])
        self.correct_ok.set_tag("off")
        self.incorrect_ok.set_tag("off")
        self.back_prize.set_tag("off")

    def hide_end_dialogue(self):
        self.btm_group.remove([self.prize_window, self.correct_ok, self.incorrect_ok, self.back_prize,
                               self.prize_window_text])
        self.ui_manager.clear()
        self.ui_manager.add([self.hints_btn, self.quit_btn, self.memo_btn, self.submit_btn, self.puzzle_elements])

    def incorrect_answer(self):
        print("Incorrect")

    def correct_answer(self):
        print("Correct")

    def unload(self):
        self.hints_btn.unload()
        self.quit_btn.unload()
        self.memo_btn.unload()
        for puzzle_ele in self.puzzle_elements:
            puzzle_ele.unload()
        self.puzzle_elements.clear()
