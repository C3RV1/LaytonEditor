from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory


class BackgroundsCategory(FilesystemCategory):
    def __init__(self):
        super(BackgroundsCategory, self).__init__()
        self.name = "Backgrounds"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNode(self, "/data_lt2/bg", self.rom.filenames["/data_lt2/bg"], None,
                                asset_class=AssetNodeBasename)
