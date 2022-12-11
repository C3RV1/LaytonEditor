from .Filesystem import FolderNodeFilterExtension, AssetNode, FilesystemCategory
from formats.gds import GDS


class ScriptFolder(FolderNodeFilterExtension):
    def __init__(self, category, path, folder, parent, extension=".gds"):
        super(ScriptFolder, self).__init__(category, path, folder, parent, extension)

    def get_asset_type(self):
        return ScriptAsset


class ScriptAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]

    def to_gds(self) -> GDS:
        return GDS(rom=self.rom, filename=self.path)


class ScriptsCategory(FilesystemCategory):
    def __init__(self):
        super(ScriptsCategory, self).__init__()
        self.name = "Scripts"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = ScriptFolder(self, "/data_lt2", self.rom.filenames["/data_lt2"], None)
