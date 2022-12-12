from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory
from formats.graphics.bg import BGImage


class BackgroundAsset(AssetNodeBasename):
    def get_bg(self) -> BGImage:
        return BGImage(self.path, rom=self.rom)


class BackgroundsCategory(FilesystemCategory):
    def __init__(self):
        super(BackgroundsCategory, self).__init__()
        self.name = "Backgrounds"

    def reset_file_system(self):
        self._root = FolderNode(self, "/data_lt2/bg", self.rom.filenames["/data_lt2/bg"], None,
                                asset_class=BackgroundAsset)
