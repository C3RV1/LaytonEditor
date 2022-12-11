from .Filesystem import FolderNodeFilterExtension, AssetNodeBasename, FilesystemCategory


class TextsCategory(FilesystemCategory):
    def __init__(self):
        super(TextsCategory, self).__init__()
        self.name = "Texts"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNodeFilterExtension(self, "/data_lt2", self.rom.filenames["/data_lt2"], None,
                                               asset_class=AssetNodeBasename)
