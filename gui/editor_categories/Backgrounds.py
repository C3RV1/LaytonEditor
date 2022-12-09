from .Filesystem import FolderNode, AssetNode, FilesystemCategory


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

    def set_rom(self, rom):
        super(BackgroundsCategory, self).set_rom(rom)
        self._root = BackgroundFolder(self, "/data_lt2/bg", self.rom.filenames["/data_lt2/bg"], None)
