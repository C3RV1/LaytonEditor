from .Filesystem import FilesystemCategory, FolderNodeOneLevel, AssetNode


class MovieFolder(FolderNodeOneLevel):
    def get_asset_type(self):
        return MovieAsset


class MovieAsset(AssetNode):
    def data(self):
        return f"Movie {self.path.split('/')[-1].split('.')[0][1:]}"


class MoviesCategory(FilesystemCategory):
    def __init__(self):
        # TODO: Sort numerically and not alphabetically
        super(MoviesCategory, self).__init__()
        self.name = "Movies"
        self.allow_rename = False

    def reset_file_system(self):
        self._root = MovieFolder(self, "/data_lt2/movie", self.rom.filenames["/data_lt2/movie"], None)
