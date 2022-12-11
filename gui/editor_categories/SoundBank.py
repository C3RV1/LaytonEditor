from .Filesystem import FilesystemCategory, FolderNodeOneLevelFilterExtension, AssetNodeBasename


class SoundBankCategory(FilesystemCategory):
    def __init__(self):
        super(SoundBankCategory, self).__init__()
        self.name = "Sound Banks"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNodeOneLevelFilterExtension(self, "/data_lt2/sound", self.rom.filenames["/data_lt2/sound"],
                                                       None, extensions=[".SWD"], asset_class=AssetNodeBasename)
