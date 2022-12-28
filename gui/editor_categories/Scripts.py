from .Filesystem import FolderNodeFilterExtension, AssetNodeBasename, FilesystemCategory
from formats.gds import GDS


class ScriptAsset(AssetNodeBasename):
    def to_gds(self) -> GDS:
        return GDS(rom=self.rom, filename=self.path)


class ScriptsCategory(FilesystemCategory):
    def __init__(self):
        super(ScriptsCategory, self).__init__()
        self.name = "Scripts"

    def reset_file_system(self):
        if self.rom.name == b"LAYTON2":
            self._root = FolderNodeFilterExtension(self, "/data_lt2", self.rom.filenames["/data_lt2"], None,
                                                   extensions=[".gds"], asset_class=ScriptAsset)
        else:
            self._root = FolderNodeFilterExtension(self, "", self.rom.filenames, None,
                                                   extensions=[".gds"], asset_class=ScriptAsset)
