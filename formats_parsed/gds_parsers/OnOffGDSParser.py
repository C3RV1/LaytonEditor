from ..gds_parser import GDSParser


class OnOffGDSParser(GDSParser):
    def __init__(self):
        super(OnOffGDSParser, self).__init__()
        self.command_name_table = {
            0x14: "create_option",
        }
