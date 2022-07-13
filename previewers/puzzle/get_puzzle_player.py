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

# TODO: CIRCLE_ANSWER, DRAW_LINE_PLAZA, LINE_DIVIDE, WEATHER, PILES_OF_PANCAKES,
#       LINE_DIVIDE_LIMITED, KNIGHT_TOUR, TILE_ROTATE, ROSES, TILE_ROTATE_2,
#       SLIPPERY_CROSSINGS, DISAPPEARING_ACT, JARS_AND_CANS, LIGHT_THE_WAY,
#       RICKETY_BRIDGE, FIND_SHAPE


def get_puzzle_player(puzzle_data: Puzzle):
    if puzzle_data.type not in PUZZLE_TYPE_DICT:
        return NullPuzzle(puzzle_data)
    return PUZZLE_TYPE_DICT[puzzle_data.type](puzzle_data)
