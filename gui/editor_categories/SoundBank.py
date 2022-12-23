import os

from .Filesystem import FilesystemCategory, FolderNodeOneLevelFilterExtension, AssetNodeBasename
from formats.sound.swdl import SWDL
from PySide6 import QtCore, QtWidgets
from typing import Callable, List, Tuple, Union
from formats_parsed.sound import sf2
from ..SettingsManager import SettingsManager


class SWDLNode(AssetNodeBasename):
    def get_swdl(self):
        return SWDL(self.path, rom=self.rom)


class SoundBankCategory(FilesystemCategory):
    def __init__(self):
        super(SoundBankCategory, self).__init__()
        self.name = "Sound Banks"

    def reset_file_system(self):
        self._root = FolderNodeOneLevelFilterExtension(self, "/data_lt2/sound", self.rom.filenames["/data_lt2/sound"],
                                                       None, extensions=[".SWD"], asset_class=SWDLNode)

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        default_context_menu = super(SoundBankCategory, self).get_context_menu(index, refresh_function)
        if isinstance(index.internalPointer(), SWDLNode):
            wav_context_actions = [
                None,
                ("Export SF2", lambda: self.export_sf2(index)),
            ]
            default_context_menu.extend(wav_context_actions)
        return default_context_menu

    def export_sf2(self, index: QtCore.QModelIndex):
        node: SWDLNode = index.internalPointer()

        filename, _ = os.path.splitext(os.path.basename(node.path))
        filename += ".sf2"
        export_path, _ = SettingsManager().export_file(None, "Export SF2...", filename, "SoundFont Files (*.sf2)")
        if export_path == "":
            return

        path = node.path
        swd = node.get_swdl()
        sf = sf2.SoundFont()
        sf.info_chunk.isft_chunk = sf2.ISFTChunk(sound_font_tool="Layton Editor")
        sf.programs = swd.programs
        sf.samples = swd.samples

        if not path.lower().endswith("999.swd"):
            main_bank_path = "/".join(path.split("/")[:-1]) + "/BG_999.SWD"
            main_bank = SWDL(main_bank_path, rom=node.rom)
            sf.set_sample_data(main_bank.samples)

        with open(export_path, "wb") as export_file:
            sf.write_stream(export_file)
