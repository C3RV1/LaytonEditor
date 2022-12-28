from ..gds_parser import GDSParser


class SlideGDSParser(GDSParser):
    def __init__(self):
        super(SlideGDSParser, self).__init__()
        self.command_name_table = {
            0x4e: ["setup_table", "Setup Table"],
            0x4f: ["add_occlusion", "Add Occlusion"],
            0x50: ["set_solution", "Set Solution"],
            0x51: ["set_tilemap", "Set Tilemap"],
            0x52: ["add_tile", "Add Tile"],
            0x53: ["add_tile_collider", "Add Tile Collider"]
        }
