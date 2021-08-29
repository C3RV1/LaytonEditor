from pg_utils.rom import RomSingleton
import formats.puzzle as pzd
from previewers.puzzle_preview.PuzzleMain import PuzzleMain


class PuzzlePlayer:
    def __init__(self):
        super(PuzzlePlayer, self).__init__()

        self.puzzle_id = 0
        self.hints_used = 0
        self.puzzle_data = pzd.Puzzle(rom=RomSingleton.RomSingleton().rom)

        self.pz_main = PuzzleMain(self)

    def set_puzzle_id(self, puzzle_id):
        self.puzzle_id = puzzle_id
        self.puzzle_data.set_internal_id(self.puzzle_id)
        self.puzzle_data.load_from_rom()
