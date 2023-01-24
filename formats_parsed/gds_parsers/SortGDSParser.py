from ..gds_parser import GDSParser


class SortGDSParser(GDSParser):
    def __init__(self):
        super(SortGDSParser, self).__init__()
        self.command_name_table = {
            0x2e: "create_tile",
        }
