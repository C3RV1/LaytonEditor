from formats.puzzle import Puzzle
from .puzzle_types.NullPuzzle import NullPuzzle
from .puzzle_types.MultipleChoice import MultipleChoice


PUZZLE_TYPE_DICT = {
    Puzzle.MULTIPLE_CHOICE: MultipleChoice
}


def get_puzzle_player(puzzle_data: Puzzle):
    if puzzle_data.type not in PUZZLE_TYPE_DICT:
        return NullPuzzle(puzzle_data)
    return PUZZLE_TYPE_DICT[puzzle_data.type](puzzle_data)
