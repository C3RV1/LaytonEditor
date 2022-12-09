from ..gds_parser import GDSParser


class TileRotate2GDSParser(GDSParser):
    def __init__(self):
        super(TileRotate2GDSParser, self).__init__()
        self.command_name_table = {
            0x60: ["start_positions_maybe", "Set Start Positions"],
            0x55: ["create_slot", "Create Slot"],
            # parameters: (x: int, y: int) of top left corner
            0x54: ["set_tile_image", "Set Tile Image"],
            # parameters: (name: str) of the file at data_lt2/ani/nazo/tile/<> (ends in .spr)
            # can be more than 1 per script
            0x57: ["create_tile", "Create Tile"],
            # parameters: (tile_image: int, center_x: int, center_y: int, anim1: str, anim2: str, anim3: str,
            #              slot: int) creates a tile with the specified anim at the specified slot
            0x58: ["create_tile2", "Create Tile2"],  # ??
            0x59: ["set_grab_size", "Set Grab Size"],
            # parameters: (x_maybe: int, y_maybe: int, w: int, h: int) always after a 0x57
            0x6d: ["set_grab_size2", "Set Grab Size 2"],  # ??
            0x5a: ["set_tile_solution", "Set Tile Solution"],
            # parameters: (tile: int, solution: int)
            0x5b: ["set_tile_solution2", "Set Tile Solution 2"]  # ??
        }
