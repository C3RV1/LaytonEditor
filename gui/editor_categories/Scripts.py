from .Filesystem import FolderNode, AssetNode, FilesystemCategory
from formats.filesystem import PlzArchive
from formats.gds import GDS


class ScriptFolder(FolderNode):
    def __init__(self, category, path, folder, parent):
        super(ScriptFolder, self).__init__(category, path, folder, parent)
        if isinstance(self.folder, PlzArchive):
            self.files = [x for x in self.folder.filenames if x.endswith(".gds")]
        else:
            self.files = [x for x in self.folder.files if x.endswith(".gds") or x.endswith(".plz")]

    def get_asset_type(self):
        return ScriptAsset

    def child_count(self):
        if isinstance(self.folder, PlzArchive):
            return len(self.files)
        return len(self.folder.folders) + len(self.files)

    def child(self, row, parent_idx):
        if 0 > row or self.child_count() <= row:
            return None
        if row not in self.children:
            if isinstance(self.folder, PlzArchive):
                name = self.files[row]
                self.children[row] = self.get_asset_type()(self.category, name, parent_idx, self.folder)
                return self.children[row]
            if row < len(self.folder.folders):
                name, folder = self.folder.folders[row]
                self.children[row] = self.get_folder_type()(self.category, self.path + "/" + name,
                                                            folder, parent_idx)
            else:
                row2 = row - len(self.files)
                name: str = self.files[row2]
                if name.endswith(".plz"):
                    path = self.path + "/" + name
                    self.children[row] = self.get_folder_type()(self.category, self.path + "/" + name,
                                                                self.category.rom.get_archive(path),
                                                                parent_idx)
                else:
                    self.children[row] = self.get_asset_type()(self.category, self.path + "/" + name,
                                                               parent_idx, self.category.rom)
        return self.children[row]


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
