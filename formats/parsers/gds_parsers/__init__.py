from .InputGDSParser import InputGDSParser
from .TileRotate2GDSParser import TileRotate2GDSParser
from .MultipleChoiceGDSParser import MultipleChoiceGDSParser
from .OnOffGDSParser import OnOffGDSParser
from .EventGDSParser import EventGDSParser
from .SortGDSParser import SortGDSParser
from .SlideGDSParser import SlideGDSParser
from .AreaGDSParser import AreaGDSParser
from formats.puzzle import Puzzle
from ..gds_parser import GDSParser


TYPE_TO_GDS_PARSER = {
    Puzzle.INPUT_DATE: InputGDSParser,
    Puzzle.INPUT_NUMERIC: InputGDSParser,
    Puzzle.INPUT_ALTERNATIVE: InputGDSParser,
    Puzzle.INPUT_CHARACTERS: InputGDSParser,
    Puzzle.ON_OFF: OnOffGDSParser,
    Puzzle.MULTIPLE_CHOICE: MultipleChoiceGDSParser,
    Puzzle.TILE_ROTATE_2: TileRotate2GDSParser,
    Puzzle.SORT: SortGDSParser,
    Puzzle.SLIDE: SlideGDSParser,
    Puzzle.AREA: AreaGDSParser
}


def get_puzzle_gds_parser(puzzle_data: Puzzle):
    return TYPE_TO_GDS_PARSER.get(puzzle_data.type, GDSParser)()