from .Filesystem import FilesystemCategory, FolderNodeOneLevel, AssetNodeBasename, FolderNodeFilterExtension


class FontsCategory(FilesystemCategory):
    def __init__(self):
        super(FontsCategory, self).__init__()
        self.name = "Fonts"

    def reset_file_system(self):
        if self.rom.name == b"LAYTON2":
            self._root = FolderNodeOneLevel(self, "/data_lt2/font", self.rom.filenames["/data_lt2/font"], None,
                                            asset_class=AssetNodeBasename)
        else:
            self._root = FolderNodeFilterExtension(self, "", self.rom.filenames, None,
                                                   extensions=[".NFTR"], asset_class=AssetNodeBasename)
