from .WriteGDSParser import WriteGDSParser
from .TileRotate2GDSParser import TileRotate2GDSParser
from .MultipleChoiceGDSParser import MultipleChoiceGDSParser
from .OnOffGDSParser import OnOffGDSParser
from .SortGDSParser import SortGDSParser
from .SlideGDSParser import SlideGDSParser
from .AreaGDSParser import AreaGDSParser
from formats.puzzle import Puzzle, PuzzleType
from ..gds_parser import GDSParser


TYPE_TO_GDS_PARSER = {
    PuzzleType.WRITE_DATE: WriteGDSParser,
    PuzzleType.WRITE_NUM: WriteGDSParser,
    PuzzleType.WRITE_ALT: WriteGDSParser,
    PuzzleType.WRITE_CHARS: WriteGDSParser,
    PuzzleType.ON_OFF: OnOffGDSParser,
    PuzzleType.MULTIPLE_CHOICE: MultipleChoiceGDSParser,
    PuzzleType.TILE_ROTATE_2: TileRotate2GDSParser,
    PuzzleType.SORT: SortGDSParser,
    PuzzleType.SLIDE: SlideGDSParser,
    PuzzleType.AREA: AreaGDSParser
}


def get_puzzle_gds_parser(puzzle_data: Puzzle):
    return TYPE_TO_GDS_PARSER.get(puzzle_data.type, GDSParser)()
