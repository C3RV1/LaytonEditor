import formats.gds
from formats_parsed.dcc import DCCParser


class GDSParser:
    def __init__(self):
        self.command_name_table = {}

    def parse_cmd(self, code: str, is_code=True):
        for v in self.command_name_table.values():
            if len(v) == 3:
                code_, not_code, _ = v
            else:
                code_, not_code = v
            if is_code:
                if code == code_:
                    return not_code
            else:
                if code == not_code:
                    return code_
        return code

    def parse_command_name(self, command: formats.gds.GDSCommand, is_code=True):
        param_names = [f"unk{i}" for i in range(len(command.params))]
        if command.command not in self.command_name_table.keys():
            return f"gds_{hex(command.command)}", command.params, param_names
        if len(self.command_name_table[command.command]) == 3:
            param_names = self.command_name_table[command.command][2]
        return self.command_name_table[command.command][0 if is_code else 1], command.params.copy(), param_names

    def reverse_command_name(self, command: str, params, is_code=True):
        if command.startswith("gds_"):
            return formats.gds.GDSCommand(int(command[4:], 16), params.copy())
        for key in self.command_name_table.keys():
            if self.command_name_table[key][0 if is_code else 1] == command:
                return formats.gds.GDSCommand(key, params.copy())
        raise ValueError(f"{command} is not a valid command")

    def parse_into_dcc(self, gds: formats.gds.GDS, dcc_parser: DCCParser):
        dcc_parser.get_path("script", create=True)
        for param in gds.params:
            dcc_parser["script::unnamed"].append(param)
        for cmd in gds.commands:
            cmd_text, params, _ = self.parse_command_name(cmd)
            dcc_parser["script::calls"].append({
                "func": cmd_text,
                "parameters": params.copy()
            })

    def parse_from_dcc(self, gds: formats.gds.GDS, dcc_parser: DCCParser):
        if not dcc_parser.exists("script"):
            return False, "Missing script"

        gds.commands = []
        gds.params = []
        for param in dcc_parser["script::unnamed"]:
            gds.params.append(param)
        for call in dcc_parser["script::calls"]:
            func = call["func"]
            params = call["parameters"]
            command = self.reverse_command_name(func, params)
            gds.commands.append(command)
        return True, ""
