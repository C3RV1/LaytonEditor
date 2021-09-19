import os
import shutil
import formats.sound.smdl as smdl
import formats.sound.sadl as sadl
import formats.sound.swd as swd
import formats.binary as binary

from formats import conf
from pg_utils.rom import RomSingleton

EXPORT_PATH = "data_extracted"
ORIGINAL_FPS = 60


def set_extension(path, ext):
    return ".".join(path.split(".")[:-1]) + ext


def load_sadl(path: str, rom=None) -> sadl.SADL:
    if rom is None:
        rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", conf.LANG)
    sadl_obj = sadl.SADL(path, 0, rom=rom)

    return sadl_obj


def load_smd(path: str, rom=None) -> tuple:
    if rom is None:
        rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", conf.LANG)

    smd_obj = smdl.SMDL(filename=path, rom=rom)

    swd_path = path.split(".")[0] + ".SWD"
    swd_file = binary.BinaryReader(rom.open(swd_path, "rb"))
    swd_presets = swd.swd_read_presetbank(swd_file).presets
    swd_file.close()
    return smd_obj, swd_presets


def clear_extracted():
    if os.path.isdir(EXPORT_PATH):
        shutil.rmtree(EXPORT_PATH)
