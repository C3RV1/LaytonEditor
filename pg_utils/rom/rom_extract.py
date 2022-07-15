import os
import shutil
from typing import Dict

from formats.sound.smdl import smdl
from formats.sound import sadl
from formats.sound import swdl
from formats.sound import sound_types
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
    swd_file = swdl.SWDL(swd_path, rom=rom)
    programs: Dict[int, sound_types.Program] = swd_file.programs
    return smd_obj, programs


def clear_extracted():
    if os.path.isdir(EXPORT_PATH):
        shutil.rmtree(EXPORT_PATH)
