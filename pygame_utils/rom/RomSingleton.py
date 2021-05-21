import formats.filesystem


class RomSingleton:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(RomSingleton.__instance, RomSingleton):
            RomSingleton.__instance = super(RomSingleton, cls).__new__(cls)
        return RomSingleton.__instance

    def __init__(self, rom_path=None, rom=None):
        if rom is not None:
            self.rom = rom
        elif rom_path is not None:
            self.rom = formats.filesystem.NintendoDSRom.fromFile(rom_path)
        elif self.rom is None:
            raise Exception("Rom can't be none")
