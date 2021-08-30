import formats.filesystem
import pg_engine as pge
from pg_utils.rom import loaders


class RomSingleton:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(RomSingleton.__instance, RomSingleton):
            RomSingleton.__instance = super(RomSingleton, cls).__new__(cls)
            RomSingleton.__instance.rom = None
        return RomSingleton.__instance

    def __init__(self, rom_path=None, rom=None):
        if rom is not None:
            self.rom = rom
        elif rom_path is not None:
            self.rom = formats.filesystem.NintendoDSRom.fromFile(rom_path)

    def get_sprite_loader(self):
        if self.rom is None:
            return pge.SpriteLoaderOS()
        else:
            return loaders.SpriteLoaderROM(self.rom)

    def get_font_loader(self):
        return pge.FontLoaderOS(fall_back_font="arial", base_path="data_permanent/fonts")
