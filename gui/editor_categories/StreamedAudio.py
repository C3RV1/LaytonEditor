from .Filesystem import FolderNode, AssetNode, FilesystemCategory


class StreamedAudioFolder(FolderNode):
    def get_asset_type(self):
        return StreamedAudioAsset


class StreamedAudioAsset(AssetNode):
    def data(self):
        return self.path.split("/")[-1].split(".")[0]


class StreamedAudioCategory(FilesystemCategory):
    def __init__(self):
        super(StreamedAudioCategory, self).__init__()
        self.name = "Streamed Audio"

    def set_rom(self, rom):
        super(StreamedAudioCategory, self).set_rom(rom)
        self._root = StreamedAudioFolder(self, "/data_lt2/stream", self.rom.filenames["/data_lt2/stream"], None)