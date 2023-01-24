from ..gds_parser import GDSParser


class MultipleChoiceGDSParser(GDSParser):
    def __init__(self):
        super(MultipleChoiceGDSParser, self).__init__()
        self.command_name_table = {
            0x14: "add_button",
        }
