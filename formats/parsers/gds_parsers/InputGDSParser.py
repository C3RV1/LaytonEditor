from ..gds_parser import GDSParser


class InputGDSParser(GDSParser):
    def __init__(self):
        super(InputGDSParser, self).__init__()
        self.command_name_table = {
            0x43: ["load_input_bg", "Load Input Background"],
            0x42: ["set_answer", "Set Answer"],
            0x41: ["set_input_type", "Set Input Type"]
        }
