from PySide6 import QtCore
from formats.filesystem import Folder, PlzArchive
from ..EditorTypes import EditorCategory, EditorObject


class FolderNode(EditorObject):
    def __init__(self, category, path, folder, parent):
        self.category = category
        self.path = path
        self.folder: Folder | PlzArchive = folder
        self.parent = parent

        self.children = {}

    def child_count(self):
        if isinstance(self.folder, PlzArchive):
            return len(self.folder.filenames)
        return len(self.folder.folders) + len(self.folder.files)

    def get_folder_type(self):
        return type(self)

    def get_asset_type(self):
        return AssetNode

    def child(self, row, parent_idx):
        if 0 > row or self.child_count() <= row:
            return None
        if row not in self.children:
            if isinstance(self.folder, PlzArchive):
                name = self.folder.filenames[row]
                self.children[row] = self.get_asset_type()(self.category, name, parent_idx, self.folder)
                return self.children[row]
            if row < len(self.folder.folders):
                name, folder = self.folder.folders[row]
                self.children[row] = self.get_folder_type()(self.category, self.path + "/" + name,
                                                            folder, parent_idx)
            else:
                row2 = row - len(self.folder.folders)
                name: str = self.folder.files[row2]
                if name.endswith(".plz"):
                    path = self.path + "/" + name
                    self.children[row] = self.get_folder_type()(self.category, self.path + "/" + name,
                                                                self.category.rom.get_archive(path),
                                                                parent_idx)
                else:
                    self.children[row] = self.get_asset_type()(self.category, self.path + "/" + name,
                                                               parent_idx, self.category.rom)
        return self.children[row]

    def data(self):
        return self.path.split("/")[-1]


class FolderNodeOneLevel(FolderNode):
    def child_count(self):
        if isinstance(self.folder, PlzArchive):
            return len(self.folder.filenames)
        return len(self.folder.files)

    def child(self, row, parent_idx):
        if 0 > row or self.child_count() <= row:
            return None
        if row not in self.children:
            if isinstance(self.folder, PlzArchive):
                name = self.folder.filenames[row]
                self.children[row] = self.get_asset_type()(self.category, name, parent_idx, self.folder)
                return self.children[row]
            name: str = self.folder.files[row]
            self.children[row] = self.get_asset_type()(self.category, self.path + "/" + name,
                                                       parent_idx, self.category.rom)
        return self.children[row]


class AssetNode(EditorObject):
    def __init__(self, category, path, parent_idx, rom):
        self.category = category
        self.path = path
        self.parent = parent_idx
        self.rom = rom

    def data(self):
        return self.path.split("/")[-1]


class FilesystemCategory(EditorCategory):
    def __init__(self):
        super(FilesystemCategory, self).__init__()
        self.name = "Filesystem"
        self._root: FolderNode = None

    def set_rom(self, rom):
        super(FilesystemCategory, self).set_rom(rom)
        self._root = FolderNode(self, "", self.rom.filenames, None)

    def row_count(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel):
        if index.internalPointer() == self:
            return self._root.child_count()
        node = index.internalPointer()
        if isinstance(node, FolderNode):
            return node.child_count()
        return 0

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel):
        parent_idx = parent
        if parent.internalPointer() == self:
            parent = self._root
        else:
            parent = parent.internalPointer()

        if isinstance(parent, AssetNode):
            return QtCore.QModelIndex()

        child = parent.child(row, parent_idx)
        if child:
            return model.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QAbstractItemModel,
               model: QtCore.QAbstractItemModel):
        if index.isValid() and index.internalPointer() != self:
            return index.internalPointer().parent
        return QtCore.QModelIndex()

    def data(self, index, role, model):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return index.internalPointer().data()
        return None
