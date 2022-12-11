from .Filesystem import FilesystemCategory, FolderNodeOneLevel, AssetNodeBasename


class FontsCategory(FilesystemCategory):
    def __init__(self):
        super(FontsCategory, self).__init__()
        self.name = "Fonts"

    def reset_file_system(self):
        self._root = FolderNodeOneLevel(self, "/data_lt2/font", self.rom.filenames["/data_lt2/font"], None,
                                        asset_class=AssetNodeBasename)
