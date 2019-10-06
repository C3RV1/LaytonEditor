from ndspy.rom import NintendoDSRom

# Allows something to edit a certain file at any time
class File:
    def __init__(self, rom: NintendoDSRom, id: int):
        self.rom = rom
        self._id = id

    @property
    def name(self):
        return self.rom.filenames[self._id]

    @name.setter
    def name(self, value: str):
        self.rom.filenames[self._id] = value

    def read(self):
        return self.rom.files[self._id]

    def write(self, data):
        self.rom.files[self._id] = data