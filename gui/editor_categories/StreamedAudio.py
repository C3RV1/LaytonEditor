from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory


class StreamedAudioCategory(FilesystemCategory):
    def __init__(self):
        super(StreamedAudioCategory, self).__init__()
        self.name = "Streamed Audio"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNode(self, "/data_lt2/stream", self.rom.filenames["/data_lt2/stream"], None,
                                asset_class=AssetNodeBasename)
