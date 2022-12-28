from .Filesystem import FolderNodeFilterExtension, AssetNodeBasename, FilesystemCategory


class TextAsset(AssetNodeBasename):
    pass


class TextsCategory(FilesystemCategory):
    def __init__(self):
        super(TextsCategory, self).__init__()
        self.name = "Texts"

    def reset_file_system(self):
        if self.rom.name == b"LAYTON2":
            self._root = FolderNodeFilterExtension(self, "/data_lt2", self.rom.filenames["/data_lt2"], None,
                                                   extensions=[".txt"], asset_class=TextAsset)
        else:
            self._root = FolderNodeFilterExtension(self, "", self.rom.filenames, None,
                                                   extensions=[".txt"], asset_class=TextAsset)
