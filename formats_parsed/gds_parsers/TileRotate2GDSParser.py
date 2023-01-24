from ..gds_parser import GDSParser


class TileRotate2GDSParser(GDSParser):
    def __init__(self):
        super(TileRotate2GDSParser, self).__init__()
        self.command_name_table = {
            0x60: "start_positions_maybe",
            0x55: "create_slot",
            # parameters: (x: int, y: int) of top left corner
            0x54: "set_tile_image",
            # parameters: (name: str) of the file at data_lt2/ani/nazo/tile/<> (ends in .spr)
            # can be more than 1 per script
            0x57: "create_tile",
            # parameters: (tile_image: int, center_x: int, center_y: int, anim1: str, anim2: str, anim3: str,
            #              slot: int) creates a tile with the specified anim at the specified slot
            0x58: "create_tile2",  # ??
            0x59: "set_grab_size",
            # parameters: (x_maybe: int, y_maybe: int, w: int, h: int) always after a 0x57
            0x6d: "set_grab_size2",  # ??
            0x5a: "set_tile_solution",
            # parameters: (tile: int, solution: int)
            0x5b: "set_tile_solution2"  # ??
        }
