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


class TileRotate2GDSParser(GDSParser):
    def __init__(self):
        super(TileRotate2GDSParser, self).__init__()
        self.command_name_table = {
            0x60: "start_positions_maybe",
            0x55: "create_slot",  # parameters: (x: int, y: int) of top left corner
            0x54: "set_tile_image",  # parameters: (name: str) of the file at data_lt2/ani/nazo/tile/<> (ends in .spr)
            0x57: "create_tile",  # parameters: (unk0: int, unk1: int, unk2: int, anim1: str, anim2: str, anim3: str,
                                  #              slot: int) creates a tile with the specified anim at the specified slot
            0x59: "set_tile_size",  # parameters: (x_maybe: int, y_maybe: int, w: int, h: int) always after a 0x57
            0x5a: "set_tile_solution",  # parameters: (tile: int, solution: int)
        }
