from typing import List, Sequence, Any

from PySide6 import QtCore
from .editor_categories import *
from .EditorTypes import EditorObject, EditorCategory
from .SettingsManager import SettingsManager


class AbstractEditorTree(QtCore.QAbstractItemModel):
    def set_rom(self, rom):
        pass

    def updated_fs(self, exclude_category=None):
        pass


class DefaultEditorTree(AbstractEditorTree):
    def __init__(self):
        super(DefaultEditorTree, self).__init__()
        self.categories = []

    def set_rom(self, rom):
        self.beginResetModel()
        self.layoutAboutToBeChanged.emit()
        self.categories = []
        if rom.name == b"LAYTON2":
            self.categories.extend([
                SpriteCategory(),
                BackgroundsCategory(),
                EventCategory(),
                PuzzleCategory(),
                PlaceCategory(),
                FontsCategory(),
                MoviesCategory(),
                SoundEffectCategory(),
                TextsCategory(),
                ScriptsCategory(),
                StreamedAudioCategory(),
                SequencedAudioCategory(),
                SoundBankCategory(),
                TimeDefinitionsNode(),
                SoundFixCategory(),
            ])
        else:
            self.categories.extend([
                SpriteCategory(),
                BackgroundsCategory(),
                FontsCategory(),
                StreamedAudioCategory(),
                TextsCategory(),
                ScriptsCategory()
            ])
        for category in self.categories:
            category.set_rom(rom)
        self.layoutChanged.emit()
        self.endResetModel()

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
            return super(DefaultEditorTree, self).flags(index)
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
            return QtCore.QModelIndex()
        editor_obj: EditorObject = _parent.internalPointer()
        return editor_obj.category.index(row, column, _parent, self)

    def parent(self, _index):
        if not _index.isValid():
            return QtCore.QModelIndex()
        editor_obj: EditorObject = _index.internalPointer()
        if editor_obj.category not in self.categories:
            return QtCore.QModelIndex()
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
        if index.internalPointer() in self.categories:
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return index.internalPointer().name
            return None
        editor_obj: EditorObject = index.internalPointer()
        return editor_obj.category.data(index, role, self)


class MultipleCategoriesEditorTree(DefaultEditorTree):
    def __init__(self, categories):
        super(MultipleCategoriesEditorTree, self).__init__()
        self.categories = categories

    def set_rom(self, rom):
        self.beginResetModel()
        self.layoutAboutToBeChanged.emit()
        for category in self.categories:
            category.set_rom(rom)
        self.layoutChanged.emit()
        self.endResetModel()


class OneCategoryEditorTree(AbstractEditorTree):
    def __init__(self, category):
        super(OneCategoryEditorTree, self).__init__()
        self.category: EditorCategory = category

    def set_rom(self, rom):
        self.beginResetModel()
        self.layoutAboutToBeChanged.emit()
        self.category.set_rom(rom)
        self.layoutChanged.emit()
        self.endResetModel()

    def updated_fs(self, exclude_category=None):
        self.layoutAboutToBeChanged.emit()
        if self.category is not exclude_category:
            self.category.reset_file_system()
        self.layoutChanged.emit()

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = ...) -> bool:
        return self.category.set_data(index, value, role, self)

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        return self.category.flags(index, self)

    def rowCount(self, index: QtCore.QModelIndex) -> int:
        return self.category.row_count(index, self)

    def index(self, row, column, _parent=None):
        return self.category.index(row, column, _parent, self)

    def parent(self, _index):
        return self.category.parent(_index, QtCore.QModelIndex(), self)

    def columnCount(self, _index):
        return self.category.column_count(_index, self)

    def data(self, index, role):
        return self.category.data(index, role, self)
