from .Filesystem import FilesystemCategory, FolderNodeOneLevel, AssetNode


class FontFolder(FolderNodeOneLevel):
    def get_asset_type(self):
        return FontAsset


class FontAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]


class FontsCategory(FilesystemCategory):
    def __init__(self):
        super(FontsCategory, self).__init__()
        self.name = "Fonts"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FontFolder(self, "/data_lt2/font", self.rom.filenames["/data_lt2/font"], None)
