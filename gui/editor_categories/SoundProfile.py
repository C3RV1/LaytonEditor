from ..EditorTypes import EditorCategory, EditorObject

from PySide6 import QtCore, QtWidgets, QtGui
from formats.dlz import SoundProfileDlz, SoundProfile


class SoundProfileNode(EditorObject):
    def __init__(self, category, sound_id, sound_profile):
        self.category = category
        self.sound_id = sound_id
        self.sound_profile: SoundProfile = sound_profile

    def get_sound_profile(self):
        return self.sound_profile

    def save(self):
        self.category: SoundProfileCategory
        self.category.sound_profile_dlz.save()

    def data(self):
        return f"Sound Profile {self.sound_id}"


class SoundProfileCategory(EditorCategory):
    def __init__(self):
        super(SoundProfileCategory, self).__init__()
        self.name = "Sound Profiles"
        self.items = {}
        self.sound_profile_dlz: SoundProfileDlz = None

    def reset_file_system(self):
        self.sound_profile_dlz = SoundProfileDlz(rom=self.rom, filename="/data_lt2/rc/snd_fix.dlz")
        self.items.clear()
        for snd_id, snd_profile in self.sound_profile_dlz.sound_profiles.items():
            self.items[snd_id] = SoundProfileNode(self, snd_id, snd_profile)

    def row_count(self, index: QtCore.QModelIndex, model: 'EditorTree') -> int:
        if index.internalPointer() is self:
            return len(self.items)
        return 0

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel) -> QtCore.QModelIndex:
        if parent.internalPointer() is not self:
            return QtCore.QModelIndex()
        if row >= len(self.items):
            return QtCore.QModelIndex()
        keys = list(self.items.keys())
        return model.createIndex(row, column, self.items[keys[row]])

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QModelIndex,
               model: QtCore.QAbstractItemModel) -> QtCore.QModelIndex:
        if index.internalPointer() is self:
            return QtCore.QModelIndex()
        return category_index

    def data(self, index: QtCore.QModelIndex, role, model: QtCore.QAbstractItemModel):
        if index.isValid() and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return index.internalPointer().data()
        return None

