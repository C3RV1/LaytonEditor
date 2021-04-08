import pygame_utils.TwoScreenRenderer
from pygame_utils.rom import RomSingleton
from PygameEngine.Sprite import Sprite
from PygameEngine.Animation import Animation
from PygameEngine.Alignment import Alignment
import formats.puzzles.puzzle_data as pzd
from pygame_utils.rom.rom_extract import load_bg, load_animation
from PygameEngine.UI.Text import Text
from utility.replace_substitutions import replace_substitutions
from previewers.puzzle_preview.PuzzleHints import PuzzleHints
from previewers.puzzle_preview.PuzzleMain import PuzzleMain


class PuzzlePlayer(pygame_utils.TwoScreenRenderer.TwoScreenRenderer):
    def __init__(self):
        super(PuzzlePlayer, self).__init__()

        self.puzzle_id = 0
        self.hints_used = 0
        self.puzzle_data = pzd.PuzzleData(rom=RomSingleton.RomSingleton().rom)

        self.btm_bg = Sprite(())
        self.btm_bg.layer = -10
        self.text_bg = Sprite(())
        self.text_bg.layer = -10
        self.puzzle_text = Text(())
        self.header_top_left = [Animation(()), Animation(()), Animation(()), Animation(())]

        self.puzzle_text.set_font("data_permanent/fonts/fontq.png", [7, 10], is_font_map=True)
        self.puzzle_text.color = (0, 0, 0)
        self.puzzle_text.bg_color = (0, 255, 0)
        self.puzzle_text.mask_color = (0, 255, 0)
        self.puzzle_text.draw_alignment = [Alignment.RIGHT, Alignment.BOTTOM]
        self.puzzle_text.world_rect.x = -256 // 2 + 10
        self.puzzle_text.world_rect.y = -192 // 2 + 22

        self.pz_main = PuzzleMain(self, self.ui_manager, self.btm_group, self.top_group)
        self.pz_hints = PuzzleHints(self, self.ui_manager, self.btm_group, self.top_group)

    def remove_all_btm(self):
        self.ui_manager.clear()
        self.btm_group.remove(self.btm_group.sprites())
        self.btm_group.add(self.btm_bg)

    def open_puzzle(self):
        self.pz_main.enter_puzzle()

    def open_hints(self):
        self.pz_hints.enter_hints()

    def load(self):
        super(PuzzlePlayer, self).load()
        self.btm_group.add(self.btm_bg)
        self.ui_manager.clear()
        self.hints_used = 0

        self.puzzle_data.set_internal_id(self.puzzle_id)
        self.puzzle_data.load_from_rom()

        self.load_puzzle_top()
        self.pz_hints.load()
        self.pz_main.load()

        self.open_puzzle()

    def load_puzzle_top(self):
        self.top_group.add([self.text_bg, self.puzzle_text, self.header_top_left])
        load_bg(self.puzzle_data.bg_path, self.btm_bg)
        load_bg(f"data_lt2/bg/nazo/system/nazo_text{self.puzzle_data.location}.arc", self.text_bg)
        for header_top_left in self.header_top_left:
            load_animation(f"data_lt2/ani/nazo/system/?/nazo_text.arc", header_top_left)
            header_top_left.draw_alignment = [header_top_left.ALIGNMENT_RIGHT, header_top_left.ALIGNMENT_BOTTOM]
        self.puzzle_text.text = replace_substitutions(self.puzzle_data.text.decode("ascii"))

        self.header_top_left[0].set_tag("nazo")
        self.header_top_left[0].world_rect.x = -256 // 2 + 5
        self.header_top_left[0].world_rect.y = -192 // 2 + 4
        for i in range(3):
            p_num = self.puzzle_data.number
            for a in range(2 - i):
                p_num //= 10
            self.header_top_left[i + 1].set_tag(str(p_num % 10))
            self.header_top_left[i + 1].world_rect.x = -256 // 2 + 23 + i * 7
            self.header_top_left[i + 1].world_rect.y = -192 // 2 + 5

    def update(self):
        self.ui_manager.update()

    def unload(self):
        super(PuzzlePlayer, self).unload()
        self.btm_bg.unload()
        self.pz_hints.unload()
        self.pz_main.unload()
