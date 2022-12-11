from .Filesystem import FolderNode, AssetNode, FilesystemCategory
from PySide6 import QtCore
from typing import Any
import os


class BackgroundFolder(FolderNode):
    def get_asset_type(self):
        return BackgroundAsset


class BackgroundAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]


class BackgroundsCategory(FilesystemCategory):
    def __init__(self):
        super(BackgroundsCategory, self).__init__()
        self.name = "Backgrounds"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = BackgroundFolder(self, "/data_lt2/bg", self.rom.filenames["/data_lt2/bg"], None)
