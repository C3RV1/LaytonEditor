from LaytonLib.binary import *
import re


class GDSCommand:
    def __init__(self, command, params=None):
        self.command = command
        self.params = [] if params == None else params

    def __repr__(self):
        return f"GDSCommand({hex(self.command)}, {self.params})"


class GDSScript:
    def __init__(self, commands=None, params=None):
        self.params = [] if params == None else params  # used when there aren't any true commands
        self.commands = [] if commands == None else commands  # used when there are commands

    @classmethod
    def from_bytes(cls, data: bytes):
        self = cls()
        rdr = BinaryReader(data)
        _ = rdr.readU32()  # File lenght
        while True:
            data_type = rdr.readU16()
            if data_type == 0:
                break
            elif data_type == 1:
                self.params.append(rdr.readU32())
            elif data_type == 2:
                self.params.append([rdr.readU16(), rdr.readU16()])
            elif data_type == 3:
                lenght = rdr.readU16()
                self.params.append(rdr.readString())
            elif data_type == 0xc:
                return self
        while True:
            opp = rdr.readU16()
            command = GDSCommand(opp)
            self.commands.append(command)
            while True:
                data_type = rdr.readU16()
                if data_type == 0:
                    break
                elif data_type == 1:
                    command.params.append(rdr.readU32())
                elif data_type == 2:
                    command.params.append([rdr.readU16(), rdr.readU16()])
                elif data_type == 3:
                    lenght = rdr.readU16()
                    command.params.append(rdr.readString())
                elif data_type == 0xc:
                    return self

    def to_bytes(self):
        data_wtr = BinaryWriter()
        for p in self.params:
            if type(p) == int:
                data_wtr.writeU16(1)
                data_wtr.writeU32(p)
            elif type(p) == list:
                data_wtr.writeU16(2)
                data_wtr.writeU16List(p)
            elif type(p) == str:
                data_wtr.writeU16(3)
                data_wtr.writeU16(len(p))
                data_wtr.write(p)
                data_wtr.writeU8(0)
        for c in self.commands:
            data_wtr.writeU16(0)
            data_wtr.writeU16(c.command)
            for p in c.params:
                if type(p) == int:
                    data_wtr.writeU16(1)
                    data_wtr.writeU32(p)
                elif type(p) == list:
                    data_wtr.writeU16(2)
                    data_wtr.writeU16List(p)
                elif type(p) == str:
                    data_wtr.writeU16(3)
                    data_wtr.writeU16(len(p))
                    data_wtr.write(p)
                    data_wtr.writeU8(0)

        data_wtr.writeU16(0xc)
        wtr = BinaryWriter()
        wtr.writeU32(len(data_wtr))
        wtr.write(data_wtr.data)
        return wtr.data

    @classmethod
    def from_simplified(cls, text):
        self = cls()
        lines = text.split("\n")
        current_command = None
        i = 0
        while i < len(lines):
            l = lines[i].split("#")[0]
            if re.match(r"int: *[0-9]+[ \t]*", l):
                self.params.append(int(re.findall("[0-9]+", l)[0]))
            elif re.match(r"vec: *\[[0-9]+, *[0-9]+\][ \t]*", l):
                self.params.append([int(x) for x in re.findall("\[([0-9]*), *([0-9]*)\]", l)[0]])
            elif re.match(r"str: \".*\"[ \t]*", l):
                self.params.append(re.findall("\"(.*)\"", l)[0])
            elif re.match(r"0x[0-9a-zA-Z]+[ \t]*", l):
                current_command = GDSCommand(int(re.findall("0x[0-9a-zA-Z]+", l)[0], 16))
                self.commands.append(current_command)
            elif re.match(r"\tint: *[0-9]+[ \t]*", l):
                current_command.params.append(int(re.findall("[0-9]+", l)[0]))
            elif re.match(r"\tvec: *\[[0-9]+, *[0-9]+\][ \t]*", l):
                current_command.params.append([int(x) for x in re.findall("\[([0-9]*), *([0-9]*)\]", l)[0]])
            elif re.match(r"\tstr: \".*\"[ \t]*", l):
                current_command.params.append(re.findall("\"(.*)\"", l)[0])
            i += 1
        return self

    def to_simplified(self):
        lines = []
        for p in self.params:
            if type(p) == int:
                lines.append(f"int: {p}\t#hex: {hex(p)}")
            elif type(p) == list:
                lines.append(f"vec: {p}")
            elif type(p) == str:
                lines.append(f"str: {p}")
        for c in self.commands:
            lines.append(hex(c.command))
            for p in c.params:
                if type(p) == int:
                    lines.append(f"\tint: {p}\t\t#hex: {hex(p)}")
                elif type(p) == list:
                    lines.append(f"\tvec: {p}")
                elif type(p) == str:
                    lines.append(f"\tstr: \"{p}\"")
            lines.append("")

        return "\n".join(lines)

    def __repr__(self):
        return f"GDSScript(commands={self.commands}, params={(self.params)})"
