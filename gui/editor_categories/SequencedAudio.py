from Filesystem import FilesystemCategory, FolderNodeOneLevelFilterExtension, AssetNodeBasename


class SequencedAudioCategory(FilesystemCategory):
    def __init__(self):
        super(SequencedAudioCategory, self).__init__()
        self.name = "Sequenced Audio"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNodeOneLevelFilterExtension(self, "/data_lt2/sound", self.rom.filenames["/data_lt2/sound"],
                                                       None, extensions=[".SMD"], asset_class=AssetNodeBasename)
