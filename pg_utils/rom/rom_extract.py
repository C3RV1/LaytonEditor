import os
import shutil
import formats.sound.smd as smd
import formats.sound.swd as swd
import formats.binary as binary

from formats import conf
from pg_utils.rom import RomSingleton
import SADLpy.SADL

EXPORT_PATH = "data_extracted"
ORIGINAL_FPS = 60


def set_extension(path, ext):
    return ".".join(path.split(".")[:-1]) + ext


def load_sadl(path: str, rom=None) -> SADLpy.SADL.SADL:
    if rom is None:
        rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", conf.LANG)
    sad_export_path = EXPORT_PATH + "/" + path
    sound_data = rom.files[rom.filenames.idOf(path)]

    # if not os.path.isfile(sad_export_path):
    #     os.makedirs(os.path.dirname(sad_export_path), exist_ok=True)
    #     with open(sad_export_path, "wb") as sad_export_file:
    #         sad_export_file.write(sound_data)

    sadl = SADLpy.SADL.SADL(sad_export_path, 0)
    sadl.read_file(sound_data)

    return sadl


def load_smd(path: str, rom=None) -> tuple:
    if rom is None:
        rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", conf.LANG)
    smd_file = binary.BinaryReader(rom.open(path, "rb"))

    smd_obj = smd.SMDL()
    smd_obj.read(smd_file)
    smd_file.close()

    swd_path = path.split(".")[0] + ".SWD"
    swd_file = binary.BinaryReader(rom.open(swd_path, "rb"))
    swd_presets = swd.swd_read_presetbank(swd_file).presets
    swd_file.close()
    return smd_obj, swd_presets


def clear_extracted():
    if os.path.isdir(EXPORT_PATH):
        shutil.rmtree(EXPORT_PATH)
