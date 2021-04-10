import formats.gds


class GDSParser:
    def __init__(self):
        self.command_name_table = {}

    def parse_command_name(self, command: formats.gds.GDSCommand):
        if command.command not in self.command_name_table.keys():
            return f"gds_{hex(command.command)}"
        return self.command_name_table[command.command]

    def reverse_command_name(self, command: str):
        if command.startswith("gds_"):
            return int(command[4:], 16)
        for key in self.command_name_table.keys():
            if self.command_name_table[key] == command:
                return key
        raise ValueError(f"{command} is not a valid command")


class InputGDSParser(GDSParser):
    def __init__(self):
        super(InputGDSParser, self).__init__()
        self.command_name_table = {
            0x43: "load_input_bg",
            0x42: "set_answer",
            0x41: "set_input_type"
        }


class MultipleChoiceGDSParser(GDSParser):
    def __init__(self):
        super(MultipleChoiceGDSParser, self).__init__()
        self.command_name_table = {
            0x14: "add_button"
        }
