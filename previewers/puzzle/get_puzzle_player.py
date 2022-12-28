from formats.puzzle import PuzzleType, Puzzle
from .puzzle_types.NullPuzzle import NullPuzzle
from .puzzle_types.MultipleChoice import MultipleChoice
from .puzzle_types.OnOff import OnOff
from .puzzle_types.Sort import Sort
from .puzzle_types.Slide import Slide
from .puzzle_types.Area import Area
from .puzzle_types.Write import Write


PUZZLE_TYPE_DICT = {
    PuzzleType.MULTIPLE_CHOICE: MultipleChoice,
    PuzzleType.ON_OFF: OnOff,
    PuzzleType.SORT: Sort,
    PuzzleType.SLIDE: Slide,
    PuzzleType.AREA: Area,
    PuzzleType.WRITE_NUM: Write,
    PuzzleType.WRITE_CHARS: Write,
    PuzzleType.WRITE_ALT: Write,
    PuzzleType.WRITE_DATE: Write
}

# TODO: CIRCLE_ANSWER, DRAW_LINE_PLAZA, LINE_DIVIDE, WEATHER, PILES_OF_PANCAKES,
#       LINE_DIVIDE_LIMITED, KNIGHT_TOUR, TILE_ROTATE, ROSES, TILE_ROTATE_2,
#       SLIPPERY_CROSSINGS, DISAPPEARING_ACT, JARS_AND_CANS, LIGHT_THE_WAY,
#       RICKETY_BRIDGE, FIND_SHAPE


def get_puzzle_player(puzzle_data: Puzzle):
    if puzzle_data.type not in PUZZLE_TYPE_DICT:
        return NullPuzzle(puzzle_data)
    return PUZZLE_TYPE_DICT[puzzle_data.type](puzzle_data)
