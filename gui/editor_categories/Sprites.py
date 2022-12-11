from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory


class SpriteCategory(FilesystemCategory):
    def __init__(self):
        super(SpriteCategory, self).__init__()
        self.name = "Sprites"

    def reset_file_system(self):
        self._root = FolderNode(self, "/data_lt2/ani", self.rom.filenames["/data_lt2/ani"], None,
                                asset_class=AssetNodeBasename)
