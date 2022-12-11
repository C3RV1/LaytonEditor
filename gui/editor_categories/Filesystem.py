import os.path
from typing import List, Tuple, Callable, Any

from PySide6 import QtCore, QtWidgets, QtGui
from formats.filesystem import Folder, PlzArchive, NintendoDSRom
from ..EditorTypes import EditorCategory, EditorObject


class FolderNode(EditorObject):
    def __init__(self, category, path, folder, parent):
        self.category = category
        self.path = path
        self.folder: Folder | PlzArchive = folder
        self.parent = parent

        self.children = {}

    def reset_children(self):
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
        return os.path.basename(self.path)


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
        self.rom: NintendoDSRom | PlzArchive = rom

    def data(self):
        return os.path.basename(self.path)


class FilesystemCategory(EditorCategory):
    def __init__(self):
        super(FilesystemCategory, self).__init__()
        self.name = "Filesystem"
        self._root: FolderNode = None
        self.allow_rename = False

    def reset_file_system(self):
        self._root = FolderNode(self, "", self.rom.filenames, None)

    def row_count(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel):
        if index.internalPointer() is self:
            return self._root.child_count()
        node = index.internalPointer()
        if isinstance(node, FolderNode):
            return node.child_count()
        return 0

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel):
        parent_idx = parent
        if parent.internalPointer() is self:
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
        if index.isValid() and index.internalPointer() is not self:
            return index.internalPointer().parent
        return QtCore.QModelIndex()

    def data(self, index, role, model):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return index.internalPointer().data()
        return None

    def get_context_menu(self, index: QtCore.QModelIndex) -> List[Tuple[str, Callable]]:
        if isinstance(index.internalPointer(), AssetNode):
            return [
                ("Replace", lambda: self.import_(index)),
                ("Export", lambda: self.export(index))
            ]
        return []

    def import_(self, index: QtCore.QModelIndex):
        import_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Import file...")
        if import_path == "":
            return
        asset: AssetNode = index.internalPointer()
        with open(import_path, "rb") as import_file:
            asset_file = asset.rom.open(asset.path, "wb")
            asset_file.write(import_file.read())
            asset_file.close()

    def export(self, index: QtCore.QModelIndex):
        export_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export file...")
        if export_path == "":
            return
        asset: AssetNode = index.internalPointer()
        with open(export_path, "wb") as export_file:
            asset_file = asset.rom.open(asset.path, "rb")
            export_file.write(asset_file.read())
            asset_file.close()

    def flags(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel) -> QtCore.Qt.ItemFlag:
        default_flags = super(FilesystemCategory, self).flags(index, model)
        if index.internalPointer() is self or not self.allow_rename:
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def set_data(self, index: QtCore.QModelIndex, value: Any, role, model) -> bool:
        if value == "":
            return False
        node = index.internalPointer()
        if isinstance(node, FolderNode):
            self.rename_folder(node, value)
        elif isinstance(node, AssetNode):
            self.rename_asset(node, value)
        model.updated_fs(self)
        return True

    def rename_asset(self, asset: AssetNode, value):
        asset.rom.rename_file(asset.path, value)
        new_path = os.path.join(os.path.dirname(asset.path), value).replace("\\", "/")
        asset.path = new_path

    def rename_folder(self, folder: FolderNode, value):
        new_path = os.path.join(os.path.dirname(folder.path), value).replace("\\", "/")
        if isinstance(folder.folder, Folder):
            self.rom.rename_folder(folder.path, new_path)
        elif isinstance(folder.folder, PlzArchive):
            self.rom.rename_file(folder.path, value)
        folder.path = new_path
        folder.reset_children()
