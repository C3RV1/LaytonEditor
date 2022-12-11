from .Filesystem import FolderNodeFilterExtension, AssetNode, FilesystemCategory


class TextFolder(FolderNodeFilterExtension):
    def __init__(self, category, path, folder, parent, extension=".txt"):
        super(TextFolder, self).__init__(category, path, folder, parent, extension)

    def get_asset_type(self):
        return TextAsset


class TextAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]


class TextsCategory(FilesystemCategory):
    def __init__(self):
        super(TextsCategory, self).__init__()
        self.name = "Texts"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = TextFolder(self, "/data_lt2", self.rom.filenames["/data_lt2"], None)
