from LaytonLib.binary import *
# Sacred functions I'm too lazy to reimplement
from LaytonLib.gdslegacy import *

class GDSCommand:
    def __init__(self, command):
        self.command = command
        self.data = []


class GDSScript:
    def __init__(self):
        self.filestart = None
        self.commands = []

    @classmethod
    def from_bytes(cls, data: bytes):
        legacyoutput = extract_from_gds(data)
        return cls.from_legacy(legacyoutput)

    @classmethod
    def from_simplified(cls, text):
        legacyoutput = extract_from_simplified(text)
        return cls.from_legacy(legacyoutput)

    @classmethod
    def from_legacy(cls, legacy):
        self = cls()
        self.filestart = legacy['start']
        for dat in legacy['commands']:
            newdat = GDSCommand(int(dat[0], 16))
            if len(dat) > 1:
                for part in dat[1:]:
                    newdat.data.append(part)
            self.commands.append(newdat)
        return self

    def to_bytes(self):
        return convert_to_gds(self.to_legacy())

    def to_simplified(self):
        return convert_to_simplified(self.to_legacy())

    def to_legacy(self):
        legacy_commands = []
        for command in self.commands:
            command: GDSCommand
            legacy_command = [hex(command.command),]
            legacy_command += command.data
            legacy_commands.append(legacy_command)
        legacy = {'start': self.filestart, 'commands': legacy_commands}
        return legacy

