from .Filesystem import FolderNode, AssetNode, FilesystemCategory


class TextFolder(FolderNode):
    def get_asset_type(self):
        return TextAsset


class TextAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]


class TextsCategory(FilesystemCategory):
    def __init__(self):
        super(TextsCategory, self).__init__()
        self.name = "Texts"

    def set_rom(self, rom):
        super(TextsCategory, self).set_rom(rom)
        self._root = TextFolder(self, "/data_lt2/txt", self.rom.filenames["/data_lt2/txt"], None)
