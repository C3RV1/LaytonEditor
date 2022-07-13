from formats.puzzle import Puzzle
from .puzzle_types.NullPuzzle import NullPuzzle
from .puzzle_types.MultipleChoice import MultipleChoice
from .puzzle_types.OnOff import OnOff
from .puzzle_types.Sort import Sort
from .puzzle_types.Slide import Slide
from .puzzle_types.Area import Area
from .puzzle_types.Write import Write


PUZZLE_TYPE_DICT = {
    Puzzle.MULTIPLE_CHOICE: MultipleChoice,
    Puzzle.ON_OFF: OnOff,
    Puzzle.SORT: Sort,
    Puzzle.SLIDE: Slide,
    Puzzle.AREA: Area,
    Puzzle.WRITE_NUM: Write,
    Puzzle.WRITE_CHARS: Write,
    Puzzle.WRITE_ALT: Write,
    Puzzle.WRITE_DATE: Write
}


def get_puzzle_player(puzzle_data: Puzzle):
    if puzzle_data.type not in PUZZLE_TYPE_DICT:
        return NullPuzzle(puzzle_data)
    return PUZZLE_TYPE_DICT[puzzle_data.type](puzzle_data)
