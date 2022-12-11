from .Filesystem import FilesystemCategory, FolderNodeOneLevelFilterExtension, AssetNodeBasename


class SoundEffectCategory(FilesystemCategory):
    def __init__(self):
        super(SoundEffectCategory, self).__init__()
        self.name = "Sound Effects"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNodeOneLevelFilterExtension(self, "/data_lt2/sound", self.rom.filenames["/data_lt2/sound"],
                                                       None, extensions=[".SED"], asset_class=AssetNodeBasename)
