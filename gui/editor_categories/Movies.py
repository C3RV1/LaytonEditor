from .Filesystem import FilesystemCategory, FolderNodeOneLevel, AssetNodeBasename


class MoviesCategory(FilesystemCategory):
    def __init__(self):
        # TODO: Sort numerically and not alphabetically
        super(MoviesCategory, self).__init__()
        self.name = "Movies"

    def reset_file_system(self):
        self._root = FolderNodeOneLevel(self, "/data_lt2/movie", self.rom.filenames["/data_lt2/movie"], None,
                                        asset_class=AssetNodeBasename)
