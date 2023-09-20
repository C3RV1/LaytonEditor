import os.path

from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory, FolderNodeFilterExtension
from PySide6 import QtCore, QtWidgets, QtGui
from typing import List, Tuple, Callable, Union
from formats.sound.sadl import SADL
from formats_parsed.sound.wav import WAV
from ..SettingsManager import SettingsManager


class SADLNode(AssetNodeBasename):
    def get_sadl(self):
        return SADL(self.path, rom=self.rom)


class StreamedAudioCategory(FilesystemCategory):
    def __init__(self):
        super(StreamedAudioCategory, self).__init__()
        self.name = "Streamed Audio"

    def reset_file_system(self):
        if self.rom.name == b"LAYTON2":
            self._root = FolderNode(self, "/data_lt2/stream", self.rom.filenames["/data_lt2/stream"], None,
                                    asset_class=SADLNode)
        else:
            self._root = FolderNodeFilterExtension(self, "", self.rom.filenames, None, extensions=[".SAD"],
                                                   asset_class=SADLNode)

