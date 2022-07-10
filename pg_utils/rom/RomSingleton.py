import formats.filesystem
import k4pg
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

    def get_sprite_loader(self) -> k4pg.SpriteLoader:
        if self.rom is None:
            return k4pg.SpriteLoaderOS()
        else:
            return loaders.SpriteLoaderROM(self.rom, base_path_rom="")

    def get_font_loader(self) -> k4pg.FontLoader:
        return loaders.FontLoaderROM(self.rom, base_path_rom="data_lt2/font",
                                     fall_back_font_os="../font_default.json", base_path_os="data_permanent/fonts",
                                     fall_back_font_sys="arial")
