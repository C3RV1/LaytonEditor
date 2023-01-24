from ..gds_parser import GDSParser


class SlideGDSParser(GDSParser):
    def __init__(self):
        super(SlideGDSParser, self).__init__()
        self.command_name_table = {
            0x4e: "setup_table",
            0x4f: "add_occlusion",
            0x50: "set_solution",
            0x51: "set_tilemap",
            0x52: "add_tile",
            0x53: "add_tile_collider",
        }
