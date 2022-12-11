from typing import List, Sequence, Any

from PySide6 import QtCore
from .editor_categories import *
from .EditorTypes import EditorObject


class EditorTree(QtCore.QAbstractItemModel):
    def __init__(self):
        super(EditorTree, self).__init__()
        self.categories = []

    def set_rom(self, rom):
        self.layoutAboutToBeChanged.emit()
        if rom.name == b"LAYTON2":
            self.categories = [
                FilesystemCategory(),
                SpriteCategory(),
                BackgroundsCategory(),
                EventCategory(),
                PuzzleCategory(),
                FontsCategory(),
                MoviesCategory(),
                StreamedAudioCategory(),
                TextsCategory(),
                ScriptsCategory()
            ]
        else:
            self.categories = [
                FilesystemCategory()
            ]
        for category in self.categories:
            category.set_rom(rom)
        self.layoutChanged.emit()

    def updated_fs(self, exclude_category=None):
        self.layoutAboutToBeChanged.emit()
        for category in self.categories:
            if category is exclude_category:
                continue
            category.reset_file_system()
        self.layoutChanged.emit()

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = ...) -> bool:
        if not index.isValid():
            return False
        return index.internalPointer().category.set_data(index, value, role, self)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if not index.isValid():
            return super(EditorTree, self).flags(index)
        return index.internalPointer().category.flags(index, self)

    def rowCount(self, index: QtCore.QModelIndex) -> int:
        if not index.isValid():
            return len(self.categories)
        editor_obj: EditorObject = index.internalPointer()
        return editor_obj.category.row_count(index, self)

    def index(self, row, column, _parent=None):
        if not _parent or not _parent.isValid():
            if row < len(self.categories):
                return self.createIndex(row, column, self.categories[row])
        editor_obj: EditorObject = _parent.internalPointer()
        return editor_obj.category.index(row, column, _parent, self)

    def parent(self, _index):
        if not _index.isValid():
            return QtCore.QModelIndex()
        editor_obj: EditorObject = _index.internalPointer()
        parent_index = self.createIndex(self.categories.index(editor_obj.category), 0,
                                        editor_obj.category)
        return editor_obj.category.parent(_index, parent_index, self)

    def columnCount(self, _index):
        if not _index.isValid():
            return 1
        editor_obj: EditorObject = _index.internalPointer()
        return editor_obj.category.column_count(_index, self)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QModelIndex()
        if not index.parent().isValid():
            if index.isValid() and role == QtCore.Qt.DisplayRole:
                return index.internalPointer().name
        editor_obj: EditorObject = index.internalPointer()
        return editor_obj.category.data(index, role, self)
