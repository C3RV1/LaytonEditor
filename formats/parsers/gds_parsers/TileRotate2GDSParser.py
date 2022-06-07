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
            0x57: ["create_tile", "Create Tile"],
            # parameters: (unk0: int, unk1: int, unk2: int, anim1: str, anim2: str, anim3: str,
            #              slot: int) creates a tile with the specified anim at the specified slot
            0x59: ["set_tile_size", "Set Tile Size"],
            # parameters: (x_maybe: int, y_maybe: int, w: int, h: int) always after a 0x57
            0x5a: ["set_tile_solution", "Set Tile Solution"],
            # parameters: (tile: int, solution: int)
        }
