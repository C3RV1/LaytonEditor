from ..EditorTypes import EditorCategory, EditorObject

from PySide6 import QtCore, QtWidgets, QtGui
from formats.dlz_types.TimeDefinitions import TimeDefinitionsDlz
from formats.dlz_types.SoundFix import SoundFixDlz


class SoundFixNode(EditorObject):
    def __init__(self, category):
        super(SoundFixNode, self).__init__()
        self.category = category
        self.name = "Sound Fix"
        self.sound_fix_dlz: SoundFixDlz = None

    def reset_file_system(self, rom):
        self.sound_fix_dlz = SoundFixDlz(rom=rom, filename="/data_lt2/rc/snd_fix.dlz")

    def get_sound_profile_dlz(self) -> SoundFixDlz:
        return self.sound_fix_dlz

    def data(self):
        return "Sound Profiles"


class TimeDefinitionsNode(EditorObject):
    def __init__(self, category):
        super().__init__()
        self.category = category
        self.name = "Time Definitions"
        self.time_def_dlz: TimeDefinitionsDlz = None

    def reset_file_system(self, rom):
        self.time_def_dlz = TimeDefinitionsDlz(rom=rom, filename="/data_lt2/rc/tm_def.dlz")

    def get_time_definitions_dlz(self):
        return self.time_def_dlz

    def data(self):
        return "Time Definitions"


class DLZCategory(EditorCategory):
    def __init__(self):
        super(DLZCategory, self).__init__()
        self.name = "DLZ"
        self.dlz_items = [
            SoundFixNode(self),
            TimeDefinitionsNode(self)
        ]

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
