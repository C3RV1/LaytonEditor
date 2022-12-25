import logging
import os.path
import struct
from typing import List, Tuple, Callable, Any, Union

from PySide6 import QtCore, QtWidgets, QtGui
from formats.filesystem import Folder, PlzArchive, NintendoDSRom, CompressedIOWrapper
from ..EditorTypes import EditorCategory, EditorObject
from ..ui.MainEditor import MainEditorUI
from ..SettingsManager import SettingsManager


class FolderNode(EditorObject):
    def __init__(self, category, path, folder, parent, asset_class=None):
        self.category = category
        self.path = path
        self.folder: Union[Folder, PlzArchive] = folder
        self.parent = parent

        self.children = {}
        if isinstance(self.folder, PlzArchive):
            self.files = self.folder.filenames
        else:
            self.files = self.folder.files

        if asset_class is None:
            asset_class = AssetNode
        self.asset_class = asset_class

    def reset_children(self):
        self.children = {}

    def child_count(self):
        if isinstance(self.folder, PlzArchive):
            return len(self.files)
        return len(self.folder.folders) + len(self.files)

    def create_folder(self, category, path, parent_idx, parent):
        return type(self)(category, path, parent_idx, parent, asset_class=self.asset_class)

    def get_asset_type(self):
        return self.asset_class

    def child(self, row, parent_idx):
        if 0 > row or self.child_count() <= row:
            return None
        if row not in self.children:
            if isinstance(self.folder, PlzArchive):
                name = self.files[row]
                self.children[row] = self.get_asset_type()(self.category, name, parent_idx, self.folder)
            elif row < len(self.folder.folders):
                name, folder = self.folder.folders[row]
                self.children[row] = self.create_folder(self.category, self.path + "/" + name, folder, parent_idx)
            else:
                row2 = row - len(self.folder.folders)
                name: str = self.files[row2]
                if name.endswith(".plz"):
                    path = self.path + "/" + name
                    self.children[row] = self.create_folder(self.category, self.path + "/" + name,
                                                            self.category.rom.get_archive(path), parent_idx)
                else:
                    self.children[row] = self.get_asset_type()(self.category, self.path + "/" + name,
                                                               parent_idx, self.category.rom)
        return self.children[row]

    def data(self):
        return os.path.basename(self.path)

    def decorative(self):
        return MainEditorUI.DIR_ICON

    def rename(self, value):
        new_path = os.path.join(os.path.dirname(self.path), value).replace("\\", "/")
        if isinstance(self.folder, Folder):
            self.category.rom.rename_folder(self.path, new_path)
        elif isinstance(self.folder, PlzArchive):
            self.category.rom.rename_file(self.path, value)
        self.path = new_path
        self.reset_children()


class FolderNodeFilterExtension(FolderNode):
    def __init__(self, *args, extensions=None, **kwargs):
        if extensions is None:
            extensions = []
        super(FolderNodeFilterExtension, self).__init__(*args, **kwargs)
        extensions = list(map(lambda x: x.lower(), extensions))
        if isinstance(self.folder, PlzArchive):
            self.files = filter(lambda x: any([x.lower().endswith(extension) for extension in extensions]),
                                self.folder.filenames)
        else:
            self.files = filter(lambda x: any([x.lower().endswith(extension) for extension in extensions + [".plz"]]),
                                self.folder.files)
        self.files = list(self.files)
        self.extensions = extensions

    def create_folder(self, category, path, parent_idx, parent):
        return type(self)(category, path, parent_idx, parent, extensions=self.extensions,
                          asset_class=self.asset_class)


class FolderNodeOneLevel(FolderNode):
    def child_count(self):
        return len(self.files)

    def child(self, row, parent_idx):
        if 0 > row or self.child_count() <= row:
            return None
        if row not in self.children:
            if isinstance(self.folder, PlzArchive):
                name = self.files[row]
                self.children[row] = self.get_asset_type()(self.category, name, parent_idx, self.folder)
                return self.children[row]
            name: str = self.files[row]
            self.children[row] = self.get_asset_type()(self.category, self.path + "/" + name,
                                                       parent_idx, self.category.rom)
        return self.children[row]


class FolderNodeOneLevelFilterExtension(FolderNodeFilterExtension, FolderNodeOneLevel):
    def __init__(self, *args, **kwargs):
        super(FolderNodeOneLevelFilterExtension, self).__init__(*args, **kwargs)

    def child_count(self):
        return FolderNodeOneLevel.child_count(self)

    def child(self, row, parent_idx):
        return FolderNodeOneLevel.child(self, row, parent_idx)


class AssetNode(EditorObject):
    def __init__(self, category, path, parent_idx, rom):
        self.category = category
        self.path = path
        self.parent = parent_idx
        self.rom: Union[NintendoDSRom, PlzArchive] = rom

    def data(self):
        return os.path.basename(self.path)

    def decorative(self):
        return MainEditorUI.FILE_ICON

    def rename(self, value):
        self.rom.rename_file(self.path, value)
        new_path = os.path.join(os.path.dirname(self.path), value).replace("\\", "/")
        self.path = new_path

    def get_asset_compression(self):
        file = self.rom.open(self.path, "rb")
        header = file.read(4)
        print(header)
        file.close()
        compression = 0
        if header[0] in [0x10, 0x30, 0x28, 0x24]:
            compression = 1
        elif struct.unpack("<I", header)[0] in [1, 2, 3, 4]:
            compression = 2
        logging.info(f"Asset {self.path} detected compression level {compression}")
        return compression


class AssetNodeBasename(AssetNode):
    def data(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    def rename(self, value):
        _, old_extension = os.path.splitext(self.path)
        value += old_extension
        self.rom.rename_file(self.path, value)
        new_path = os.path.join(os.path.dirname(self.path), value).replace("\\", "/")
        self.path = new_path


class FilesystemCategory(EditorCategory):
    def __init__(self):
        super(FilesystemCategory, self).__init__()
        self.name = "Filesystem"
        self._root: FolderNode = None
        self.allow_rename = True

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
        if not index.isValid():
            return None
        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            return index.internalPointer().data()
        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            return index.internalPointer().decorative()
        return None

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        if isinstance(index.internalPointer(), AssetNode):
            return [
                ("Replace", lambda: self.import_(index, refresh_function)),
                ("Export", lambda: self.export(index))
            ]
        return []

    def import_(self, index: QtCore.QModelIndex,
                refresh_function: Callable):
        import_path = SettingsManager().import_file(None, "Import file...")
        if import_path == "":
            return
        asset: AssetNode = index.internalPointer()
        with open(import_path, "rb") as import_file:
            asset_compression = asset.get_asset_compression()
            asset_file = asset.rom.open(asset.path, "wb")
            if asset_compression != 0:
                asset_file = CompressedIOWrapper(asset_file, asset_compression == 2)
            asset_file.write(import_file.read())
            asset_file.close()

        refresh_function(index, index)

    def export(self, index: QtCore.QModelIndex):
        asset: AssetNode = index.internalPointer()
        filename = os.path.basename(asset.path)
        export_path = SettingsManager().export_file(None, "Export file...", filename)
        if export_path == "":
            return
        with open(export_path, "wb") as export_file:
            asset_file = asset.rom.open(asset.path, "rb")
            asset_compression = asset.get_asset_compression()
            if asset_compression != 0:
                asset_file = CompressedIOWrapper(asset_file, asset_compression == 2)
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
        node: Union[AssetNode, FolderNode] = index.internalPointer()
        node.rename(value)
        model.updated_fs(self)
        return True
