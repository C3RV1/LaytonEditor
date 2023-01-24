import formats.gds
from formats_parsed.dcc import DCCParser


class GDSParser:
    def __init__(self):
        self.command_name_table = {}

    def parse_command_name(self, command: formats.gds.GDSCommand):
        if command.command not in self.command_name_table.keys():
            return f"gds_{hex(command.command)}", command.params.copy()
        return self.command_name_table[command.command], command.params.copy()

    def reverse_command_name(self, command: str, params):
        if command.startswith("gds_"):
            return formats.gds.GDSCommand(int(command[4:], 16), params.copy())
        for key in self.command_name_table.keys():
            if self.command_name_table[key] == command:
                return formats.gds.GDSCommand(key, params.copy())
        raise ValueError(f"{command} is not a valid command")

    def serialize_into_dcc(self, gds: formats.gds.GDS, dcc_parser: DCCParser):
        for param in gds.params:
            dcc_parser["::unnamed"].append(param)
        for cmd in gds.commands:
            cmd_text, params = self.parse_command_name(cmd)
            dcc_parser["::calls"].append({
                "func": cmd_text,
                "parameters": params.copy()
            })

    def parse_from_dcc(self, gds: formats.gds.GDS, dcc_parser: DCCParser):
        gds.commands = []
        gds.params = []
        for param in dcc_parser["::unnamed"]:
            gds.params.append(param)
        for call in dcc_parser["::calls"]:
            func = call["func"]
            params = call["parameters"]
            command = self.reverse_command_name(func, params)
            gds.commands.append(command)
        return True, ""
