from .Filesystem import FolderNode, AssetNode, FilesystemCategory


class SpriteFolder(FolderNode):
    def get_asset_type(self):
        return SpriteAsset


class SpriteAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]


class SpriteCategory(FilesystemCategory):
    def __init__(self):
        super(SpriteCategory, self).__init__()
        self.name = "Sprites"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = SpriteFolder(self, "/data_lt2/ani", self.rom.filenames["/data_lt2/ani"], None)
