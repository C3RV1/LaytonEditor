from ..EditorTypes import EditorCategory, EditorObject

from PySide6 import QtCore, QtWidgets, QtGui
from formats.dlz import SoundProfileDlz, SoundProfile


class SoundProfileNode(EditorObject):
    def __init__(self, category):
        super(SoundProfileNode, self).__init__()
        self.category = category
        self.name = "Sound Profiles"
        self.items = {}
        self.sound_profile_dlz: SoundProfileDlz = None

    def reset_file_system(self, rom):
        self.sound_profile_dlz = SoundProfileDlz(rom=rom, filename="/data_lt2/rc/snd_fix.dlz")

    def get_sound_profile_dlz(self):
        return self.sound_profile_dlz

    def data(self):
        return "Sound Profiles"


class DLZCategory(EditorCategory):
    def __init__(self):
        super(DLZCategory, self).__init__()
        self.name = "DLZ"
        self.dlz_items = [SoundProfileNode(self)]

    def reset_file_system(self):
        for dlz_item in self.dlz_items:
            dlz_item.reset_file_system(self.rom)

    def row_count(self, index: QtCore.QModelIndex, model: 'EditorTree') -> int:
        if index.internalPointer() is self:
            return len(self.dlz_items)
        return 0

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel) -> QtCore.QModelIndex:
        if parent.internalPointer() is not self:
            return QtCore.QModelIndex()
        if row >= len(self.dlz_items):
            return QtCore.QModelIndex()
        return model.createIndex(row, column, self.dlz_items[row])

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QModelIndex,
               model: QtCore.QAbstractItemModel) -> QtCore.QModelIndex:
        if index.internalPointer() is self:
            return QtCore.QModelIndex()
        return category_index

    def data(self, index: QtCore.QModelIndex, role, model: QtCore.QAbstractItemModel):
        if index.isValid() and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return index.internalPointer().data()
        return None

