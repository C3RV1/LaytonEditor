import pygame_utils.TwoScreenRenderer
from pygame_utils.rom import RomSingleton
from PygameEngine.Sprite import Sprite
from PygameEngine.Animation import Animation
from PygameEngine.Alignment import Alignment
import formats.puzzles.puzzle_data as pzd
from pygame_utils.rom.rom_extract import load_bg, load_animation
from PygameEngine.UI.Text import Text
from utility.replace_substitutions import replace_substitutions


class PuzzlePlayer(pygame_utils.TwoScreenRenderer.TwoScreenRenderer):
    def __init__(self):
        super(PuzzlePlayer, self).__init__()

        self.puzzle_id = 0
        self.puzzle_data = pzd.PuzzleData(rom=RomSingleton.RomSingleton().rom)

        self.puzzle_bg = Sprite(())
        self.text_bg = Sprite(())
        self.text_bg.layer = -10

        self.puzzle_text = Text(())
        self.puzzle_text.set_font("data_permanent/fonts/fontq.png", [7, 10], is_font_map=True)
        self.puzzle_text.color = (0, 0, 0)
        self.puzzle_text.bg_color = (0, 255, 0)
        self.puzzle_text.mask_color = (0, 255, 0)
        self.puzzle_text.draw_alignment = [Alignment.ALIGNMENT_RIGHT, Alignment.ALIGNMENT_BOTTOM]
        self.puzzle_text.world_rect.x = -256 // 2 + 10
        self.puzzle_text.world_rect.y = -192 // 2 + 22

        self.header_top_left = [Animation(()), Animation(()), Animation(()), Animation(())]

    def load(self):
        super(PuzzlePlayer, self).load()
        self.top_screen_group.add([self.text_bg, self.puzzle_text])
        self.top_screen_group.add(self.header_top_left)
        self.bottom_screen_group.add([self.puzzle_bg])

        self.puzzle_data.set_internal_id(self.puzzle_id)
        self.puzzle_data.load_from_rom()

        load_bg(self.puzzle_data.bg_path, self.puzzle_bg)
        load_bg(f"data_lt2/bg/nazo/system/nazo_text{self.puzzle_data.location}.arc", self.text_bg)
        for header_top_left in self.header_top_left:
            load_animation(f"data_lt2/ani/nazo/system/?/nazo_text.arc", header_top_left)
            header_top_left.draw_alignment = [header_top_left.ALIGNMENT_RIGHT, header_top_left.ALIGNMENT_BOTTOM]

        self.header_top_left[0].set_tag("nazo")
        self.header_top_left[0].world_rect.x = -256 // 2 + 5
        self.header_top_left[0].world_rect.y = -192 // 2 + 4
        for i in range(3):
            p_num = self.puzzle_data.number
            for a in range(2-i):
                p_num //= 10
            self.header_top_left[i + 1].set_tag(str(p_num % 10))
            self.header_top_left[i + 1].world_rect.x = -256 // 2 + 23 + i * 7
            self.header_top_left[i + 1].world_rect.y = -192 // 2 + 5

        self.puzzle_text.text = replace_substitutions(self.puzzle_data.text.decode("ascii"))

    def update(self):
        return

    def unload(self):
        super(PuzzlePlayer, self).unload()
        self.puzzle_bg.unload()
